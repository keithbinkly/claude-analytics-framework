# QA — Decisions

Structured decision records. Each entry captures what was decided, why, and what was rejected.

---

## 2026-02-16: QA as separate domain agent from Builder

**Decision:** QA gets its own domain agent rather than being a phase of Builder. Accumulates separate memory (investigation patterns, gotchas, qa-playbook).

**Rationale:** QA sessions produce fundamentally different learnings than build sessions. A builder learns "how to construct models." A QA agent learns "what goes wrong and how to find it." Mixing these memories dilutes both.

**Alternatives rejected:**
- QA as Builder phase — loses QA-specific pattern accumulation
- QA merged with Analytics Manager — different skills (validation vs analysis)

**Confidence:** High

---

## 2026-02-05: 0.1% variance threshold

**Decision:** Hard threshold at 0.1% variance. No rounding, no "close enough."

**Rationale:** Small variances compound across dimensions and time periods. A 0.2% variance at the total level can mask a 15% variance at the partner level. The threshold prevents cascading errors.

**Confidence:** High (empirically validated across multiple QA cycles)

---

## 2026-01-26: Template execution order (1→2→3→4)

**Decision:** Always execute QA templates in order: granular variance → aggregated totals → dimension drill-down → trend analysis.

**Rationale:** Granular first catches issues that totals-only would miss. Drill-down only needed when variance found. Trend analysis is the final confidence check.

**Alternatives rejected:**
- Start with totals (faster but misses offsetting errors)
- Random template selection based on "intuition" (inconsistent, misses patterns)

**Confidence:** High

---

## 2026-01-08: Decision trace as mandatory artifact

**Decision:** Every resolved QA issue produces a decision trace in `shared/decision-traces/traces.json`.

**Rationale:** 76% reduction in QA resolution time when traces exist for similar issues. The traces are the highest-ROI artifact in the entire system.

**Confidence:** High (measured)

---

## 2026-02-17: Two-phase GBOS filtering (date + EXISTS belt-and-suspenders)

**Decision:** Use two-phase GBOS filtering: date filter first (`processorbusinessdate IN dim_date`, sargable), then EXISTS semi-join to exact batch keys. Pre-compute any non-sargable expressions (CASE/split_part) in upstream CTE so the join predicate is sargable.

**Rationale:** EXISTS-only failed because Redshift full-scans GBOS to evaluate the semi-join without a leading sargable predicate. Date-only failed because Redshift couldn't optimize subquery bounds into partition predicates for full-refresh. Two-phase: date provides partition pruning (~3 days vs 5+ years), EXISTS provides exact key restriction.

**Alternatives rejected:** EXISTS-only (v1): failed with WLM abort. Date-only with subquery bounds: failed for full-refresh. Pure date filter without EXISTS: works for incremental but not full-refresh.

**Confidence:** High

---

## 2026-02-17: eWallet extracted from canonical transaction models into standalone models

**Decision:** `int_transactions__posted_ewallet` and `int_transactions__auth_ewallet` are separate models that canonical models LEFT JOIN via posted_txn_uid/auth_uid. Canonical models (posted_all, auth_all) have zero GBOS dependencies.

**Rationale:** GBOS join chain caused WLM aborts even with date+EXISTS two-phase filter in some execution contexts. Extracting eWallet means: canonical models are reliable regardless of GBOS issues, eWallet models can fail without breaking downstream pipeline, consumers only join eWallet when needed.

**Alternatives rejected:** Keeping GBOS joins inline in canonical models: reliable for incremental but unreliable for full-refresh in dev.

**Confidence:** High

---

## 2026-02-17: delete+insert over merge for incremental models with join-derived duplicates

**Decision:** When `incremental_strategy='merge'` fails with "Found multiple matches to update the same tuple", switch to `incremental_strategy='delete+insert'`.

**Rationale:** The source query produces duplicate unique_key values due to joins (txn_type_hierarchy producing 1:N). Merge cannot resolve which row wins when multiple source rows match one target row. delete+insert handles this by deleting all rows for the unique_key range then re-inserting.

**Alternatives rejected:** Fixing the join upstream: correct long-term but slower to deploy. Merge with source dedup: adds complexity and is brittle when upstream changes.

**Confidence:** High

---

## 2026-02-17: Event-grain incremental layer + full-refresh cumulative mart for cohort metrics

