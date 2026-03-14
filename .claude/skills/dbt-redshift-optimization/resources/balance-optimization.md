# Balance Table Optimization: Delta Models

## Purpose
Optimize daily snapshot tables that create massive redundancy. Essential for account balances, portfolio positions, and other slowly-changing data.

**Impact:** 80-90% storage reduction + 10x query speedup.

---

## The Problem

### Daily Snapshot Approach
```
1 billion accounts × 365 days = 365 billion rows per year
```

**Issues:**
- 80-90% of rows unchanged day-to-day
- Queries scan billions of redundant rows
- Storage costs explode
- Slow performance despite SORTKEY

**Example:** Account balance = $100 for 30 days → 30 identical rows stored.

---

## The Solution: Delta Model (Event-Based)

**Core Concept:** Store only when values change, not every day.

### Before (Daily Snapshots)
```
Day 1: Account 123, Balance $100
Day 2: Account 123, Balance $100  ← Redundant
Day 3: Account 123, Balance $100  ← Redundant
...
Day 30: Account 123, Balance $100  ← Redundant
Day 31: Account 123, Balance $150  ← Changed!
```
**Result:** 31 rows

### After (Delta Model)
```
Day 1: Account 123, Balance $100
Day 31: Account 123, Balance $150  ← Only changes stored
```
**Result:** 2 rows (93% reduction)

---

## Implementation

### Stage 1: Delta Model (Change Events Only)

```sql
-- models/staging/stg_account_balance_changes.sql
{{
  config(
    materialized='incremental',
    unique_key=['account_id', 'balance_change_date'],
    dist='account_id',
    sort='balance_change_date',
    post_hook="ANALYZE {{ this }}"
  )
}}

WITH daily_snapshots AS (
    SELECT
        account_id,
        snapshot_date,
        balance
    FROM {{ source('raw', 'account_daily_snapshots') }}
    
    {% if is_incremental() %}
    WHERE snapshot_date > (SELECT MAX(balance_change_date) FROM {{ this }})
    {% endif %}
),

changes_only AS (
    SELECT
        account_id,
        snapshot_date AS balance_change_date,
        balance,
        LAG(balance) OVER (
            PARTITION BY account_id 
            ORDER BY snapshot_date
        ) AS prior_balance
    FROM daily_snapshots
)

SELECT
    account_id,
    balance_change_date,
    balance,
    balance - COALESCE(prior_balance, 0) AS net_change_amount
FROM changes_only
WHERE balance != COALESCE(prior_balance, -999999)  -- Only changed rows
   OR prior_balance IS NULL  -- First record
```

**Result:** 80-90% row reduction immediately.

---

### Stage 2: Account Tier Classification

Build actionable segments on top of the delta table:

```sql
-- models/marts/customer/account_activity_tiers.sql
{{
  config(
    materialized='table',
    dist='account_id',
    sort='activity_tier',
    post_hook="ANALYZE {{ this }}"
  )
}}

WITH recent_change AS (
    -- Get most recent balance change for each account
    SELECT
        account_id,
        balance_change_date AS current_change_date,
        balance,
        DATEDIFF(day, balance_change_date, CURRENT_DATE) AS days_since_last_change
    FROM {{ ref('stg_account_balance_changes') }}
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY account_id 
        ORDER BY balance_change_date DESC
    ) = 1
),

activity_summary AS (
    -- Calculate 90-day activity metrics
    SELECT
        account_id,
        COUNT(*) AS num_changes_90_days,
        SUM(ABS(net_change_amount)) AS total_90_day_absolute_change,
        AVG(ABS(net_change_amount)) AS avg_change_magnitude
    FROM {{ ref('stg_account_balance_changes') }}
    WHERE balance_change_date >= CURRENT_DATE - 90
    GROUP BY 1
)

SELECT
    r.account_id,
    r.balance AS current_balance,
    r.days_since_last_change,
    COALESCE(a.num_changes_90_days, 0) AS changes_last_90_days,
    COALESCE(a.total_90_day_absolute_change, 0) AS total_activity_90_days,
    COALESCE(a.avg_change_magnitude, 0) AS avg_change_size,
    
    -- Tier classification logic
    CASE
        -- Tier 1: High Velocity (frequent, recent activity)
        WHEN r.days_since_last_change <= 7 
         AND COALESCE(a.num_changes_90_days, 0) >= 10 
        THEN 'Tier 1: High Velocity'
        
        -- Tier 2: Active/Stable (recent change, significant activity)
        WHEN r.days_since_last_change <= 30 
         AND COALESCE(a.total_90_day_absolute_change, 0) > 1000 
        THEN 'Tier 2: Active/Stable'
        
        -- Tier 3: Low Usage (some activity, but infrequent)
        WHEN r.days_since_last_change <= 90 
          OR COALESCE(a.total_90_day_absolute_change, 0) > 0 
        THEN 'Tier 3: Low Usage'
        
        -- Tier 4: Dormant (no activity in 90+ days)
        ELSE 'Tier 4: Dormant/Inactive'
    END AS activity_tier,
    
    -- Additional flags
    CASE WHEN r.days_since_last_change >= 90 THEN TRUE ELSE FALSE END AS is_dormant,
    CASE WHEN r.balance = 0 THEN TRUE ELSE FALSE END AS is_zero_balance
    
FROM recent_change r
LEFT JOIN activity_summary a USING (account_id)
```

