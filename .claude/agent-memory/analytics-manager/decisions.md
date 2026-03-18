# Analytics Manager — Decisions

Structured decision records. Each entry captures what was decided, why, and what was rejected.

---

## 2026-02-16: Analytics Manager as domain agent for BI

**Decision:** Analytics Manager is the domain agent for all business intelligence and analysis work. Absorbs the analyst task agent and the multi-analyst ensemble.

**Rationale:** Analysis work produces its own distinct learnings — which questions produce actionable insights, which metrics stakeholders actually care about, how to present findings for different audiences. These patterns don't belong in Builder (infrastructure) or Context Builder (definitions).

**Alternatives rejected:**
- Analyst as sub-agent only (no persistent memory for analysis patterns)
- Merge with Context Builder (analysis patterns ≠ definition patterns)

**Confidence:** High

---

## 2026-02-12: Multi-analyst ensemble architecture

**Decision:** Fan out complex questions to 4 parallel analyst personas, then synthesize. Validation score: 4.28/5.0.

**Rationale:** Single-perspective analysis misses blind spots. Multiple analytical lenses (trends, anomalies, benchmarks, root causes) catch issues that any single analyst would miss.

**Alternatives rejected:**
- Single analyst with prompts to consider multiple angles (doesn't truly parallelize thinking)
- 2 analysts (not enough perspective diversity)
- 6+ analysts (diminishing returns, synthesis becomes harder)

**Confidence:** High (validated at 4.28/5.0)

---

## 2026-02-09: Certified metrics only — no raw SQL for analysis

**Decision:** Analytics Manager NEVER writes raw SQL against base tables. All analysis goes through the semantic layer.

**Rationale:** Raw SQL bypasses certified metric definitions, creating "two truths" — one from the semantic layer and one from ad-hoc queries. This erodes trust in the certified metrics.

**Alternatives rejected:**
- Allow raw SQL as fallback (creates the two-truths problem)
- Allow raw SQL for "exploration" (slippery slope — exploration becomes production)

**Confidence:** High (Keith directive: "If it's not in the semantic layer, it doesn't exist for analysis")
