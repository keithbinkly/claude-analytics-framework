# Table Design: Distribution and Sort Keys

## Purpose
Correct table design is the foundation of Redshift performance. DISTKEY and SORTKEY determine how data is distributed across nodes and organized on disk.

**Impact:** 5-10x query speedup when done correctly.

---

## Distribution Key (DISTKEY)

### What It Does
DISTKEY determines how rows are distributed across compute nodes. Correct distribution enables:
- **Collocated joins** (data needed for join is on same node)
- **Even workload** (all nodes process similar amounts of data)
- **No data shuffling** (avoid cross-node data movement)

###

 Selection Criteria

| Scenario | Recommended DISTKEY | Why |
|----------|---------------------|-----|
| **Fact table joins dimension** | Join column (e.g., `customer_id`) | Enables collocated joins |
| **No obvious join pattern** | `EVEN` | Distributes data evenly |
| **Small dimension table** (<10M rows) | `ALL` | Replicates to every node |
| **Uncertain/evolving** | `AUTO` | Let Redshift decide |
| **Skewed data** (top 5% = 80% volume) | See DISTKEY Anti-Pattern below | Avoid data skew |

### Example: Fact Table
```sql
{{
  config(
    materialized='incremental',
    dist='customer_id',  -- Matches customer dimension
    sort=['transaction_timestamp', 'status']
  )
}}

SELECT
    transaction_id,
    customer_id,
    transaction_timestamp,
    amount_usd,
    status
FROM {{ ref('stg_transactions') }}
```

### Example: Small Dimension Table
```sql
{{
  config(
    materialized='table',
    dist='all',  -- Replicate to all nodes
    sort='customer_id'
  )
}}

SELECT
    customer_id,
    customer_name,
    customer_type
FROM {{ ref('stg_customers') }}
WHERE customer_status = 'ACTIVE'
```

### DISTKEY Anti-Pattern (For Skewed Data)

**Problem:** Top 100 customers drive 80% of transactions. Using `DISTKEY(customer_id)` creates massive skew on certain nodes.

**Solution:** Break the colocation rule intentionally.

```sql
-- Fact table: Distribute EVENLY
{{
  config(
    dist='even',  -- Or 'auto'
    sort=['transaction_timestamp', 'customer_id']
  )
}}

-- Dimension table: Replicate to ALL nodes
{{
  config(
    dist='all',
    sort='customer_id'
  )
}}
```

**How It Works:**
1. Fact table distributed evenly → No skew
2. Dimension replicated everywhere → Join becomes local on every node
3. No cross-node shuffling → Fast joins despite breaking colocation

**When to Use:**
- Top 5% of customers/accounts drive >50% of activity
- Node imbalance observed (check data skew query below)
- Large fact table (billions of rows) with small dimension (<10M rows, <100MB)

---

## Sort Key (SORTKEY)

### What It Does
SORTKEY determines physical data ordering on disk. Enables **zone maps** that allow Redshift to skip entire blocks during scans.

**Impact:** Can reduce data scanned by 90-99% with correct SORTKEY.

### Selection Criteria

**First column:** Most frequently filtered column (usually timestamp)
**Second column:** Highly selective column filtered WITH first column
**Third+ columns:** Rarely needed; stick to 1-2 columns

| Query Pattern | SORTKEY Configuration | Benefit |
|---------------|----------------------|---------|
| Time-series analysis | `sort='transaction_timestamp'` | Skip all blocks outside date range |
| Time + Status filters | `sort=['transaction_timestamp', 'status']` | Skip blocks outside date+status |
| ID lookups | `sort='transaction_id'` | Only if querying by exact ID frequently |

### COMPOUND vs INTERLEAVED

**COMPOUND (Recommended):**
- Fastest when filtering on first column
- Good when filtering on first + second columns
- Most common choice

**INTERLEAVED:**
- Equal weight to all columns
- Rarely recommended
- Use only when no clear primary filter

**Default:** Always use COMPOUND unless you have specific reason not to.

### Example: Transaction Fact Table
```sql
{{
  config(
    dist='customer_id',
    sort=['transaction_timestamp', 'status']  -- COMPOUND
  )
}}
```

**Optimized Query:**
```sql
-- This query is HIGHLY optimized
SELECT customer_id, SUM(amount_usd)
FROM {{ ref('fct_transactions') }}
WHERE transaction_timestamp >= '2025-10-01'  -- Uses SORTKEY
  AND transaction_timestamp < '2025-11-01'
  AND status = 'SUCCESS'  -- Uses second SORTKEY column
GROUP BY 1
```

