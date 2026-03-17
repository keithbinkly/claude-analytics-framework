<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/knowledge-base/troubleshooting.md
-->

> analytics-workspace migration note: this is a curated analytics-workspace troubleshooting reference covering the highest-frequency dbt pipeline issues. Use this first, then fall back to the fuller `dbt-agent` troubleshooting guide for niche cases.

# Troubleshooting

## Redshift Table Materialization Rename Errors

Symptom:

```text
ERROR: relation "schema.model_name" does not exist (SQLSTATE 42P01)
Error executing materialization macro 'materialization_table_redshift'
```

Root cause:

Redshift table materialization can fail during temp-table rename and backup-table handling.

Preferred fix:

```sql
{{
    config(
        materialized='table',
        backup=false
    )
}}
```

Use especially when working on datashare-heavy clusters or permission-constrained environments.

## Redshift View Materialization Rename Errors

Symptom:

```text
ERROR: relation "schema.view_name" does not exist (SQLSTATE 42P01)
Error executing materialization macro 'materialization_view_redshift'
```

Preferred fix:

```sql
{{
    config(
        materialized='view',
        bind=false
    )
}}
```

This can avoid late-binding behavior that causes rename failures on some Redshift setups.

## Redshift Temp Table Collision

Symptom:

```text
Relation already exists (42P07)
dbt run failed for #int_model__dbt_tmp
```

Root cause:

An interrupted prior run left a session-scoped temp table alive in the pool.

Preferred fixes:

1. Run again with `--full-refresh` when safe.
2. Drop the temp table with a targeted macro when full refresh is too costly.
3. Avoid interrupting scoped runs unless necessary.

## Many-To-Many Join Duplicates

Symptoms:

- unique tests fail unexpectedly
- row counts jump after a join
- one business key produces multiple output rows

Root cause:

A mapping or history table has multiple rows per join key and multiplies the result set.

Preferred fixes:

- aggregate the right-hand side before joining
- validate cardinality with `COUNT(DISTINCT key)`
- add staging-level uniqueness tests for join keys

Redshift-friendly pattern:

```sql
SELECT
    verificationactivitykey,
    LISTAGG(verificationstatusreason, ', ')
        WITHIN GROUP (ORDER BY verificationstatusreason) AS verificationstatusreason
FROM some_mapping_table
GROUP BY 1
```

## History Table Fan-Out

Symptoms:

- current-state models show duplicate historical rows
- point-in-time logic silently joins to multiple revisions

Preferred fixes:

- constrain to the intended effective row
- rank revisions and keep one row per business key
- document whether the model wants current-state or historical-state semantics

## Incremental Unique-Key Failures

Symptoms:

- merge fails with duplicate-match or tuple-update errors
- incremental runs succeed on full refresh but fail incrementally

Preferred fixes:

- verify the configured `unique_key` is truly unique at the model grain
- de-duplicate upstream before merge
- switch to `delete+insert` when merge semantics are too strict for the source shape

## Working Rules

- Compile before running.
- Validate grain before blaming materialization.
- Prefer explicit filters over implied filtering through shared infrastructure joins.
- Use targeted QA checks instead of broad row-count-only comparisons.
