---
name: dbt-jinja-sql-optimizer
version: 1.0.0
description: |
  Comprehensive Jinja templating and SQL optimization for dbt models. Master macros, filters, control flow,
  and utility packages (dbt-utils, codegen) to generate cleaner, more maintainable SQL. Covers dynamic column
  selection, environment-specific logic, SQL generation patterns, and best practices.

tags: [jinja, macros, dbt, sql-generation, dbt-utils, codegen, templates]
entry_point: true

triggers:
  - "jinja macro"
  - "optimize jinja"
  - "dbt macro"
  - "dynamic sql"
  - "sql generation"
  - "dbt-utils"
  - "codegen"
  - "template sql"

capabilities:
  - write_jinja_macros
  - optimize_sql_templates
  - use_dbt_utils_macros
  - generate_dynamic_columns
  - create_generic_tests
  - refactor_repetitive_sql
  - implement_environment_logic
  - generate_surrogate_keys
  - create_date_spines
  - optimize_union_operations

progressive_loading:
  always_load:
    - SKILL.md
  on_demand:
    - references/jinja_basics.md
    - references/dbt_functions.md
    - references/advanced_jinja.md
    - references/utility_packages.md
    - references/sql_generation.md
    - references/testing.md
    - references/examples.md
---

# Jinja SQL Optimizer Skill

## Purpose
Transform repetitive SQL into clean, maintainable dbt models using Jinja templating, macros, and utility packages. Eliminate code duplication, enable dynamic SQL generation, and follow dbt best practices.

