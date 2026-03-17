---
name: dbt-preflight
description: |
  analytics-workspace-root pre-execution guidance for dbt model work. Use when deciding whether a dbt run is
  safe, estimating runtime and risk, or choosing whether to sample before execution.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-preflight/SKILL.md
-->

# analytics-workspace dbt Preflight

Estimate execution cost and risk before running dbt work from `dbt-enterprise`.

## Use This Skill To

- estimate runtime and scale risk before execution
- decide whether to sample first
- flag high-risk join patterns
- document why a full run or sample run was chosen

## Read First

- `knowledge/reference/tools/dbt-mcp-tools-reference.md`
- `knowledge/reference/standards/mandatory-compile-rule.md`
- `knowledge/domains/dbt-pipelines/reference/migration-quick-reference.md`
- `knowledge/domains/redshift/reference/anti-pattern-impact.yml`
- `knowledge/domains/dbt-pipelines/decision-traces/rules.json`

If needed, fall back to:

- `dbt-agent/shared/reference/MANDATORY_COMPILE_RULE.md`
- `dbt-agent/.claude/skills/dbt-preflight/SKILL.md`

## Core Rule

Preflight happens before execution, not after failure.

At minimum, assess:

- prior runtime if known
- upstream size and volume risk
- join fan-out or anti-pattern risk
- whether sampling is safer than a blind full run

## Mandatory Execution Rule

If execution proceeds:

1. compile first
2. only run after compile succeeds
3. keep dbt CLI execution in `dbt-enterprise`

## Output Expectations

A preflight result should state:

- estimated runtime or uncertainty level
- major risk flags
- recommendation: proceed, proceed with caution, or sample first
- why that recommendation was chosen
