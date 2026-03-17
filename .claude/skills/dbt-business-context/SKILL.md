---
name: dbt-business-context
description: |
  Captures and structures business context for dbt pipeline work from analytics-workspace root. Use when
  gathering requirements, parsing stakeholder notes, documenting key metrics, or creating
  the business-context artifact for a pipeline.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-business-context/SKILL.md
-->

# analytics-workspace dbt Business Context

Requirements-capture guidance for the pipeline workflow.

## Use This Skill To

- document the purpose of a pipeline
- define business metrics precisely
- capture acceptance criteria
- record stakeholder or legacy-script context
- create `handoffs/[pipeline]/business-context.md`

## Read First

- `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md`
- `knowledge/domains/dbt-pipelines/reference/legacy-kpi-gold-standard-metrics.md`
- `.claude/skills/dbt-orchestrator/resources/handoff-protocols.md`

If needed, fall back to:

- `dbt-agent/.claude/skills/dbt-business-context/SKILL.md`

## Required Output Shape

`business-context.md` should cover:

- overview
- source information
- key metrics
- acceptance criteria
- domain glossary
- out of scope
- questions for discovery

## Migration Note

This analytics-workspace version is the preferred control-plane reference.

Use `dbt-agent` only when the analytics-workspace copy does not yet contain enough domain-specific depth.
