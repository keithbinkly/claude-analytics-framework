# Unified Redshift Anti-Pattern Guide

**Version:** 1.0.0
**Last Updated:** 2026-01-23

This guide combines **syntactic** (detected from SQL text) and **physical** (detected from runtime metrics) anti-patterns into a unified reference.

---

## Quick Reference: All Anti-Patterns

### Tier 1: Critical (Fix Immediately)

| ID | Pattern | Type | Impact | Detection |
|----|---------|------|--------|-----------|
| **S-01** | `NOT IN (subquery)` | Syntactic | **4.18x** slower | Code review |
| **S-02** | `OR in JOIN` | Syntactic | **4.07x** slower | Code review |
| **P-01** | Disk Spiller | Physical | Memory exhaustion | `temp_blocks > 0` |
| **P-02** | Skewed Worker | Physical | CPU saturation | `cpu_skew > 0.95` |

### Tier 2: High (Fix in Sprint)

| ID | Pattern | Type | Impact | Detection |
|----|---------|------|--------|-----------|
| **S-03** | Deep nesting (3+) | Syntactic | **3.06x** slower | Code review |
| **P-03** | Ghost Scanner | Physical | I/O waste | `scan_rows > 10M, return < 100` |
| **P-04** | Cartesian Bomb | Physical | Row explosion | `join_rows > inputs * 10` |

### Tier 3: Medium (Track)

| ID | Pattern | Type | Impact | Detection |
|----|---------|------|--------|-----------|
| **S-04** | `SELECT *` | Syntactic | **2.08x** slower | Code review |
| **P-05** | Serial Leader | Physical | Leader bottleneck | High CPU on `aggr` step |
| **S-05** | `DISTINCT` in aggregation | Syntactic | **1.33x** slower | Code review |
| **S-06** | Accidental `CROSS JOIN` | Syntactic | **1.28x** slower | Code review |

---

## Syntactic Anti-Patterns (Detected from SQL Text)

These patterns can be caught **before execution** during code review or CI/CD.

### S-01: NOT IN Subquery

**Impact:** 4.18x slower than baseline
**Why it fails:** NULL handling issues prevent optimizer from using efficient anti-join.

```sql
-- BAD: NOT IN subquery
SELECT * FROM orders
WHERE customer_id NOT IN (SELECT customer_id FROM churned_customers)

-- GOOD: NOT EXISTS (use this)
SELECT * FROM orders o
WHERE NOT EXISTS (
    SELECT 1 FROM churned_customers c
    WHERE c.customer_id = o.customer_id
)
```

### S-02: OR in JOIN Condition

**Impact:** 4.07x slower than baseline
**Why it fails:** OR prevents hash/merge joins, forcing nested loop scans.

```sql
-- BAD: OR in JOIN
SELECT * FROM transactions t
JOIN accounts a ON t.from_account = a.id OR t.to_account = a.id

-- GOOD: UNION ALL with separate joins
SELECT t.*, a.* FROM transactions t
JOIN accounts a ON t.from_account = a.id
UNION ALL
SELECT t.*, a.* FROM transactions t
JOIN accounts a ON t.to_account = a.id
WHERE t.from_account != t.to_account
```

### S-03: Deep Nesting (3+ Levels)

**Impact:** 3.06x slower than baseline
**Why it fails:** Deep subqueries are harder for optimizer to flatten and parallelize.

```sql
-- BAD: Nested subqueries
SELECT * FROM (
    SELECT * FROM (
        SELECT * FROM (
            SELECT * FROM orders WHERE status = 'active'
        ) x WHERE amount > 100
    ) y WHERE region = 'US'
) z WHERE customer_type = 'premium'

-- GOOD: Flat CTEs
WITH active_orders AS (
    SELECT * FROM orders WHERE status = 'active'
),
high_value AS (
    SELECT * FROM active_orders WHERE amount > 100
),
us_region AS (
    SELECT * FROM high_value WHERE region = 'US'
)
SELECT * FROM us_region WHERE customer_type = 'premium'
```

### S-04: SELECT *

**Impact:** 2.08x slower than baseline
**Why it fails:** Redshift is columnar; fewer columns = less I/O.

```sql
-- BAD: SELECT *
SELECT * FROM large_table

-- GOOD: Explicit columns
SELECT id, customer_id, amount, created_at FROM large_table
```

### S-05: DISTINCT in Aggregation

**Impact:** 1.33x slower than baseline
**Why it fails:** COUNT(DISTINCT) requires sorting/hashing entire dataset.

```sql
-- BAD: COUNT DISTINCT
SELECT COUNT(DISTINCT customer_id) FROM orders

-- GOOD: Pre-aggregate
WITH distinct_customers AS (
    SELECT customer_id FROM orders GROUP BY customer_id
)
SELECT COUNT(*) FROM distinct_customers

-- ALTERNATIVE: Approximate (if exact not needed)
SELECT APPROXIMATE COUNT(DISTINCT customer_id) FROM orders
```

