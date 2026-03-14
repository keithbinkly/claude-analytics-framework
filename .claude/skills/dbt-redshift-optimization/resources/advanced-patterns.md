# Advanced Optimization Patterns

## Purpose
Expert-level Redshift optimization techniques for complex analytical problems. These patterns solve specific challenges in financial data modeling.

**Impact:** 10-30x speedup for specific use cases.

---

## When to Use These Patterns

Use advanced patterns when:
- Basic DISTKEY/SORTKEY optimization isn't enough
- Dealing with data skew (top 5% drives 80% volume)
- Need near-instant dashboard queries
- Building behavioral analytics (sessionization)
- Complex window function queries

---

## Pattern 1: DISTKEY Anti-Pattern for Skewed Data

### The Problem
**Standard advice:** Match DISTKEY on join columns for collocated joins.

**When it fails:** Top 100 customers drive 80% of transactions → massive data skew on certain nodes.

### The Counter-Intuitive Solution
Break the colocation rule intentionally. Use broadcast distribution.

```sql
-- ❌ TRADITIONAL (causes skew with power users)
-- models/marts/finance/fct_transactions.sql
{{
  config(
    dist='customer_id',  -- Skewed! Top customers overwhelm certain nodes
    sort='transaction_timestamp'
  )
}}

-- ✅ CLEVER FIX (eliminates skew)
-- Fact table: Distribute EVENLY
{{
  config(
    dist='even',  -- Or 'auto' - spreads data evenly
    sort=['transaction_timestamp', 'customer_id']
  )
}}

-- Dimension table: Replicate to ALL nodes
-- models/dimensions/dim_customers.sql
{{
  config(
    dist='all',  -- Replicate to every node (small dimension)
    sort='customer_id'
  )
}}
```

### How It Works
1. **Fact table** distributed EVEN → Data spread evenly across all nodes
2. **Dimension table** distributed ALL → Copied to every node
3. **Join** becomes local on every node → No cross-node shuffling
4. **Skew eliminated** → All nodes work equally hard

### When to Use
- Large fact table (billions of rows) with skewed join key
- Small dimension table (<10M rows, <100MB)
- Top 5% of customers/accounts drive >50% of activity
- Query performance degraded due to node imbalance

### Validation
Check for data skew before and after:

```sql
-- Check distribution across slices
SELECT 
    slice,
    COUNT(*) as row_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as pct_of_total
FROM {{ ref('fct_transactions') }}
GROUP BY slice
ORDER BY row_count DESC;

-- Ideal: All slices have similar percentages (within 10-15%)
-- Bad: One slice has 40%, others have 5-10%
```

---

## Pattern 2: Short Query Acceleration (SQA) for RFM

### The Problem
RFM (Recency, Frequency, Monetary) analysis requires:
- Multiple aggregations across billions of transaction rows
- But final result is tiny (one row per customer)
- Dashboards need <2 second response times

### The Solution
Pre-calculate metrics in small tables → Redshift SQA bypasses normal queue.

### Implementation: 3-Stage Pipeline

#### Stage 1: Pre-Calculate RFM Components

```sql
-- models/marts/customer/mv_customer_recency.sql
{{
  config(
    materialized='table',
    dist='all',  -- Small result, replicate everywhere
    sort='customer_id',
    post_hook="ANALYZE {{ this }}"
  )
}}

SELECT
    customer_id,
    MAX(transaction_timestamp) AS last_transaction_date,
    DATEDIFF(day, MAX(transaction_timestamp), CURRENT_DATE) AS days_since_last_transaction
FROM {{ ref('fct_transactions') }}
WHERE status = 'SUCCESS'
GROUP BY 1
```

```sql
-- models/marts/customer/mv_customer_frequency.sql
{{
  config(
    materialized='table',
    dist='all',
    sort='customer_id'
  )
}}

SELECT
    customer_id,
    COUNT(DISTINCT transaction_id) AS transaction_count_lifetime,
    COUNT(DISTINCT CASE 
        WHEN transaction_timestamp >= CURRENT_DATE - 90 
        THEN transaction_id 
    END) AS transaction_count_90d
FROM {{ ref('fct_transactions') }}
WHERE status = 'SUCCESS'
GROUP BY 1
```

```sql
-- models/marts/customer/mv_customer_monetary.sql
{{
  config(
    materialized='table',
    dist='all',
    sort='customer_id'
  )
}}

SELECT
    customer_id,
    SUM(amount_usd) AS total_spend_lifetime,
    AVG(amount_usd) AS avg_transaction_value,
    SUM(CASE 
        WHEN transaction_timestamp >= CURRENT_DATE - 90 
        THEN amount_usd 
    END) AS total_spend_90d
FROM {{ ref('fct_transactions') }}
WHERE status = 'SUCCESS'
GROUP BY 1
```