---

### Stage 3: Pre-Aggregated Dashboard Metrics

```sql
-- models/marts/customer/account_tier_summary.sql
{{
  config(
    materialized='table',
    dist='all',  -- Small result, replicate
    sort='activity_tier'
  )
}}

SELECT
    activity_tier,
    COUNT(*) AS account_count,
    SUM(current_balance) AS total_balance,
    AVG(current_balance) AS avg_balance,
    AVG(days_since_last_change) AS avg_days_dormant,
    AVG(changes_last_90_days) AS avg_90d_change_frequency
FROM {{ ref('account_activity_tiers') }}
GROUP BY 1
```

**Dashboard queries now instant:**
```sql
SELECT * FROM account_tier_summary WHERE activity_tier = 'Tier 4: Dormant/Inactive'
```

---

## Performance Comparison

### Before (Daily Snapshots)
- **Table Size**: 3 billion rows (1B accounts × 3 days)
- **Query Time**: 45-90 seconds for tier classification
- **Storage**: ~200 GB

### After (Delta Model)
- **Table Size**: 300 million rows (only changes)
- **Query Time**: 3-5 seconds for tier classification
- **Storage**: ~20 GB

**10x improvement in both speed and storage.**

---

## Advanced: Dormancy Analysis

### Analyzing Time Between Changes

```sql
-- models/marts/customer/account_dormancy_analysis.sql
{{
  config(
    materialized='table',
    dist='account_id',
    sort='last_change_date'
  )
}}

WITH change_windows AS (
    SELECT
        account_id,
        balance_change_date,
        -- Calculate days until next change
        LEAD(balance_change_date, 1, CURRENT_DATE) OVER (
            PARTITION BY account_id
            ORDER BY balance_change_date
        ) AS next_change_date
    FROM {{ ref('stg_account_balance_changes') }}
)

SELECT
    account_id,
    balance_change_date AS last_change_date,
    DATEDIFF(day, balance_change_date, next_change_date) AS days_dormant,
    CASE 
        WHEN DATEDIFF(day, balance_change_date, next_change_date) >= 90 
            THEN 'Dormant'
        WHEN DATEDIFF(day, balance_change_date, next_change_date) >= 30 
            THEN 'Low Activity'
        ELSE 'Active'
    END AS activity_tier
FROM change_windows
```

---

## Advanced: Tier Transition Tracking

Track how accounts move between tiers over time:

```sql
-- models/marts/customer/account_tier_transitions.sql
{{
  config(
    materialized='incremental',
    unique_key=['account_id', 'analysis_date'],
    dist='account_id',
    sort='analysis_date'
  )
}}

WITH daily_tiers AS (
    -- Run daily to capture point-in-time tier assignments
    SELECT
        CURRENT_DATE AS analysis_date,
        account_id,
        activity_tier,
        current_balance
    FROM {{ ref('account_activity_tiers') }}
    
    {% if is_incremental() %}
    WHERE CURRENT_DATE > (SELECT MAX(analysis_date) FROM {{ this }})
    {% endif %}
)

SELECT
    analysis_date,
    account_id,
    activity_tier AS current_tier,
    LAG(activity_tier, 1) OVER (
        PARTITION BY account_id 
        ORDER BY analysis_date
    ) AS prior_tier,
    -- Flag tier changes
    CASE 
        WHEN activity_tier != LAG(activity_tier, 1) OVER (
            PARTITION BY account_id ORDER BY analysis_date
        ) THEN TRUE 
        ELSE FALSE 
    END AS tier_changed
FROM daily_tiers
```

