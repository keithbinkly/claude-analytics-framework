---
name: dbt-data-discovery
description: |
  Profiles source data, validates schemas, and documents discovery findings for dbt pipeline
  work from CAF root. Use when investigating source tables, validating column assumptions,
  checking join readiness, or creating a data-discovery report.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-data-discovery/SKILL.md
-->

# CAF dbt Data Discovery

Pre-build data profiling and discovery guidance for pipeline work.

## Use This Skill To

- profile source tables before implementation
- validate schema assumptions before coding
- quantify nulls, distributions, and date coverage
- document suppression risks and volume trace
- create `handoffs/[pipeline]/data-discovery-report.md`

## Read First

- `knowledge/reference/tools/dbt-mcp-tools-reference.md`
- `knowledge/reference/standards/folder-structure-and-naming.md`
- `knowledge/reference/tools/redshift-discovery-snippets.md`
- `knowledge/domains/dbt-pipelines/reference/field-mappings.md`
- `knowledge/domains/dbt-pipelines/reference/baas-join-registry.yml`
- `.claude/skills/dbt-orchestrator/resources/handoff-protocols.md`

If needed, fall back to:

- `dbt-agent/.claude/skills/dbt-data-discovery/SKILL.md`

## Operating Rule

Always profile before assuming:

- use dbt MCP metadata tools for source details and lineage
- use `execute_sql` when VPN is unavailable
- use `dbt show` when `{{ ref() }}` or project context is required and VPN is available

## Required Output Shape

`data-discovery-report.md` should cover:

- executive summary
- source inventory
- schema validation
- volume trace
- cardinality analysis
- suppression risks
- recommendations for architecture
