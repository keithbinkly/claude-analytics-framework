# Context Builder — Decisions

Structured decision records. Each entry captures what was decided, why, and what was rejected.

---

## 2026-02-16: Context Builder absorbs Learner agent role

**Decision:** Context Builder is the domain agent that owns knowledge curation, semantic layer development, and business context integration. The existing learner task agent becomes a mode of Context Builder.

**Rationale:** The learner's core function ("We already have this" + knowledge gap detection) is fundamentally about structured context — organizing knowledge so agents can find and use it. Semantic layer development (MetricFlow YAML) is another form of structured context. Both are about translating business knowledge into machine-readable formats.

**Alternatives rejected:**
- Separate Learner domain agent — too narrow for a domain agent (knowledge curation alone)
- Merge learner into System Architect — System Architect is meta-level (agents about agents), Context Builder is domain-level (business knowledge)

**Confidence:** High

---

## 2026-01-20: MetricFlow dbt 1.11+ syntax standard

**Decision:** All semantic layer definitions follow dbt 1.11+ MetricFlow syntax. No legacy syntax.

**Rationale:** dbt 1.11 introduced breaking changes to MetricFlow syntax. Maintaining backward compatibility creates confusion. Clean cut to new syntax.

**Confidence:** High

---

## 2026-01-05: Semantic model per grain

**Decision:** One semantic model per unique grain (e.g., daily transactions, monthly summaries, account-level attributes).

**Rationale:** Mixing grains in a single semantic model creates ambiguous metric calculations. Each grain gets its own model with clearly defined entities and dimensions.

**Alternatives rejected:**
- One semantic model per source table (too granular, duplicates shared dimensions)
- One semantic model per business domain (too coarse, mixes grains)

**Confidence:** High

---

## 2026-02-17: Two-tier semantic architecture (Gold vs Detail)

**Decision:** Maintain two semantic model tiers — Gold (pre-aggregated, account×date grain, 112 cols) for certified KPIs; Detail (event-level, LONG format) for any query needing extended dimensions like merchant_nm, mcc, bank, business_division, reloader_segment.

**Rationale:** MetricFlow enforces 1:1 relationship between semantic models and source tables with no automatic aggregate awareness or query routing. Two tiers are the minimum to serve both certified executive KPIs and exploratory dimensional breakouts. If Tier 1 ≠ aggregated Tier 2, there is a data quality bug (fanout or suppression).

**Alternatives rejected:**
- Single event-level model — cannot serve certified KPIs without expensive aggregation on every query
- Single pre-aggregated model — cannot serve extended dimension breakouts without unpivoting WIDE to LONG

**Confidence:** High

---

## 2026-02-17: Transaction classification via canonical macros

**Decision:** All transaction classification (flow, category, subcategory) is handled by three canonical macros: `txn_flow()`, `txn_category()`, `txn_subcategory()`. No inline CASE statements in models.

**Rationale:** Four-plus legacy scripts had copy-paste drift — slight variations in CASE logic across pipelines. Single source of truth enables: single audit point, one update location when new txn_type_codes are added, testable in isolation.

**Alternatives rejected:**
- Inline CASE per model — copy-paste drift, impossible to audit
- External lookup table — adds join complexity, harder to version-control logic

**Confidence:** High

---

## 2026-02-17: 14 standard dimensions must be preserved across all Arc Insights reporting models

**Decision:** All Arc Insights mart models must include: product_type, bank, brand, portfolio, product, business_division, business_segment, business_channel, business_sub_channel, product_sub_channel, reloader_segment (from actives join, not account_base), calendar_month, prior_ytd_ind.

**Rationale:** These 14 dimensions are the standard enterprise KPI reporting slice. Any mart model missing them loses dimensional analysis capability for stakeholders. reloader_segment specifically comes from the actives join — sourcing it from account_base produces wrong segment assignments.

**Alternatives rejected:**
- Subset of dimensions per model — creates inconsistent reporting surfaces
- Dynamic dimension loading — adds query complexity without benefit

**Confidence:** High

---

## 2026-02-17: Metric type classification (FLOW/STOCK/RATE) drives tier routing

**Decision:** FLOW metrics (GDV, Purchase, Revenue — sum over time) → either tier. STOCK metrics (Net Ledger Balance, Active Account count at specific date — point-in-time) → Gold tier only. RATE metrics (GDV/Active, Avg Txn Size — derived ratios) → Gold tier for reliable denominator counts.

**Rationale:** Event-level aggregation for STOCK metrics requires complex window logic that doesn't exist in the event stream. Pre-aggregated Gold tier has correct point-in-time snapshots. RATE metrics need reliable denominators — Gold's certified account counts are the source of truth.

**Alternatives rejected:**
- All metrics from Detail tier — STOCK metrics require window functions not available in MetricFlow
- All metrics from Gold tier — cannot serve extended dimension breakouts (high-cardinality dims not in Gold)

**Confidence:** High

---

## 2026-02-17: Reconciliation model with 0.1% variance threshold

**Decision:** Built `kpi_reconciliation` semantic model that alerts when aggregated Detail tier totals differ from Gold tier totals by more than 0.1%. Triggers investigation for fanout (Detail overcounts) or suppression (Detail undercounts). Variance tolerance: <0.1% for monthly aggregates and dimensional slices; <0.5% for rolling/PoP/YoY.

**Rationale:** Two-tier architecture creates a built-in data quality check. If tiers agree, both are correct. If they disagree, there is a structural bug — always fanout or suppression. Higher tolerance for rolling/PoP/YoY due to inherent date boundary handling differences between systems.

**Alternatives rejected:**
- Manual spot-check QA — misses systematic structural issues
- Single-tier with no reconciliation — removes the quality feedback loop

**Confidence:** High

---

## 2026-02-17: 7-level semantic QA validation protocol

**Decision:** Semantic QA follows 7 levels: (1) additive consistency — parts sum to whole, (2) rate/ratio consistency — rate = numerator/denominator, (3) cross-grain — daily sums = monthly = quarterly, (4) cross-dimension — dimensional slices sum to total, (5) cross-model — event model vs cardholder model agree, (6) business reasonableness — ranges and expected relationships, (7) legacy comparison (VPN required). Levels 1-6 run without VPN via dbt MCP API.

**Rationale:** Simple variance comparison against legacy misses structural issues like fan-out, additive failures, and cross-grain inconsistencies. Structured 7-level approach catches all discrepancy categories. Most validation work (levels 1-6) can be done without VPN access.

**Alternatives rejected:**
- Legacy comparison only — misses structural bugs; VPN dependency blocks iteration
- Single-pass QA — insufficient for enterprise data quality bar

**Confidence:** High

---

## 2026-02-17: Primary transaction source is int_transactions__posted_all

**Decision:** The canonical event-level transaction model is `int_transactions__posted_all` (event-first, LONG format, all enrichment flags pre-attached). Related canonical models: `int_transactions__auth_all` (auth attempts/declines), `int_transaction_pairs__purchase` (auth+posted paired), `int_transaction_pairs__purchase_detail` (cardholder grain).

**Rationale:** Event-first sourcing eliminates the WIDE→LONG transformation required when sourcing from `fct_dly_acct_txn_summary`. Single aggregation step (events→target grain) vs triple step (events→daily summary→unpivot→target grain). All enrichment flags already attached.

**Alternatives rejected:**
- fct_dly_acct_txn_summary as event source — requires unpivot macro, triple aggregation, more compute per query

**Confidence:** High
