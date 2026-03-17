---
name: dbt-standards
description: |
  Shared analytics-workspace-root standards for dbt model placement, naming, and canonical reuse. Use when
  deciding where a model belongs, what naming convention to follow, or which existing
  canonical models should be reused.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-standards/SKILL.md
-->

# analytics-workspace dbt Standards

Placement, naming, and reuse guidance for dbt workflow design.

## Read First

- `knowledge/reference/standards/folder-structure-and-naming.md`
- `knowledge/reference/standards/controlled-vocabulary.yml`
- `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md`
- `knowledge/domains/dbt-pipelines/reference/baas-join-registry.yml`
- `knowledge/domains/redshift/reference/anti-pattern-impact.yml`

If needed, fall back to:

- `dbt-agent/shared/reference/architecture-validation-checklist.md`
- `dbt-agent/.claude/skills/dbt-standards/SKILL.md`

## Use This Skill To

- validate folder placement
- validate naming conventions
- check for canonical overlap before building
- flag Redshift anti-patterns during review
- advise whether a model belongs in staging, intermediate, or marts

## Mandatory Reuse Rule

Before recommending new models:

1. ask the user for known overlap
2. consult the canonical registry
3. search for related existing models or patterns

## Output Expectations

Any recommendation should make these explicit:

- proposed path
- naming rationale
- canonical reuse candidates
- unresolved dependencies still outside analytics-workspace
