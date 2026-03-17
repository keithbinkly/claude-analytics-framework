# Type Casting & UNION Gotchas (Redshift)

**Purpose**: Prevent type mismatch errors that cause runtime failures despite successful compilation

---

## The Core Problem

**Symptom**: `ERROR: UNION types [type1] and [type2] cannot be matched`

**Why It's Sneaky**: dbt compilation succeeds, but Redshift runtime fails

---

## Common UNION Type Mismatches

### 1. Integer Literals vs VARCHAR Columns

**❌ WRONG**:
```sql
SELECT auth_response, ... FROM auth_table  -- auth_response is VARCHAR
UNION ALL
SELECT 1000, ... FROM posted_table  -- 1000 is INTEGER literal
```

**✅ CORRECT**:
```sql
SELECT auth_response, ... FROM auth_table
UNION ALL
SELECT '1000'::VARCHAR, ... FROM posted_table  -- Explicit cast to match
```

**Lesson**: When hardcoding values in UNION, **always cast to match the other CTE's type**

---

### 2. NULL with Different Implicit Types

**❌ WRONG**:
```sql
SELECT merchant, 0 AS rank, ... FROM merchants
UNION ALL
SELECT merchant, rank_value, ... FROM rankings  -- rank_value is BIGINT
```

**Problem**: `0` is INTEGER, `rank_value` is BIGINT, UNION may fail

**✅ CORRECT**:
```sql
SELECT merchant, NULL::INT AS rank, ... FROM merchants
UNION ALL
SELECT merchant, rank_value::INT, ... FROM rankings
```

**Lesson**: Use `NULL::TYPE` instead of arbitrary default values (0, -1, etc.) when semantic meaning is "no value"

---

### 3. TIMESTAMP WITH TIME ZONE vs TIMESTAMP

**❌ WRONG**:
```sql
SELECT CONVERT_TIMEZONE('UTC', 'America/Los_Angeles', CURRENT_TIMESTAMP) AS update_time
```

**Problem**: `CURRENT_TIMESTAMP` returns `TIMESTAMP WITH TIME ZONE`, but `CONVERT_TIMEZONE()` expects `TIMESTAMP`

**✅ CORRECT**:
```sql
SELECT CONVERT_TIMEZONE('America/Los_Angeles', CURRENT_TIMESTAMP::TIMESTAMP) AS update_time
```

**Lesson**: Redshift timestamp functions are picky about WITH/WITHOUT time zone

---

### 4. Implicit vs Explicit Type Inference

**❌ RISKY**:
```sql
CASE 
  WHEN condition THEN 'Daily'
  ELSE NULL  -- What type is this NULL?
END AS time_period
```

**✅ SAFER**:
```sql
CASE 
  WHEN condition THEN 'Daily'
  ELSE NULL::VARCHAR
END AS time_period
```

**Lesson**: Be explicit with NULL types in CASE statements

---

## Pre-Flight Type Check Query

**Run this BEFORE executing models with UNION**:

```sql
-- Check types in each CTE that will be UNIONed
WITH cte_1 AS (
    SELECT column_a, column_b, column_c
    FROM {{ ref('model_1') }}
    LIMIT 1
),
cte_2 AS (
    SELECT column_a, column_b, column_c
    FROM {{ ref('model_2') }}
    LIMIT 1
)
SELECT 'CTE_1' AS source, pg_typeof(column_a) AS a_type, pg_typeof(column_b) AS b_type, pg_typeof(column_c) AS c_type FROM cte_1
UNION ALL
SELECT 'CTE_2', pg_typeof(column_a), pg_typeof(column_b), pg_typeof(column_c) FROM cte_2;
```

**Expected**: Same type for each column across all rows

---

## Redshift Type Hierarchy (for UNION)

When Redshift encounters mixed types in UNION, it tries implicit conversion following this hierarchy (simplified):

1. **Numeric**: SMALLINT → INTEGER → BIGINT → DECIMAL → REAL → DOUBLE PRECISION
2. **String**: CHAR → VARCHAR
3. **Date/Time**: DATE → TIMESTAMP → TIMESTAMP WITH TIME ZONE

**Problem**: If conversion isn't straightforward, UNION fails

**Solution**: **Always cast explicitly** instead of relying on implicit conversion

---

## Common Casting Patterns

### String to Number
```sql
'12345'::INTEGER
'12345.67'::DECIMAL(10,2)
```

### Number to String
```sql
1000::VARCHAR
1000::VARCHAR(10)  -- With length limit
```

