# Query Patterns: Best Practices and Anti-Patterns

## Purpose
Write SQL queries that leverage your table design for maximum performance. Avoid common anti-patterns that slow down Redshift.

**Impact:** 2-5x query speedup from following these patterns.

---

## Core Rules

### Rule 1: Filter Early Using SORTKEY

**Always** include your SORTKEY column in WHERE clauses.

```sql
-- ✅ GOOD: Uses SORTKEY for block pruning
SELECT customer_id, SUM(amount_usd) as total_spend
FROM {{ ref('fct_transactions') }}
WHERE transaction_timestamp >= '2025-10-01'
  AND transaction_timestamp < '2025-11-01'
GROUP BY 1

-- ❌ BAD: Function prevents SORTKEY usage
SELECT customer_id, SUM(amount_usd) as total_spend
FROM {{ ref('fct_transactions') }}
WHERE DATE(transaction_timestamp) = '2025-10-01'
GROUP BY 1

-- ✅ GOOD: Apply function to comparison value
SELECT customer_id, SUM(amount_usd) as total_spend
FROM {{ ref('fct_transactions') }}
WHERE transaction_timestamp >= '2025-10-01'
  AND transaction_timestamp < '2025-10-02'
GROUP BY 1
```

**Why:** Functions on columns prevent zone map pruning. Redshift must scan entire table.

---

### Rule 2: SELECT Only Required Columns

Redshift is columnar. Each column = separate I/O.

```sql
-- ❌ BAD: Scans all 20 columns
SELECT * FROM {{ ref('fct_transactions') }}
WHERE transaction_timestamp >= '2025-10-01'

-- ✅ GOOD: Scans only 5 columns
SELECT 
    transaction_id,
    customer_id,
    transaction_timestamp,
    amount_usd,
    status
FROM {{ ref('fct_transactions') }}
WHERE transaction_timestamp >= '2025-10-01'
```

**Impact:** Can reduce query time by 50-80% depending on table width.

---

### Rule 3: Push Predicates Down to CTEs

Apply filters as early as possible in the query.

```sql
-- ❌ BAD: Filters applied late
WITH all_transactions AS (
    SELECT * FROM {{ ref('fct_transactions') }}
),

all_customers AS (
    SELECT * FROM {{ ref('dim_customers') }}
)

SELECT *
FROM all_transactions t
JOIN all_customers c USING (customer_id)
WHERE t.transaction_timestamp >= '2025-10-01'
  AND c.customer_type = 'PREMIUM'

-- ✅ GOOD: Filters pushed into CTEs
WITH filtered_transactions AS (
    SELECT 
        transaction_id,
        customer_id,
        amount_usd
    FROM {{ ref('fct_transactions') }}
    WHERE transaction_timestamp >= '2025-10-01'  -- Filter early!
),

premium_customers AS (
    SELECT customer_id, customer_name
    FROM {{ ref('dim_customers') }}
    WHERE customer_type = 'PREMIUM'  -- Filter early!
)

SELECT *
FROM filtered_transactions t
JOIN premium_customers c USING (customer_id)
```

**Why:** Reduces data flowing through query, smaller intermediate results.

---

### Rule 4: Use Explicit Column Lists in CTEs

Even in CTEs, be explicit about columns.

```sql
-- ❌ BAD
WITH base AS (
    SELECT * FROM {{ ref('fct_transactions') }}  -- 30 columns
)
SELECT customer_id, SUM(amount_usd)
FROM base
GROUP BY 1

-- ✅ GOOD
WITH base AS (
    SELECT 
        customer_id, 
        amount_usd
    FROM {{ ref('fct_transactions') }}  -- Only 2 columns
)
SELECT customer_id, SUM(amount_usd)
FROM base
GROUP BY 1
```

---

## Anti-Pattern 1: GROUPING SETS

### Problem
GROUPING SETS not supported in all Redshift versions and often inefficient.

### Solution
Convert to UNION ALL of explicit GROUP BYs.

```sql
-- ❌ BAD: GROUPING SETS
SELECT
    portfolio,
    product,
    GROUPING_ID(portfolio, product) as grouping_level,
    SUM(amount) as total
FROM transactions
GROUP BY GROUPING SETS (
    (portfolio, product),
    (portfolio),
    ()
)

-- ✅ GOOD: UNION ALL
SELECT portfolio, product, 0 as grouping_level, SUM(amount) as total
FROM transactions
GROUP BY portfolio, product

UNION ALL

SELECT portfolio, NULL, 1 as grouping_level, SUM(amount) as total
FROM transactions
GROUP BY portfolio

UNION ALL

SELECT NULL, NULL, 3 as grouping_level, SUM(amount) as total
FROM transactions
```

**Performance:** Often 2-3x faster, more portable.

---

## Anti-Pattern 2: Deeply Nested Subqueries

### Problem
Nested subqueries (>3 levels) hurt readability and performance.

### Solution
Flatten to CTEs.

