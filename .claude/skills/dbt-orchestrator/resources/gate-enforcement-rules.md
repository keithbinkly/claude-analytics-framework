<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-orchestrator/resources/gate-enforcement-rules.md
-->

# Gate Enforcement Rules

CAF-owned gate rules for the pipeline lifecycle.

## Rule Set

- Gates are mandatory by default.
- Gate approval must be explicit.
- State changes should be written only to the current source-of-truth location.
- If a gate dependency is still external to CAF, say so explicitly.

## Gate 1: Requirements Review

### Required Artifact

`handoffs/[pipeline]/business-context.md`

### Minimum Validation

- business context file exists
- `## Key Metrics` section exists
- `## Acceptance Criteria` section exists

## Gate 2: Data Findings Review

### Required Artifact

`handoffs/[pipeline]/data-discovery-report.md`

### Minimum Validation

- source inventory present
- schema validation present
- volume trace present
- suppression risks documented

## Gate 3: Architecture Review

### Required Artifact

`handoffs/[pipeline]/tech-spec.md`

### Minimum Validation

- model inventory present
- transformation rules documented
- test requirements documented
- dependencies mapped

## Gate 4: Deployment Review

### Required Artifacts

- `handoffs/[pipeline]/qa-report.md`
- deployment or handoff package if required by workflow

### Minimum Validation

- QA variance is within threshold or explicitly explained
- dbt tests passing or documented
- compilation succeeded

## Skip Protocol

Only allow gate skip when:

- the user explicitly requests it
- the reason is documented
- the gate status is written as skipped rather than passed

## Blocked State Protocol

If a required artifact or validation criterion is missing:

- mark the gate blocked
- summarize the missing requirements
- do not advance phase state

## Migration Note

This CAF copy should be treated as authoritative for the gate contract.

If deeper operational detail is still needed during migration, fall back to the matching `dbt-agent` resource and record that dependency explicitly.
