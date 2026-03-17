# Redshift Discovery Snippets (Datashare Compatible)

These queries are optimized for Redshift environments using Datashares. They use `SVV_ALL_*` system views to ensure visibility across both local and shared databases.

## 📚 AWS Documentation References
- [SVV_ALL_COLUMNS](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_ALL_COLUMNS.html)
- [SVV_ALL_TABLES](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_ALL_TABLES.html)
- [SVV_ALL_SCHEMAS](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_ALL_SCHEMAS.html)
- [SVV System Views Overview](https://docs.aws.amazon.com/redshift/latest/dg/svv_views.html)
- [Redshift Datashares](https://docs.aws.amazon.com/redshift/latest/dg/datashare-overview.html)

## 🔑 Key Concept: SVV_ALL_* vs SVV_*

| View Type | Scope | Use Case |
|-----------|-------|----------|
| `SVV_TABLES` / `SVV_COLUMNS` | **Local Database Only** | Checking tables physically created in your current DB. |
| `SVV_ALL_TABLES` / `SVV_ALL_COLUMNS` | **Local + Datashares** | **Discovery.** Finding tables in `gbos`, `ods`, or other shared schemas. |

---

## 🔍 1. Find a Table by Name (Fuzzy Search)
Search for a table across all connected databases and schemas.

**Reference:** [SVV_ALL_TABLES](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_ALL_TABLES.html)

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

## 🔎 2. Find a Column by Name
Find every table that contains a specific column. Useful for tracing lineage or finding join keys.

**Reference:** [SVV_ALL_COLUMNS](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_ALL_COLUMNS.html)

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

## 📋 3. Get Full Table Definition
List all columns, data types, and order for a specific table.

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

## 🔗 4. Find Tables Containing Multiple Columns (Join Candidates)
Find tables that contain *both* Column A and Column B. Great for finding link tables or verifying schema assumptions.

```sql
SELECT 
    database_name,
    schema_name,
    table_name
FROM svv_all_columns
WHERE column_name IN ('column_a', 'column_b')
GROUP BY 1, 2, 3
HAVING COUNT(DISTINCT column_name) = 2 -- Must match number of columns in list
ORDER BY 1, 2, 3;
```

## 📂 5. List All Schemas in a Database
See what schemas are available in a specific database (e.g., `gbos_db`).

**Reference:** [SVV_ALL_SCHEMAS](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_ALL_SCHEMAS.html)

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

## 📊 6. Table Stats & Row Counts (Local Only)
*Note: `svv_table_info` only works for local tables. For datashares, you must query the table directly.*

**Reference:** [SVV_TABLE_INFO](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_TABLE_INFO.html)

```sql
-- Only works for local tables
SELECT 
    schema as schema_name, 
    table as table_name, 
    tbl_rows as row_count, 
    size as size_mb 
FROM svv_table_info
ORDER BY size DESC;
```

## 🤝 7. List Available Datashares
See what external data is available to you via Datashares.

**Reference:** [SVV_DATASHARES](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_DATASHARES.html)

```sql
SELECT 
    share_name,
    share_owner,
    source_database,
    consumer_database
FROM pg_catalog.svv_datashares
ORDER BY share_name;
```

## 📦 8. List Objects in a Datashare
See exactly what tables and schemas are inside a specific datashare.

**Reference:** [SVV_DATASHARE_OBJECTS](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_DATASHARE_OBJECTS.html)

```sql
SELECT 
    share_name,
    object_type,
    object_name
FROM pg_catalog.svv_datashare_objects
WHERE share_name = 'your_share_name' -- Optional filter
ORDER BY share_name, object_type, object_name;
```

## 🔐 9. Check Table Permissions (Who can do what?)
See exactly which users or roles have SELECT, INSERT, etc. privileges on a table. Works for both local and shared tables.

**Reference:** [SVV_RELATION_PRIVILEGES](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_RELATION_PRIVILEGES.html)

```sql
SELECT 
    namespace_name as schema_name,
    relation_name as table_name,
    privilege_type,
    identity_name as grantee,
    identity_type -- 'user' or 'role'
FROM pg_catalog.svv_relation_privileges
WHERE relation_name = 'your_table_name'
ORDER BY schema_name, table_name;
```

## 👤 10. Check User Roles & Grants
See which roles a user belongs to. Useful for debugging "why can't I see this table?" (often due to missing role).

**Reference:** [SVV_USER_GRANTS](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_USER_GRANTS.html)

```sql
SELECT 
    user_name,
    role_name,
    admin_option
FROM pg_catalog.svv_user_grants
WHERE user_name ILIKE '%your_username%'
ORDER BY user_name, role_name;
```

## 👑 11. Check Database & Table Ownership
*   **Databases:** See all connected databases (local & shared) and their owners.
*   **Local Tables:** See owners of tables in the current database.

**References:** [SVV_REDSHIFT_DATABASES](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_REDSHIFT_DATABASES.html) | [PG_TABLES](https://docs.aws.amazon.com/redshift/latest/dg/r_PG_TABLES.html)

```sql
-- 1. List all databases (Local + Shared)
SELECT 
    database_name,
    database_owner,
    database_type -- 'local' or 'shared'
FROM pg_catalog.svv_redshift_databases
ORDER BY database_name;

-- 2. List Local Table Owners (Does not show Datashare tables)
SELECT 
    schemaname, 
    tablename, 
    tableowner 
FROM pg_catalog.pg_tables 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename;
```


