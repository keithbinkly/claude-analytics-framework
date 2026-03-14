<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-tech-spec-writer/resources/transformation-rules-format.md
-->

# Transformation Rules Format

Use this helper when documenting non-trivial column logic in a tech spec.

## Required Columns

| Column | Description | Example |
|--------|-------------|---------|
| **Target Column** | output column name | `net_revenue` |
| **Source Column(s)** | inputs used | `txn_amount, fee_amount` |
| **Transformation** | brief logic summary | `txn_amount - fee_amount` |
| **Business Rule Reference** | requirement or rule id | `BR-001` |

## Template

```markdown
| Target Column | Source Column(s) | Transformation | Business Rule |
|---------------|------------------|----------------|---------------|
| net_revenue | txn_amount, fee_amount | txn_amount - COALESCE(fee_amount, 0) | BR-001 |
| product_name | product_code | CASE mapping to business names | BR-002 |
| is_active | status, end_date | status='A' AND end_date IS NULL | BR-003 |
```

## Common Categories

- direct mappings
- calculations
- CASE mappings
- date transformations
- NULL handling
- aggregations
- window functions
- joins and lookups

## Example Patterns

### Calculation

```sql
gross_amount - COALESCE(discount, 0) + COALESCE(tax, 0) AS net_amount
```

### CASE Mapping

```sql
CASE
    WHEN score >= 80 THEN 'High'
    WHEN score >= 50 THEN 'Medium'
    ELSE 'Low'
END AS risk_level
```

### NULL Handling

```sql
COALESCE(product_name, 'Unknown') AS product_name
```

### Join Lookup

```sql
LEFT JOIN {{ ref('dim_product') }} p
  ON f.product_id = p.product_id
```

## Guidance

- keep each rule traceable to a business requirement
- separate simple table rows from truly complex logic blocks
- call out division-by-zero handling explicitly
- note where joins are optional vs required