**Decision:** Layer 1: `int_gbos_registration_metrics_daily` — incremental, event-grain daily counts only (no cumulative). Layer 2: `mrt_gbos_registration_cohort_metrics` — full-refresh table, adds cumulative via `SUM() OVER (... ROWS UNBOUNDED PRECEDING)` window function.

**Rationale:** Cross-join (product_stack × cohort_date × snapshot_date) produced ~66 billion intermediate rows → WLM timeout. Separating incremental (daily events) from cumulative (window function on event grain) reduces daily incremental to ~50K rows and full-refresh to ~270M rows with simple window computation.

**Alternatives rejected:** Fill-forward all time: 330B rows, impossible. Keeping cross-join: WLM timeout always.

**Confidence:** High

---

## 2026-02-17: DuckDB unit tests for logic validation before VPN-required warehouse QA

**Decision:** Use dbt SQL unit testing (dbt-sql-unit-testing skill with DuckDB) to validate business logic locally without VPN. Run unit tests first; only proceed to warehouse QA after unit tests pass.

**Rationale:** VPN dependency creates scheduling friction. Logic errors that unit tests can catch (NULL handling, UNION ALL column alignment, grouping sets, retention policy logic) don't need warehouse access. Separates logic validation (VPN-free) from data validation (VPN-required). mcc_desc passthrough had 10/10 unit tests passing before any warehouse access needed.

**Alternatives rejected:** Skip directly to warehouse QA: creates bottleneck on VPN availability, wastes warehouse time on logic errors.

**Confidence:** High

---

## 2026-02-17: Rate reasonableness checks for new filtered metrics without legacy comparison

**Decision:** When QA-ing new metrics with no legacy equivalent (e.g., CP/CNP, POS entry mode), use industry benchmark range checks instead of legacy comparison. CP approval 80-99% normal, CNP 60-95% normal, contactless >= chip approval rate expected. Dimensional integrity + additive validation + rate reasonableness replaces Template 1-4 variance analysis.

**Rationale:** New filtered metrics have no legacy comparison. Dimensional integrity (dimension values exist and are clean) + additive validation (filtered totals sum to portfolio total) + rate reasonableness covers the same ground without requiring a legacy baseline.

**Alternatives rejected:** Legacy comparison: impossible for new metrics. Row count comparison: doesn't catch rate calculation errors.

**Confidence:** High

---

## 2026-02-17: Unique test required on enrichment models that document 1:1 grain

**Decision:** After discovering fpa_group_enrichment produced 2x duplicates due to claimed-but-unenforced 1:1 grain, add unique test to all enrichment intermediate models that document "1 row per account" in their grain definition.

**Rationale:** Models that claim 1:1 grain in documentation but lack a unique test will silently fan-out when upstream ODS sources produce duplicates. The test documents and enforces the contract. The missing test allowed 66M CI failures to be introduced undetected.

**Alternatives rejected:** Trust documentation: insufficient — upstream changes can violate documented grain without warning.

**Confidence:** High

---

## 2026-02-17: Legacy comparison uses same-grain only — new grains not compared to legacy

**Decision:** When a legacy model has only Weekly grain and the new model adds Daily and Monthly, compare ONLY Weekly grain for variance validation. Daily/Monthly are acknowledged as new features with no comparison baseline.

**Rationale:** Apples-to-apples comparison requires identical grain. Different time aggregation methods produce legitimately different numbers. Comparing Weekly legacy to all-grain totals inflates apparent variance and creates false FAIL signals.

**Alternatives rejected:** Compare all rows total: inflates variance due to grain differences. Skip legacy comparison entirely: misses real regressions in the existing grain.

**Confidence:** High

---

## 2026-03-13: Semantic API parser must support base64 jsonResult fallback

**Decision:** For Semantic Layer GraphQL polling workflows, parser must attempt `json.loads(jsonResult)` first, then fallback to `json.loads(base64.b64decode(jsonResult).decode("utf-8"))`. This logic should live in a shared helper imported by all Semantic API scripts.

**Rationale:** Query execution can succeed (`status=SUCCESSFUL`, `totalRows>0`) while parse step fails if code assumes plain JSON only. This caused repeated false debugging loops and incomplete QA runs.

**Alternatives rejected:**
- Keep parser logic duplicated per script: drift risk and repeated breakage.
- Assume synchronous query output shape only: brittle across endpoints/versions.

**Confidence:** High