#### Stage 2: Combine into RFM Score

```sql
-- models/marts/customer/customer_rfm_scores.sql
{{
  config(
    materialized='table',
    dist='all',  -- Entire customer base fits in memory
    sort='rfm_segment'
  )
}}

WITH rfm_raw AS (
    SELECT
        c.customer_id,
        r.days_since_last_transaction,
        f.transaction_count_90d,
        m.total_spend_90d,
        -- Normalize to 1-5 scale using NTILE
        NTILE(5) OVER (ORDER BY r.days_since_last_transaction DESC) AS recency_score,
        NTILE(5) OVER (ORDER BY f.transaction_count_90d) AS frequency_score,
        NTILE(5) OVER (ORDER BY m.total_spend_90d) AS monetary_score
    FROM {{ ref('dim_customers') }} c
    LEFT JOIN {{ ref('mv_customer_recency') }} r USING (customer_id)
    LEFT JOIN {{ ref('mv_customer_frequency') }} f USING (customer_id)
    LEFT JOIN {{ ref('mv_customer_monetary') }} m USING (customer_id)
)

SELECT
    customer_id,
    days_since_last_transaction,
    transaction_count_90d,
    total_spend_90d,
    recency_score,
    frequency_score,
    monetary_score,
    -- Combined RFM score
    (recency_score * 100) + (frequency_score * 10) + monetary_score AS rfm_score,
    -- Segment classification
    CASE
        WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 
            THEN 'Champions'
        WHEN recency_score >= 3 AND frequency_score >= 3 
            THEN 'Loyal Customers'
        WHEN recency_score >= 4 AND frequency_score <= 2 
            THEN 'New Customers'
        WHEN recency_score <= 2 AND frequency_score >= 3 
            THEN 'At Risk'
        WHEN recency_score <= 2 AND frequency_score <= 2 
            THEN 'Hibernating'
        ELSE 'Needs Attention'
    END AS rfm_segment
FROM rfm_raw
```

### Performance Characteristics
- **Without MVs**: 30-60 seconds (scanning billions of rows)
- **With MVs + SQA**: <2 seconds (joining three small tables)
- **15-30x speedup** for dashboard queries

### Maintenance Strategy
```yaml
# dbt_project.yml
models:
  your_project:
    marts:
      customer:
        mv_customer_recency:
          +materialized: table
          +pre-hook: "DELETE FROM {{ this }}"
        mv_customer_frequency:
          +materialized: table  
          +pre-hook: "DELETE FROM {{ this }}"
        mv_customer_monetary:
          +materialized: table
          +pre-hook: "DELETE FROM {{ this }}"

# Schedule: Refresh these MVs once daily at 2 AM
# RFM scores remain fast all day
```

---

## Pattern 3: Transaction Sessionization (Gaps & Islands)

### The Problem
Group related transactions into "sessions" for:
- Fraud detection (rapid-fire transactions)
- User behavior analysis (shopping patterns)
- Cart abandonment tracking

**Traditional approach:** Self-joins are prohibitively slow on billions of rows.

### The Solution
Use window functions with running sums. No joins needed.

### Implementation: 3-Step CTE Pattern

```sql
-- models/marts/behavior/fct_transaction_sessions.sql
{{
  config(
    materialized='incremental',
    unique_key='transaction_id',
    dist='customer_id',
    sort=['customer_id', 'transaction_timestamp'],
    incremental_strategy='merge'
  )
}}

WITH lagged_time AS (
    -- Step 1: Calculate time gap between consecutive transactions
    SELECT
        transaction_id,
        customer_id,
        transaction_timestamp,
        merchant_id,
        amount_usd,
        -- Time since previous transaction (in seconds)
        DATEDIFF(
            second,
            LAG(transaction_timestamp) OVER (
                PARTITION BY customer_id 
                ORDER BY transaction_timestamp
            ),
            transaction_timestamp
        ) AS seconds_since_last_transaction
    FROM {{ ref('fct_transactions') }}
    
    {% if is_incremental() %}
    WHERE transaction_timestamp > (
        SELECT MAX(transaction_timestamp) FROM {{ this }}
    )
    {% endif %}
),

session_starts AS (
    -- Step 2: Flag new session starts (gaps > 5 minutes)
    SELECT
        *,
        CASE 
            WHEN seconds_since_last_transaction > 300  -- 5 minutes
                OR seconds_since_last_transaction IS NULL  -- First transaction
            THEN 1 
            ELSE 0 
        END AS is_new_session
    FROM lagged_time
),

sessions_assigned AS (
    -- Step 3: Create persistent session_id using running sum
    SELECT
        transaction_id,
        customer_id,
        transaction_timestamp,
        merchant_id,
        amount_usd,
        seconds_since_last_transaction,
        is_new_session,
        -- Running sum creates unique, sequential session IDs
        SUM(is_new_session) OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_timestamp
            ROWS UNBOUNDED PRECEDING
        ) AS session_id_sequence
    FROM session_starts
)

SELECT
    transaction_id,
    customer_id,
    transaction_timestamp,
    merchant_id,
    amount_usd,
    seconds_since_last_transaction,
    -- Create global session ID
    customer_id || '-' || session_id_sequence AS session_id,
    session_id_sequence AS session_number
FROM sessions_assigned
```

