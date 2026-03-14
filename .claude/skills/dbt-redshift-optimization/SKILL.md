---
name: dbt-redshift-optimization
description: |
  Comprehensive Redshift optimization for dbt projects. Analyzes SQL queries, detects
  anti-patterns, recommends table design improvements, and generates optimized rewrites.
  Use when asked about "optimize performance", "slow query", "distribution key", "incremental
  strategy", "DISTKEY", "SORTKEY", "query against Redshift", "this model is slow", "reduce
  runtime", "query plan", or "why is this taking so long". Also use when reviewing SQL for
  Redshift-specific anti-patterns or choosing between incremental strategies (delete+insert
  vs merge). Covers table design, incremental strategies, window functions, and advanced
  performance patterns.
---

# Redshift SQL Optimization Reference

Optimization patterns for dbt models and SQL queries on Amazon Redshift. Focus on table design (DISTKEY/SORTKEY), query patterns, and advanced techniques for high-volume financial data.

**Core principle:** Minimize data scanned, shuffled, and written. Correct table design beats query tweaking.

---

## Reference Tools

**Before optimizing, you MUST check:**

| Tool | Path | Check Before | Why |
|------|------|--------------|-----|
| **Anti-Patterns** | `shared/reference/anti-pattern-impact.yml` | ANY optimization | Quantified impact data |
| **Join Registry** | `shared/reference/baas-join-registry.yml` | Join optimization | Known join patterns |

### Anti-Pattern Impact Reference

| Pattern | Impact | Fix |
|---------|--------|-----|
| `NOT IN (subquery)` | 4.18x slower | Use `NOT EXISTS` |
| `OR` in JOIN | 4.07x slower | Use `UNION ALL` |
| Nested subqueries 3+ | 3.06x slower | Use CTEs |
| `SELECT *` | 2.08x slower | List columns |

---

## Quick Decision Tree

### "My query is slow. What do I do?"

```
START
  ↓
Is the table > 100M rows?
  ↓ YES → Check table design (DISTKEY/SORTKEY)
  |       → See: resources/table-design.md
  ↓ NO
  ↓
Does query have anti-patterns?
  - GROUPING SETS
  - Nested subqueries (>3 levels)
  - SELECT *
  - Functions on filter columns
  ↓ YES → Rewrite query
  |       → See: resources/query-patterns.md
  ↓ NO
  ↓
Is it incremental model scanning too much data?
  ↓ YES → Optimize incremental strategy
  |       → See: resources/incremental-strategies.md
  ↓ NO
  ↓
Does it use complex window functions or joins?
  ↓ YES → Apply advanced patterns
          → See: resources/advanced-patterns.md
```

---

## When to Use Each Resource

### 1. Table Design (`resources/table-design.md`)
**Use when:**
- Creating new fact or dimension tables
- Query scans too many rows despite filters
- Joins are slow (data shuffling)
- New dbt model for large dataset

**Key Topics:**
- DISTKEY selection (collocated joins)
- SORTKEY selection (data pruning)
- Data type optimization
- Compression encoding
- Anti-pattern: Using DISTKEY on skewed data

**Quick Win:** Correct DISTKEY + SORTKEY = 5-10x speedup

---

### 2. Query Patterns (`resources/query-patterns.md`)
**Use when:**
- Writing new SQL/dbt models
- Query has anti-patterns flagged
- Need to rewrite legacy SQL
- Performance review of existing models

**Key Topics:**
- Filter early (use SORTKEY in WHERE)
- SELECT only required columns
- Avoid functions on filter columns
- Predicate pushdown
- Anti-patterns: GROUPING SETS, nested subqueries, SELECT *, Cartesian joins

**Quick Win:** Remove SELECT * + add filters = 2-5x speedup

---

### 3. Incremental Strategies (`resources/incremental-strategies.md`)
**Use when:**
- Table > 100M rows
- Daily/hourly refresh pattern
- Full refresh takes too long
- Need to process only new/changed data

**Key Topics:**
- Time-based incremental (append)
- Merge strategy (updates + inserts)
- Delete+insert strategy
- When to use full refresh
- Troubleshooting incremental models

**Quick Win:** Convert large table to incremental = 10-20x faster refreshes

---

### 4. Advanced Patterns (`resources/advanced-patterns.md`)
**Use when:**
- Need expert-level optimization
- Building complex analytical models
- Dealing with data skew
- High-frequency queries (dashboards)
- Transaction sessionization
- Customer behavior analysis

**Key Topics:**
- DISTKEY anti-pattern (for skewed data)
- Short Query Acceleration (SQA) for RFM
- Transaction sessionization (gaps & islands)
- Conditional aggregation
- QUALIFY clause patterns
- Materialized views

