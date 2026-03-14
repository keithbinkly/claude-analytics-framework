---
name: dbt-sql-unit-testing
description: |
  CAF-root guidance for fast local SQL transformation tests using mock data and DuckDB-style
  workflows. Use when validating edge cases, complex SQL logic, or bug fixes before slower
  warehouse QA.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-sql-unit-testing/SKILL.md
-->

# CAF dbt SQL Unit Testing

Fast local logic-validation guidance for dbt pipeline work.

## Use This Skill To

- test complex transformation logic with mock data
- validate edge cases before warehouse execution
- reproduce prior QA variance scenarios locally
- iterate on logic when VPN or warehouse access is unavailable

## Read First

- `knowledge/domains/dbt-pipelines/reference/qa-validation-checklist.md`
- `knowledge/domains/dbt-pipelines/reference/troubleshooting.md`
- `knowledge/domains/dbt-pipelines/decision-traces/rules.json`

If needed, fall back to:

- `dbt-agent/.claude/skills/dbt-sql-unit-testing/SKILL.md`

## When To Prefer This

Use local SQL unit testing when:

- logic is complex and narrow
- edge cases matter more than warehouse scale
- you need a fast loop before dbt execution
- warehouse or VPN access is constrained

## Output Expectations

A unit-test recommendation or plan should state:

- what logic is being tested
- why local unit tests are appropriate
- which edge cases should be covered
- whether further warehouse QA is still required