**Business Questions Answered:**
- "What % of High Velocity accounts dropped to Dormant last quarter?"
- "How long does the average account stay in Tier 3?"
- "Which accounts are moving up vs. down?"

---

## Handling Edge Cases

### Pattern A: Accounts with No Recent Activity

```sql
-- Ensure ALL accounts represented, even if no recent changes
WITH all_accounts AS (
    SELECT DISTINCT account_id 
    FROM {{ ref('dim_accounts') }}
),

recent_activity AS (
    SELECT 
        account_id,
        MAX(balance_change_date) AS last_change_date
    FROM {{ ref('stg_account_balance_changes') }}
    GROUP BY 1
)

SELECT
    a.account_id,
    COALESCE(
        DATEDIFF(day, r.last_change_date, CURRENT_DATE), 
        9999  -- Flag for "no activity ever"
    ) AS days_since_last_change
FROM all_accounts a
LEFT JOIN recent_activity r USING (account_id)
```

---

### Pattern B: High-Frequency Micro-Changes

Filter out noise (e.g., daily interest accrual of $0.02):

```sql
-- Filter out changes below materiality threshold
SELECT
    account_id,
    balance_change_date,
    balance,
    net_change_amount
FROM {{ ref('stg_account_balance_changes') }}
WHERE ABS(net_change_amount) >= 1.00  -- Ignore sub-dollar changes
```

---

### Pattern C: Periodic Balance Resets

Handle monthly statement cycles:

```sql
-- Detect and flag periodic resets
WITH balance_patterns AS (
    SELECT
        account_id,
        balance_change_date,
        balance,
        LAG(balance) OVER (
            PARTITION BY account_id 
            ORDER BY balance_change_date
        ) AS prior_balance,
        CASE 
            WHEN balance = 0 
             AND LAG(balance) OVER (
                PARTITION BY account_id 
                ORDER BY balance_change_date
            ) > 100 
            THEN TRUE 
            ELSE FALSE 
        END AS is_reset_event
    FROM {{ ref('stg_account_balance_changes') }}
)

-- Exclude reset events from activity calculations
SELECT * FROM balance_patterns WHERE NOT is_reset_event
```

---

## Optimization Tips

### Tip 1: Partition by Time for Lifecycle Management

For very large delta tables (>1 billion rows):

```sql
{{
  config(
    materialized='incremental',
    partition_by={
      'field': 'balance_change_date',
      'data_type': 'date',
      'granularity': 'month'
    }
  )
}}
```

Then drop old partitions:
```sql
-- Maintenance job
ALTER TABLE account_balance_delta 
DROP PARTITION (balance_change_date < '2023-01-01');
```

---

### Tip 2: Separate Hot and Cold Data

Keep recent data (90 days) in a "hot" table:

```sql
-- models/staging/stg_account_balance_changes_hot.sql
{{
  config(
    materialized='incremental',
    dist='account_id',
    sort='balance_change_date'
  )
}}

SELECT *
FROM {{ ref('stg_account_balance_changes') }}
WHERE balance_change_date >= CURRENT_DATE - 90

-- Use hot table for real-time analysis
-- Use full table for historical deep dives
```

---

### Tip 3: Pre-Calculate Tier Assignments Daily

Don't recalculate tiers on every query. Calculate once daily:

```yaml
# dbt_project.yml
models:
  your_project:
    marts:
      customer:
        account_activity_tiers:
          +materialized: table
          +pre-hook: "DELETE FROM {{ this }}"  # Full refresh daily
```

**Dashboard queries become trivial:**
```sql
SELECT * FROM account_activity_tiers 
WHERE activity_tier = 'Tier 4: Dormant/Inactive'
```

---

## Monitoring & Validation

### Check Data Reduction Ratio

```sql
-- Compare snapshot vs delta table sizes
SELECT 
    'Full Snapshots' AS model,
    COUNT(*) AS row_count
FROM raw.account_daily_snapshots
WHERE snapshot_date >= CURRENT_DATE - 90

UNION ALL

SELECT 
    'Delta Model' AS model,
    COUNT(*) AS row_count
FROM {{ ref('stg_account_balance_changes') }}
WHERE balance_change_date >= CURRENT_DATE - 90;

-- Expected: Delta model = 10-20% of full snapshot size
```

---

### Verify No Data Loss