**Bad Query:**
```sql
-- This query CANNOT use SORTKEY efficiently
SELECT customer_id, SUM(amount_usd)
FROM {{ ref('fct_transactions') }}
WHERE status = 'SUCCESS'  -- Filters on second column only!
GROUP BY 1
```

---

## Data Type Optimization

### Use Smallest Appropriate Types

**Why:** Redshift is columnar. Smaller columns = fewer disk blocks = less I/O = faster queries.

| Data | Too Large | Right-Sized | Savings |
|------|-----------|-------------|---------|
| Card number | `VARCHAR(255)` | `VARCHAR(16)` | 93% |
| Status code | `VARCHAR(255)` | `VARCHAR(15)` | 94% |
| Country code | `VARCHAR(255)` | `VARCHAR(2)` | 99% |
| Transaction ID | `VARCHAR(50)` | `BIGINT` | 80% |

### Recommended Data Types

```sql
-- Staging model with optimized types
SELECT
    transaction_id::BIGINT,              -- Not VARCHAR
    customer_id::BIGINT,                 -- Not VARCHAR
    transaction_timestamp::TIMESTAMP,     -- Not VARCHAR!
    card_network::VARCHAR(10),           -- Not VARCHAR(255)
    card_last_four::VARCHAR(4),          -- Not VARCHAR(255)
    amount_usd::DECIMAL(18, 2),          -- Not FLOAT (precision issues)
    merchant_id::BIGINT,
    merchant_category::VARCHAR(30),
    status::VARCHAR(15),                 -- Not VARCHAR(255)
    country_code::VARCHAR(2)             -- Not VARCHAR(255)
FROM {{ source('raw', 'transactions') }}
```

### Common Mistakes

| ❌ Mistake | ✅ Fix |
|-----------|--------|
| `VARCHAR(255)` everywhere | Right-size each column |
| Store dates as `VARCHAR` | Use `DATE` or `TIMESTAMP` |
| Use `FLOAT` for money | Use `DECIMAL(18, 2)` |
| Use `VARCHAR` for IDs | Use `BIGINT` |

---

## Compression Encoding

### Let Redshift Auto-Compress

**Best Practice:** Use `ENCODE AUTO` (default since mid-2020s).

```sql
{{
  config(
    materialized='table',
    dist='customer_id',
    sort='transaction_timestamp'
  )
}}

-- Redshift automatically applies optimal encodings:
-- - ZSTD for strings
-- - AZ64 for DECIMAL
-- - DELTA for sequential integers
-- - LZO for mixed patterns
```

### Understanding Encoding Types

| Encoding | Best For | Example Columns |
|----------|----------|-----------------|
| **ZSTD** | Text, high compression | status, card_network, merchant_name |
| **AZ64** | Numbers with good compression | amount_usd, balance |
| **DELTA** | Sequential or sorted integers | transaction_id, sequence numbers |
| **LZO** | General purpose | Mixed data types |
| **RAW** | Already compressed data | Pre-compressed files |

### When to Override Auto-Encoding

**Rarely.** Only if:
1. You have deep knowledge of data patterns
2. Benchmarking shows improvement
3. Specific encoding provides measurable benefit

---

## Complete Example: Optimized Transaction Table

```sql
-- models/marts/finance/fct_transactions.sql
{{
  config(
    materialized='incremental',
    unique_key='transaction_id',
    dist='customer_id',  -- Joins with customer dimension
    sort=['transaction_timestamp', 'status'],  -- Most common filters
    on_schema_change='fail',
    post_hook='ANALYZE {{ this }}'
  )
}}

SELECT
    -- Optimized data types
    transaction_id::BIGINT,
    customer_id::BIGINT,
    transaction_timestamp::TIMESTAMP,
    
    -- Right-sized VARCHARs
    card_network::VARCHAR(10),
    card_type::VARCHAR(10),
    merchant_category::VARCHAR(30),
    status::VARCHAR(15),
    
    -- Proper numeric types
    amount_usd::DECIMAL(18, 2),
    merchant_id::BIGINT

FROM {{ ref('stg_transactions') }}

{% if is_incremental() %}
    WHERE transaction_timestamp > (SELECT MAX(transaction_timestamp) FROM {{ this }})
{% endif %}
```

**Why This Works:**
1. ✅ DISTKEY matches join column (customer_id)
2. ✅ SORTKEY matches primary filter (transaction_timestamp)
3. ✅ All data types right-sized
4. ✅ Incremental strategy reduces processing
5. ✅ ANALYZE updates statistics for query planner

---

## Monitoring Table Health

### Check Data Skew

Data skew means some nodes have much more data than others. This is BAD.

