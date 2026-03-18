# QA — Napkin

Corrections, anti-patterns, and common QA failures. Updated as patterns emerge.

---

## Anti-Patterns

### Row Count Only
**Problem:** Comparing only row counts. Hides offsetting errors (e.g., 100 rows added, 100 different rows dropped).
**Fix:** Always use Template 1 (granular variance) first. Row counts are necessary but NOT sufficient.

### Totals-Only Comparison
**Problem:** Comparing aggregated totals masks dimension-level issues. Total revenue matches but partner-level is off by 15%.
**Fix:** Drill down with Template 3 on every dimension before declaring PASS.

### "Close Enough" on 0.2%
**Problem:** Rounding away small variances. They compound across dimensions and time periods.
**Fix:** Investigate anything > 0.1%. The threshold is not negotiable.

### NULL Silent Drops
**Problem:** NULLs silently drop from aggregates. `SUM(amount)` excludes NULL rows without warning.
**Fix:** Use `COALESCE(amount, 0)` in comparisons. Count NULLs separately.

### No Date Bounds
**Problem:** Running validation queries without date filters. Full table scans are slow and include irrelevant data.
**Fix:** Always filter to the relevant date range for comparison.

### Declaring FAIL Without Root Cause
**Problem:** Flagging variance without tracing to the specific SQL logic that causes it.
**Fix:** Always trace to specific model + specific logic. Migration agent can't fix what's unknown.

### Skipping Decision Trace Lookup
**Problem:** Spending 45 minutes investigating an issue that was already solved 3 sessions ago.
**Fix:** Search `shared/decision-traces/` BEFORE investigating. The same pattern repeats.

## Patterns That Work

- **Template 1 → 2 → 3 → 4 order**: Granular first, then aggregate, then drill-down, then trends
- **Hypothesis → test → confirm/reject cycle**: Structured investigation beats random querying
- **Decision trace reuse**: 76% reduction in resolution time when traces exist
- **Dual-mode QA**: DuckDB for logic (no VPN), Redshift for production validation (VPN)
- **QA templates pre-written in handoff**: Builder creates the validation SQL, QA agent runs it

---

### Investigating Fan-Out in the Reported Model When Root Cause Is a Sister Stream
**Problem:** Spent time verifying posted_all (which was clean at 0.0% inflation) before discovering auth_all had 64 duplicates. The ticket said "posted fan-out" but the actual inflation came from auth_all fan-out affecting downstream shared aggregates.
**Fix:** When fan-out is reported, check grain integrity on ALL streams that feed the downstream metric simultaneously. Don't serialize the investigation by the ticket description.

### Trusting Local QA Pass as Evidence CI Will Pass
**Problem:** Local QA showed 58.6M rows = 58.6M distinct posted_txn_uid (PASSED). CI showed 66M unique test failures. Local environment had cleaner data than CI; ODS sources that produce duplicates may only expose them in CI's data snapshot.
**Fix:** Local clean does not guarantee CI clean. When CI fails a unique test that passed locally, investigate the CI data directly. The 2x exact duplicate pattern is a stale build signal, not a join fan-out signal.

### EXISTS-Only GBOS Prefilter Without Date Filter — Redshift Still Full-Scans
**Problem:** V1 of the GBOS fix used EXISTS semi-join only (no date filter). This still caused WLM abort because Redshift had to full-scan GBOS to evaluate the semi-join. EXISTS alone doesn't provide partition pruning in Redshift without a leading sargable predicate.
**Fix:** For Redshift: date filter (sargable, triggers sort key pruning) must come BEFORE EXISTS. Two-phase: date narrows rows, EXISTS selects exact keys.

### Full-Refresh on Massive Transaction Models Without Batch Vars — Guaranteed WLM Abort
**Problem:** `dbt run --full-refresh --select int_transactions__posted_all` (no vars) scans 5+ years of data and hits WLM limits in both dev and prod. This wastes 15-30 minutes before aborting.
**Fix:** NEVER run full-refresh on canonical transaction models without batch_start_date/batch_end_date vars. Always constrain: `--vars '{"batch_start_date": "...", "batch_end_date": "..."}'`.

### Comparing New Model to Stale Legacy Logic Rather Than Intended Behavior
**Problem:** Merchant Spend QA showed $150M discrepancy for Quickbooks because the QA script was comparing against legacy CASE WHEN hardcoded product logic that was already known to be stale. The investigation traced to a real difference — but the legacy was wrong, not the dbt model.
**Fix:** Before declaring a variance as a bug in the dbt model, verify the legacy logic is the ground truth and not itself stale. Ask: "Should this legacy logic be ported, or is it outdated?"

### Using Compiled SQL to Verify Model State Instead of Querying the Warehouse
**Problem:** Copilot repeatedly checked compiled SQL to determine if a model was built correctly, or checked code definitions instead of running the actual table query. Compiled SQL shows what would run, not what's in the warehouse. Schema drift, stale builds, and missing full-refresh are invisible through compile.
**Fix:** Use `dbt show --inline 'SELECT COUNT(*), MAX(calendar_date) FROM ref("model")'` or `execute_sql` to query actual warehouse state. Compiled SQL confirms logic; warehouse query confirms data.

### Activating Wrong Branch/Context at Session Start Due to Stale EXEC_SUMMARY
**Problem:** Copilot defaulted to stale P1 (Merchant Spend) from EXEC_SUMMARY.md instead of the actual task (Funds Movement), causing branch switch to wrong feature branch and wasted setup time.
**Fix:** Always pass explicit context at session activation: task name + branch name. EXEC_SUMMARY.md P1 may be outdated. Verify current task from the actual handoff document, not from the priority stack.

### MetricFlow Dimension Not Found Due to Missing Entity Qualification
**Problem:** `product_stack` in `--group-by` returns QueryError: Dimension not found. Must be qualified as `gbos_registration_events__product_stack`. Looks like a data problem but is a query syntax error.
**Fix:** Always entity-qualify MetricFlow dimensions: `semantic_model_name__dimension_name`. Error message "Dimension not found" means entity qualification is missing, not that the dimension doesn't exist.

### zsh Glob Interpretation of `{{ }}` in MetricFlow `--where` Clauses
**Problem:** `mf query --where {{ Dimension('product') }} == 'X'` fails with `zsh: no matches found: {{`. Looks like a MetricFlow syntax error or data issue.
**Fix:** Always quote the entire `--where` clause in zsh: `--where "{{ Dimension('product') }} == 'X'"`. This is a shell quoting issue, not a MetricFlow or data issue.

### Pasting "Variance < 0.1%" Into PR Without Running Actual Validation Queries
**Problem:** QA templates are manually run and results pasted into PR — creating opportunity for false sign-off without actual execution. A developer can claim PASS without running the suite.
**Fix:** Require specific evidence in QA reports: link to dbt Cloud run or session log with actual query output. Never accept "looks good" — require variance % with at least 4 decimal places and the query that produced it.