```sql
-- ❌ BAD: Deep nesting
SELECT *
FROM (
    SELECT *
    FROM (
        SELECT *
        FROM (
            SELECT * FROM base_table
            WHERE filter1
        )
        WHERE filter2
    )
    WHERE filter3
)
WHERE filter4

-- ✅ GOOD: Flat CTEs
WITH level1 AS (
    SELECT * FROM base_table
    WHERE filter1
),

level2 AS (
    SELECT * FROM level1
    WHERE filter2
),

level3 AS (
    SELECT * FROM level2
    WHERE filter3
)

SELECT * FROM level3
WHERE filter4
```

**Why:** Easier to read, debug, and optimize. Query planner works better with CTEs.

---

## Anti-Pattern 3: Cartesian Joins

### Problem
Missing join conditions create data explosions.

### Detection
```sql
-- ❌ BAD: Cartesian join (no ON clause)
SELECT *
FROM table_a a, table_b b
WHERE a.date = '2025-01-01'  -- This is WHERE, not JOIN condition!
```

### Solution
Always use explicit JOIN with ON clause.

```sql
-- ✅ GOOD: Explicit join condition
SELECT *
FROM table_a a
JOIN table_b b ON a.id = b.id
WHERE a.date = '2025-01-01'
```

---

## Anti-Pattern 4: Functions in WHERE Clause

### Problem
Functions on columns prevent index/zone map usage.

### Common Mistakes

```sql
-- ❌ BAD: DATE() prevents SORTKEY usage
WHERE DATE(transaction_timestamp) = '2025-01-01'

-- ✅ GOOD: Range query
WHERE transaction_timestamp >= '2025-01-01'
  AND transaction_timestamp < '2025-01-02'

-- ❌ BAD: YEAR() prevents pruning
WHERE YEAR(transaction_timestamp) = 2025

-- ✅ GOOD: Range query
WHERE transaction_timestamp >= '2025-01-01'
  AND transaction_timestamp < '2026-01-01'

-- ❌ BAD: LOWER() prevents optimization
WHERE LOWER(status) = 'success'

-- ✅ GOOD: Store in consistent case
WHERE status = 'SUCCESS'
```

---

## Anti-Pattern 5: Using DISTINCT as a Band-Aid

### Problem
DISTINCT is expensive. Often indicates data quality issue.

### Better Approach
Understand why duplicates exist and fix at source.

```sql
-- ❌ BAD: DISTINCT hides problem
SELECT DISTINCT
    customer_id,
    customer_name
FROM {{ ref('fct_transactions') }}

-- ✅ GOOD: Fix the join
SELECT 
    customer_id,
    customer_name
FROM {{ ref('dim_customers') }}
```

---

## Advanced Pattern 1: Conditional Aggregation

### Single-Pass Multi-Metric Calculation

Instead of multiple queries or subqueries, use CASE in aggregations.

```sql
-- ❌ BAD: Multiple passes
SELECT COUNT(*) as total FROM transactions;
SELECT COUNT(*) as successful FROM transactions WHERE status = 'SUCCESS';
SELECT COUNT(*) as failed FROM transactions WHERE status = 'FAILED';

-- ✅ GOOD: Single pass
SELECT
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'SUCCESS' THEN 1 END) as successful,
    COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as failed,
    SUM(CASE WHEN status = 'SUCCESS' THEN amount ELSE 0 END) as successful_amount
FROM transactions
```

**Performance:** 3-4x faster for multiple metrics.

---

## Advanced Pattern 2: Window Functions (Efficient)

### Single Pass vs Multiple Passes

```sql
-- ❌ BAD: Multiple window passes
WITH step1 AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY key ORDER BY date) as rn
    FROM table
),

step2 AS (
    SELECT *, SUM(amount) OVER (PARTITION BY key ORDER BY date) as running_sum
    FROM table
)

-- ✅ GOOD: Single pass
SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY key ORDER BY date) as rn,
    SUM(amount) OVER (PARTITION BY key ORDER BY date) as running_sum,
    LAG(value) OVER (PARTITION BY key ORDER BY date) as prev_value
FROM table
```

**Why:** Window functions with same PARTITION BY and ORDER BY can be computed in single pass.

---

## Advanced Pattern 3: QUALIFY Clause

### Filtering Window Function Results Directly

```sql
-- ❌ TRADITIONAL: Requires CTE
WITH ranked AS (
    SELECT
        customer_id,
        transaction_id,
        transaction_timestamp,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_timestamp DESC) as rn
    FROM {{ ref('fct_transactions') }}
)
SELECT * FROM ranked WHERE rn = 1

-- ✅ GOOD: Direct filtering with QUALIFY
SELECT
    customer_id,
    transaction_id,
    transaction_timestamp
FROM {{ ref('fct_transactions') }}
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_timestamp DESC) = 1
```

**Why:** Cleaner, sometimes faster, no intermediate CTE needed.

---