### Session-Level Analytics

```sql
-- models/marts/behavior/fct_sessions.sql
{{
  config(
    materialized='table',
    dist='customer_id',
    sort=['customer_id', 'session_start_time']
  )
}}

SELECT
    session_id,
    customer_id,
    MIN(transaction_timestamp) AS session_start_time,
    MAX(transaction_timestamp) AS session_end_time,
    DATEDIFF(
        second,
        MIN(transaction_timestamp),
        MAX(transaction_timestamp)
    ) AS session_duration_seconds,
    COUNT(transaction_id) AS transactions_in_session,
    SUM(amount_usd) AS session_total_spend,
    COUNT(DISTINCT merchant_id) AS unique_merchants_visited,
    -- Session classification
    CASE
        WHEN COUNT(transaction_id) = 1 THEN 'Single Transaction'
        WHEN COUNT(DISTINCT merchant_id) = 1 THEN 'Single Merchant'
        WHEN COUNT(transaction_id) >= 5 THEN 'Shopping Spree'
        ELSE 'Multi-Merchant'
    END AS session_type
FROM {{ ref('fct_transaction_sessions') }}
GROUP BY 1, 2
```

### Use Cases

#### Fraud Detection
```sql
-- Flag suspicious rapid-fire sessions
SELECT
    session_id,
    customer_id,
    session_duration_seconds,
    transactions_in_session,
    session_total_spend
FROM {{ ref('fct_sessions') }}
WHERE transactions_in_session >= 10
  AND session_duration_seconds < 60  -- 10+ txns in under 1 minute
  AND session_total_spend > 5000
```

#### Cart Abandonment
```sql
-- Identify incomplete purchase sessions
WITH merchant_sessions AS (
    SELECT
        s.session_id,
        s.customer_id,
        s.transactions_in_session,
        -- Did they complete purchase at final merchant?
        MAX(CASE 
            WHEN t.merchant_id = 'CHECKOUT_MERCHANT' 
            THEN 1 ELSE 0 
        END) AS completed_checkout
    FROM {{ ref('fct_sessions') }} s
    JOIN {{ ref('fct_transaction_sessions') }} t 
        USING (session_id)
    WHERE s.session_type = 'Multi-Merchant'
    GROUP BY 1, 2, 3
)

SELECT
    customer_id,
    COUNT(*) AS abandoned_sessions,
    AVG(transactions_in_session) AS avg_items_before_abandon
FROM merchant_sessions
WHERE completed_checkout = 0
GROUP BY 1
HAVING COUNT(*) >= 3  -- Frequent abandoners
```

**Performance:** 10-20x faster than self-join approaches.

---

## Pattern 4: Conditional Aggregation (Single-Pass)

### The Problem
Dashboard queries need multiple time-window metrics:
- Today's revenue
- Yesterday's revenue
- Last 7 days revenue
- Last 30 days revenue

**Naive approach:** 4 separate queries.

### The Solution
Use CASE WHEN inside aggregations for single-pass computation.

```sql
-- models/marts/reporting/daily_metrics_multi_window.sql
{{
  config(
    materialized='table',
    dist='all',
    sort='metric_date'
  )
}}

SELECT
    CURRENT_DATE AS metric_date,
    
    -- Today's metrics
    COUNT(DISTINCT CASE 
        WHEN transaction_timestamp::DATE = CURRENT_DATE 
        THEN customer_id 
    END) AS active_customers_today,
    
    SUM(CASE 
        WHEN transaction_timestamp::DATE = CURRENT_DATE 
        THEN amount_usd 
    END) AS revenue_today,
    
    -- Yesterday's metrics
    COUNT(DISTINCT CASE 
        WHEN transaction_timestamp::DATE = CURRENT_DATE - 1 
        THEN customer_id 
    END) AS active_customers_yesterday,
    
    SUM(CASE 
        WHEN transaction_timestamp::DATE = CURRENT_DATE - 1 
        THEN amount_usd 
    END) AS revenue_yesterday,
    
    -- Last 7 days
    COUNT(DISTINCT CASE 
        WHEN transaction_timestamp >= CURRENT_DATE - 7 
        THEN customer_id 
    END) AS active_customers_7d,
    
    SUM(CASE 
        WHEN transaction_timestamp >= CURRENT_DATE - 7 
        THEN amount_usd 
    END) AS revenue_7d,
    
    -- Last 30 days
    COUNT(DISTINCT CASE 
        WHEN transaction_timestamp >= CURRENT_DATE - 30 
        THEN customer_id 
    END) AS active_customers_30d,
    
    SUM(CASE 
        WHEN transaction_timestamp >= CURRENT_DATE - 30 
        THEN amount_usd 
    END) AS revenue_30d

FROM {{ ref('fct_transactions') }}
WHERE transaction_timestamp >= CURRENT_DATE - 30  -- Only scan last 30 days
  AND status = 'SUCCESS'
```

