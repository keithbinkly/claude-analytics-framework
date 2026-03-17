# Redshift Intelligence Playbook

Empirical warehouse data that agents should query **before** making design decisions. Organized by decision point, not by system table.

**Principle:** Agents should make decisions from warehouse reality, not just heuristics. Query first, decide second.

---

## Phase 1: Build-Time Intelligence

### 1.1 DISTKEY Selection

**When:** Choosing DISTKEY for a new or redesigned table.

**Decision:** Which column to distribute on.

**Query: Find the most-joined columns for tables in this domain**
```sql
-- Which columns cause the most data redistribution during joins?
-- High bytes = wrong DISTKEY alignment. Target these for DISTKEY matching.
SELECT
    tbl,
    (SELECT "table" FROM svv_table_info WHERE "table"::oid = tbl) AS table_name,
    SUM(bytes) AS total_redistribution_bytes,
    COUNT(*) AS redistribution_events
FROM stl_dist
WHERE starttime >= DATEADD('day', -14, CURRENT_DATE)
GROUP BY 1
ORDER BY 3 DESC
LIMIT 20;
```

**Query: Check candidate DISTKEY skew BEFORE committing**
```sql
-- Replace 'candidate_column' and 'your_table' with actuals
SELECT
    candidate_column,
    COUNT(*) AS row_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM your_table
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20;
```

**Interpret:**
- No single value > 40% of rows → safe for DISTKEY
- 40-60% → marginal, consider `dist='even'` instead
- > 60% → do NOT use as DISTKEY, will cause severe skew
- If the column is also the most-joined column, accept up to 50% skew (join colocation benefit outweighs skew cost)

**Query: Check what existing tables use for DISTKEY (for join alignment)**
```sql
-- Find DISTKEY of tables this new model will join
SELECT "table", diststyle, sortkey1
FROM svv_table_info
WHERE "table" IN ('table_a', 'table_b', 'table_c')
ORDER BY "table";
```

**Action:** Match DISTKEY with the largest table you join on. If joining on `customer_id` and the fact table has `dist='customer_id'`, your model should too.

---

### 1.2 SORTKEY Selection

**When:** Choosing SORTKEY for a new table.

**Decision:** Which column(s) to sort on for zone map pruning.

**Query: What filters does BI actually use on similar tables?**
```sql
-- Extract WHERE clause patterns from recent queries against your domain
SELECT
    SUBSTRING(querytxt, 1, 500) AS query_sample,
    elapsed / 1000000.0 AS seconds,
    starttime
FROM stl_query
WHERE querytxt ILIKE '%your_table_or_domain%'
  AND querytxt ILIKE '%WHERE%'
  AND starttime >= DATEADD('day', -14, CURRENT_DATE)
  AND userid != 1  -- exclude admin
ORDER BY starttime DESC
LIMIT 30;
```

**Query: Are zone maps being used effectively on existing tables?**
```sql
-- Check scan efficiency: rows scanned vs rows returned
-- High ratio = zone maps not pruning (wrong SORTKEY or missing ANALYZE)
SELECT
    s.tbl,
    t."table" AS table_name,
    SUM(s.rows) AS total_rows_scanned,
    SUM(s.rows_pre_filter) AS rows_before_filter,
    CASE WHEN SUM(s.rows_pre_filter) > 0
        THEN ROUND(100.0 * SUM(s.rows) / SUM(s.rows_pre_filter), 2)
        ELSE NULL
    END AS scan_efficiency_pct
FROM stl_scan s
JOIN svv_table_info t ON s.tbl = t."table"::oid
WHERE s.starttime >= DATEADD('day', -7, CURRENT_DATE)
  AND t."table" IN ('relevant_table_1', 'relevant_table_2')
GROUP BY 1, 2
ORDER BY total_rows_scanned DESC;
```

**Interpret:**
- scan_efficiency_pct near 100% = zone maps pruning well (SORTKEY aligned with filters)
- scan_efficiency_pct < 10% = full table scan despite filters (SORTKEY misaligned or missing ANALYZE)

**Action:**
1. Put the most common WHERE clause column first in SORTKEY
2. Date columns almost always belong in SORTKEY (Tableau/BI filter by date range)
3. Run `ANALYZE table_name` after every `dbt run` (use `post_hook`)

---

### 1.3 Materialization Strategy

**When:** Deciding view vs table vs incremental for a new model.

**Decision:** How to materialize based on access patterns.

