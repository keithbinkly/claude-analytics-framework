# Prevention Tests Registry

> **Purpose**: Catalog of dbt tests that prevent common failure modes identified through QA analysis.
> These tests encode lessons learned from production issues like the 99% suppression incident (GBOS Registration).

---

## Overview

Prevention tests are dbt tests designed to catch issues BEFORE they reach production. They complement standard data quality tests by explicitly checking for failure modes we've observed.

### Categories

1. **Volume Tests** - Detect unexpected data suppression
2. **Join Health Tests** - Catch orphan records and join failures
3. **Event Distribution Tests** - Ensure expected event types present
4. **Date Boundary Tests** - Validate date filter behavior
5. **Incremental Health Tests** - Prevent incremental strategy failures

---

## 1. Volume Tests

### Test: Row Count Within Expected Range

**Problem Prevented**: 99% data suppression (GBOS registration incident)

**Implementation**:
```yaml
# schema.yml
models:
  - name: int_transactions__posted
    tests:
      - dbt_utils.expression_is_true:
          expression: "count(*) >= 1000000"  # Minimum expected rows
          severity: error
          meta:
            prevention_category: volume
            incident_reference: GBOS-2025-10-30
```

**Custom Test**:
```sql
-- tests/generic/test_row_count_in_range.sql
{% test row_count_in_range(model, min_rows, max_rows=none) %}

with row_count as (
    select count(*) as cnt from {{ model }}
)
select cnt
from row_count
where cnt < {{ min_rows }}
{% if max_rows %}
   or cnt > {{ max_rows }}
{% endif %}

{% endtest %}
```

**Usage**:
```yaml
models:
  - name: int_transactions__posted
    tests:
      - row_count_in_range:
          min_rows: 1000000
          max_rows: 500000000
```

---

### Test: Volume Trace Multi-Stage

**Problem Prevented**: Filter suppression not detected until final output

**Implementation**:
```sql
-- tests/singular/test_volume_trace_transactions.sql
-- Validates row counts at each filter stage

{% set stages = [
    ('raw', 'stg_edw__fct_posted_transaction', none),
    ('date_filtered', 'stg_edw__fct_posted_transaction', "processor_business_dt >= '2020-01-01'"),
    ('status_filtered', 'int_transactions__posted_base', none),
    ('final', 'int_transactions__posted', none)
] %}

with stage_counts as (
    {% for stage_name, model, filter in stages %}
    select
        '{{ stage_name }}' as stage,
        count(*) as row_count
    from {{ ref(model) }}
    {% if filter %}where {{ filter }}{% endif %}
    {% if not loop.last %}union all{% endif %}
    {% endfor %}
),

stage_comparison as (
    select
        stage,
        row_count,
        lag(row_count) over (order by
            case stage
                when 'raw' then 1
                when 'date_filtered' then 2
                when 'status_filtered' then 3
                when 'final' then 4
            end
        ) as prev_row_count,
        100.0 * (row_count - lag(row_count) over (...)) /
            nullif(lag(row_count) over (...), 0) as pct_change
    from stage_counts
)

select *
from stage_comparison
where pct_change < -50  -- Alert if any stage loses >50% of rows
```

---

## 2. Join Health Tests

### Test: Join Success Rate

**Problem Prevented**: Orphan records from failed joins

**Implementation**:
```sql
-- tests/generic/test_join_success_rate.sql
{% test join_success_rate(model, left_column, right_model, right_column, min_rate=0.95) %}

with join_stats as (
    select
        count(*) as total_rows,
        count(r.{{ right_column }}) as matched_rows
    from {{ model }} l
    left join {{ ref(right_model) }} r
        on l.{{ left_column }} = r.{{ right_column }}
)

select *
from join_stats
where matched_rows::float / nullif(total_rows, 0) < {{ min_rate }}

{% endtest %}
```

**Usage**:
```yaml
models:
  - name: int_transactions__enriched
    tests:
      - join_success_rate:
          left_column: account_id
          right_model: dim_account
          right_column: account_id
          min_rate: 0.99
```

---

### Test: No Orphan Records

**Problem Prevented**: Records without required parent records

**Implementation**:
```yaml
models:
  - name: fct_transactions
    columns:
      - name: account_id
        tests:
          - relationships:
              to: ref('dim_account')
              field: account_id
              severity: error
              meta:
                prevention_category: join_health
```

---

## 3. Event Distribution Tests

### Test: Expected Event Types Present

**Problem Prevented**: Missing event types due to filter suppression

**Implementation**:
```sql
-- tests/generic/test_expected_values_present.sql
{% test expected_values_present(model, column, expected_values) %}

with expected as (
    {% for value in expected_values %}
    select '{{ value }}' as expected_value
    {% if not loop.last %}union all{% endif %}
    {% endfor %}
),

actual as (
    select distinct {{ column }} as actual_value
    from {{ model }}
)

select e.expected_value
from expected e
left join actual a on e.expected_value = a.actual_value
where a.actual_value is null

{% endtest %}
```

**Usage**:
```yaml
models:
  - name: int_transactions__posted
    tests:
      - expected_values_present:
          column: transaction_type
          expected_values: ['PURCHASE', 'REFUND', 'AUTHORIZATION', 'VOID']
```

---

### Test: Event Distribution Within Bounds