**Performance:**
- **4 separate queries**: 20-40 seconds total
- **Single conditional aggregation**: 5-8 seconds
- **4-5x speedup** by scanning data once

---

## Pattern 5: QUALIFY Clause for Top-N

### The Problem
Finding "most recent transaction per customer" requires:
1. Window function (ROW_NUMBER)
2. CTE to wrap it
3. Filter the CTE

### The Solution
Use QUALIFY to filter window function results directly.

```sql
-- ❌ TRADITIONAL: Requires CTE
WITH ranked AS (
    SELECT
        customer_id,
        transaction_id,
        transaction_timestamp,
        amount_usd,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_timestamp DESC
        ) AS rn
    FROM {{ ref('fct_transactions') }}
)
SELECT * FROM ranked WHERE rn = 1

-- ✅ CLEVER: Direct filtering with QUALIFY
SELECT
    customer_id,
    transaction_id,
    transaction_timestamp,
    amount_usd
FROM {{ ref('fct_transactions') }}
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY customer_id 
    ORDER BY transaction_timestamp DESC
) = 1
```

### More QUALIFY Examples

**Top 3 merchants by spend per customer:**
```sql
SELECT
    customer_id,
    merchant_id,
    SUM(amount_usd) AS total_spend
FROM {{ ref('fct_transactions') }}
GROUP BY 1, 2
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY customer_id 
    ORDER BY SUM(amount_usd) DESC
) <= 3
```

**Most recent status per account:**
```sql
SELECT
    account_id,
    status,
    updated_at
FROM {{ ref('fct_account_status_history') }}
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY account_id 
    ORDER BY updated_at DESC
) = 1
```

**Performance:** 2-3x faster, cleaner code.

---

## Pattern 6: Materialized Views for Dashboards

### When to Use
- Expensive aggregations run repeatedly (hourly/daily)
- Predictable query patterns
- Dashboard needs <2 second response

### Implementation

```sql
-- models/marts/reporting/mv_daily_revenue_by_network.sql
{{
  config(
    materialized='table',
    dist='card_network',
    sort='transaction_date',
    post_hook=[
      "ANALYZE {{ this }}",
      "CREATE MATERIALIZED VIEW IF NOT EXISTS {{ this }}_mv 
       DISTKEY(card_network) 
       SORTKEY(transaction_date) AS 
       SELECT * FROM {{ this }}"
    ]
  )
}}

SELECT
    DATE_TRUNC('day', transaction_timestamp) AS transaction_date,
    card_network,
    COUNT(transaction_id) AS total_transactions,
    SUM(amount_usd) AS total_revenue,
    COUNT(DISTINCT customer_id) AS unique_customers,
    AVG(amount_usd) AS avg_transaction_size
FROM {{ ref('fct_transactions') }}
WHERE status = 'SUCCESS'
GROUP BY 1, 2
```

**Refresh Strategy:**
```yaml
# dbt_project.yml
on-run-end:
  - "REFRESH MATERIALIZED VIEW {{ target.schema }}.mv_daily_revenue_by_network_mv"
```

---

## Summary: When to Use Each Pattern

| Pattern | Use Case | Expected Speedup |
|---------|----------|------------------|
| **DISTKEY Anti-Pattern** | Skewed data (top 5% = 80% volume) | 3-5x |
| **SQA for RFM** | Customer segmentation dashboards | 15-30x |
| **Sessionization** | Behavioral analysis, fraud detection | 10-20x |
| **Conditional Aggregation** | Multi-timeframe dashboard metrics | 4-5x |
| **QUALIFY** | Top-N per group queries | 2-3x |
| **Materialized Views** | Repeatedly-run aggregations | 15-30x |

---

**Remember:** These are expert patterns. Start with basic DISTKEY/SORTKEY optimization first, then apply these when foundational optimization isn't enough.