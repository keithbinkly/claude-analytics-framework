# Check Join Pattern

Look up how to join tables using the BaaS join registry.

## Usage
```
/check-join <source_table> <target_table>
```

## Examples
```
/check-join edw.fct_posted_transaction edw.dim_account
/check-join gbos.account edw.dim_account
/check-join gss_checkpayment.checksettlement gss_checkpayment.checksettlementtransaction
```

## Action

1. Load `knowledge/domains/dbt-pipelines/reference/baas-join-registry.yml`
2. Search for join pattern between specified tables
3. Return:
   - Join key columns
   - Join type (INNER/LEFT)
   - Frequency in production queries
   - Orphan risk flag

## Response Format

```
Join: {{ source }} → {{ target }}
Key: {{ source_column }} = {{ target_column }}
Type: {{ join_type }} ({{ frequency }} occurrences)
Orphan Risk: {{ yes/no }}
```

If no join found:
```
No documented join between {{ source }} and {{ target }}.
Check: joins_by_target in case relationship is reversed.
```

## Registry Location
- BaaS: `knowledge/domains/dbt-pipelines/reference/baas-join-registry.yml`
- Universal: `knowledge/domains/dbt-pipelines/reference/join-registry.yml`
