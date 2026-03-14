---
name: dbt-decision-trace
description: |
  Case-based reasoning from past QA resolutions. Logs decision traces during QA triage,
  synthesizes generalized rules from patterns, and searches for similar past cases to
  accelerate problem-solving. Use when asked to "search past QA resolutions", "log this
  fix", "have we seen this before", "similar issue", "synthesize rules", or "what was the
  root cause last time". Implements experience replay and knowledge codification.
---

# dbt-decision-trace: Case-Based Reasoning + Rule Synthesis

Log QA resolution patterns, synthesize generalized rules, and accelerate problem-solving.

---

## Purpose

Agents repeatedly solve similar issues from scratch. This skill provides institutional
memory by:

1. **Logging traces** during QA resolution
2. **Synthesizing rules** from patterns across traces
3. **Matching rules** at QA start for instant recommendations
4. **Promoting rules** to skill resources when mature

### Learning Loop

```
QA Issue → Triage → Resolution → Log Trace
    ↑                              │
    │                              ↓
Match Rules ← Synthesize ← Multiple Similar Traces
    │              │
    │              ↓
    │         rules.json
    │              │
    │              ↓ (when mature)
    └──── Skill Resources ← Promote Rule
```

### Target Metrics

| Metric | Target |
|--------|--------|
| Traces logged | 50+ within 3 months |
| Rules synthesized | 10+ mature rules |
| Rule match rate | >60% of issues match a rule |
| Resolution time reduction | 30% when rule matches |
| Repeated mistakes | <10% are duplicates of prior |

---

## Core Operations

**Full schemas and code:** `resources/schemas-and-code.md`

| Operation | Purpose |
|-----------|---------|
| `log_trace(trace)` | Append a completed QA trace to traces.json |
| `search_traces(symptom, error_type)` | Find top 3 similar past cases by similarity score |
| `match_rules(symptom, error_type)` | Match against synthesized rules (faster, higher confidence) |
| `synthesize_rules()` | Cluster traces and generate generalized rules |
| `get_rules(confidence)` | Retrieve all rules, optionally filtered by confidence |
| `get_stats()` | Aggregate counts, avg resolution time, error type breakdown |

---

## Integration Points

### At QA Start (dbt-qa Phase 0)

**Check rules FIRST** (faster, higher confidence), then fall back to traces:

```python
# Step 1: Check rules first
matching_rules = match_rules(symptom, error_type)

if matching_rules and matching_rules[0]['score'] > 0.5:
    rule = matching_rules[0]['rule']
    print(f"Pattern matched: {rule['pattern_id']}")
    print(f"Recommended: {rule['recommended_action']['first_try']}")
    print(f"Success rate: {rule['metrics']['success_rate']:.0%}")
    # Try this first before standard triage

# Step 2: Fall back to trace search if no rules match
else:
    traces = search_traces(symptom, error_type)
    if traces and traces[0]['score'] > 0.8:
        print(f"Found similar case: {traces[0]['trace']['id']}")
        print(f"Resolution: {traces[0]['trace']['resolution']['fix']}")
```

### At QA Resolution (dbt-qa Phase 5)

Log trace before marking QA complete. Full template: `resources/schemas-and-code.md`.

### After QA Session (Synthesis Trigger)

```python
stats = get_stats()
if stats['total_traces'] >= 5 and stats['total_traces'] % 5 == 0:
    # /synthesize-traces
```

---

## Confidence Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **low** | 1 trace, unverified | Monitor only, show in emerging patterns |
| **medium** | 2+ traces OR 1 verified with high reuse potential | Suggest to user with rationale |
| **high** | 3+ traces, >90% success rate | Auto-suggest, consider promotion to skill resources |

---

## Error Types

| Error Type | Description | Common Fixes |
|------------|-------------|--------------|
| `fan_out` | Row multiplication from joins | Add DISTINCT, change join type |
| `grain_violation` | Wrong aggregation level | Add GROUP BY, fix grain |
| `missing_rows` | Fewer rows than expected | Check WHERE filters, INNER vs LEFT join |
| `duplicate_rows` | More rows than expected | Add DISTINCT, fix join keys |
| `type_mismatch` | Data type conversion issues | Explicit CAST, handle NULLs |
| `null_values` | Unexpected NULLs | COALESCE, NULLIF, fix source |
| `performance` | Query too slow | Optimize joins, add filters |
| `other` | Doesn't fit categories | Document for future |

## Fix Categories

| Category | Description | Example |
|----------|-------------|---------|
| `filter_missing` | Missing WHERE clause | Added `WHERE status = 'active'` |
| `join_cardinality` | Wrong join producing fan-out | Changed to LEFT JOIN with DISTINCT |
| `date_boundary` | Date filter edge case | Fixed `>=` vs `>` for date range |
| `logic_error` | Business logic mistake | Corrected calculation formula |
| `data_quality` | Source data issue | Added COALESCE for NULLs |
| `performance` | Optimization needed | Added temp date filter |

---

## Troubleshooting Rationalizations (Red Flags)

| You're Thinking... | Reality |
|---|---|
| "Just make the test pass" | The test is telling you something is wrong. Investigate first. |
| "There's a board meeting in 2 hours" | Rushing to a fix without diagnosis creates bigger problems. |
| "We've already spent 2 days on this" | Sunk cost doesn't justify skipping proper diagnosis. |
| "I'll just update the accepted values" | Are the new values valid business data or bugs? Verify first. |
| "It's probably just a flaky test" | "Flaky" means there's an underlying issue. Find it. |

---

## Storage Structure

```
shared/decision-traces/
├── traces.json         # Raw traces (append-only)
├── index.json          # Quick lookup indexes
├── rules.json          # Synthesized rules (v2.0)
├── rules-schema.json   # Validation schema (v2.0)
├── viewer.html         # Visual trace browser
└── README.md           # Documentation
```

Current state: 6 traces, 3 rules + 3 emerging (last updated 2025-12-31)

---

## Commands

| Command | Purpose |
|---------|---------|
| `/synthesize-traces` | Run synthesis, generate/update rules |
| `/synthesize-traces --dry-run` | Preview changes without writing |
| `/synthesize-traces --promote` | Auto-promote high-confidence rules |

---

## Related Skills

- **dbt-qa** - Primary consumer of traces and rules
- **dbt-migration** - Queries traces for known issues
- **dbt-preflight** - Informs cost estimation with past experiences
