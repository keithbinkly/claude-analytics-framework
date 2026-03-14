# Incremental Strategies for Large Tables

## Purpose
Process only new or changed data instead of full table refreshes. Essential for tables > 100M rows.

**Impact:** 10-20x faster refresh times.

---

## When to Use Incremental Models

### Decision Criteria

| Table Characteristic | Use Incremental? |
|---------------------|------------------|
| > 100M rows | ✅ YES |
| Daily/hourly refresh | ✅ YES |
| Append-only (transactions, events) | ✅ YES |
| Updates/deletes common | ⚠️ MAYBE (use merge) |
| < 10M rows | ❌ NO (full refresh is fast) |
| Complex transformations | ⚠️ MAYBE (test performance) |

---

## Strategy 1: Append (Time-Based)

**Best for:** Transaction logs, event streams, immutable data

```sql
{{
  config(
    materialized='incremental',
    unique_key='transaction_id',
    dist='customer_id',
    sort=['transaction_timestamp', 'status'],
    incremental_strategy='append',
    on_schema_change='fail'
  )
}}

SELECT
    transaction_id,
    customer_id,
    transaction_timestamp,
    amount_usd,
    status
FROM {{ ref('stg_transactions') }}

{% if is_incremental() %}
    WHERE transaction_timestamp > (
        SELECT MAX(transaction_timestamp) FROM {{ this }}
    )
{% endif %}
```

**How it works:**
- First run: Processes all data
- Subsequent runs: Only processes new data (timestamp > max existing)
- No updates or deletes

**Performance:** Fastest strategy (no merge overhead)

---

## Strategy 2: Merge (Updates + Inserts)

**Best for:** Slowly changing dimensions, updateable facts

```sql
{{
  config(
    materialized='incremental',
    unique_key='customer_id',
    dist='customer_id',
    sort='updated_at',
    incremental_strategy='merge',
    on_schema_change='sync_all_columns'
  )
}}

SELECT
    customer_id,
    customer_name,
    customer_status,
    updated_at
FROM {{ ref('stg_customers') }}

{% if is_incremental() %}
    WHERE updated_at > (
        SELECT MAX(updated_at) FROM {{ this }}
    )
{% endif %}
```

**How it works:**
- Matches on `unique_key`
- Updates existing rows
- Inserts new rows
- More expensive than append

**Performance:** Slower than append, but handles updates

---

## Strategy 3: Delete+Insert

**Best for:** When you need to replace date partitions

```sql
{{
  config(
    materialized='incremental',
    unique_key='transaction_id',
    dist='customer_id',
    sort=['transaction_date', 'transaction_timestamp'],
    incremental_strategy='delete+insert'
  )
}}

SELECT
    transaction_id,
    customer_id,
    transaction_date,
    transaction_timestamp,
    amount_usd
FROM {{ ref('stg_transactions') }}

{% if is_incremental() %}
    WHERE transaction_date >= CURRENT_DATE - 3
{% endif %}
```

**How it works:**
- Deletes rows matching incremental predicate
- Inserts all new rows matching predicate
- Useful for reprocessing recent dates

---

## Advanced: Custom Incremental Logic

### Pattern: Process Last N Days

```sql
{{
  config(
    materialized='incremental',
    unique_key=['customer_id', 'metric_date'],
    dist='customer_id',
    sort='metric_date'
  )
}}

{% if is_incremental() %}
    -- Delete last 7 days to reprocess
    {{ delete_from_table(this, "metric_date >= CURRENT_DATE - 7") }}
{% endif %}

SELECT
    customer_id,
    metric_date,
    metric_value
FROM {{ ref('source_table') }}
{% if is_incremental() %}
    WHERE metric_date >= CURRENT_DATE - 7
{% endif %}
```

---

## Troubleshooting

### Problem: Incremental model misses data

**Symptoms:**
- Row counts don't match expected
- Data gaps in final table

**Causes:**
1. Incremental predicate wrong
2. Late-arriving data
3. Source timestamp not reliable

**Solutions:**
1. Validate predicate logic
2. Add lookback window: `WHERE timestamp > MAX(timestamp) - INTERVAL '1 day'`
3. Use sequence number instead of timestamp if available

---

### Problem: Incremental slower than expected

**Check:**
1. Is unique_key indexed properly? (Redshift doesn't have indexes, but check DISTKEY/SORTKEY)
2. Is merge needed or would append work?
3. Is incremental predicate using SORTKEY?

**Solutions:**
1. Ensure SORTKEY matches incremental filter
2. Switch to append if updates not needed
3. Consider processing in smaller batches

---

## Full Refresh Strategy

### When to Full Refresh

- Schema changes require it
- Data quality issues detected
- Logic changes significantly
- Periodic validation (monthly/quarterly)

```bash
# Command line
dbt run --full-refresh --select model_name

# Or in model
dbt run --full-refresh --select +model_name+  # Include upstream/downstream
```

---

## Summary: Strategy Selection

| Data Pattern | Strategy | Why |
|--------------|----------|-----|
| Append-only events | `append` | Fastest, simplest |
| Updates rare | `append` | Good enough |
| Updates common | `merge` | Handles changes |
| Reprocess partitions | `delete+insert` | Replaces chunks |
| Complex changes | Custom logic | Maximum control |

**Remember:** Start with append, add complexity only when needed.
