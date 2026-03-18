# Builder — Napkin

Corrections, anti-patterns, and things that went wrong. Updated as patterns emerge.

---

## Anti-Patterns (from production experience)

### Copilot Trust Issue
**Problem:** Copilot checks compiled SQL instead of actual warehouse state. Iterates on code when `dbt run --full-refresh` was needed.
**Fix:** Always verify warehouse reality. Decision framework at `shared/reference/copilot-decision-framework.md`.

### eWallet 1:1 Assumption
**Problem:** Assumed 1:1 join between posted and auth eWallet transactions. Reality was M:N. Caused row fanout.
**Fix:** Always verify join cardinality with `COUNT(DISTINCT)` before and after joins. Check join registry.

### Skipping Pre-flight
**Problem:** Running `dbt run` on large models without cost estimation. Hit runtime thresholds.
**Fix:** Pre-flight check is mandatory. Use `dbt-preflight` skill.

### Folder Placement Guessing
**Problem:** Placing models in wrong folders without checking architecture docs.
**Fix:** Always validate against `shared/knowledge-base/folder-structure-and-naming.md`.

### Not Checking Canonical Registry
**Problem:** Writing custom logic that already exists as a canonical model/macro.
**Fix:** Search `shared/knowledge-base/canonical-models-registry.md` before writing ANY new logic.

## Patterns That Work

- **Compile-first workflow**: Write SQL → compile → fix → compile again → only then run
- **Canonical model search before every new model**: Registry check saves hours of reimplementation
- **DuckDB CTE injection for unit tests**: Test logic without VPN, catch issues before warehouse run
- **PLAN.md as state machine**: Any session can resume without context loss
- **Environment-aware date limits**: Always apply `{{ var('start_date') }}` / `{{ var('end_date') }}`

---

### Unnecessary Wide-to-Long Pivoting
**Problem:** Converting WIDE output to LONG format when the consumer (cohort analysis, time-series) needs WIDE. `mrt_cohort__analysis` had 23 UNION ALL branches multiplying rows 23x before being pivoted back to WIDE at the mart layer.
**Fix:** Match format to what the consumer needs. If output needs WIDE, stay WIDE. Delete intermediate LONG models that add no value. Eliminating `int_cohort__metrics_long` removed the single largest performance bottleneck in Arc Insights.

### OR in JOIN Conditions
**Problem:** Using `OR` in JOIN predicates causes Redshift to perform full cross-join scans. Example: `ON a.id = b.id OR a.alt_id = b.alt_id`. Impact: 4.07x slower.
**Fix:** Rewrite as `UNION ALL` with two separate joins, each with a single equality condition. Reference: `shared/reference/anti-pattern-impact.yml`.

### Deep CTE Nesting (3+ Levels)
**Problem:** Nesting CTEs three or more levels deep forces the query planner to materialize intermediate results, often without statistics. Impact: 3.06x slower.
**Fix:** Flatten to a maximum of 2 levels. If logic is complex, break into an intermediate dbt model with its own materialization.

### SELECT * in Production Models
**Problem:** `SELECT *` in dbt models breaks when upstream schemas change, hides column lineage, and prevents the query planner from pruning columns. Impact: 2.08x slower.
**Fix:** Always use explicit column lists. Document column purpose in schema.yml.

### Temporary Debug Filters Left in Production Code
**Problem:** Hardcoded date filters (`calendar_date >= CURRENT_DATE - 7`) added during development silently override macro-based date logic in production. The batch-loading remediation handoff was created because TEMP DEBUG FILTERs in `int_transactions__auth_all` and `int_transactions__posted_all` limited production data to 7 days instead of 2021-01-01.
**Fix:** Mark every temporary filter with `-- TEMP DEBUG FILTER: REMOVE BEFORE PROD`. Create a follow-up handoff item when adding any such filter. Never run `--full-refresh` in production without confirming no debug filters are active.

### Trusting DBT_PROFILES_DIR with Tilde (~) Expansion
**Problem:** `export DBT_PROFILES_DIR=~/.dbt` fails with dbt-fusion. Fusion does not expand `~` reliably, causing `dbt1005: No profiles.yml found at ~/.dbt/profiles.yml`.
**Fix:** Always use absolute paths: `export DBT_PROFILES_DIR="$HOME/.dbt"`. For VS Code settings, use `${env:HOME}/.dbt`. This bit a production onboarding session and cost 45+ minutes.

### Upstream Deferral Masking Local Schema Changes
**Problem:** When `upstream_prod_enabled: true` is set, `dbt show` resolves upstream refs against production models. Local schema additions (new columns) are invisible in `dbt show` output even after compilation succeeds locally. Caused a false "mcc_desc is missing" diagnosis.
**Fix:** When validating new column additions, run `dbt show` with `--vars '{"upstream_prod_enabled": false}'` or equivalent. Only re-enable deferral after verifying local model outputs are correct.

### UNION ALL Schema Mismatch (Shift-Left Column Additions)
**Problem:** Adding a column to one branch of a UNION ALL model without updating all other branches causes `dbt0301` compilation errors. Easy to miss when there are 5+ UNION branches.
**Fix:** When adding a column to any model with UNION ALL, grep for all CTE branches that participate in the union and add the column (or a `NULL AS column_name` placeholder) to every branch.

### NOT IN (Subquery) for Filtering
**Problem:** `NOT IN (SELECT id FROM defunct_table)` is 4.18x slower than alternatives on Redshift, and returns unexpected results when the subquery contains NULLs (entire filter evaluates to false).
**Fix:** Use `NOT EXISTS (SELECT 1 FROM defunct_table WHERE defunct_table.id = main.id)` or `LEFT JOIN ... WHERE defunct_table.id IS NULL`. Validated in `int_edw_kpi__account_base` where this shrunk the workset by ~150M rows before 8 downstream joins.

### Redshift Stuck Temp Tables After Session Crash
**Problem:** If a dbt run is interrupted (SIGINT, crash), Redshift may retain `#temp` tables in the session. Subsequent runs fail with `42P07: Relation already exists`.
**Fix:** Create and run `macros/temp_drop_table.sql` to force-drop the stuck table. Standard `DROP TABLE IF EXISTS #temp_name` in a macro invoked via `dbt run-operation` works. Cost if missed: 15+ min debugging a spurious error.
