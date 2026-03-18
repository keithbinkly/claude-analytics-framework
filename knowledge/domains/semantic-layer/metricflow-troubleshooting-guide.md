# MetricFlow Troubleshooting Guide
## How to Generate semantic_manifest.json with dbt Core

---

## 🎯 Problem Statement

When using **dbt Fusion 2.0 (preview)** for development, the `semantic_manifest.json` file required by MetricFlow is not generated, resulting in this error:

```
ERROR: Unable to load the semantic manifest.
  Please ensure that you are running `mf` in the root directory of a dbt project
  and that the semantic manifest artifact exists.
```

---

## ✅ Solution: Use dbt Core for Parsing

As recommended by dbt Labs: **"Do all your development process in Fusion and then just do a dbt parse with dbt Core whenever you need the semantic_manifest.json"**

---

## 📋 Prerequisites

1. **dbt Core 1.8+** must be installed in your environment (alongside dbt Fusion)
2. **dbt-metricflow** must be installed
3. **dbt-redshift** adapter must be installed

Check your installation:
```bash
pip list | grep -i dbt
```

You should see:
- `dbt-core` (1.8 or higher)
- `dbt-metricflow`
- `dbt-redshift`

---

## 🔧 Required Fixes to Semantic Models

### Issue 1: Conflicting Entity/Dimension Definitions

**Error:**
```
element `merchant` is of type SemanticModelElementType.DIMENSION, 
but it is used as types [dimension, entity] across the model.
```

**Fix:** Remove entity definitions that duplicate dimension names.

**Before:**
```yaml
entities:
  - name: merchant
    type: foreign
    expr: merchant
  
  - name: product_stack
    type: foreign
    expr: product_stack

dimensions:
  - name: merchant
    type: categorical
    expr: merchant
```

**After:**
```yaml
entities:
  - name: merchant_auth_event
    type: primary
    expr: concat(calendar_date, '-', merchant, '-', ...)

dimensions:
  - name: merchant
    type: categorical
    expr: merchant
```

### Issue 2: Missing Aggregation Time Dimension

**Error:**
```
Aggregation time dimension for measure attempt_amt is not set!
```

**Fix:** Add `defaults.agg_time_dimension` to the semantic model.

```yaml
semantic_models:
  - name: merchant_auth_decline_analytics
    model: ref('mrt_merchant_auth_decline_analytics')
    
    # Add this section
    defaults:
      agg_time_dimension: calendar_date
    
    entities: [...]
    dimensions: [...]
    measures: [...]
```

### Issue 3: Deprecated Cumulative Metric Parameters

**Error:**
```
Cumulative fields `type_params.window` and `type_params.grain_to_date` 
have been moved and will soon be deprecated.
```

**Fix:** Nest window parameters under `cumulative_type_params`.

**Before:**
```yaml
metrics:
  - name: rolling_7d_decline_rate
    type: cumulative
    type_params:
      measure: decline_cnt
      window: 7 days  # ❌ Deprecated location
```

**After:**
```yaml
metrics:
  - name: rolling_7d_decline_rate
    type: cumulative
    type_params:
      measure: decline_cnt
      cumulative_type_params:  # ✅ New location
        window: 7 days
```

---

## 🚀 Step-by-Step Process

### Step 1: Activate Virtual Environment

```bash
cd /Users/kbinkly/git-repos/dbt_projects/dbt-enterprise
source .venv/bin/activate
```

Verify activation:
```bash
which dbt
# Should output: /Users/kbinkly/git-repos/dbt_projects/dbt-enterprise/.venv/bin/dbt

dbt --version
# Should output: dbt Core 1.10.13 (or similar)
```

### Step 2: Apply Semantic Model Fixes

Make the three fixes described above to:
- `models/marts/marts_NEW/operational/transaction_monitoring/semantic_models/sem_merchant_auth_decline_analytics.yml`
- `models/marts/marts_NEW/operational/transaction_monitoring/metrics/merchant_auth_decline_metrics.yml`

### Step 3: Run dbt parse with dbt Core

```bash
dbt parse --no-partial-parse
```

**Expected output:**
```
Running with dbt=1.10.13
Registered adapter: redshift=1.9.5
[Some warnings about missing nodes - these are OK]
Performance info: /Users/.../target/perf_info.json
```

**Key:** No errors about semantic models or validation failures.

### Step 4: Verify semantic_manifest.json Was Created

```bash
ls -lh target/semantic_manifest.json
```

**Expected output:**
```
-rw-r--r--  1 user  staff  31K Oct 22 13:00 target/semantic_manifest.json
```

### Step 5: Test MetricFlow Query

