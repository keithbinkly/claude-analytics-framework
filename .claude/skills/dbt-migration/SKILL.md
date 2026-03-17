---
name: dbt-migration
description: |
  analytics-workspace-root implementation guidance for building dbt models from approved specs. Use when
  translating legacy SQL or report logic into dbt models, implementing an approved tech spec,
  or planning the Phase 4 build sequence from analytics-workspace while keeping dbt execution in
  `dbt-enterprise`.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-migration/SKILL.md
-->

# analytics-workspace dbt Migration

Implementation guidance for Phase 4 pipeline work from analytics-workspace root.

## Use This Skill To

- implement an approved `tech-spec.md`
- translate legacy SQL or report logic into dbt models
- plan staging, intermediate, and mart model creation
- decide whether to reuse, extend, or build new models
- prepare execution and QA handoff notes

## Read First

- `knowledge/domains/dbt-pipelines/reference/migration-quick-reference.md`
- `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md`
- `knowledge/domains/dbt-pipelines/reference/baas-join-registry.yml`
- `knowledge/domains/dbt-pipelines/reference/macros-registry.md`
- `knowledge/reference/standards/folder-structure-and-naming.md`
- `knowledge/reference/standards/controlled-vocabulary.yml`
- `knowledge/reference/standards/mandatory-compile-rule.md`
- `knowledge/domains/redshift/reference/anti-pattern-impact.yml`
- `.claude/skills/dbt-preflight/SKILL.md`
- `.claude/skills/sql-hidden-gems/SKILL.md`
- `.claude/skills/dbt-migration/resources/qa-execution-handoff-template.md`

If needed, fall back to:

- `dbt-agent/.claude/skills/dbt-migration/SKILL.md`
- `dbt-agent/.claude/skills/dbt-fundamentals/SKILL.md`

## Input Contract

Before implementation, confirm these exist:

- `handoffs/[pipeline]/business-context.md`
- `handoffs/[pipeline]/data-discovery-report.md`
- `handoffs/[pipeline]/tech-spec.md`

## Mandatory Build Rules

Before writing SQL:

1. ask the user for overlap hints
2. consult canonical references
3. search for existing reusable patterns
4. validate folder placement before recommending new files

Before execution:

1. run preflight
2. compile before run
3. execute dbt CLI from `dbt-enterprise`, never analytics-workspace root

## Output Expectations

A migration/build plan should make these explicit:

- what is being reused vs built new
- target file paths and layers
- join and anti-pattern checks applied
- compile-before-run sequence
- whether a builder-to-QA handoff package should be created
- unresolved dependencies still outside analytics-workspace
