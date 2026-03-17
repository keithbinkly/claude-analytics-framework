---
name: sql-hidden-gems
description: |
  analytics-workspace-root guidance for advanced SQL patterns that are useful when standard modeling
  approaches are not enough. Use for deeper analytical patterns, fanout avoidance,
  reconciliation tactics, advanced aggregations, and Redshift-aware SQL design ideas.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/sql-hidden-gems/SKILL.md
-->

# analytics-workspace SQL Hidden Gems

Advanced SQL reference for migration, debugging, and analytical edge cases.

## Use This Skill To

- detect fanout and pre-aggregate before joins
- choose safer anti-join and reconciliation patterns
- apply gaps-and-islands or advanced aggregation techniques
- reason about Redshift-friendly tactics when standard SQL is clumsy
- deepen a migration design when the obvious pattern is not enough

## Read First

- `knowledge/domains/redshift/reference/anti-pattern-impact.yml`
- `knowledge/domains/dbt-pipelines/reference/baas-join-registry.yml`
- `knowledge/domains/dbt-pipelines/reference/troubleshooting.md`

If needed, fall back to:

- `dbt-agent/.claude/skills/sql-hidden-gems/SKILL.md`

## When To Reach For This

Use it when:

- a join pattern is causing fanout or reconciliation pain
- you need a more robust statistical or analytical pattern
- simple GROUP BY logic is not expressive enough
- you want a stronger SQL option before inventing bespoke logic

## Output Expectations

A good recommendation should state:

- the advanced pattern being used
- why the standard approach is weak here
- Redshift caveats if relevant
- whether the pattern should become a macro, model, or one-off query
