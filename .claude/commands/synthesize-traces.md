# Synthesize Decision Traces

Analyze decision traces and synthesize generalized rules for accelerated problem-solving.

---

## Trigger

Run this command when:
- New traces have been logged (5+ since last synthesis)
- Weekly maintenance cycle
- User requests `/synthesize-traces`

---

## Workflow

### Step 1: Load Current State

Read the trace and rule files:

```
knowledge/domains/dbt-pipelines/decision-traces/traces.json   # Raw traces
knowledge/domains/dbt-pipelines/decision-traces/rules.json    # Existing rules
knowledge/domains/dbt-pipelines/decision-traces/index.json    # Lookup indexes
```

Report current state:
- Total traces: X
- Existing rules: Y
- Emerging patterns: Z

### Step 2: Cluster Similar Traces

Group traces by similarity:

1. **Exact match clusters**: Same `error_type` + `fix_category`
2. **Symptom similarity**: Jaccard similarity on symptom keywords > 0.7
3. **Root cause clusters**: Same underlying issue, different symptoms

For each cluster with 2+ traces:
- Extract common detection signals
- Generalize symptom description
- Compute success rate from verified resolutions

### Step 3: Generate/Update Rules

For each cluster meeting threshold (min_traces >= 2):

**If new pattern:**
```json
{
  "pattern_id": "rule_{fix_category}_{hash}",
  "version": 1,
  "source_traces": ["trace_1", "trace_2"],
  "confidence": "medium",
  ...
}
```

**If existing rule matches:**
- Add new trace to `source_traces`
- Update `metrics.times_applied`
- Recalculate `metrics.success_rate`
- Bump `version` if pattern changes

### Step 4: Promote Emerging Patterns

Check `emerging_patterns` for any that now have 2+ similar traces:
- Move to `rules` array
- Remove from `emerging_patterns`
- Set `confidence: "medium"`

### Step 5: Flag New Emerging Patterns

For singleton traces not matching any rule:
- Add to `emerging_patterns`
- Set `awaiting_confirmation: 1`
- Suggest potential rule name

### Step 6: Update Files

Write updated files:
- `knowledge/domains/dbt-pipelines/decision-traces/rules.json` - New/updated rules
- `knowledge/domains/dbt-pipelines/decision-traces/index.json` - Ensure fully indexed
- `knowledge/domains/dbt-pipelines/decision-traces/synthesis_log.json` - Append run record

### Step 7: Report Results

Output summary:

```
## Synthesis Complete

**Traces analyzed**: 6
**Rules created**: 0 new, 3 updated
**Emerging patterns**: 3 (awaiting confirmation)

### Rules by Confidence
| Rule | Confidence | Times Applied | Success Rate |
|------|------------|---------------|--------------|
| rule_incremental_merge_tuple_collision | medium | 1 | 100% |
| rule_program_filter_shared_infrastructure | medium | 1 | 100% |
| rule_daily_grain_retention_policy | medium | 1 | 100% |

### Emerging Patterns (need 1 more trace)
- rule_redshift_temp_table_stuck
- rule_missing_source_column
- rule_dbt_fusion_yaml_strict

### Recommendations
- [ ] Log more traces to confirm emerging patterns
- [ ] Review rules with confidence < medium
```

---

## Confidence Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **low** | 1 trace, unverified | Monitor only |
| **medium** | 2+ traces OR 1 verified | Suggest to user |
| **high** | 3+ traces, >90% success | Auto-apply with confirmation |

---

## Promotion Criteria

Rules are promoted to skill resources when:
- `confidence: "high"`
- `times_applied >= 3`
- `success_rate >= 0.9`
- No contradicting traces in last 30 days

Promotion target: `.claude/skills/dbt-redshift-optimization/resources/troubleshooting.md` or relevant skill resource.

---

## Arguments

| Arg | Description | Default |
|-----|-------------|---------|
| `--min-traces` | Minimum traces for rule | 2 |
| `--dry-run` | Show what would change without writing | false |
| `--promote` | Auto-promote high-confidence rules | false |

---

## Example Usage

```bash
# Standard synthesis
/synthesize-traces

# Dry run to preview changes
/synthesize-traces --dry-run

# With lower threshold for testing
/synthesize-traces --min-traces 1

# Auto-promote mature rules
/synthesize-traces --promote
```
