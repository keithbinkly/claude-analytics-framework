<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/knowledge-base/redshift-discovery-snippets.md
-->

> CAF migration note: this is a curated CAF copy of the discovery snippets most useful for pipeline work. Use this first, then fall back to the fuller `dbt-agent` version if needed.

# Redshift Discovery Snippets

Queries and patterns for Redshift discovery work, especially in environments that use datashares.

## Datashare Rule

Prefer `SVV_ALL_*` views during discovery because they see local and shared objects.

| View family | Scope | Best use |
|-------------|-------|----------|
| `SVV_TABLES`, `SVV_COLUMNS` | Local DB only | Local physical tables |
| `SVV_ALL_TABLES`, `SVV_ALL_COLUMNS` | Local + shared | Discovery and search |

## Find Table By Name

```sql
SELECT
    database_name,
    schema_name,
    table_name,
    table_type
FROM svv_all_tables
WHERE table_name ILIKE '%partial_table_name%'
ORDER BY database_name, schema_name, table_name;
```

## Find Column By Name

```sql
SELECT
    database_name,
    schema_name,
    table_name,
    column_name,
    data_type,
    ordinal_position
FROM svv_all_columns
WHERE column_name ILIKE '%column_name%'
ORDER BY database_name, schema_name, table_name;
```

## Get Full Table Definition

```sql
SELECT
    database_name,
    schema_name,
    table_name,
    column_name,
    data_type,
    is_nullable,
    ordinal_position
FROM svv_all_columns
WHERE schema_name = 'your_schema'
  AND table_name = 'your_table'
ORDER BY database_name, ordinal_position;
```

## Find Join-Candidate Tables

```sql
SELECT
    database_name,
    schema_name,
    table_name
FROM svv_all_columns
WHERE column_name IN ('column_a', 'column_b')
GROUP BY 1, 2, 3
HAVING COUNT(DISTINCT column_name) = 2
ORDER BY 1, 2, 3;
```

## List Schemas In A Database

```sql
SELECT
    database_name,
    schema_name,
    schema_owner,
    schema_type
FROM svv_all_schemas
WHERE database_name ILIKE '%db_name%'
ORDER BY schema_name;
```

## Local Table Size And Row Counts

```sql
SELECT
    schema as schema_name,
    table as table_name,
    tbl_rows as row_count,
    size as size_mb
FROM svv_table_info
ORDER BY size DESC;
```

Use this only for local tables. For datashared objects, query the table directly.

## Check Datashares

```sql
SELECT
    share_name,
    share_owner,
    source_database,
    consumer_database
FROM pg_catalog.svv_datashares
ORDER BY share_name;
```

## List Datashare Objects

```sql
SELECT
    share_name,
    object_type,
    object_name
FROM pg_catalog.svv_datashare_objects
WHERE share_name = 'your_share_name'
ORDER BY share_name, object_type, object_name;
```

## Check Table Permissions

```sql
SELECT
    namespace_name as schema_name,
    relation_name as table_name,
    privilege_type,
    identity_name as grantee,
    identity_type
FROM pg_catalog.svv_relation_privileges
WHERE relation_name = 'your_table_name'
ORDER BY schema_name, table_name;
```

## Check User Roles

```sql
SELECT
    user_name,
    role_name,
    admin_option
FROM pg_catalog.svv_user_grants
WHERE user_name ILIKE '%your_username%'
ORDER BY user_name, role_name;
```

## Ownership Checks

```sql
SELECT
    database_name,
    database_owner,
    database_type
FROM pg_catalog.svv_redshift_databases
ORDER BY database_name;
```

```sql
SELECT
    schemaname,
    tablename,
    tableowner
FROM pg_catalog.pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename;
```
