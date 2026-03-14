---
name: dbt-tech-spec-writer
description: |
  CAF-root architecture and specification guidance for dbt pipeline work. Use when designing
  a pipeline, creating a tech spec, documenting model inventory, validating architecture
  decisions, or preparing Gate 3 review artifacts.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-tech-spec-writer/SKILL.md
-->

# CAF dbt Tech Spec Writer

Create reviewable dbt architecture specifications from CAF root while keeping dbt execution in `dbt-enterprise`.

## Use This Skill To

- create `handoffs/[pipeline]/tech-spec.md`
- define model inventory and dependency graph
- document transformation rules and test requirements
- capture architecture decisions and risks
- prepare Gate 3 architecture review

## Read First

- `knowledge/domains/dbt-pipelines/reference/migration-quick-reference.md`
- `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md`
- `knowledge/reference/standards/folder-structure-and-naming.md`
- `knowledge/reference/standards/architecture-validation-checklist.md`
- `knowledge/domains/dbt-pipelines/reference/baas-join-registry.yml`
- `knowledge/domains/redshift/reference/anti-pattern-impact.yml`
- `.claude/skills/dbt-tech-spec-writer/resources/tech-spec-template.md`
- `.claude/skills/dbt-tech-spec-writer/resources/model-inventory-format.md`
- `.claude/skills/dbt-tech-spec-writer/resources/transformation-rules-format.md`
- `.claude/skills/dbt-tech-spec-writer/resources/review-checklist.md`

If needed, fall back to:

- `dbt-agent/shared/reference/architecture-validation-checklist.md`
- `dbt-agent/.claude/skills/dbt-tech-spec-writer/SKILL.md`

## Mandatory Design Rules

Before proposing new models:

1. ask the user for known overlap
2. consult the canonical registry
3. search for reusable models and patterns

Before approving placement:

1. read the actual structure guides in `dbt-enterprise`
2. validate path, purpose, and depth
3. record rejected alternatives

## Output Expectations

A good tech spec should make these explicit:

- target models and layers
- canonical reuse candidates
- folder-placement rationale
- transformation rules
- test requirements
- risks and mitigations
- unresolved dependencies still outside CAF
