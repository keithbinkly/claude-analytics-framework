# Local CI Simulation for dbt

## Quick Syntax Check (no warehouse needed)
```bash
dbt compile -s model1 model2 model3
```

## Full CI Simulation with state:modified+
```bash
# 1. Save baseline manifest from main
mkdir -p /tmp/dbt_prod_state
git stash && git checkout main
dbt compile
cp target/manifest.json /tmp/dbt_prod_state/manifest.json
git checkout <feature-branch> && git stash pop

# 2. Build only modified models + downstream
dbt build --select state:modified+ --state /tmp/dbt_prod_state/
```

## Schema Change Strategy
- `on_schema_change='sync_all_columns'` lets CI pass without full refresh
- New columns added via ALTER TABLE, populated for lookback window only
- Schedule full refresh on prod separately after merge

## Lesson (2026-03-04)
Don't wait for dbt Cloud CI logs — simulate locally with `dbt compile` first. Catches SQL errors in seconds vs minutes waiting for cloud job.