### S-06: Accidental CROSS JOIN

**Impact:** 1.28x slower than baseline
**Why it fails:** Cross joins produce M x N rows; often indicates missing join condition.

```sql
-- BAD: Implicit cross join
SELECT * FROM table_a, table_b

-- GOOD: Explicit join
SELECT * FROM table_a
INNER JOIN table_b ON table_a.key = table_b.key
```

---

## Physical Anti-Patterns (Detected from Runtime Metrics)

These patterns are detected **after execution** by analyzing `svl_query_metrics`.

### P-01: The Disk Spiller

**Signature:** `temp_blocks_to_disk > 0`
**Why it fails:** Memory exhaustion forces slow disk I/O.

**Common Causes:**
- Cartesian products (missing join keys)
- Wide rows (`SELECT *`)
- Hash joining two very large unsorted tables

**Fix:**
1. Reduce columns selected
2. Review join logic for fan-out
3. Request larger WLM slot (if valid use case)

**Example:** See `optimization_gallery/01_mega_case_distinct/`

### P-02: The Skewed Worker

**Signature:** `cpu_skew > 0.95` OR `io_skew > 0.95`
**Why it fails:** One node does 98%+ of work while others idle.

**Common Causes:**
- Poor DISTKEY (low cardinality or many NULLs)
- `GROUP BY` on skewed column
- Large table broadcast

**Fix:**
1. Change DISTKEY to high-cardinality column (`user_id`, not `status`)
2. Run `ANALYZE` to update statistics
3. Consider `DISTSTYLE EVEN` if no join benefit

**Example:** See `optimization_gallery/02_skewed_join_card_apps/`

### P-03: The Ghost Scanner

**Signature:** `scan_row_count > 10,000,000` AND `return_row_count < 100`
**Why it fails:** Scans massive data but throws 99.999% away.

**Common Causes:**
- Filter column is not a SORTKEY
- Functions on columns defeat zone maps: `DATE_TRUNC('month', col) = ...`
- Table needs VACUUM

**Fix:**
1. Add filter column to SORTKEY
2. Rewrite: `WHERE col BETWEEN ... AND ...` instead of functions
3. Run `VACUUM SORT ONLY`

**Example:** See `optimization_gallery/03_heavy_scanner_mstr/`

### P-04: The Cartesian Bomb

**Signature:** `join_row_count > (left_input + right_input) * 10`
**Why it fails:** Join produces more rows than inputs (fan-out).

**Common Causes:**
- Many-to-many joins (non-unique keys on both sides)
- Missing key in composite join
- Duplicate data in source tables

**Fix:**
1. Verify grain: `SELECT COUNT(*), COUNT(DISTINCT key) FROM table`
2. Aggregate child to parent grain BEFORE joining

### P-05: The Serial Leader

**Signature:** `step_label = 'aggr'` AND high `cpu_time`
**Why it fails:** Final aggregation bottlenecks on single Leader node.

**Common Causes:**
- `LISTAGG` function
- `MEDIAN` / percentile functions
- Complex Python UDFs

**Fix:**
1. Push aggregation to compute nodes via subqueries
2. Remove Leader-only functions if possible

---

## Combined Pattern Detection

Some issues manifest as BOTH syntactic AND physical patterns:

| Syntactic Pattern | Often Causes Physical Pattern |
|-------------------|------------------------------|
| `SELECT *` | Disk Spiller (wide rows) |
| `OR in JOIN` | Cartesian Bomb (fan-out) |
| Deep nesting | Skewed Worker (poor distribution) |
| `NOT IN (subquery)` | Ghost Scanner (full scans) |
| `CROSS JOIN` | Cartesian Bomb |

**Best practice:** Check BOTH during code review (syntactic) AND after execution (physical).

---

## Integration with Existing Tools

### In dbt Models
Reference `shared/reference/anti-pattern-impact.yml` for substitution patterns.

### In MicroStrategy
Use filters aligned with SORTKEY. See `optimization_gallery/03_heavy_scanner_mstr/`.

### In Ad-Hoc Analysis
Use `COPILOT_SELF_SERVICE.md` guide with GitHub Copilot.

---

## Measured Impact Summary

| Detection Type | Patterns | Queries Analyzed | Key Insight |
|---------------|----------|------------------|-------------|
| **Syntactic** | 6 patterns | 474,144 queries | `NOT IN` is worst (4.18x) |
| **Physical** | 5 patterns | 186,448 queries | 98.5% of runtime is problematic |

**Combined coverage:** Detects issues at code review time (syntactic) AND in production (physical).

---

## References

- **Syntactic patterns:** `shared/reference/anti-pattern-impact.yml`
- **Physical patterns:** `ANTI_PATTERN_DIRECTORY.md`
- **Optimization examples:** `optimization_gallery/`
- **Top offenders:** `OFFENDER_REGISTRY.md`
- **Self-service guide:** `COPILOT_SELF_SERVICE.md`
