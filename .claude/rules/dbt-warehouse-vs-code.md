# Compiled SQL != Materialized Data

## The Golden Rule

Compiled SQL being correct does NOT mean data is materialized. When a column appears missing or query results seem wrong after `dbt compile` succeeds, the model is not materialized — run `dbt run --full-refresh`, don't re-edit the SQL.

## Column Not Found Loop (Pattern A)

```
Compile succeeds → query fails "column not found" → agent edits SQL → compile succeeds → query still fails
```

**Fix:** `dbt run --full-refresh` on the model. The compiled SQL was correct all along.

## Circuit Breaker

2+ "column not found" errors on the same model → stop editing SQL. The model needs `--full-refresh`.

Use MCP tools (`get_model_details`, `execute_sql`) to verify warehouse state, not compiled SQL output.