**Quick Win:** Apply advanced pattern = 10-30x speedup for specific use cases

---

### 5. Balance Optimization (`resources/balance-optimization.md`)
**Use when:**
- Daily snapshot tables (accounts, balances)
- Billions of rows with low change rate
- Need to analyze dormancy or stability
- Account tier classification

**Key Topics:**
- Delta model (event-based vs daily snapshots)
- Account tier classification
- Balance volatility analysis
- 80-90% data reduction techniques

**Quick Win:** Delta model = 10x storage reduction + 10x query speedup

---

## Common Use Cases

### Use Case 1: Optimize New dbt Model
**Scenario:** Creating a new `fct_transactions` model for 500M rows.

**Steps:**
1. Read `resources/table-design.md` → Choose DISTKEY/SORTKEY
2. Read `resources/query-patterns.md` → Write optimized SQL
3. Read `resources/incremental-strategies.md` → Set up incremental logic
4. Test and measure performance

**Config Example:**
```yaml
{{
  config(
    materialized='incremental',
    unique_key='transaction_id',
    dist='customer_id',
    sort=['transaction_timestamp', 'status'],
    incremental_strategy='append'
  )
}}
```

---

### Use Case 2: Fix Slow Query
**Scenario:** Dashboard query takes 60 seconds, needs to be <5 seconds.

**Steps:**
1. Run EXPLAIN on query
2. Check for anti-patterns → `resources/query-patterns.md`
3. Check table design → `resources/table-design.md`
4. Apply rewrites
5. Validate with EXPLAIN ANALYZE

**Common Fixes:**
- Add SORTKEY filter to WHERE clause
- Remove SELECT *
- Convert GROUPING SETS to UNION ALL
- Flatten nested subqueries to CTEs

---

### Use Case 3: Optimize Customer 360 Metrics
**Scenario:** Need fast customer segmentation queries for dashboards.

**Steps:**
1. Read `resources/advanced-patterns.md` → SQA pattern
2. Pre-calculate metrics in materialized models
3. Use DISTKEY='all' for small dimension tables
4. Apply conditional aggregation

**Result:** 30-second queries → <2 seconds

---

### Use Case 4: Handle Daily Balance Snapshots
**Scenario:** 1 billion accounts × 365 days = 365 billion rows.

**Steps:**
1. Read `resources/balance-optimization.md`
2. Implement delta model (store only changes)
3. Build tier classification on top
4. Monitor data reduction

**Result:** 365B rows → 30-50B rows (10x reduction)

---

## Performance Estimation Framework

### Quick Estimates

| Optimization | Expected Speedup | Difficulty |
|--------------|------------------|------------|
| Add correct SORTKEY filter | 5-10x | Easy |
| Fix DISTKEY (collocated join) | 3-5x | Medium |
| Remove SELECT * | 2-3x | Easy |
| Convert to incremental | 10-20x | Medium |
| Apply delta model | 10x | Hard |
| Use materialized views | 15-30x | Medium |
| Advanced patterns (sessionization) | 10-20x | Hard |

### Complexity Scoring

**Simple (1-3):** Basic SELECT, single table, few columns
**Moderate (4-6):** Joins, aggregations, window functions
**Complex (7-10):** Multiple CTEs, nested logic, advanced analytics

---

## Integration with dbt

### Model Configuration Patterns

**Staging (Views):**
```yaml
{{
  config(
    materialized='view',
    dist='customer_id',
    sort='transaction_timestamp'
  )
}}
```

**Intermediate (Tables/Incremental):**
```yaml
{{
  config(
    materialized='incremental',
    unique_key='id',
    dist='customer_id',
    sort=['created_at', 'status']
  )
}}
```

**Marts (Tables with Aggregations):**
```yaml
{{
  config(
    materialized='table',
    dist='all',  # Small result, replicate
    sort='date',
    post_hook='ANALYZE {{ this }}'
  )
}}
```

---

## Troubleshooting Guide

### Problem: Query scanning too many rows
**Check:** EXPLAIN output, look for full table scans
**Solution:** 
1. Add SORTKEY column to WHERE clause
2. Verify SORTKEY is set correctly on table
3. Run ANALYZE on table

**Resource:** `resources/table-design.md`, `resources/query-patterns.md`

---

### Problem: Joins are slow (data shuffling)
**Check:** EXPLAIN shows DS_BCAST_DIST or DS_DIST_NONE
**Solution:**
1. Match DISTKEY on joined tables
2. For small dimensions, use DISTKEY='all'
3. For skewed data, use DISTKEY anti-pattern

**Resource:** `resources/table-design.md`, `resources/advanced-patterns.md`

---

