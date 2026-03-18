# Builder — Decisions

Structured decision records. Each entry captures what was decided, why, and what was rejected.

---

## 2026-02-16: Builder absorbs orchestrator + architect + migration + discovery

**Decision:** Builder is the domain agent that coordinates all pipeline phases. The existing task agents (orchestrator, architect, sql-builder-agent, discovery-agent) become specialist modes deployed by Builder.

**Rationale:** A single pipeline owner prevents context fragmentation. The orchestrator's coordination role, architect's design role, migration's implementation role, and discovery's profiling role are all phases of the same workflow. One domain agent with accumulated memory across all phases learns more than 4 separate agents.

**Alternatives rejected:**
- Separate domain agents per phase — loses cross-phase learning (e.g., discovery findings inform implementation patterns)
- Single mega-agent with no specialist modes — too much context in one prompt

**Confidence:** High (explicit architectural decision from agent-map.yaml)

---

## 2026-01-20: Canonical model reuse as hard requirement

**Decision:** Every new model must check the canonical models registry before writing custom logic. Target: 75-90% reuse.

**Rationale:** 87% canonical reuse achieved across 40+ pipelines. Custom logic that duplicates canonical models is wasted effort and creates maintenance burden.

**Confidence:** High (empirically validated)

---

## 2025-12-22: DuckDB CTE injection for SQL unit testing

**Decision:** Use DuckDB CTE injection pattern for unit testing SQL logic without VPN/warehouse access.

**Rationale:** Enables testing during VPN-off sessions. Catches logic errors before expensive warehouse runs. The dbt-sql-unit-testing skill provides the pattern.

**Alternatives rejected:**
- Only test on warehouse (requires VPN, slow feedback loop)
- Mock frameworks (too much setup overhead for SQL testing)

**Confidence:** High (proven in merchant-spend and funds-movement pipelines)

---

## 2026-02-17: WIDE format for cohort/time-series marts, not LONG

**Decision:** Cohort and time-series mart models use WIDE format (metrics as columns, dates as rows). Intermediate LONG models that exist purely to be pivoted back to WIDE are eliminated.

**Rationale:** `mrt_cohort__analysis` originally used a 23-UNION intermediate model to convert WIDE→LONG, then pivoted back to WIDE at the mart. Deleting the LONG intermediate and rewriting WIDE directly eliminated 23x row multiplication. QA confirmed 0.098% variance (within 0.1% threshold). Format should match what the consumer needs — not a theoretical preference for "LONG is better."

**Alternatives rejected:**
- LONG format throughout: Consumer (Tableau/Cohort dashboards) needs WIDE; forcing LONG adds 23x rows and a mandatory final pivot with no benefit
- Hybrid (LONG intermediate, WIDE mart): Tested — eliminated because intermediate model had no other consumers

**Confidence:** High (validated in production, QA passed)

---

## 2026-02-17: Batch loading via dbt vars for historical backfills under WLM constraints

**Decision:** Historical backfills use a `batch_full_refresh_filter` macro parameterized by `--vars '{"batch_start": "...", "batch_end": "..."}'`. Monthly batch granularity is the standard unit.

**Rationale:** Running `--full-refresh` on 4+ years of transaction data hits WLM memory limits. Monthly batches keep query size within WLM allocation. Idempotent by design — any failed batch can be re-run with the same vars. Alternative orchestrator scripts are acceptable but require external execution and are harder to debug mid-backfill.

**Alternatives rejected:**
- Single full-refresh run: Fails at WLM timeout, leaves partial state
- WLM queue reconfiguration: Requires platform team involvement, not under our control
- Python/bash orchestration script: Valid fallback but adds operational complexity vs. native dbt vars

**Confidence:** High (Option A selected in batch-loading-strategy handoff, macro implemented)

---

## 2026-02-17: dist='acct_uid' as default for account-grain models

**Decision:** Account-grain models use `dist='acct_uid'` as the distribution key. Small dimension tables used widely in joins use `dist='all'`.

**Rationale:** Redshift redistributes data at join time when distribution keys don't match. Setting `dist='acct_uid'` on fact and account models co-locates them with the most common join pattern. `int_baas_account_details_core` was previously `dist='bps_lob'` (a low-cardinality text field), causing full redistributions on every join. Verified via `svv_table_info` after `--full-refresh`.

