---
name: dbt-lineage
description: |
  CAF-root lineage and dependency-analysis guidance for dbt pipeline work. Use when tracing
  upstream or downstream impact, understanding migration order, checking what depends on a
  model or source, or inspecting manifest-driven lineage.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-lineage/SKILL.md
-->

# CAF dbt Lineage

Dependency and impact-analysis guidance for CAF-routed dbt workflows.

## Use This Skill To

- trace upstream and downstream model dependencies
- understand migration order
- inspect impact radius before changing a model
- reason about manifest-driven lineage
- locate which models use a given source or model

## Read First

- `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md`
- `knowledge/reference/standards/folder-structure-and-naming.md`
- `knowledge/reference/tools/dbt-mcp-tools-reference.md`

If needed, fall back to:

- `dbt-agent/.claude/skills/dbt-lineage/SKILL.md`

## Preferred Inputs

Use whichever is available:

- manifest artifacts in the execution repo
- dbt MCP lineage and model-detail tools
- explicit model or source names from the task

## Output Expectations

A lineage result should make these explicit:

- direct parents
- direct children
- likely impact radius
- build or migration order when relevant
- uncertainty if the manifest or environment is stale
