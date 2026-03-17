---
name: dbt-fundamentals
description: |
  analytics-workspace-root foundational dbt guidance covering layers, modeling, testing, materializations,
  and command patterns. Use when implementation work needs general dbt reference material
  that is broader than a single specialized skill.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-fundamentals/SKILL.md
-->

# analytics-workspace dbt Fundamentals

General dbt reference guidance for analytics-workspace-routed pipeline work.

## Use This Skill To

- explain basic dbt architecture and layering
- choose materialization directionally
- recall common command and selector patterns
- apply general testing and modeling rules during implementation
- support Phase 4 build work when a specialized skill is too narrow

## Read First

- `knowledge/reference/standards/folder-structure-and-naming.md`
- `knowledge/reference/standards/mandatory-compile-rule.md`
- `knowledge/reference/tools/dbt-mcp-tools-reference.md`
- `knowledge/domains/dbt-pipelines/reference/migration-quick-reference.md`

If needed, fall back to:

- `dbt-agent/.claude/skills/dbt-fundamentals/SKILL.md`

## Core Reminders

- prefer `ref()` and `source()` over hard-coded tables
- keep layering explicit: staging -> intermediate -> marts
- compile before run
- run dbt CLI from `dbt-enterprise`
- use more specialized analytics-workspace skills when the question is really about QA, standards, preflight, or migration

## Output Expectations

When using this skill in implementation guidance, state:

- which dbt principle applies
- whether the advice is generic vs project-specific
- whether a more specialized analytics-workspace skill should take over
