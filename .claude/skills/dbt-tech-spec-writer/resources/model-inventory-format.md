<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-tech-spec-writer/resources/model-inventory-format.md
-->

# Model Inventory Format

Use this helper when filling the model-inventory section of a tech spec.

## Required Columns

| Column | Description | Example |
|--------|-------------|---------|
| **Model Name** | full model name with prefix | `int_transactions__daily_agg` |
| **Layer** | staging, intermediate, or marts | `intermediate` |
| **Materialization** | how the model is built | `view`, `table`, `incremental` |
| **Grain** | what one row represents | `transaction`, `day+account` |
| **Unique Key** | row-uniqueness columns | `txn_id`, `[date, account_id]` |
| **Est. Rows** | expected scale | `1M`, `100K` |
| **Reuse Status** | `NEW`, `CANONICAL`, `EXTEND` | `CANONICAL` |

## Template

```markdown
| Model Name | Layer | Materialization | Grain | Unique Key | Est. Rows | Reuse Status |
|------------|-------|-----------------|-------|------------|-----------|--------------|
| `stg_source__table` | staging | view | transaction | txn_uid | 100M | N/A |
| `int_domain__enriched` | intermediate | table | transaction | txn_uid | 100M | NEW |
| `int_domain__aggregated` | intermediate | incremental | day+account | [date, acct_id] | 5M | CANONICAL |
| `mrt_domain__summary` | marts | table | month+product | [month, product_id] | 100K | NEW |
```

## Layer Summary

- `stg_`: source-aligned cleaning, light casting, no real business logic
- `int_`: business logic, joins, reusable transformations
- `mrt_`: business-ready outputs and final aggregations

## Reuse Status Rules

- `NEW`: built specifically for this pipeline
- `CANONICAL`: reused directly from an existing model
- `EXTEND`: builds on an existing canonical model with additional logic

## Grain Check

Always verify the documented grain with a duplicate check before approving the tech spec.

```sql
SELECT
    [unique_key_columns],
    COUNT(*) AS cnt
FROM {{ ref('model_name') }}
GROUP BY [unique_key_columns]
HAVING COUNT(*) > 1
LIMIT 10;
```