## Core Philosophy
**DRY (Don't Repeat Yourself) meets SQL.** If you're copying SQL patterns, create a macro. If you're hardcoding column lists, use dynamic generation.

---

## Quick Decision Tree

### "When should I use Jinja vs plain SQL?"

```
START
  ↓
Do you have repetitive SQL patterns across models?
  ↓ YES → Create a macro
  |       → See: Macro Patterns below
  ↓ NO
  ↓
Do you need environment-specific logic (dev/prod)?
  ↓ YES → Use target variable & conditionals
  |       → See: Environment Logic below
  ↓ NO
  ↓
Do you need dynamic column selection?
  ↓ YES → Use loops + get_column_values
  |       → See: Dynamic Columns below
  ↓ NO
  ↓
Does dbt-utils already solve this?
  ↓ YES → Use existing macro
          → See: dbt-utils Quick Reference below
```

---

## Essential Jinja Syntax

### 1. Three Delimiters

```sql
{# Comments - documentation only #}

{% ... %}  -- Statements: control flow, no output
           -- if/for/set/macro definitions

{{ ... }}  -- Expressions: output values
           -- ref(), source(), variables, macro calls
```

### 2. Variable Assignment

```sql
-- Set variables at top of model
{% set payment_methods = ["credit_card", "paypal", "bank_transfer"] %}
{% set start_date = "2024-01-01" %}

-- Use in SQL
WHERE payment_method IN (
  {%- for method in payment_methods %}
    '{{ method }}'{% if not loop.last %},{% endif %}
  {%- endfor %}
)
```

### 3. Control Flow

```sql
{% if target.name == 'prod' %}
    -- Production-only logic
    WHERE is_deleted = FALSE
{% elif target.name == 'dev' %}
    -- Development sampling
    LIMIT 1000
{% else %}
    -- Default
{% endif %}
```

### 4. Loops

```sql
-- Basic loop
{% for column in columns %}
    {{ column }}{% if not loop.last %},{% endif %}
{% endfor %}

-- Loop properties
loop.first   -- True on first iteration
loop.last    -- True on last iteration
loop.index   -- Current iteration (1-indexed)
```

### 5. Whitespace Control

```sql
-- Strip whitespace with minus sign
{%- for item in items -%}
    {{ item }}
{%- endfor -%}

-- Keeps compiled SQL clean
```

---

## Common Patterns

### Pattern 1: Dynamic Column Selection

**Problem**: Hardcoded column lists become outdated

```sql
-- ❌ BAD: Hardcoded
SELECT
    user_id,
    email,
    first_name,
    last_name
FROM {{ ref('users') }}
```

**Solution**: Use dbt_utils.star() or get_column_values

```sql
-- ✅ GOOD: Dynamic
{% set exclude_cols = ['_fivetran_synced', '_dbt_source_relation'] %}

SELECT
    {{ dbt_utils.star(
        from=ref('users'),
        except=exclude_cols
    ) }}
FROM {{ ref('users') }}
```

### Pattern 2: Pivot Operations

**Problem**: Need to pivot dynamic values into columns

```sql
-- Get unique values
{% set payment_methods = dbt_utils.get_column_values(
    table=ref('payments'),
    column='payment_method'
) %}

-- Generate pivot
SELECT
    order_id,
    {{ dbt_utils.pivot(
        column='payment_method',
        values=payment_methods,
        agg='sum',
        then_value='amount',
        prefix='total_',
        suffix='_amount'
    ) }}
FROM {{ ref('payments') }}
GROUP BY 1
```

### Pattern 3: Union Multiple Tables

**Problem**: Union many similar tables with different columns

```sql
-- ❌ BAD: Manual UNION ALL
SELECT * FROM table1
UNION ALL
SELECT * FROM table2
-- ... repeat 20 times

-- ✅ GOOD: Dynamic union
{% set tables = dbt_utils.get_relations_by_pattern(
    schema_pattern='raw_data',
    table_pattern='events_%'
) %}

{{ dbt_utils.union_relations(
    relations=tables,
    exclude=['_loaded_at']
) }}
```

### Pattern 4: Generate Surrogate Keys

```sql
-- Create hash-based unique key
SELECT
    {{ dbt_utils.generate_surrogate_key([
        'user_id',
        'order_id',
        'timestamp'
    ]) }} as unique_key,
    *
FROM {{ ref('orders') }}
```

### Pattern 5: Date Spine

**Problem**: Need continuous date series

```sql
-- Generate all dates in range
{{ dbt_utils.date_spine(
    datepart="day",
    start_date="cast('2024-01-01' as date)",
    end_date="cast('2024-12-31' as date)"
) }}
```

### Pattern 6: Safe Math Operations

```sql
-- Avoid divide-by-zero errors
SELECT
    {{ dbt_utils.safe_divide('revenue', 'orders') }} as avg_order_value,
    {{ dbt_utils.safe_add(['col_a', 'col_b', 'col_c']) }} as total
FROM {{ ref('metrics') }}
```

---

## Creating Macros

### Basic Macro Structure

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    ({{ column_name }} / 100.0)::numeric(16, {{ precision }})
{% endmacro %}

-- Usage in model:
SELECT
    {{ cents_to_dollars('amount_cents') }} as amount_dollars
FROM {{ ref('payments') }}
```

### Macro with Conditional Logic

```sql
{% macro get_date_column() %}
    {% if target.name == 'prod' %}
        created_at
    {% else %}
        cast(created_at as date)  -- Faster for dev
    {% endif %}
{% endmacro %}
```

### Query-Returning Macro

```sql
{% macro get_max_timestamp(table, column) %}
    {% set query %}
        SELECT MAX({{ column }}) FROM {{ table }}
    {% endset %}

    {% set result = run_query(query) %}
    {% if execute %}
        {% set max_value = result.columns[0][0] %}
        {{ return(max_value) }}
    {% endif %}
{% endmacro %}

-- Usage:
{% set last_updated = get_max_timestamp(ref('source_table'), 'updated_at') %}
```

---

## dbt-utils Quick Reference

### Introspective Macros (Query Metadata)

```sql
-- Get unique column values
{% set statuses = dbt_utils.get_column_values(
    table=ref('orders'),
    column='status'
) %}

-- Get filtered columns
{% set numeric_cols = dbt_utils.get_filtered_columns_in_relation(
    from=ref('metrics'),
    except=['id', 'created_at']
) %}

-- Get relations by pattern
{% set staging_tables = dbt_utils.get_relations_by_pattern(
    schema_pattern='staging',
    table_pattern='stg_%'
) %}
```

### SQL Generators

```sql
-- Deduplicate rows
{{ dbt_utils.deduplicate(
    relation=ref('raw_events'),
    partition_by='user_id',
    order_by='timestamp desc'
) }}

-- Group by 1,2,3 shorthand
SELECT col1, col2, col3, SUM(amount)
FROM {{ ref('data') }}
{{ dbt_utils.group_by(n=3) }}

-- Unpivot wide to long
{{ dbt_utils.unpivot(
    relation=ref('wide_table'),
    cast_to='varchar',
    exclude=['id', 'created_at'],
    field_name='metric_name',
    value_name='metric_value'
) }}
```

### Generic Tests

```sql
# schema.yml
models:
  - name: orders
    tests:
      # Equal row counts
      - dbt_utils.equal_rowcount:
          compare_model: ref('backup_orders')

      # Expression validation
      - dbt_utils.expression_is_true:
          expression: "total >= subtotal"

      # Recency check
      - dbt_utils.recency:
          datepart: day
          field: created_at
          interval: 1

      # Sequential values
      - dbt_utils.sequential_values:
          interval: 1
          column_name: id
```

---

## codegen Quick Reference

### Generate Source YAML

```bash
# Run as operation
dbt run-operation generate_source --args '{
  "schema_name": "raw_jaffle_shop",
  "generate_columns": true,
  "include_descriptions": true
}'
```

### Generate Base Model SQL

```bash
dbt run-operation generate_base_model --args '{
  "source_name": "raw_jaffle_shop",
  "table_name": "customers",
  "materialized": "view"
}'
```

### Generate Model YAML

```bash
dbt run-operation generate_model_yaml --args '{
  "model_names": ["customers", "orders"]
}'
```

---

## Best Practices

### 1. **Favor Readability Over Cleverness**

```sql
-- ✅ GOOD: Clear and obvious
{% set payment_methods = ["credit_card", "paypal"] %}