**Query: How often is this domain queried? By whom?**
```sql
-- Query frequency and cost for tables in this domain
SELECT
    CASE
        WHEN querytxt ILIKE '%model_name_1%' THEN 'model_name_1'
        WHEN querytxt ILIKE '%model_name_2%' THEN 'model_name_2'
        ELSE 'other'
    END AS target_model,
    COUNT(*) AS query_count,
    AVG(elapsed / 1000000.0) AS avg_seconds,
    MAX(elapsed / 1000000.0) AS max_seconds,
    COUNT(DISTINCT userid) AS distinct_users
FROM stl_query
WHERE starttime >= DATEADD('day', -14, CURRENT_DATE)
  AND (querytxt ILIKE '%model_name_1%' OR querytxt ILIKE '%model_name_2%')
GROUP BY 1
ORDER BY 2 DESC;
```

**Interpret:**
| Pattern | Recommendation |
|---------|---------------|
| > 50 queries/day, avg > 5s | Materialize as TABLE |
| > 50 queries/day, avg < 2s | Current materialization is fine |
| < 5 queries/day, any duration | VIEW is acceptable (save build time) |
| Growing avg duration over weeks | Consider incremental or pre-aggregation |
| Single BI service account dominates | Optimize DIST/SORT for that account's query patterns |

**Query: Table sizes for cost/benefit of materialization**
```sql
SELECT
    "table",
    tbl_rows,
    size AS size_mb,
    ROUND(size / 1024.0, 2) AS size_gb,
    diststyle,
    sortkey1,
    unsorted  -- % of table that needs re-sorting
FROM svv_table_info
WHERE "schema" = 'analytics'
  AND "table" LIKE 'mrt_%'
ORDER BY tbl_rows DESC;
```

---

### 1.4 Pre-Change STL Metric Snapshot (MANDATORY for Performance Changes)

**When:** Before deploying ANY performance-motivated change (DIST/SORT, materialization, query rewrite).

**Why:** STL tables have 2-5 day retention. If you deploy a change and then try to compare before/after, the "before" data may already be gone. Capture baseline FIRST.

**Step 1: Snapshot baseline query times**
```sql
-- Run BEFORE deploying changes. Save results to a temp table or file.
CREATE TABLE #baseline_metrics AS
SELECT
    DATE_TRUNC('hour', starttime) AS hour,
    COUNT(*) AS query_count,
    AVG(elapsed / 1000000.0) AS avg_seconds,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY elapsed / 1000000.0) AS p50_seconds,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY elapsed / 1000000.0) AS p95_seconds,
    MAX(elapsed / 1000000.0) AS max_seconds
FROM stl_query
WHERE querytxt ILIKE '%target_model%'
  AND starttime >= DATEADD('day', -7, CURRENT_DATE)
  AND userid != 1
GROUP BY 1
ORDER BY 1;

-- Also snapshot physical metadata
SELECT "table", diststyle, sortkey1, size, tbl_rows, skew_rows, unsorted
FROM svv_table_info
WHERE "table" = 'target_model';
```

**Step 2: Save to gitignored location**
```bash
# Save baseline metrics before deploying
dbt show --inline "SELECT * FROM #baseline_metrics" --output json > session-logs/baseline_target_model_$(date +%Y%m%d).json
```

**Step 3: After deploying, compare**
```sql
-- Use the saved baseline for matched comparison
-- (The #baseline_metrics temp table expires, so use the saved JSON if needed)
```

**Key lesson (from 2026-02-19 registration funnel QA):** Without pre-change snapshots, the QA agent could not find reliable before-samples in STL tables due to retention limits. This turned a straightforward before/after comparison into an inconclusive investigation.

---

## Phase 2: QA-Time Intelligence

### 2.1 Physical Layout Validation (Post-Deploy)

```sql
-- Confirm DISTKEY, SORTKEY, and table stats applied correctly
SELECT
    "schema",
    "table",
    diststyle,
    sortkey1,
    sortkey_num,
    size AS size_mb,
    tbl_rows,
    unsorted,
    skew_rows
FROM svv_table_info
WHERE "table" IN ('model_1', 'model_2', 'model_3')
ORDER BY "table";
```

**Check:**
- `diststyle` matches your config (`KEY(column)`, `EVEN`, `ALL`)
- `sortkey1` matches your first sort column
- `unsorted` < 20% (run VACUUM if high)
- `skew_rows` < 2.0 (> 4.0 = severe skew problem)

