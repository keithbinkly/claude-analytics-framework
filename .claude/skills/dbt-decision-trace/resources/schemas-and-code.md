# dbt-decision-trace: Schemas and Code Reference

## Trace Schema

```json
{
  "id": "qa_YYYY-MM-DD_NNN",
  "timestamp": "ISO8601",
  "model": "model_name",
  "agent_session": "session_id",

  "problem": {
    "symptom": "human-readable description",
    "error_type": "fan_out|grain_violation|missing_rows|duplicate_rows|type_mismatch|null_values|performance|other",
    "severity": "blocking|degraded|cosmetic",
    "context": "migration|refactoring|new_model|incremental_testing"
  },

  "triage_path": [{
    "step": 1,
    "hypothesis": "what we suspected",
    "check": "what was checked",
    "query_or_action": "SQL or command",
    "cost_seconds": 0,
    "result": "what was found",
    "ruled_out": "hypothesis eliminated",
    "led_to": "next hypothesis or resolution"
  }],

  "resolution": {
    "fix": "what change was made",
    "root_cause": "underlying reason",
    "fix_location": "file:line",
    "verified": true,
    "fix_category": "filter_missing|join_cardinality|date_boundary|logic_error|data_quality|performance"
  },

  "reuse_guidance": {
    "when_applicable": "symptoms that suggest this solution",
    "when_not_applicable": "false positive indicators",
    "abstraction_level": "specific|general|pattern"
  },

  "cost_total": {
    "checks_run": 0,
    "time_minutes": 0,
    "models_built": 0
  }
}
```

---

## Rule Schema (v2.0)

```json
{
  "pattern_id": "rule_incremental_merge_tuple_collision",
  "version": 1,
  "source_traces": ["qa_2025-12-16_001"],
  "created": "2025-12-31T00:00:00Z",
  "last_updated": "2025-12-31T00:00:00Z",
  "confidence": "low|medium|high",

  "pattern": {
    "generalized_symptom": "Abstracted symptom description",
    "error_types": ["duplicate_rows", "other"],
    "contexts": ["incremental_testing", "refactoring"],
    "detection_signals": ["keyword1", "keyword2"]
  },

  "recommended_action": {
    "first_try": "Primary fix to attempt",
    "rationale": "Why this works",
    "implementation": {
      "file_pattern": "*.sql",
      "change": "Code change template"
    },
    "alternatives": ["Alternative 1", "Alternative 2"]
  },

  "applicability": {
    "when_applicable": ["Condition 1", "Condition 2"],
    "when_not_applicable": ["Exception 1", "Exception 2"]
  },

  "metrics": {
    "times_applied": 1,
    "success_rate": 1.0,
    "avg_resolution_minutes": 20,
    "last_applied": "2025-12-31T00:00:00Z"
  }
}
```

---

## Core Function Implementations

### log_trace()

```python
def log_trace(trace: dict) -> str:
    assert 'problem' in trace
    assert 'resolution' in trace
    trace_id = f"qa_{datetime.now().strftime('%Y-%m-%d')}_{next_sequence()}"
    trace['id'] = trace_id
    trace['timestamp'] = datetime.now().isoformat()
    with open('shared/decision-traces/traces.json', 'r+') as f:
        data = json.load(f)
        data['traces'].append(trace)
        f.seek(0)
        json.dump(data, f, indent=2)
    update_index(trace)
    return trace_id
```

### search_traces()

```python
def search_traces(symptom: str, error_type: str = None) -> list[dict]:
    with open('shared/decision-traces/traces.json') as f:
        data = json.load(f)
    matches = []
    for trace in data['traces']:
        score = similarity(symptom, trace['problem']['symptom'])
        if error_type and trace['problem']['error_type'] == error_type:
            score *= 1.5
        matches.append({'trace': trace, 'score': score})
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:3]
```

### match_rules() (v2.0)

```python
def match_rules(symptom: str, error_type: str = None) -> list[dict]:
    with open('shared/decision-traces/rules.json') as f:
        data = json.load(f)
    matches = []
    symptom_words = set(symptom.lower().split())
    for rule in data['rules']:
        signals = set(s.lower() for s in rule['pattern']['detection_signals'])
        overlap = len(symptom_words & signals)
        if overlap > 0:
            score = overlap / len(signals)
            if error_type and error_type in rule['pattern'].get('error_types', []):
                score *= 1.5
            confidence_boost = {'low': 0.8, 'medium': 1.0, 'high': 1.2}
            score *= confidence_boost.get(rule['confidence'], 1.0)
            matches.append({'rule': rule, 'score': score})
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:3]
```

### synthesize_rules() (v2.0)

```python
def synthesize_rules(min_traces: int = 2, similarity_threshold: float = 0.7) -> dict:
    # See /synthesize-traces command for full algorithm
    pass
```

### get_rules() / get_stats()

```python
def get_rules(confidence: str = None) -> list[dict]:
    with open('shared/decision-traces/rules.json') as f:
        data = json.load(f)
    rules = data['rules']
    if confidence:
        rules = [r for r in rules if r['confidence'] == confidence]
    return rules

def get_stats() -> dict:
    with open('shared/decision-traces/traces.json') as f:
        trace_data = json.load(f)
    with open('shared/decision-traces/rules.json') as f:
        rule_data = json.load(f)
    traces = trace_data['traces']
    rules = rule_data['rules']
    emerging = rule_data.get('emerging_patterns', [])
    return {
        'total_traces': len(traces),
        'total_rules': len(rules),
        'emerging_patterns': len(emerging),
        'by_error_type': Counter(t['problem']['error_type'] for t in traces),
        'by_fix_category': Counter(t['resolution']['fix_category'] for t in traces),
        'rules_by_confidence': Counter(r['confidence'] for r in rules),
        'avg_checks_per_resolution': sum(t['cost_total']['checks_run'] for t in traces) / len(traces) if traces else 0,
        'avg_time_minutes': sum(t['cost_total']['time_minutes'] for t in traces) / len(traces) if traces else 0
    }
```

---

## Integration: At QA Resolution (dbt-qa Phase 5)

```python
trace = {
    "model": current_model,
    "problem": {
        "symptom": symptom_description,
        "error_type": identified_error_type,
        "severity": severity_level,
        "context": "migration"
    },
    "triage_path": triage_steps,
    "resolution": {
        "fix": applied_fix,
        "root_cause": root_cause,
        "fix_location": file_location,
        "verified": True,
        "fix_category": fix_category
    },
    "reuse_guidance": {
        "when_applicable": "similar symptoms",
        "when_not_applicable": "different context",
        "abstraction_level": "general"
    },
    "cost_total": {
        "checks_run": len(triage_steps),
        "time_minutes": elapsed_time,
        "models_built": models_run_count
    }
}
trace_id = log_trace(trace)
```

---

## Investigation Document Template

```markdown
# Investigation: <Model/Job Name>

**Date:** YYYY-MM-DD
**Status:** Unresolved / Resolved

## Summary
Brief description of the failure and symptoms.

## What Was Checked

### Tools Used
- [ ] get_job_run_error - findings
- [ ] git history (`git log --oneline -20`) - findings
- [ ] Data investigation (`dbt show`) - findings

### Hypotheses Tested
| Hypothesis | Evidence | Result |
|---|---|---|
| Recent code change | No changes to affected models in 7 days | Ruled out |

## Patterns Observed
- [What patterns were found]

## Resolution / Next Steps
1. [ ] [Action item]
```
