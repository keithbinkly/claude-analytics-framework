# Semantic Layer

**Maintainer:** Keith
**Status:** Accepting contributions

## What This Covers

MetricFlow configuration, metric definitions, semantic models, saved queries, dimension/entity design, and BI tool integrations via the dbt Semantic Layer.

## Why This Folder Matters

The semantic layer is how we define "one metric, one definition" for the business. When Claude helps write semantic YAML, it needs to know our conventions — naming patterns, metric types, grain rules, and the gotchas we've hit. Without this knowledge, it writes generic MetricFlow YAML. With it, it writes YAML that passes `mf validate` on first try.

## How Agents Use This Folder

Claude reads files here when:
- You mention "semantic layer", "MetricFlow", or "metrics"
- You're writing or editing `sem_*.yml` files
- You ask about dimension design, saved queries, or BI integrations

This folder works alongside the `dbt-semantic-layer-developer` skill (`.claude/skills/dbt-semantic-layer-developer/`) which has the MetricFlow spec and syntax reference. This folder adds **our team's** conventions on top.

## What to Add

### `patterns/` — Proven approaches

- Semantic model templates for common grain patterns (daily, account-level, transaction-level)
- Metric type decision guide ("when to use ratio vs derived")
- Saved query templates for common BI consumption patterns
- Dimension naming conventions and hierarchies

### `reference/` — Facts about our semantic layer

- Inventory of deployed semantic models and their grains
- List of active metrics with definitions
- BI tool integration status (which tools consume which saved queries)
- MetricFlow version compatibility notes (Fusion vs Core 1.10)

### `decisions/` — Why we do things this way

- "Why we use `delete+insert` not `merge` for incremental semantic models"
- "Why metric names include the domain prefix"
- "Why we separate approved vs declined in the semantic model rather than using a filter"
- CI lessons (name matching, partial parse, inline vs dedicated files — see `.claude/rules/dbt-semantic-ci-lessons.md`)

## Getting Started

If you're contributing semantic layer content, start with:

1. **Document one semantic model** — its grain, measures, dimensions, and why it's shaped that way
2. **Document one tricky metric** — the one that took debugging to get right
3. **Document one decision** — something non-obvious about our semantic layer setup

## Environment Note

Our semantic layer uses a dual installation:
- **Fusion 2.0** (`dbt run/build/test`) — for all pipeline work
- **Core 1.10 `.venv`** (`mf query/validate`) — for MetricFlow validation only

Never activate `.venv` for upstream pipeline work.