### 2.2 Before/After Performance Gate

```sql
-- Collect matched workload samples for runtime comparison
WITH baseline AS (
    SELECT elapsed / 1000000.0 AS seconds
    FROM stl_query
    WHERE userid = (SELECT usesysid FROM pg_user WHERE usename = 'svc_dbt_bi')
      AND querytxt ILIKE '%target_model%'
      AND starttime BETWEEN DATEADD('day', -14, CURRENT_DATE)
                        AND DATEADD('day', -7, CURRENT_DATE)
),
current AS (
    SELECT elapsed / 1000000.0 AS seconds
    FROM stl_query
    WHERE userid = (SELECT usesysid FROM pg_user WHERE usename = 'svc_dbt_bi')
      AND querytxt ILIKE '%target_model%'
      AND starttime >= DATEADD('day', -7, CURRENT_DATE)
)
SELECT
    (SELECT AVG(seconds) FROM baseline) AS baseline_avg_s,
    (SELECT AVG(seconds) FROM current) AS current_avg_s,
    (SELECT COUNT(*) FROM baseline) AS baseline_sample_n,
    (SELECT COUNT(*) FROM current) AS current_sample_n,
    CASE
        WHEN (SELECT AVG(seconds) FROM baseline) > 0
        THEN ROUND(100.0 * ((SELECT AVG(seconds) FROM baseline) - (SELECT AVG(seconds) FROM current))
            / (SELECT AVG(seconds) FROM baseline), 2)
        ELSE NULL
    END AS pct_improvement;
```

**Gate:** >= 30% improvement for performance-motivated changes. If < 30%, document as conditional pass and collect more samples.

### 2.3 Redshift Alert Review (Most Underutilized)

```sql
-- Redshift TELLS you what's wrong. Query this proactively.
SELECT
    event_time,
    solution AS alert_type,
    SUBSTRING(solution, 1, 200) AS recommendation,
    query,
    SUBSTRING(querytxt, 1, 200) AS query_preview
FROM stl_alert_event_log a
JOIN stl_query q ON a.query = q.query
WHERE a.event_time >= DATEADD('day', -7, CURRENT_DATE)
  AND q.querytxt ILIKE '%your_domain%'
ORDER BY a.event_time DESC
LIMIT 50;
```

**Common alerts and what to do:**

| Alert | Meaning | Agent Action |
|-------|---------|-------------|
| `Missing statistics` | ANALYZE not run | Add `post_hook: "ANALYZE {{ this }}"` |
| `Nested loop join` | Bad join plan, usually missing DISTKEY | Align DISTKEY on join columns |
| `Very selective filter` | Good filter but full scan | Add column to SORTKEY |
| `Cartesian product` | Cross join detected | Fix JOIN condition or add WHERE |
| `Distribution ds_dist_all` | Broadcasting large table | Consider DISTKEY change |

---

## Phase 3: Ongoing Intelligence

### 3.1 BI Query Pattern Discovery

**When:** Understanding what Tableau/Looker actually runs against your models.

```sql
-- What does the BI service account actually query?
SELECT
    REGEXP_REPLACE(
        SUBSTRING(querytxt, 1, 100),
        '(FROM|JOIN)\s+\w+\.(\w+)',
        '\1 \2'
    ) AS query_shape,
    COUNT(*) AS frequency,
    AVG(elapsed / 1000000.0) AS avg_seconds,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY elapsed / 1000000.0) AS p95_seconds
FROM stl_query
WHERE userid = (SELECT usesysid FROM pg_user WHERE usename = 'svc_dbt_bi')
  AND starttime >= DATEADD('day', -7, CURRENT_DATE)
  AND querytxt NOT ILIKE '%pg_catalog%'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 30;
```

**Action:** The top query patterns reveal what SORTKEY should be. If 80% of queries filter by `product_stack + date`, those are your SORTKEY columns.

### 3.2 Performance Regression Detection

```sql
-- Detect models getting slower over time
WITH weekly_stats AS (
    SELECT
        DATE_TRUNC('week', starttime) AS week,
        CASE
            WHEN querytxt ILIKE '%mrt_model_a%' THEN 'mrt_model_a'
            WHEN querytxt ILIKE '%mrt_model_b%' THEN 'mrt_model_b'
            ELSE 'other'
        END AS model,
        AVG(elapsed / 1000000.0) AS avg_seconds,
        COUNT(*) AS query_count
    FROM stl_query
    WHERE starttime >= DATEADD('week', -8, CURRENT_DATE)
      AND userid = (SELECT usesysid FROM pg_user WHERE usename = 'svc_dbt_bi')
    GROUP BY 1, 2
)
SELECT *
FROM weekly_stats
WHERE model != 'other'
ORDER BY model, week;
```