```sql
-- Validate delta model captures all accounts
WITH snapshot_accounts AS (
    SELECT DISTINCT account_id
    FROM raw.account_daily_snapshots
    WHERE snapshot_date = CURRENT_DATE
),

delta_accounts AS (
    SELECT DISTINCT account_id
    FROM {{ ref('stg_account_balance_changes') }}
)

SELECT 
    COUNT(DISTINCT s.account_id) AS accounts_in_snapshots,
    COUNT(DISTINCT d.account_id) AS accounts_in_delta,
    COUNT(DISTINCT s.account_id) - COUNT(DISTINCT d.account_id) AS missing_accounts
FROM snapshot_accounts s
LEFT JOIN delta_accounts d USING (account_id);

-- missing_accounts should be 0 or only new accounts
```

---

### Query Performance Comparison

```sql
-- Run EXPLAIN on both approaches
EXPLAIN
SELECT account_id, AVG(balance)
FROM raw.account_daily_snapshots
WHERE snapshot_date >= CURRENT_DATE - 90
GROUP BY 1;

EXPLAIN
SELECT 
    account_id, 
    balance AS current_balance
FROM {{ ref('stg_account_balance_changes') }}
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY account_id 
    ORDER BY balance_change_date DESC
) = 1;

-- Delta approach should show 80-90% fewer blocks scanned
```

---

## Use Case Examples

### 1. Identify Dormant Accounts for Outreach

```sql
SELECT
    account_id,
    current_balance,
    days_since_last_change
FROM {{ ref('account_activity_tiers') }}
WHERE activity_tier = 'Tier 4: Dormant/Inactive'
  AND current_balance > 1000  -- High-value dormant
ORDER BY current_balance DESC
LIMIT 1000;
```

---

### 2. Track Account Reactivation Rate

```sql
SELECT
    DATE_TRUNC('month', analysis_date) AS month,
    COUNT(DISTINCT CASE 
        WHEN prior_tier = 'Tier 4: Dormant/Inactive' 
         AND current_tier != 'Tier 4: Dormant/Inactive'
        THEN account_id 
    END) AS reactivated_accounts,
    COUNT(DISTINCT CASE 
        WHEN prior_tier = 'Tier 4: Dormant/Inactive'
        THEN account_id 
    END) AS total_dormant_accounts
FROM {{ ref('account_tier_transitions') }}
WHERE tier_changed = TRUE
GROUP BY 1
ORDER BY 1 DESC;
```

---

### 3. High-Value Active Account Report

```sql
SELECT
    account_id,
    current_balance,
    changes_last_90_days,
    total_activity_90_days,
    activity_tier
FROM {{ ref('account_activity_tiers') }}
WHERE activity_tier IN ('Tier 1: High Velocity', 'Tier 2: Active/Stable')
  AND current_balance > 10000
ORDER BY total_activity_90_days DESC;
```

---

## Summary: Delta Model Benefits

| Metric | Daily Snapshots | Delta Model | Improvement |
|--------|----------------|-------------|-------------|
| **Storage** | 200 GB | 20 GB | 90% reduction |
| **Query Time** | 45-90 sec | 3-5 sec | 10x faster |
| **Row Count** | 3 billion | 300 million | 90% reduction |
| **Cost** | High | Low | 90% savings |

---

## Implementation Checklist

### Phase 1: Build Delta Model (Week 1)
- [ ] Create `stg_account_balance_changes` (delta model)
- [ ] Validate row count reduction (expect 80-90%)
- [ ] Verify no data loss (all accounts represented)
- [ ] Monitor query performance

### Phase 2: Build Tier Classification (Week 2)
- [ ] Create `account_activity_tiers` model
- [ ] Validate tier distribution makes business sense
- [ ] Create `account_tier_summary` for dashboards
- [ ] Schedule daily refresh

### Phase 3: Advanced Analytics (Week 3-4)
- [ ] Create `account_dormancy_analysis`
- [ ] Create `account_tier_transitions` (incremental)
- [ ] Build dashboard reports
- [ ] Monitor data quality

### Phase 4: Optimization (Ongoing)
- [ ] Add partitioning if needed (>1B rows)
- [ ] Separate hot/cold data if needed
- [ ] Tune materiality thresholds
- [ ] Monitor and adjust tier definitions

---

**Remember:** The delta model is the foundation. Get this right, and everything else (tier classification, dormancy analysis) becomes fast and efficient.