### Problem: Incremental model slow or incorrect
**Check:** How much data is processed each run?
**Solution:**
1. Verify incremental predicate is efficient
2. Check if SORTKEY helps filter
3. Consider merge vs. append strategy
4. Validate unique_key is correct

**Resource:** `resources/incremental-strategies.md`

---

### Problem: Dashboard queries timeout
**Check:** Query frequency, result size
**Solution:**
1. Pre-calculate in materialized model
2. Use conditional aggregation (single pass)
3. Apply Short Query Acceleration pattern

**Resource:** `resources/advanced-patterns.md`

---

### Problem: Daily snapshots table too large
**Check:** How many rows unchanged daily?
**Solution:**
1. Implement delta model (store only changes)
2. Use window functions to detect changes
3. Build tier classification on delta table

**Resource:** `resources/balance-optimization.md`

---

## Best Practices Checklist

### Before Writing Any SQL
- [ ] Understand the query pattern (filtering, joining, aggregating)
- [ ] Know the data volume (rows, bytes)
- [ ] Identify the most selective filter (usually timestamp)
- [ ] Plan DISTKEY for joins
- [ ] Plan SORTKEY for filters

### For Every dbt Model
- [ ] Set materialization appropriately (view/table/incremental)
- [ ] Configure DISTKEY
- [ ] Configure SORTKEY (compound for multiple filters)
- [ ] Add post-hook: ANALYZE {{ this }}
- [ ] Document the optimization choices in YAML

### After Model Creation
- [ ] Run EXPLAIN to verify query plan
- [ ] Check data skew (rows per slice)
- [ ] Monitor query performance
- [ ] Set up alerts for slow queries

---

## Performance Monitoring

### Key Metrics to Track
1. **Query runtime** (compare before/after)
2. **Rows scanned** (from EXPLAIN)
3. **Data skew** (max rows per slice / avg rows per slice)
4. **Compilation time** (dbt compilation + Redshift planning)
5. **Storage size** (compression effectiveness)

### How to Measure
```sql
-- Check data skew
SELECT 
    slice,
    COUNT(*) as row_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as pct_of_total
FROM your_table
GROUP BY slice
ORDER BY row_count DESC;

-- Check table stats
SELECT 
    "table",
    size,
    tbl_rows,
    skew_rows
FROM svv_table_info
WHERE "table" = 'your_table';
```

---

## Getting Started

### Step 1: Assess Current State
Run performance audit on slowest queries:
1. Identify top 10 slowest models (dbt run logs)
2. Run EXPLAIN on each
3. Document current runtime and rows scanned

### Step 2: Prioritize Optimizations
Focus on:
1. **High-impact, low-effort:** Add filters, remove SELECT *
2. **High-impact, medium-effort:** Fix DISTKEY/SORTKEY
3. **High-impact, high-effort:** Convert to incremental, advanced patterns

### Step 3: Implement and Measure
For each optimization:
1. Read relevant resource file
2. Apply changes
3. Test in dev
4. Measure improvement
5. Deploy to prod
6. Monitor

### Step 4: Document
Update model YAML with:
- Why DISTKEY/SORTKEY chosen
- Expected performance characteristics
- Optimization decisions made

---

## Summary: The 3-Layer Optimization Framework

### Layer 1: Foundation (Table Design)
**Impact:** 5-10x speedup
**Effort:** Medium
**Resource:** `table-design.md`

Get DISTKEY and SORTKEY right. Everything else builds on this.

---

### Layer 2: Query Patterns (SQL Best Practices)
**Impact:** 2-5x speedup
**Effort:** Easy to Medium
**Resource:** `query-patterns.md`, `incremental-strategies.md`

Write queries that leverage your table design. Use filters, avoid anti-patterns.

---

### Layer 3: Advanced Techniques (Expert Patterns)
**Impact:** 10-30x speedup for specific cases
**Effort:** Hard
**Resource:** `advanced-patterns.md`, `balance-optimization.md`

Apply when foundational optimization isn't enough. Domain-specific patterns.

---

## Quick Reference: Load the Right Resource

| Your Question | Load This Resource |
|---------------|-------------------|
| "How do I set DISTKEY/SORTKEY?" | `table-design.md` |
| "What anti-patterns should I avoid?" | `query-patterns.md` |
| "How do I make incremental models faster?" | `incremental-strategies.md` |
| "How do I optimize for skewed data?" | `advanced-patterns.md` |
| "How do I handle daily balance snapshots?" | `balance-optimization.md` |
| "What's the fastest way to calculate RFM?" | `advanced-patterns.md` |
| "How do I sessionize transactions?" | `advanced-patterns.md` |

---

**Remember:** The best optimization is the one that makes your schema do the work. Start with table design, then write queries that leverage it.