## Query Rewrite Examples

### Example 1: Optimizing Transaction Summary

**Before (Multiple Issues):**
```sql
SELECT 
    *,  -- Anti-pattern: SELECT *
    DATE(transaction_timestamp) as txn_date  -- Anti-pattern: function in SELECT
FROM {{ ref('fct_transactions') }}
WHERE YEAR(transaction_timestamp) = 2025  -- Anti-pattern: function in WHERE
  AND status IN (SELECT status FROM valid_statuses)  -- Inefficient subquery
```

**After (Optimized):**
```sql
-- Pre-calculate valid statuses as CTE or temp table
WITH valid_statuses AS (
    SELECT 'SUCCESS' as status
    UNION ALL SELECT 'PENDING'
)

SELECT 
    transaction_id,
    customer_id,
    transaction_timestamp,
    transaction_timestamp::DATE as txn_date,  -- Cast, not function
    amount_usd,
    status
FROM {{ ref('fct_transactions') }}
WHERE transaction_timestamp >= '2025-01-01'  -- Range, not function
  AND transaction_timestamp < '2026-01-01'
  AND status IN (SELECT status FROM valid_statuses)
```

---

### Example 2: Efficient RFM Calculation

```sql
-- ✅ GOOD: Single-pass RFM
WITH customer_metrics AS (
    SELECT
        customer_id,
        -- Recency
        DATEDIFF(day, MAX(transaction_timestamp), CURRENT_DATE) as days_since_last_txn,
        -- Frequency
        COUNT(transaction_id) as txn_count,
        -- Monetary
        SUM(amount_usd) as total_spend,
        AVG(amount_usd) as avg_spend
    FROM {{ ref('fct_transactions') }}
    WHERE transaction_timestamp >= CURRENT_DATE - 365
    GROUP BY 1
)

SELECT
    customer_id,
    days_since_last_txn,
    txn_count,
    total_spend,
    -- Score components using NTILE
    NTILE(5) OVER (ORDER BY days_since_last_txn DESC) as recency_score,
    NTILE(5) OVER (ORDER BY txn_count) as frequency_score,
    NTILE(5) OVER (ORDER BY total_spend) as monetary_score
FROM customer_metrics
```

---

## Testing Query Performance

### Use EXPLAIN
```sql
EXPLAIN
SELECT customer_id, SUM(amount_usd)
FROM {{ ref('fct_transactions') }}
WHERE transaction_timestamp >= '2025-10-01'
GROUP BY 1;
```

Look for:
- **DS_BCAST_DIST**: Broadcasting large table (bad)
- **DS_DIST_NONE**: No distribution key match on join (bad)
- **Seq Scan**: Full table scan (check if SORTKEY being used)

### Use EXPLAIN ANALYZE
```sql
EXPLAIN ANALYZE
SELECT customer_id, SUM(amount_usd)
FROM {{ ref('fct_transactions') }}
WHERE transaction_timestamp >= '2025-10-01'
GROUP BY 1;
```

Shows actual execution time and rows processed.

---

## Validation Queries

### Validate Rewrite Produces Same Results

```sql
-- Original query
WITH original AS (
    SELECT customer_id, SUM(amount_usd) as total
    FROM {{ ref('fct_transactions') }}
    WHERE DATE(transaction_timestamp) = '2025-10-01'
    GROUP BY 1
),

-- Optimized query
optimized AS (
    SELECT customer_id, SUM(amount_usd) as total
    FROM {{ ref('fct_transactions') }}
    WHERE transaction_timestamp >= '2025-10-01'
      AND transaction_timestamp < '2025-10-02'
    GROUP BY 1
)

-- Compare results
SELECT
    'MATCH' as result
WHERE (SELECT COUNT(*) FROM original) = (SELECT COUNT(*) FROM optimized)
  AND (SELECT SUM(total) FROM original) = (SELECT SUM(total) FROM optimized)

UNION ALL

SELECT 'MISMATCH' as result
WHERE (SELECT COUNT(*) FROM original) != (SELECT COUNT(*) FROM optimized)
   OR (SELECT SUM(total) FROM original) != (SELECT SUM(total) FROM optimized)
```

---

## Summary: Query Pattern Checklist

### Before Writing SQL
- [ ] Know the SORTKEY of tables you'll query
- [ ] Plan to filter on SORTKEY in WHERE clause
- [ ] List only columns you need (no SELECT *)
- [ ] Push filters into CTEs early

### While Writing SQL
- [ ] Use explicit JOIN conditions
- [ ] Avoid functions on filter columns
- [ ] Use CASE for conditional aggregation
- [ ] Combine window functions with same PARTITION/ORDER

### After Writing SQL
- [ ] Run EXPLAIN to check query plan
- [ ] Validate results match original (if rewriting)
- [ ] Test performance in dev
- [ ] Document optimization decisions

---

**Remember:** The query pattern that leverages your table design (DISTKEY/SORTKEY) will always be fastest.
