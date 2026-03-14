<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/knowledge-base/field-mappings.md
-->

> CAF migration note: this is a curated CAF copy of the field mappings that repeatedly matter in dbt pipeline work. Use this first, then fall back to the fuller `dbt-agent` version if needed.

# Field Mappings

Quick reference for field-name and business-logic variations that repeatedly cause dbt migration mistakes.

## Authorization Reason Codes

### Preferred Fields

| Table or model | Field | Guidance |
|----------------|-------|----------|
| `stg_edw__fct_authorization_transaction` | `auth_reason_desc` | Raw processor values; avoid for final business logic when enriched fields exist |
| `int_transactions__auth_all` | `combined_reason_codes` | Prefer for reporting and filtering |
| `int_transactions__auth_purchase_agg` | `combined_reason_codes` | Use for aggregation logic |

### Approval Values To Exclude

To avoid double-counting successful transactions, exclude:

- `Success`
- `Transaction Approved`
- `Partial Approval`

Example:

```sql
WHERE auth_reason_desc NOT IN ('Success', 'Transaction Approved', 'Partial Approval')
```

## Date Field Variations

Some multi-grain models populate all date columns at once, so NULL checks do not identify the grain.

Wrong pattern:

```sql
CASE
  WHEN calendar_date IS NOT NULL AND week_end_date IS NULL THEN 'Daily'
END
```

Preferred pattern:

```sql
daily AS (
    SELECT calendar_date, ...
    GROUP BY calendar_date, ...
),
weekly AS (
    SELECT week_end_date, ...
    GROUP BY week_end_date, ...
),
unioned AS (
    SELECT 'Daily' AS time_period, calendar_date, ... FROM daily
    UNION ALL
    SELECT 'Weekly' AS time_period, week_end_date AS calendar_date, ... FROM weekly
)
```

## Transaction Type Hierarchies

`stg_edw__txn_type_hier_txn_type_xref` can carry business rules in `hier_business_rule_1`.

Common rule families:

- NULL -> default join
- MCC-based comparisons
- amount threshold comparisons

When using this mapping, verify the actual business-rule pattern before assuming a simple equality join.

## Merchant Name Fields

| Model | Field | Guidance |
|-------|-------|----------|
| `stg_edw__fct_*` | `merchant_nm` | Raw merchant value from source |
| `int_merchant_mapping` | `merchant_nm` | Raw join key |
| `int_merchant_mapping` | `merchant_cleaned` | Prefer for reporting |
| `int_transactions__*_agg` | `merchant_cleaned` | Prefer for aggregated reporting |

## Common Gotchas

### `portfolio` vs `product_stack`

- source-facing models often use `portfolio`
- marts and seeds often use `product_stack`

### `auth_response` Type

- source values may be numeric
- posted transactions may hardcode approval values
- cast explicitly for UNION compatibility

### Rank Columns In UNIONs

- use `NULL::INT` rather than arbitrary placeholders
- preserve semantic meaning while maintaining type compatibility
