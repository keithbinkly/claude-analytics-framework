# Compile Before Run

## Zero Tolerance

Before every `dbt run`, `dbt build`, or `dbt test`, always run `dbt compile` first. No exceptions. If compile fails, fix it before touching the warehouse.

Compile takes 5-10 seconds. A warehouse error takes 2-5 minutes. That's 12-30x ROI.

## Sequence

```
dbt compile → fix errors → dbt compile (clean) → dbt run
```

Never skip to `dbt run` because "it's a small change." Small changes cause syntax errors at the same rate as large ones.
