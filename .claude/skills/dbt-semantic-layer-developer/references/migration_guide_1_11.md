# Latest Metrics Spec (dbt 1.11+) — Migration Guide

**Source:** [docs.getdbt.com/docs/build/latest-metrics-spec](https://docs.getdbt.com/docs/build/latest-metrics-spec)

The new spec creates an open standard for defining metrics/dimensions that works across multiple platforms.

---

## What Changed

| Component | Old (Legacy) | New (1.11+) |
|-----------|-------------|-------------|
| **Semantic model location** | Top-level `semantic_models:` key | Nested under `models: > semantic_model: enabled: true` |
| **Entities/Dimensions** | Separate `entities:` and `dimensions:` arrays | Column-level `entity:` and `dimension:` properties |
| **Measures** | `measures:` array in semantic model | **Deprecated** — replaced by `type: simple` metrics |
| **type_params** | Wrapper for metric params | **Deprecated** — params promoted to direct keys (`expr`, `percentile`, `non_additive_dimension`, `join_to_timespine`, `fill_nulls_with`) |
| **Time granularity** | `type_params: time_granularity:` | `granularity:` at column level |
| **Agg time dimension** | Per-dimension | `agg_time_dimension:` set once at model level |
| **Derived metrics** | `type_params.metrics` | `input_metrics` |
| **Ratio metrics** | `type_params.numerator/denominator` | Direct `numerator:` / `denominator:` keys |
| **Cumulative metrics** | `cumulative_type_params` nested | Top-level `window`, `grain_to_date`, `period_agg` |
| **Conversion metrics** | `conversion_type_params`, `base_measure` | Unnested, `base_metric` |

---

## Old Format → New Format Example

**OLD (pre-1.11):**
```yaml
semantic_models:
  - name: orders
    model: ref('fct_orders')
    entities:
      - name: order_id
        type: primary
    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
    measures:
      - name: order_total
        agg: sum

metrics:
  - name: total_revenue
    type: simple
    type_params:
      measure: order_total
```

**NEW (1.11+):**
```yaml
models:
  - name: fct_orders
    semantic_model:
      enabled: true
      agg_time_dimension: order_date
    columns:
      - name: order_id
        entity:
          type: primary
      - name: order_date
        dimension:
          type: time
          granularity: day
      - name: order_total
        metrics:
          - type: simple
            name: total_revenue
            agg: sum
```

---

## Migration Command

```bash
# Auto-migrate existing YAML to new format
dbt-autofix deprecations --semantic-layer

# Then validate
dbt parse
mf validate-configs
```

**Caveats:**
- `dbt-autofix` only processes current project files — dependent packages must update independently
- dbt Copilot doesn't yet support generating the new YAML spec — validate AI-generated content manually
- Both old and new formats are supported during transition; old format will show deprecation warnings

---

## Derived Semantics (1.12+)

Create dimensions and entities from upstream semantic models without duplicating definitions:

```yaml
models:
  - name: fct_orders
    semantic_model:
      enabled: true
      derived_semantics:
        - model: ref('dim_customers')
          join:
            type: left
            on: "fct_orders.customer_id = dim_customers.customer_id"
```

This avoids re-declaring dimensions that already exist in upstream semantic models. MetricFlow resolves the join path automatically.
