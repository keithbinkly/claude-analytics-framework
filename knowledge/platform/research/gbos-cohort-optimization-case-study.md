# Project Update: GBOS Cohort Optimization Complete

**Date:** 2026-01-16
**Session Type:** Pipeline Optimization + Learning Cycle
**Duration:** Multi-session (2026-01-14 to 2026-01-16)

---

## Executive Summary

Successfully deployed a two-layer architecture that fixed a WLM timeout issue in `mrt_gbos_registration_cohort_progress`. The pipeline went from **infinite (timeout)** to **15 min full refresh / 5 min incremental**. More importantly, this session revealed a **process gap in lineage verification** that caused extra debugging—now fixed with two new mandatory checkpoints in our QA process.

**Key Wins:**
- Pipeline deployed and running in production
- Semantic layer metrics now accessible via API
- Two new QA checkpoints prevent future "orphaned lineage" bugs
- Knowledge base updated with patterns for O(n²) → O(n) transformations

---

## What We Did

### 1. Fixed the WLM Timeout (Technical)

**Problem:** `mrt_gbos_registration_cohort_progress` used a cross-join pattern:
- 36M cohorts × 1,840 days = 66B+ intermediate rows
- Result: WLM timeout on every full refresh

**Solution:** Two-layer window function architecture:
```
Layer 1: int_gbos_registration_metrics_daily (incremental)
         └── UNION ALL unpivoting, daily counts only

Layer 2: mrt_gbos_registration_cohort_metrics (table)
         └── Window function: SUM() OVER (ORDER BY date ROWS UNBOUNDED PRECEDING)
```

**Performance:**
| Metric | Before | After |
|--------|--------|-------|
| Full refresh | WLM timeout (∞) | 15 min |
| Incremental | N/A | 5 min |
| Complexity | O(n²) | O(n) |

### 2. Discovered and Fixed Orphaned Lineage Bug

**What happened:** Created new optimized models, marked old model "deprecated," but production merge job kept failing.

**Root cause:** Semantic model + 3 views still referenced the old (broken) model. New models weren't wired up.

**Fix:** Converted old model to a VIEW that reads from new model (backward compatibility layer). No ref changes needed downstream.

### 3. Added Two-Gate Lineage Protection to QA Process

**Gap identified:** Neither the adversarial reviews (GPT 5.2, Gemini 3 Pro) nor our implementation process checked downstream consumers before/after model replacement.

**Fix applied:**
- **Phase 2.0.1** (Pre-implementation): Inventory downstream consumers before coding
- **Phase 5.3** (Post-implementation): Verify lineage is wired correctly before PR

---

## Why This Matters

### For the GBOS Pipeline
- Stakeholders can now see cohort progression metrics in Tableau
- Failure reason tracking is now available (was blocked by timeout)
- Future metric additions won't require schema changes (EAV format)

### For Our Process
This was a **near-miss**. We almost shipped a "fix" that didn't fix the production issue because:
1. Adversarial reviews focused on SQL correctness, not deployment integration
2. Dev builds succeeded (38s) giving false confidence
3. No lineage verification before closing the ticket

The two new QA checkpoints ensure this pattern won't repeat.

### For Future Pipelines
The troubleshooting guide now documents:
- **N×M cross-join fanout** pattern and solution (two-layer window function)
- **Orphaned lineage** pattern and solution (pre/post lineage verification)

---

## Performance Predictions vs Actuals

| Metric | Prediction | Actual | Analysis |
|--------|------------|--------|----------|
| Full refresh | 2-5 min (Gemini) | **15 min** | 3-7x slower than predicted |
| Incremental | ~1 min | **5 min** | 5x slower than predicted |

**Lesson:** Predictions were directionally correct (∞ → finite) but underestimated production conditions. Future estimates should include confidence intervals: "5-10 min (±3x under load)."

---

## What's Next

| Task | Priority | Status |
|------|----------|--------|
| Semantic layer metrics testing | Active | Copilot pulling metrics via API |
| Tableau visualization updates | Active | Team working on views |
| Failure reason dashboard | Next | Waiting for stakeholder feedback |
| Documentation + business context | Next | For AI analyst capabilities |

---

## How to Use This

### For Pipeline Developers
When you see a model with WLM timeout and "as of date" cumulative logic:
1. Check `shared/knowledge-base/troubleshooting.md` → "WLM Timeout from N×M Cross-Join Fanout"
2. Apply two-layer architecture pattern
3. Use Phase 2.0.1 + Phase 5.3 lineage checks for replacements

### For QA
New mandatory checkpoints in `shared/reference/qa-validation-checklist.md`:
- **Phase 2.0.1**: Downstream Impact Analysis (before coding)
- **Phase 5.3**: Lineage Verification (before PR)

---

## Files Changed

```
Modified (dbt-enterprise):
  mrt_gbos_registration_cohort_progress.sql  # TABLE → VIEW (backward-compat)
  _mrt_gbos_registration__schema.yml         # Updated description

Created (dbt-enterprise):
  int_gbos_registration_metrics_daily.sql    # Layer 1 incremental
  mrt_gbos_registration_cohort_metrics.sql   # Layer 2 window function

Modified (dbt-agent):
  shared/reference/qa-validation-checklist.md   # +Phase 2.0.1, +Phase 5.3
  shared/knowledge-base/troubleshooting.md      # +2 new patterns
  .dots/dbt-agent-gbos-cohort-optimization.md   # Closed with resolution
```

---

## Metrics

| Metric | Value |
|--------|-------|
| QA variance | 0.00% |
| Canonical model reuse | N/A (new architecture) |
| Production full refresh | 15 min |
| Production incremental | 5 min |
| Process improvements added | 2 (Phase 2.0.1, Phase 5.3) |
| Troubleshooting patterns added | 2 |

---

## Retrospective Insights

### What Worked Well
1. **Adversarial reviews** caught real issues (incremental logic, DIST/SORTKEY)
2. **Preflight analysis** confirmed old model was actually broken
3. **0.00% QA variance** using structured templates
4. **Quick resolution** once lineage issue identified

### What Could Improve
1. **Lineage not in review scope** — now fixed with Phase 2.0.1/5.3
2. **Runtime predictions overconfident** — add confidence intervals
3. **Dev ≠ Prod awareness** — dev was 38s, prod was 15 min
4. **Should have kicked off Learner cycle automatically** at milestone

---

## Process Note

This learning cycle was initiated manually when Keith asked for retrospective. The Learner Agent protocol (`.claude/commands/learner.md`) defines triggers for automatic learning cycles:
- Completed handoffs
- Closed dots
- Repeated patterns in session logs

**Improvement:** Future milestone completions should automatically trigger learning extraction + Project Update generation without requiring user prompt.

---

*Generated by Learner Agent learning cycle on 2026-01-16*
