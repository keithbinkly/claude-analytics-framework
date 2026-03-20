---
contributed: 2026-03-19
source: samsung-decline-deep-dive / disbursements pipeline
partner: Samsung (applicable to all partners)
benefits: everyone
related:
  - analysis_2026-03-14_001
  - ent-doc-SAMSUNG_QA_VALIDATION_REPORT
  - ent-doc-SAMSUNG_ROVO_RESEARCH_2026_03_10
tags: [upstream-drill-down, semantic-layer, ISO-8583, decline-analysis]
---

# Upstream Drill-Down Pattern

## What We Found

When the semantic layer returns an unhelpfully generic bucket (e.g., "Declined (generic)" at 44.7% of all declines), the actionable root causes live in **upstream intermediate models** that carry raw codes the semantic layer aggregates away.

The Samsung decline investigation proved this pattern: the semantic layer correctly reported that 44.7% of declines were "Declined" — but that category was a black box containing 69,793 transactions with no actionable reason. By drilling into `int_samsung__external_details` (which carries raw ISO 8583 `network_association_response_code`), we decomposed the bucket into 3 structural problems:

- **Code 59 (suspected fraud):** 61.4% of generic declines, $5.35M — plateaued at 700-1,000/month across 50+ banks
- **Code 51 (NSF):** 27% — 5x spike on 1st/2nd of month, 96% under $100
- **Code 63 (service not allowed):** 26% — BIN config gap at 35+ issuers

Each requires a different fix type (network registration, engineering, partnerships). The semantic layer answer was correct but not actionable. The upstream answer was both.

## When This Applies

- Semantic layer returns a high-volume bucket with a generic label ("Declined", "Other", "Unknown")
- You need to decompose an aggregate category into root causes
- The upstream intermediate models carry raw codes, flags, or statuses that the mart aggregates into categories
- Business stakeholders need actionable root causes, not category percentages

## The Pattern (4 steps)

1. **Identify the generic bucket** via semantic layer (MCP `execute_sql` or ensemble query)
2. **Find the upstream model** that carries raw codes — search with `get_related_models()` or `tldr search` for the dimension name
3. **Cross-reference** raw codes with a second dimension (issuing bank, time, amount) to find concentration and trends
4. **Present both layers**: the semantic layer answer (what % is declining) AND the upstream answer (why, and what to do about it)

## Evidence

- Samsung "Declined (generic)": 69,793 txns → decomposed into 8 ISO 8583 codes, top 3 accounting for 82%
- Bank concentration analysis: all-time vs current-quarter showed Bancorp/Stride spike resolved but long tail plateaued
- Weekly trend: "Big 3" codes converged at ~100-250/week each — no single fix solves it
- Full write-up: `dbt-agent/docs/visualizations/data-stories/disbursements/samsung-decline-deep-dive.html`

## Key Insight

The semantic layer enriches raw data into business-friendly categories. That enrichment is lossy by design — it trades detail for clarity. When the business question requires the detail back, go upstream, don't fight the semantic layer. This **complements** the semantic layer rather than replacing it.
