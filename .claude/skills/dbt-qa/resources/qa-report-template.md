<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/.claude/skills/dbt-qa/resources/report-template.md
-->

# QA Report Template

Workspace-owned template for `handoffs/[pipeline]/qa-report.md`.

```markdown
# QA Validation Report: [Model or Pipeline Name]

**Date**: YYYY-MM-DD
**Validator**: [agent name]
**Total Time**: [X minutes]

## Summary

**Result**: ACCEPT | REWORK

| Metric | Threshold | Actual | Status |
|--------|-----------|--------|--------|
| Overall Variance | < 0.1% | X.XX% | PASS/FAIL |
| Incremental Validation | required/optional | [status] | PASS/FAIL |
| Compilation Status | pass | [status] | PASS/FAIL |

## Execution Summary

- Scope tested: [models / selectors / time range]
- Method used: [template / query set / comparison approach]
- Compile before run followed: [YES/NO]

## Findings

### Variance Analysis
- [Dimension 1]: X.X% variance - [root cause]
- [Dimension 2]: X.X% variance - [root cause]

### Edge Cases
- NULL handling: [status]
- Duplicate behavior: [status]
- Late arrivals / incremental behavior: [status]

### Test Results
- dbt tests: [passed/failed]
- Additional checks: [summary]

## Recommendation

[ACCEPT for production / REWORK with specific fixes]

## Next Steps

1. [action item]
2. [action item]

## Fallback Usage

- analytics-workspace-only guidance sufficient: [YES/NO]
- If no, list any `dbt-agent` fallback references used
```
