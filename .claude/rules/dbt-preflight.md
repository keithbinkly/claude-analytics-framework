# Preflight Checks

## Before Building

1. **Check dependencies**: Run `dbt ls --select +model_name` or use manifest-parser. Identify missing upstream models and build in correct order. Never assume upstream dependencies exist in the warehouse. (Skipping this causes 60-90 min error cascades.)

2. **Environment date filters**: Every date-filtered model must use `transactions_full_refresh_filter` or `batch_full_refresh_filter` macros. Never hardcode date ranges. See `dbt-agent/shared/reference/temp-filter-quick-reference.md`.

3. **Large run check**: Before running any model that could take >120 seconds or touches >500M upstream rows, estimate runtime and join risk. If 2+ flags or xxl upstream, require user confirmation and suggest a sample query first.

## Before Placing Models

Load actual architecture docs from dbt-enterprise (`intermediate_structure_guide.md`, `transactions_structure_guide.md`, `marts_structure_guide.md`). Never rely on generic dbt guidance or memory. Maximum path depth: 4 levels.

## Data Safety

Never write actual warehouse query results or production data to files that would be committed to git. Use only gitignored locations: `session-logs/` and `handoffs/`.
