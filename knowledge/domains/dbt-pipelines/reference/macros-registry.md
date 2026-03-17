<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/knowledge-base/macros-registry.md
-->

> analytics-workspace migration note: this is a curated analytics-workspace copy of the macro registry used during migration and architecture review. Prefer this from analytics-workspace root, then inspect the macro source in the execution repo if needed.

# Macros Registry

Reusable dbt macro reference for avoiding duplicated logic during migration and design work.

## What To Check For

Before writing new logic, check whether an existing macro already handles:

- transaction classification
- hierarchy-key join logic
- environment-aware date filtering
- CI limiting or execution filters

## Transaction Classification Macros

**Typical location**: `macros/transactions/classification.sql`

### `txn_is_fee(...)`

- Purpose: flag fee transactions
- Used in: transaction canonical models such as posted and auth flows

### `txn_is_adjustment(...)`

- Purpose: flag internal credit or adjustment transactions
- Used in: transaction canonical models

### `txn_flow(...)`

- Purpose: map hierarchy logic into funds-in, funds-out, or other flows

### `txn_category(...)`

- Purpose: high-level transaction categorization
- Use when repeated CASE logic would otherwise be duplicated across models

### `txn_subcategory(...)`

- Purpose: more detailed transaction subcategorization
- Use when the classification logic is too complex to inline cleanly

## Transaction Type Hierarchy Join Macro

**Typical location**: `macros/revenue/get_txn_type_hierarchy_key.sql`

### `get_txn_type_hierarchy_key(mcc, amount, hier_business_rule)`

- Purpose: evaluate MCC and amount threshold rules for hierarchy joins
- Typical use: join conditions involving `txn_type_hierarchy`
- Use instead of repeating complex CASE logic in multiple models

Example:

```sql
LEFT JOIN txn_type_hierarchy tth
  ON pt.txn_type_uid = tth.txn_type_uid
 AND {{ get_txn_type_hierarchy_key('pt.mcc', 'pt.total_post_amt', 'tth.hier_business_rule_1') }} = 1
```

## Date And Environment Macros

**Typical location**: `macros/utilities/transactions_time_filters.sql`

### `transactions_full_refresh_filter(column_name)`

- Purpose: apply environment-aware date limits for transaction models
- Use for dev and CI safety instead of ad hoc date filters

### `limit_ci()`

- Purpose: apply CI-only limits
- Use when the logic is specifically meant to reduce CI cost or runtime

## Migration Workflow

Before creating net-new logic:

1. check this registry
2. inspect the actual macro source if a candidate looks close
3. confirm parameter compatibility
4. prefer macro reuse when the same logic appears in 2+ models

## Macro Vs Model

Use a macro when:

- logic is row-level and reusable
- the main value is parameterized SQL generation

Use a model when:

- the logic creates reusable precomputed data
- the output should be queried as a stable relation
