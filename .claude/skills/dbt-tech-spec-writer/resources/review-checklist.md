<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-tech-spec-writer/resources/review-checklist.md
-->

# Architecture Review Checklist

Use this for Gate 3 review of a dbt tech spec.

## Model Design

- [ ] all required metrics map to models
- [ ] layers are correct
- [ ] grains are explicit
- [ ] naming follows conventions
- [ ] materializations are justified
- [ ] placement was validated against structure guides

## Canonical Reuse

- [ ] reuse opportunities were checked first
- [ ] reuse percentage is documented
- [ ] new models are justified
- [ ] extension points are explicit

## Transformation Logic

- [ ] business rules are mapped
- [ ] complex logic is documented
- [ ] edge cases are handled
- [ ] calculation assumptions are reviewable

## Quality And Testing

- [ ] critical columns have tests
- [ ] suppression and volume risks are addressed
- [ ] legacy or certified comparison approach is documented
- [ ] incremental validation plan exists when relevant

## Dependencies And Risk

- [ ] upstream dependencies are explicit
- [ ] downstream impact is called out
- [ ] no circular dependencies exist
- [ ] major risks have mitigations
- [ ] architecture decisions include rationale and trade-offs

## Approval

- [ ] APPROVE
- [ ] APPROVE WITH CONDITIONS
- [ ] REJECT