```bash
mf query --metrics total_declines --group-by merchant --limit 5
```

---

## 📝 Complete Working Example

Here's the exact semantic model structure that works:

```yaml
# sem_merchant_auth_decline_analytics.yml
semantic_models:
  - name: merchant_auth_decline_analytics
    description: Merchant-level auth/decline analytics
    model: ref('mrt_merchant_auth_decline_analytics')
    
    defaults:
      agg_time_dimension: calendar_date  # ✅ Required for measures
    
    entities:
      - name: merchant_auth_event
        type: primary
        expr: >
          concat(
            coalesce(calendar_date::varchar, ''),
            '-',
            coalesce(merchant, '')
          )
    
    dimensions:
      - name: calendar_date
        type: time
        type_params:
          time_granularity: day
        expr: calendar_date
      
      - name: merchant
        type: categorical
        expr: merchant
    
    measures:
      - name: decline_cnt
        agg: sum
        expr: decline_cnt
        create_metric: true
```

And the metrics file:

```yaml
# merchant_auth_decline_metrics.yml
metrics:
  - name: total_declines
    type: simple
    type_params:
      measure: decline_cnt
  
  - name: rolling_7d_decline_rate
    type: cumulative
    type_params:
      measure: decline_cnt
      cumulative_type_params:  # ✅ Nested correctly
        window: 7 days
```

---

## 🔄 Development Workflow

### For Day-to-Day Development (Use dbt Fusion)

```bash
# Use dbt Fusion for model development
dbt run --select my_model
dbt test --select my_model
```

### When You Need MetricFlow (Use dbt Core)

```bash
# Generate semantic manifest with dbt Core
dbt parse --no-partial-parse

# Query metrics with MetricFlow
mf query --metrics my_metric --group-by dimension
mf list metrics
mf list dimensions --metrics my_metric
```

---

## 🐛 Common Errors and Fixes

### Error: "command not found: mf"

**Cause:** Virtual environment not activated or mf not installed

**Fix:**
```bash
source .venv/bin/activate
pip install dbt-metricflow
```

### Error: "Could not find adapter type redshift"

**Cause:** dbt-redshift adapter not installed

**Fix:**
```bash
pip install dbt-redshift
```

### Error: "At least one time spine must be configured"

**Cause:** No time spine model configured

**Fix:** Create `metricflow_time_spine.sql` and configure in YAML:

```sql
-- models/staging/edw/metricflow_time_spine.sql
{{ config(materialized='table') }}

select calendar_date as date_day
from {{ ref('stg_edw__dim_date') }}
where calendar_date between '2020-01-01' and current_date + 365
```

```yaml
# models/staging/edw/metricflow_time_spine.yml
models:
  - name: metricflow_time_spine
    time_spine:
      standard_granularity_column: date_day
    columns:
      - name: date_day
        granularity: day
```

Then build it:
```bash
dbt run --select metricflow_time_spine
```

### Error: "Semantic Manifest validation failed"

**Cause:** Issues in semantic model YAML (see Issues 1-3 above)

**Fix:** Apply the three fixes documented above, then re-run `dbt parse`

---

## 📊 Success Indicators

You'll know it's working when:

1. ✅ `dbt parse` completes without semantic validation errors
2. ✅ `target/semantic_manifest.json` file exists and is recent (check timestamp)
3. ✅ `mf list metrics` shows your metrics
4. ✅ `mf query` returns data without errors

---

## 🎓 Key Takeaways

1. **dbt Fusion 2.0 preview** does NOT generate `semantic_manifest.json`
2. **dbt Core 1.8+** is required to generate the semantic manifest
3. Both can coexist in the same virtual environment
4. Use **dbt Fusion for development**, **dbt Core for parsing**
5. Three critical fixes needed:
   - Remove duplicate entity/dimension names
   - Add `defaults.agg_time_dimension`
   - Nest cumulative parameters under `cumulative_type_params`

---

## 📚 Related Files

- Semantic Model: `models/marts/marts_NEW/operational/transaction_monitoring/semantic_models/sem_merchant_auth_decline_analytics.yml`
- Metrics: `models/marts/marts_NEW/operational/transaction_monitoring/metrics/merchant_auth_decline_metrics.yml`
- Time Spine: `models/staging/edw/metricflow_time_spine.sql` + `.yml`
- Implementation Guide: `docs/metricflow_implementation_guide.md`
- Query Cookbook: `docs/metricflow_query_cookbook.md`

---

**Last Updated:** October 22, 2025  
**Tested With:** dbt Core 1.10.13, dbt-metricflow 0.11.0, dbt-redshift 1.9.5