SELECT
    order_id,
    {% for method in payment_methods %}
    SUM(CASE WHEN payment_method = '{{ method }}'
        THEN amount ELSE 0 END) as {{ method }}_total
    {% if not loop.last %},{% endif %}
    {% endfor %}
FROM {{ ref('payments') }}

-- ❌ BAD: Too clever, hard to debug
{{ generate_payment_aggregates(get_all_methods()) }}
```

### 2. **Set Variables at Top**

```sql
-- ✅ GOOD: Variables declared upfront
{% set lookback_days = 30 %}
{% set min_amount = 100 %}

SELECT *
FROM {{ ref('orders') }}
WHERE created_at > CURRENT_DATE - {{ lookback_days }}
  AND amount > {{ min_amount }}
```

### 3. **Use dbt-utils Before Writing Custom**

```sql
-- ❌ BAD: Reinventing the wheel
{% macro my_safe_divide(a, b) %}
    CASE WHEN {{ b }} = 0 THEN NULL
         ELSE {{ a }} / {{ b }}
    END
{% endmacro %}

-- ✅ GOOD: Use existing
{{ dbt_utils.safe_divide(numerator, denominator) }}
```

### 4. **Comment Complex Jinja**

```sql
{#
  This macro generates a CASE statement for each payment method
  to calculate total amounts by method. It dynamically queries
  the payments table to get all active payment methods.
#}
{% macro calculate_payment_totals() %}
    ...
{% endmacro %}
```

### 5. **Test Macro Output**

```bash
# Compile to see generated SQL
dbt compile --select model_name

# Check: target/compiled/project/models/model_name.sql
```

---

## Environment-Specific Patterns

### Development Sampling

```sql
SELECT *
FROM {{ ref('large_fact_table') }}
WHERE 1=1
{% if target.name == 'dev' %}
    AND created_at >= CURRENT_DATE - 7  -- Last week only
    LIMIT 10000
{% endif %}
```

### Schema Overrides

```sql
{% if target.name == 'dev' %}
    {% set schema_suffix = '_dev' %}
{% else %}
    {% set schema_suffix = '' %}
{% endif %}

SELECT *
FROM my_schema{{ schema_suffix }}.my_table
```

### Full Refresh Logic

```sql
{% if var('full_refresh', false) %}
    -- Rebuild from scratch
    DROP TABLE IF EXISTS {{ this }};
{% endif %}

SELECT *
FROM {{ ref('source') }}
```

---

## Debugging Tips

### 1. Use log() Function

```sql
{% set my_var = "test" %}
{{ log("Debug: my_var = " ~ my_var, info=True) }}
```

### 2. Check Compiled SQL

```bash
# Always verify generated SQL
dbt compile --select model_name
cat target/compiled/project_name/models/model_name.sql
```

### 3. Use --debug Flag

```bash
dbt run --select model_name --debug
# Shows full Jinja compilation process
```

### 4. Test Incrementally

```sql
-- Comment out complex logic, test piece by piece
-- {% for item in items %}
SELECT '{{ item }}' as test_value
-- {% endfor %}
```

---

## Common Anti-Patterns to Avoid

### ❌ Don't: Over-Abstract Everything

```sql
-- Too many layers of macros = hard to debug
{{ super_macro(outer_macro(inner_macro(data))) }}
```

### ❌ Don't: Inline Complex Logic

```sql
-- Hard to read
WHERE date = {{ dbt_utils.get_single_value("SELECT MAX(date) FROM ...") }}
```

### ❌ Don't: Forget to Quote Strings

```sql
-- ❌ WRONG: Jinja looks for variable named credit_card
{{ my_macro(credit_card) }}

-- ✅ CORRECT: Pass string literal
{{ my_macro('credit_card') }}
```

### ❌ Don't: Use SELECT * with star() Macro

```sql
-- ❌ WRONG: Redundant
SELECT {{ dbt_utils.star(ref('table')) }}

-- ✅ CORRECT: Just use star macro
{{ dbt_utils.star(ref('table')) }}
```

---

## Progressive Loading Resources

This skill uses progressive loading for efficiency:

- **SKILL.md** (this file): Always loaded - quick reference and patterns
- **references/jinja_basics.md**: On-demand - detailed Jinja syntax
- **references/dbt_functions.md**: On-demand - all dbt Jinja functions
- **references/advanced_jinja.md**: On-demand - statement blocks, adapters
- **references/utility_packages.md**: On-demand - complete dbt-utils/codegen docs
- **references/sql_generation.md**: On-demand - SQL generation patterns
- **references/testing.md**: On-demand - generic/singular test patterns
- **references/examples.md**: On-demand - real-world examples

Use the command `load references/<file>.md` to access detailed documentation.

---

## Integration with Pipeline Migration

This skill is valuable during pipeline migration for:

1. **Refactoring Legacy SQL** - Convert procedural SQL to declarative dbt
2. **Eliminating Duplication** - Extract repeated logic into macros
3. **Dynamic Column Handling** - Adapt to schema changes
4. **Environment Safety** - Dev/prod logic separation
5. **Testing** - Generate validation tests quickly

Pair with `dbt-migration` skill for complete migration workflow.

---

## Quick Wins

Start with these high-impact patterns:

1. **Replace SELECT * → dbt_utils.star()** with exclusions
2. **Extract repeated CASE statements → macro**
3. **Dynamic pivots → dbt_utils.pivot()**
4. **Manual unions → dbt_utils.union_relations()**
5. **Hardcoded surrogate keys → dbt_utils.generate_surrogate_key()**

---

**Generated**: 2025-11-03
**Tool**: Skill Seekers + Manual Compression
**Sources**:
- dbt official documentation (docs.getdbt.com)
- dbt-utils package (hub.getdbt.com/dbt-labs/dbt_utils)
- dbt-codegen package (hub.getdbt.com/dbt-labs/codegen)
- Datacoves Jinja cheat sheet