```sql
-- Check distribution across slices
SELECT 
    slice,
    COUNT(*) as row_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as pct_of_total
FROM {{ ref('fct_transactions') }}
GROUP BY slice
ORDER BY row_count DESC;

-- Ideal: All slices have similar percentages (within 10-15% of each other)
-- Bad: One slice has 40%, others have 5%
```

### Check Table Statistics

```sql
-- View table info
SELECT 
    "table",
    size,
    tbl_rows,
    skew_rows
FROM svv_table_info
WHERE "table" = 'fct_transactions'
  AND "schema" = 'analytics';
```

### Run ANALYZE Regularly

```sql
-- In dbt model post-hook
{{
  config(
    post_hook='ANALYZE {{ this }}'
  )
}}
```

Or manually:
```sql
ANALYZE fct_transactions;
```

**When to Run:**
- After significant data load (>10% of table)
- Weekly for active tables
- After schema changes

---

## Decision Framework: Choosing DISTKEY and SORTKEY

### Step 1: Understand Query Patterns

Ask these questions:
1. What tables are joined most often?
2. What columns are filtered most frequently?
3. What is the data volume?
4. Are there skew patterns?

### Step 2: Choose DISTKEY

```
Is table < 10M rows?
  ↓ YES → Use DISTKEY='all' (replicate)
  ↓ NO
  ↓
Does table join with another large table?
  ↓ YES → Use join column as DISTKEY
  |       Example: DISTKEY='customer_id'
  ↓ NO
  ↓
Is there significant data skew?
  ↓ YES → Use DISTKEY='even' or 'auto'
  |       Consider anti-pattern (even + replicate dimension)
  ↓ NO
  ↓
Use DISTKEY='even' or 'auto'
```

### Step 3: Choose SORTKEY

```
What column is filtered most often?
  ↓ Usually timestamp → Make it first SORTKEY column
  
Is there a second frequent filter?
  ↓ YES → Add as second SORTKEY column
  |       Example: SORTKEY=['timestamp', 'status']
  ↓ NO
  ↓
Use single-column SORTKEY
```

---

## Common Patterns by Table Type

### Large Fact Tables (Transactions, Events)
```yaml
dist: 'customer_id'  # Or account_id, user_id
sort: ['event_timestamp', 'event_type']
materialized: 'incremental'
```

### Small Dimension Tables (<10M rows)
```yaml
dist: 'all'  # Replicate
sort: 'dimension_id'
materialized: 'table'
```

### Aggregated Marts
```yaml
dist: 'all'  # Small result, replicate
sort: 'date_key'
materialized: 'table'
```

### Slowly Changing Dimensions
```yaml
dist: 'dimension_id'
sort: ['dimension_id', 'valid_from']
materialized: 'table'
```

---

## Troubleshooting

### Problem: Queries still slow after setting DISTKEY/SORTKEY

**Check:**
1. Are you actually filtering on SORTKEY columns?
2. Is ANALYZE run recently?
3. Is there data skew?
4. Are you using functions on SORTKEY columns in WHERE clause?

**Solutions:**
1. Add SORTKEY to WHERE clause
2. Run ANALYZE
3. Check data distribution (skew query above)
4. Rewrite filters to avoid functions on columns

---

### Problem: Joins are slow (data shuffling)

**Check EXPLAIN output for:**
- `DS_BCAST_DIST` (broadcast distribution)
- `DS_DIST_NONE` (no distribution key match)

**Solutions:**
1. Match DISTKEY on both joined tables
2. Use DISTKEY='all' for small dimensions
3. Consider anti-pattern for skewed data

---

### Problem: Data skew detected

**Symptoms:**
- One slice has 40% of data, others have 5-10%
- Queries slow despite good SORTKEY usage

**Causes:**
- DISTKEY on low-cardinality column
- DISTKEY on highly skewed column (e.g., top customers)

**Solutions:**
1. Change DISTKEY to higher-cardinality column
2. Use DISTKEY='even'
3. Apply anti-pattern (even + replicate dimension)

---

## Summary: The 3-Step Framework

### Step 1: Choose DISTKEY
- **Goal:** Even distribution + collocated joins
- **Most common:** Join column (customer_id, account_id)
- **Small tables:** 'all' (replicate)
- **Skewed data:** 'even' + replicate dimension

### Step 2: Choose SORTKEY
- **First column:** Most common filter (usually timestamp)
- **Second column:** Secondary filter used WITH first column
- **Keep it simple:** 1-2 columns maximum

### Step 3: Monitor and Adjust
- Check data skew regularly
- Run ANALYZE after loads
- Use EXPLAIN to verify query plans
- Adjust based on actual usage patterns

---

**Remember:** Table design is the foundation. Get this right, and everything else becomes easier.