### Date/Time Conversions
```sql
CURRENT_DATE::TIMESTAMP  -- Date to timestamp
CURRENT_TIMESTAMP::TIMESTAMP  -- Remove time zone
CURRENT_TIMESTAMP::DATE  -- Truncate to date
'2025-07-01'::DATE  -- String to date
```

### NULL with Type
```sql
NULL::INTEGER
NULL::VARCHAR
NULL::TIMESTAMP
NULL::DECIMAL(10,2)
```

### Boolean Casting (Redshift)
**❌ RISKY**:
```sql
is_active::VARCHAR  -- Can fail in views/semantic layer with "invalid input syntax"
```

**✅ SAFER**:
```sql
CASE WHEN is_active THEN 'true' ELSE 'false' END
```

**Lesson**: Redshift boolean casting in views is strict. Use CASE WHEN for explicit string conversion.

---

## Debugging Workflow

**When you get "UNION types cannot be matched" error:**

1. **Identify the UNION location** in compiled SQL (`target/compiled/`)
2. **Extract each CTE** involved in the UNION
3. **Run type check query** (see above) on sample rows
4. **Find the mismatched column(s)**
5. **Add explicit cast** to make types identical
6. **Re-run model**

**Time Savings**: This workflow reduces debugging from 20 min → 5 min

---

## Type-Safe Model Template

```sql
-- models/marts/template_with_union.sql
{{ config(materialized='table') }}

WITH 

source_a AS (
    SELECT 
        column_1::VARCHAR AS col_1,  -- Explicit cast
        column_2::INTEGER AS col_2,
        column_3::DECIMAL(10,2) AS col_3,
        column_4::TIMESTAMP AS col_4
    FROM {{ ref('source_a') }}
),

source_b AS (
    SELECT 
        column_1::VARCHAR AS col_1,  -- Match source_a types exactly
        column_2::INTEGER AS col_2,
        column_3::DECIMAL(10,2) AS col_3,
        column_4::TIMESTAMP AS col_4
    FROM {{ ref('source_b') }}
),

combined AS (
    SELECT * FROM source_a
    UNION ALL
    SELECT * FROM source_b  -- Types guaranteed to match
)

SELECT * FROM combined
```

**Pattern**: Cast at CTE level, not in UNION

---

## Window Function Gotchas

### ROW_NUMBER() Returns BIGINT
```sql
-- If joining or UNIONing with INTEGER columns
ROW_NUMBER() OVER (...)::INTEGER  -- Cast if needed
```

### DENSE_RANK() Also Returns BIGINT
```sql
DENSE_RANK() OVER (...)::INTEGER
```

**Lesson**: Window functions return BIGINT, may need casting for UNION or joins

---

## Float vs Decimal

**For Money/Amounts**:
```sql
SUM(amount)::DECIMAL(15,2)  -- Precise
```

**For Ratios/Percentages**:
```sql
(decline_amt / attempt_amt)::FLOAT  -- OK for ratios
ROUND(100.0 * decline_amt / attempt_amt, 2)::FLOAT  -- Percentage
```

**Lesson**: Use DECIMAL for money, FLOAT for calculated metrics

---

## Quick Reference: Redshift Types

| Type | Example | Cast Syntax | Notes |
|------|---------|-------------|-------|
| INTEGER | 1000 | `value::INTEGER` | 32-bit signed |
| BIGINT | 1000000000 | `value::BIGINT` | 64-bit signed, window functions return this |
| VARCHAR | 'text' | `value::VARCHAR` | Variable length string |
| VARCHAR(N) | 'text' | `value::VARCHAR(10)` | Max N characters |
| DECIMAL(P,S) | 123.45 | `value::DECIMAL(10,2)` | Precision P, Scale S |
| FLOAT | 123.45 | `value::FLOAT` | Approximate, 8-byte |
| DATE | '2025-07-01' | `value::DATE` | Date only |
| TIMESTAMP | '2025-07-01 12:00:00' | `value::TIMESTAMP` | Date + time, no time zone |
| BOOLEAN | TRUE | `value::BOOLEAN` | True/False |

---

## Last Resort: Debug Compiled SQL

If type check query doesn't reveal the issue:

1. Find compiled SQL: `target/compiled/models/.../model_name.sql`
2. Copy entire query
3. Run in SQL client with `EXPLAIN` to see execution plan
4. Redshift error will show exact line number of type mismatch

---

## Last Updated
2025-10-09

**Maintenance**: Add new type gotchas as discovered
