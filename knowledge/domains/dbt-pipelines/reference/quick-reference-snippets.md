# 🚀 Quick Reference Snippets

**Purpose**: Copy-paste ready code patterns for common dbt development tasks  
**When to Use**: Need to quickly implement standard patterns without searching multiple files  
**Last Updated**: October 19, 2025

---

## 📋 Table of Contents

1. [Environment-Aware Filtering](#environment-aware-filtering)
2. [Incremental Configurations](#incremental-configurations)
3. [QA Validation Templates](#qa-validation-templates)
4. [Model Config Patterns](#model-config-patterns)
5. [Folder Placement Cheat Sheet](#folder-placement-cheat-sheet)
6. [Common Jinja Patterns](#common-jinja-patterns)

---

## 🌍 Environment-Aware Filtering

### Pattern 1: Basic Date Filter (Dev/CI: 6 months, Prod: Full)
```sql
{% if env_var('DBT_CLOUD_ENVIRONMENT_TYPE', 'development') in ('ci', 'continuous-integration', 'development') %}
    and createdate >= dateadd('month', -6, current_date)  -- Dev/CI: 6 months
{% else %}
    and createdate >= dateadd('year', -2, current_date)   -- Prod: 2 years (or full history)
{% endif %}
```

### Pattern 2: Using apply_date_filter() Macro
```sql
select
    transaction_uid,
    transaction_date,
    account_uid,
    amount
from {{ ref('stg_edw__fct_posted_transaction') }}
where 1=1
    {{ apply_date_filter('transaction_date') }}  -- Automatically handles env-aware filtering
    and transaction_status = 'POSTED'
```

### Pattern 3: Limit Rows in CI (Testing)
```sql
select
    *
from {{ ref('base_model') }}
where condition = true
{{ limit_ci() }}  -- Adds LIMIT 100 in CI environment
```

### Pattern 4: Month-End Only Filtering
```sql
select
    *
from {{ ref('source_model') }}
where 1=1
    {{ apply_month_end_filter('calendar_date') }}  -- Only month-end dates
```

---

## ⚡ Incremental Configurations

### Pattern 1: Basic Incremental (Merge Strategy)
```sql
{{ config(
    materialized='incremental',
    unique_key='transaction_uid',
    incremental_strategy='merge',
    on_schema_change='fail'
) }}

select
    transaction_uid,
    transaction_date,
    account_uid,
    amount,
    current_timestamp as _dbt_updated_at
from {{ ref('stg_source') }}
{% if is_incremental() %}
where transaction_date >= dateadd('day', -3, 
    (select max(transaction_date) from {{ this }}))
{% endif %}
```

### Pattern 2: Delete+Insert Strategy (Lookback Window)
```sql
{{ config(
    materialized='incremental',
    unique_key='account_uid',
    incremental_strategy='delete+insert',
    on_schema_change='fail'
) }}

select
    account_uid,
    balance_date,
    ending_balance,
    current_timestamp as _dbt_updated_at
from {{ ref('stg_account_balances') }}
{% if is_incremental() %}
where balance_date >= dateadd('day', -7,
    (select max(balance_date) from {{ this }}))
{% endif %}
```

### Pattern 3: Composite Unique Key (Multiple Columns)
```sql
{{ config(
    materialized='incremental',
    unique_key=['account_uid', 'calendar_date', 'product_uid'],
    incremental_strategy='merge',
    on_schema_change='fail'
) }}

select
    account_uid,
    calendar_date,
    product_uid,
    metric_value
from {{ ref('base_metrics') }}
{% if is_incremental() %}
where calendar_date >= dateadd('day', -30,
    (select max(calendar_date) from {{ this }}))
{% endif %}
```

---

## ✅ QA Validation Templates

### Template 1: Product-Level Metric Comparison
```sql
-- QA: Compare NEW vs LEGACY metrics by product
WITH new_metrics AS (
    select
        product,
        calendar_month,
        sum(metric_value) as total_value
    from {{ ref('new_model_name') }}
    group by 1, 2
),
legacy_metrics AS (
    select
        product,
        calendar_month,
        sum(case when metric_name = 'Target Metric Name' 
            then cy else 0 end) as total_value
    from {{ ref('stg_analytics__bia_edwkpi_fkm_master') }}
    where metric_name = 'Target Metric Name'
    group by 1, 2
)
select 
    coalesce(n.product, l.product) as product,
    coalesce(n.calendar_month, l.calendar_month) as month,
    n.total_value as new_value,
    l.total_value as legacy_value,
    n.total_value - l.total_value as variance,
    (n.total_value - l.total_value) / nullif(l.total_value, 0) * 100 as pct_variance,
    case 
        when abs((n.total_value - l.total_value) / nullif(l.total_value, 0) * 100) < 0.01 
        then '✅ PASS'
        else '❌ FAIL'
    end as status
from new_metrics n
full outer join legacy_metrics l 
    using (product, calendar_month)
order by product, month desc;
```

### Template 2: Time Series Trend Comparison
```sql
-- QA: Compare daily trends NEW vs LEGACY
WITH new_daily AS (
    select
        calendar_date,
        count(distinct account_uid) as active_accounts
    from {{ ref('new_model_name') }}
    group by 1
),
legacy_daily AS (
    select
        calendar_date,
        sum(case when metric_name = 'Active Accounts' 
            then cy else 0 end) as active_accounts
    from {{ ref('stg_analytics__bia_edwkpi_fkm_master') }}
    where metric_name = 'Active Accounts'
    group by 1
)
select
    coalesce(n.calendar_date, l.calendar_date) as date,
    n.active_accounts as new_count,
    l.active_accounts as legacy_count,
    (n.active_accounts - l.active_accounts) / nullif(l.active_accounts, 0) * 100 as pct_variance,
    case 
        when abs((n.active_accounts - l.active_accounts) / nullif(l.active_accounts, 0) * 100) < 0.01 
        then '✅ PASS'
        else '❌ FAIL'
    end as status
from new_daily n
full outer join legacy_daily l using (calendar_date)
where coalesce(n.calendar_date, l.calendar_date) >= dateadd('month', -3, current_date)
order by date desc;
```

### Template 3: Account-Level Sample Comparison
```sql
-- QA: Compare random sample of accounts NEW vs LEGACY
WITH sample_accounts AS (
    select distinct account_uid
    from {{ ref('new_model_name') }}
    order by random()
    limit 100
),
new_sample AS (
    select
        n.account_uid,
        n.metric_value
    from {{ ref('new_model_name') }} n
    inner join sample_accounts s using (account_uid)
),
legacy_sample AS (
    select
        l.account_uid,
        sum(case when l.metric_name = 'Target Metric' 
            then l.cy else 0 end) as metric_value
    from {{ ref('stg_analytics__bia_edwkpi_fkm_master') }} l
    inner join sample_accounts s using (account_uid)
    where l.metric_name = 'Target Metric'
    group by 1
)
select
    coalesce(n.account_uid, l.account_uid) as account_uid,
    n.metric_value as new_value,
    l.metric_value as legacy_value,
    (n.metric_value - l.metric_value) / nullif(l.metric_value, 0) * 100 as pct_variance,
    case 
        when abs((n.metric_value - l.metric_value) / nullif(l.metric_value, 0) * 100) < 0.01 
        then '✅ PASS'
        else '❌ FAIL'
    end as status
from new_sample n
full outer join legacy_sample l using (account_uid)
order by abs(pct_variance) desc;
```

### Template 4: Aggregation Level Comparison (Summary)
```sql
-- QA: Compare grand totals NEW vs LEGACY
WITH new_total AS (
    select
        'Grand Total' as level,
        sum(metric_value) as total_value,
        count(distinct account_uid) as account_count,
        count(*) as row_count
    from {{ ref('new_model_name') }}
),
legacy_total AS (
    select
        'Grand Total' as level,
        sum(case when metric_name = 'Target Metric' 
            then cy else 0 end) as total_value,
        count(distinct account_uid) as account_count,
        count(*) as row_count
    from {{ ref('stg_analytics__bia_edwkpi_fkm_master') }}
    where metric_name = 'Target Metric'
)
select
    n.level,
    n.total_value as new_total,
    l.total_value as legacy_total,
    n.total_value - l.total_value as value_variance,
    (n.total_value - l.total_value) / nullif(l.total_value, 0) * 100 as pct_variance,
    n.account_count as new_accounts,
    l.account_count as legacy_accounts,
    n.row_count as new_rows,
    l.row_count as legacy_rows,
    case 
        when abs((n.total_value - l.total_value) / nullif(l.total_value, 0) * 100) < 0.01 
        then '✅ PASS'
        else '❌ FAIL'
    end as status
from new_total n
cross join legacy_total l;
```

---

## 🔧 Model Config Patterns

### Pattern 1: Standard Intermediate Model
```sql
{{ config(
    materialized='table',
    tags=['intermediate', 'domain_name'],
    schema='intermediate'
) }}
```

### Pattern 2: Large Fact Table (Incremental)
```sql
{{ config(
    materialized='incremental',
    unique_key='unique_id',
    incremental_strategy='merge',
    on_schema_change='fail',
    tags=['fact', 'incremental'],
    schema='intermediate'
) }}
```

### Pattern 3: Mart Model (Analysis-Ready)
```sql
{{ config(
    materialized='table',
    tags=['mart', 'reporting'],
    schema='marts'
) }}
```

### Pattern 4: Report Model (Final Output)
```sql
{{ config(
    materialized='view',
    tags=['report', 'executive'],
    schema='reports'
) }}
```

### Pattern 5: Debug/Development Model (Ephemeral)
```sql
{{ config(
    materialized='ephemeral',
    tags=['debug']
) }}
```

---

## 📁 Folder Placement Cheat Sheet

```
┌─────────────────────────────────────────────────────────────────────────┐
│ PROJECT STRUCTURE                                                       │
└─────────────────────────────────────────────────────────────────────────┘

models/
├── staging/                          # Raw data, minimal transformation
│   ├── edw/                         # stg_edw__<table_name>
│   ├── ods/                         # stg_ods__<table_name>
│   └── analytics/                   # stg_analytics__<table_name>
│
├── intermediate/                     # Business logic, reusable
│   ├── wonderwall_kpi/              # int_wonderwall__<concept>
│   ├── transactions/                # int_transactions__<concept>
│   ├── accounts/                    # int_accounts__<concept>
│   └── baas_wonderwall_kpi/        # int_baas_<pipeline>__<concept>
│
├── marts/                           # Analysis-ready, denormalized
│   ├── wonderwall/                  # mrt_wonderwall__<purpose>
│   ├── ds_feature_store/            # Data science features
│   └── executive/                   # Executive dashboards
│
└── reports/                         # Final outputs, specific audiences
    ├── executive/                   # rpt_executive__<purpose>
    ├── operations/                  # rpt_operations__<purpose>
    └── finance/                     # rpt_finance__<purpose>

┌─────────────────────────────────────────────────────────────────────────┐
│ NAMING CONVENTIONS                                                      │
└─────────────────────────────────────────────────────────────────────────┘

Staging:       stg_<source>__<table>
               Example: stg_edw__fct_posted_transaction

Intermediate:  int_<domain>__<concept>
               Example: int_transactions__posted_enriched

Marts:         mrt_<domain>__<purpose>
               Example: mrt_wonderwall__at_a_glance

Reports:       rpt_<audience>__<purpose>
               Example: rpt_executive__monthly_summary

┌─────────────────────────────────────────────────────────────────────────┐
│ QUICK DECISION TREE                                                     │
└─────────────────────────────────────────────────────────────────────────┘

Is it a raw source?                     → staging/
Does it have business logic?            → intermediate/
Is it analysis-ready and wide?          → marts/
Is it for a specific audience/report?   → reports/
```

---

## 🎯 Common Jinja Patterns

### Pattern 1: Dynamic Column Selection
```sql
{% set columns = ['col1', 'col2', 'col3'] %}

select
    {% for col in columns %}
    {{ col }}{{ "," if not loop.last }}
    {% endfor %}
from source_table
```

### Pattern 2: Conditional Column (Target-Based)
```sql
select
    account_uid,
    transaction_date,
    {% if target.name == 'prod' %}
    encrypted_ssn,
    {% else %}
    'XXX-XX-XXXX' as encrypted_ssn,  -- Masked in dev/ci
    {% endif %}
    amount
from {{ ref('sensitive_data') }}
```

### Pattern 3: Union Multiple Sources
```sql
{% set sources = ['source_a', 'source_b', 'source_c'] %}

{% for source in sources %}
select
    '{{ source }}' as source_name,
    *
from {{ ref(source) }}
{{ "union all" if not loop.last }}
{% endfor %}
```

### Pattern 4: Generate Date Series
```sql
with date_spine as (
    {{ dbt_date.get_date_dimension('2020-01-01', 'current_date') }}
)

select
    date_day,
    date_week,
    date_month,
    date_year
from date_spine
```

### Pattern 5: Parameterized Filtering
```sql
{% set lookback_days = var('lookback_days', 30) %}

select
    *
from {{ ref('source') }}
where transaction_date >= dateadd('day', -{{ lookback_days }}, current_date)
```

### Pattern 6: Ref with Error Handling
```sql
{% set model_exists = execute and load_relation(ref('optional_model')) is not none %}

select
    a.*,
    {% if model_exists %}
    b.additional_field
    {% else %}
    null as additional_field
    {% endif %}
from {{ ref('base_model') }} a
{% if model_exists %}
left join {{ ref('optional_model') }} b
    on a.key = b.key
{% endif %}
```

---

## 🔍 Common Data Quality Checks

### Pattern 1: Null Check in dbt_expectations
```yaml
# schema.yml
version: 2

models:
  - name: model_name
    tests:
      - dbt_expectations.expect_column_values_to_not_be_null:
          column_name: "required_field"
```

### Pattern 2: Unique Combination Check
```yaml
# schema.yml
version: 2

models:
  - name: model_name
    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - account_uid
            - calendar_date
            - product_uid
```

### Pattern 3: Value Range Check
```yaml
# schema.yml
version: 2

models:
  - name: model_name
    columns:
      - name: percentage_field
        tests:
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 100
```

### Pattern 4: Row Count Comparison
```yaml
# schema.yml
version: 2

models:
  - name: model_name
    tests:
      - dbt_expectations.expect_table_row_count_to_be_between:
          min_value: 1000000  # At least 1M rows
          max_value: 100000000  # At most 100M rows
```

---

## 💡 Usage Tips

1. **Always copy the entire snippet** - Don't modify patterns unless necessary
2. **Update placeholder names**:
   - `new_model_name` → your actual model name
   - `Target Metric` → your actual metric name
   - `domain_name` → your actual domain (transactions, accounts, etc.)
3. **Test in development first** - Use `{{ limit_ci() }}` for quick validation
4. **Check QA templates** - Use Template 1-4 based on your validation needs
5. **Folder placement** - When in doubt, use the decision tree in the cheat sheet

---

## 📚 Related Resources

- **Full Migration Process**: `shared/reference/pipeline-build-playbook.md`
- **QA Methodology**: `shared/reference/qa-validation-checklist.md`
- **Folder Structure Details**: `shared/knowledge-base/folder-structure-and-naming.md`
- **Troubleshooting**: `shared/knowledge-base/troubleshooting.md`
- **Canonical Models**: `shared/knowledge-base/canonical-models-registry.md`

---

**Last Updated**: October 19, 2025  
**Maintained by**: dbt-agent framework  
**Feedback**: Add new patterns via session logs or direct contribution