**Problem Prevented**: Skewed distribution indicating filter issues

**Implementation**:
```sql
-- tests/singular/test_event_distribution.sql
with distribution as (
    select
        transaction_type,
        count(*) as cnt,
        100.0 * count(*) / sum(count(*)) over () as pct
    from {{ ref('int_transactions__posted') }}
    group by 1
)

select *
from distribution
where
    (transaction_type = 'PURCHASE' and pct < 60)  -- Expected: 60-80%
    or (transaction_type = 'REFUND' and pct > 15)  -- Expected: 5-15%
    or (transaction_type = 'VOID' and pct > 5)     -- Expected: 1-5%
```

---

## 4. Date Boundary Tests

### Test: Date Range Consistency

**Problem Prevented**: Date filter excluding expected data

**Implementation**:
```sql
-- tests/generic/test_date_range_valid.sql
{% test date_range_valid(model, date_column, min_date='2020-01-01', max_days_lag=3) %}

select *
from (
    select
        min({{ date_column }}) as earliest_date,
        max({{ date_column }}) as latest_date,
        current_date - {{ max_days_lag }} as expected_max
    from {{ model }}
) validation
where
    earliest_date > '{{ min_date }}'::date  -- Too recent
    or latest_date < expected_max            -- Too stale

{% endtest %}
```

**Usage**:
```yaml
models:
  - name: int_transactions__posted
    tests:
      - date_range_valid:
          date_column: processor_business_dt
          min_date: '2020-01-01'
          max_days_lag: 3
```

---

### Test: No Future Dates

**Problem Prevented**: Invalid future-dated records

**Implementation**:
```yaml
models:
  - name: fct_transactions
    columns:
      - name: transaction_date
        tests:
          - dbt_utils.expression_is_true:
              expression: "<= current_date"
              severity: error
```

---

## 5. Incremental Health Tests

### Test: No Duplicates After Incremental

**Problem Prevented**: Incremental strategy creating duplicates

**Implementation**:
```yaml
models:
  - name: int_transactions__posted
    columns:
      - name: transaction_uid
        tests:
          - unique:
              severity: error
              meta:
                prevention_category: incremental_health
```

---

### Test: Incremental Lookback Coverage

**Problem Prevented**: Late-arriving data not captured

**Implementation**:
```sql
-- tests/singular/test_incremental_lookback.sql
-- Run after incremental to verify lookback captured updates

with recent_changes as (
    select count(*) as updated_count
    from {{ ref('int_transactions__posted') }}
    where _etl_updated_at >= current_date - 3  -- Lookback window
)

select *
from recent_changes
where updated_count = 0  -- Should have SOME updates in lookback window
```

---

## Implementation Guide

### Adding Prevention Tests to a Model

1. **Identify Risk Category** - What failure mode are you preventing?
2. **Choose Test Type** - Generic (reusable) or singular (model-specific)?
3. **Set Severity** - `error` for blocking, `warn` for alerting
4. **Add Metadata** - Document the incident or risk being addressed

### Example Complete Configuration

```yaml
# models/marts/finance/_finance__models.yml
models:
  - name: mrt_revenue__monthly
    description: "Monthly revenue by product"

    # Prevention tests
    tests:
      # Volume test
      - row_count_in_range:
          min_rows: 10000
          max_rows: 10000000
          severity: error
          meta:
            prevention_category: volume

      # Event distribution test
      - expected_values_present:
          column: product_category
          expected_values: ['CARD', 'ACH', 'WIRE', 'OTHER']
          severity: error
          meta:
            prevention_category: event_distribution

    columns:
      - name: revenue_month
        tests:
          - not_null
          - date_range_valid:
              min_date: '2020-01-01'
              max_days_lag: 45  # Monthly aggregation

      - name: product_id
        tests:
          - relationships:
              to: ref('dim_product')
              field: product_id
              severity: error
              meta:
                prevention_category: join_health
```

---

## Registry of Known Issues

| Issue | Date | Root Cause | Prevention Test Added |
|-------|------|------------|----------------------|
| GBOS 99% suppression | 2025-10-30 | event_request_type filter | volume_trace, expected_values_present |
| Orphan transactions | 2025-09-15 | Account join failure | join_success_rate |
| Duplicate incrementals | 2025-08-22 | Merge key collision | unique on uid |

---

## Integration with 4-Agent Workflow

Prevention tests should be specified during **Phase 3: Architecture** (dbt-tech-spec-writer):

```markdown
## 7. Test Requirements (Tech Spec Section)

| Model | Test | Severity | Prevention Category |
|-------|------|----------|---------------------|
| int_transactions__posted | row_count_in_range(min=1M) | error | volume |
| int_transactions__posted | expected_values_present(transaction_type) | error | event_distribution |
| int_transactions__enriched | join_success_rate(account_id, 99%) | error | join_health |
```

During **Phase 4: Implementation** (dbt-migration), these tests are added to schema.yml files.

---

## Maintenance

### Quarterly Review

- Review test effectiveness (false positives, missed issues)
- Add tests for any new failure modes discovered
- Update thresholds based on data growth
- Archive obsolete tests

### Adding New Prevention Tests

1. Document the incident that revealed the need
2. Create the test (generic or singular)
3. Add to this registry with metadata
4. Include in relevant tech spec templates
