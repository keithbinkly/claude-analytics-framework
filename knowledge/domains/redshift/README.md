# Redshift

**Maintainer:** Keith
**Status:** Accepting contributions

## What This Covers

Amazon Redshift-specific optimization patterns, table design, query tuning, anti-patterns, and operational knowledge that applies across all our analytics work.

## Why This Folder Matters

Redshift has specific performance characteristics that generic SQL knowledge misses — distribution keys, sort keys, the cost of merge on composite keys, when to use `delete+insert` vs `merge`, and anti-patterns that are 2-4x slower than alternatives. When Claude knows these, it writes faster SQL from the start.

## How Agents Use This Folder

Claude reads files here when:
- You mention "optimize", "slow query", "DISTKEY", "SORTKEY", or "performance"
- You're reviewing SQL for Redshift-specific issues
- The preflight check flags a model as potentially expensive

This folder works alongside:
- `dbt-redshift-optimization` skill — comprehensive optimization patterns
- `.claude/rules/dbt-preflight.md` — pre-execution cost estimation

## What's Here Already

- `reference/anti-pattern-impact.yml` — measured performance impact of common anti-patterns:
  - `NOT IN (subquery)` → 4.18x slower (use `NOT EXISTS`)
  - `OR` in JOIN → 4.07x slower (use `UNION ALL`)
  - Deep nesting 3+ → 3.06x slower (use CTEs)
  - `SELECT *` → 2.08x slower (list explicit columns)

## What to Add

### `patterns/` — Proven approaches

- DISTKEY selection decision tree (high cardinality join key → DISTKEY)
- SORTKEY patterns for common query shapes
- Incremental strategy guide (`delete+insert` vs `merge` — we learned this the hard way)
- Window function optimization patterns
- Large table tactics (sampling, approximate aggregation)

### `reference/` — Facts about our Redshift setup

- Cluster configuration and node types
- Schema and table ownership conventions
- System table queries for performance diagnosis
- WLM queue configuration and concurrency limits

### `decisions/` — Why we do things this way

- "Why we use `delete+insert` over `merge` for composte-key incrementals" (per-row amount inflation at month boundaries — see `.claude/rules/dbt-incremental-merge-lessons.md`)
- "Why we pre-filter with date macros instead of full table scans"
- "Why we prefer EDW over ODS source tables"

## Getting Started

The anti-pattern reference is already here. Next most valuable additions:

1. **DISTKEY/SORTKEY patterns** — for our most common table shapes
2. **A query optimization example** — before/after with measured improvement
3. **System table queries** — the diagnostic SQLs you use to investigate slow models