**Alert if:** avg_seconds increases > 50% week-over-week for same model.

### 3.3 Join Quality Analysis

```sql
-- Find queries with nested loop joins (almost always bad on Redshift)
SELECT
    query,
    segment,
    step,
    rows,
    SUBSTRING(querytxt, 1, 200) AS query_preview
FROM stl_nestloop n
JOIN stl_query q ON n.query = q.query
WHERE n.starttime >= DATEADD('day', -7, CURRENT_DATE)
ORDER BY n.rows DESC
LIMIT 20;
```

**Action:** Nested loops on Redshift indicate missing or misaligned DISTKEY. The optimizer couldn't find a hash join path. Fix the DISTKEY alignment between joined tables.

### 3.4 WLM Queue Pressure

```sql
-- Are queries spending time waiting in queue vs executing?
SELECT
    service_class,
    COUNT(*) AS query_count,
    AVG(queue_elapsed / 1000000.0) AS avg_queue_seconds,
    AVG(exec_elapsed / 1000000.0) AS avg_exec_seconds,
    ROUND(100.0 * AVG(queue_elapsed) / NULLIF(AVG(queue_elapsed + exec_elapsed), 0), 2) AS pct_time_queuing
FROM stl_wlm_query
WHERE starttime >= DATEADD('day', -7, CURRENT_DATE)
GROUP BY 1
ORDER BY pct_time_queuing DESC;
```

**Action:** If pct_time_queuing > 30%, the cluster needs WLM tuning or queries need to be faster to free slots.

---

## Decision Matrix: Which Queries to Run When

| Agent Phase | Required Queries | Optional Queries |
|-------------|-----------------|-----------------|
| **New model design** | 1.1 (DISTKEY skew + join alignment), 1.2 (BI filter patterns) | 1.3 (access frequency) |
| **DIST/SORT change** | 1.1 (skew check), 2.1 (physical validation), 2.2 (before/after) | 2.3 (alert review) |
| **Materialization change** | 1.3 (access frequency), 2.1 (physical validation), 2.2 (before/after) | 3.1 (BI patterns) |
| **Performance investigation** | 2.3 (alerts), 3.1 (BI patterns), 3.3 (join quality) | 3.2 (regression), 3.4 (WLM) |
| **Post-deploy QA** | 2.1 (physical), 2.2 (before/after) | 2.3 (alerts), 3.2 (regression) |
| **Periodic health check** | 3.2 (regression), 2.3 (alerts), 3.4 (WLM) | 3.3 (join quality) |

---

## System Table Quick Reference

| Table | What It Contains | Retention |
|-------|-----------------|-----------|
| `svv_table_info` | Physical metadata (DIST, SORT, rows, size, skew) | Current state |
| `stl_query` | Query history (text, elapsed, user) | ~2-5 days |
| `stl_explain` | Query execution plans | ~2-5 days |
| `stl_scan` | Table scan details (rows scanned, bytes) | ~2-5 days |
| `stl_dist` | Data redistribution during queries | ~2-5 days |
| `stl_hash` | Hash join performance | ~2-5 days |
| `stl_nestloop` | Nested loop joins (red flag) | ~2-5 days |
| `stl_alert_event_log` | Redshift optimizer warnings | ~2-5 days |
| `stl_wlm_query` | WLM queue + execution time | ~2-5 days |
| `svv_diskusage` | Per-slice disk usage (true skew) | Current state |
| `svl_query_summary` | Step-by-step query execution | ~2-5 days |
| `svl_compile` | Compilation time, plan caching | ~2-5 days |

**Note:** STL tables have limited retention (cluster-dependent, typically 2-5 days). For historical trending, snapshot key metrics into a persistent table or dbt model.

---

## Integration Points

| Agent | Uses Sections | How |
|-------|--------------|-----|
| **Builder** | Phase 1 (all) | Before choosing DIST/SORT/materialization |
| **QA** | Phase 2 (all) | During validation |
| **Redshift Optimization skill** | Phase 1 + Phase 3 | During optimization work |
| **Preflight** | 1.3 (table sizes) | Cost estimation |
| **System Architect** | Phase 3 (all) | Periodic health assessment |