**Alternatives rejected:**
- Default `dist='even'`: Causes redistribution on every join against account-keyed facts
- `dist='bps_lob'`: Low cardinality, caused redistribution in production (was the production state pre-fix)
- `dist='all'` for fact tables: Only valid for small dimensions; fact tables are too large

**Confidence:** High (verified in Arc Insights foundation optimization pass, 2026-01-28)

---

## 2026-02-17: NOT EXISTS over NOT IN for defunct record exclusion

**Decision:** All defunct/inactive record exclusion filters use `NOT EXISTS` with a correlated subquery. `NOT IN` is banned for this pattern.

**Rationale:** `NOT EXISTS` is 4.18x faster than `NOT IN` on Redshift for this use case. Additionally, `NOT IN` produces incorrect results when the subquery contains NULL values — the entire filter evaluates to false (no rows excluded), which is a silent data quality failure. Applied in `int_edw_kpi__account_base` to filter ~150M rows before 8 downstream joins.

**Alternatives rejected:**
- `NOT IN (subquery)`: 4.18x slower and silently broken on NULLs
- `LEFT JOIN ... WHERE key IS NULL`: Valid alternative with equivalent performance, but more verbose and harder to read as "exclusion" intent

**Confidence:** High (documented in anti-pattern-impact.yml, validated in production)

---

## 2026-02-27: DOB decrypt via DSFS pattern with batch vars

**Decision:** Use `pdr_stg.decryptaes()` scoped to account_base (INNER JOIN) as primary DOB source, with pre-computed `dob_year` as fallback. Batch vars (`dob_batch_start`/`dob_batch_end`) for controlled prod backfill; default 1-year rolling window for dev.

**Rationale:** Previous approach used a 3-year unscoped decrypt window — only 54.45% DOB quality (below 80% gate). The DSFS model (`dsfs_a_age_bin`) proved the decrypt pattern works at production scale. INNER JOIN to account_base bounds decrypt to ~9M relevant profiles instead of scanning full `dim_consumer_profile` (~50M+). Batch vars follow the same pattern as `batch_full_refresh_filter` in transaction models.

**Alternatives rejected:**
- Remove date window entirely: Too expensive for dev iteration (~50M decrypts per run)
- Make model incremental: Adds complexity for a ~9M row model; table + batch vars is simpler
- Use only pre-computed `dob_year`: Coverage too low (54%) — many BaaS partners never populate it

**Confidence:** High (DSFS pattern proven, batch var pattern proven in transaction models)

---

## 2026-02-17: Absolute paths for DBT_PROFILES_DIR — never tilde expansion

**Decision:** `DBT_PROFILES_DIR` must always be set to an absolute path using `$HOME` or `${env:HOME}` in VS Code settings. The `~` shorthand is explicitly prohibited.

**Rationale:** dbt-fusion does not reliably expand `~` in `DBT_PROFILES_DIR`, causing `dbt1005: No profiles.yml found` errors that are confusing to diagnose because the path looks correct. Applied fix in `dbt-apple/.vscode/settings.json`. The profiles.yml symlink at `~/.dbt/profiles.yml → dbt-enterprise/profiles.yml` remains valid — only the env var setting is the issue.

**Alternatives rejected:**
- Unset `DBT_PROFILES_DIR` entirely: Works if the default lookup path is correct, but fragile across machines
- Fix dbt-fusion to expand `~`: Not under our control

**Confidence:** High (root cause confirmed and fixed in 2026-01-20 handoff)

---

## 2026-02-17: ANALYZE post-hook on all table-materialized models

**Decision:** Every model with `materialized='table'` that feeds downstream joins must include `post_hook: "ANALYZE {{ this }}"`.

**Rationale:** Redshift's query planner uses table statistics to choose join strategies and sort elimination. Tables materialized without ANALYZE have stale or missing statistics, causing the planner to choose nested loop joins instead of hash joins. The ANALYZE post-hook ensures statistics are refreshed on every run at negligible cost (a few seconds on typical model sizes).

**Alternatives rejected:**
- Manual ANALYZE: Requires remembering to run separately; breaks in CI/automated runs
- Rely on Redshift auto-ANALYZE: Auto-ANALYZE runs on a schedule that may lag behind data changes; post-hook guarantees freshness for the current run

**Confidence:** High (applied across all Arc Insights foundation models, 2026-01-28)
