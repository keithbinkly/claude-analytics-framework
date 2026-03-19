---
name: dbt-qa
description: |
  Shared workspace-root QA guidance for validating dbt models against legacy or certified outputs.
  Use when running variance analysis, checking data quality, investigating mismatches, or
  preparing a QA report for a pipeline.
---

<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/.claude/skills/dbt-qa/SKILL.md
-->

# dbt QA

QA workflow guidance for validating dbt pipeline outputs.

## Read First

- `knowledge/domains/dbt-pipelines/reference/qa-validation-checklist.md`
- `knowledge/reference/tools/dbt-mcp-tools-reference.md`
- `knowledge/domains/dbt-pipelines/reference/troubleshooting.md`
- `knowledge/domains/dbt-pipelines/decision-traces/rules.json`
- `knowledge/domains/dbt-pipelines/decision-traces/selected-traces.json`
- `knowledge/domains/dbt-pipelines/decision-traces/README.md`
- `.claude/skills/dbt-orchestrator/resources/handoff-protocols.md`
- `.claude/skills/dbt-qa/resources/qa-report-template.md`
- `.claude/skills/dbt-migration/resources/qa-execution-handoff-template.md`

If needed, fall back to:

- `knowledge/domains/dbt-pipelines/decision-traces/rules.json`
- `knowledge/domains/dbt-pipelines/decision-traces/traces-full.json`
- `dbt-agent/.claude/skills/dbt-qa/SKILL.md`

## Use This Skill To

- run QA templates against new vs legacy outputs
- investigate metric variance
- validate grain and duplicate behavior
- document pass/fail status for QA handoff
- create `handoffs/[pipeline]/qa-report.md`

## Core QA Rule

Do not rely on row-count matching alone.

Prefer:

- aggregate sanity check
- granular variance analysis
- edge-case validation
- incremental vs full-refresh validation when relevant

## Output Expectations

A QA result should state:

- what was compared
- which template or method was used
- variance or pass/fail result
- whether unresolved issues remain
- whether further dbt-agent fallback references were needed
