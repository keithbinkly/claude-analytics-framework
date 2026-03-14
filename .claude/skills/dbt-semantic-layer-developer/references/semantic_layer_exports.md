# Semantic Layer Exports

**Exports** enable running saved queries and writing output to tables/views in your data warehouse. This provides access to Semantic Layer data through standard SQL interfaces.

---

## When to Use Exports

| Scenario | Use Exports | Use Dynamic API |
|----------|-------------|-----------------|
| BI tools without native SL integration | Yes | |
| Pre-computed metric tables for performance | Yes | |
| Centralized metric definition across many tables | Yes | |
| Flexible ad-hoc querying | | Yes |
| Real-time metric values | | Yes |

---

## Export Commands

```bash
# Single saved query -> table
dbt sl export --saved-query monthly_revenue

# All saved queries -> tables
dbt sl export-all

# Production jobs (in dbt Cloud)
# Set environment variable: DBT_EXPORT_SAVED_QUERIES=TRUE
```

---

## Export Configuration in Saved Query

```yaml
saved_queries:
  - name: monthly_revenue_by_region
    description: Monthly revenue broken down by region
    query_params:
      metrics:
        - total_revenue
        - order_count
      group_by:
        - TimeDimension('order_date', 'month')
        - Dimension('customer__region')
    exports:
      - name: revenue_by_region_table
        config:
          alias: sl_monthly_revenue_by_region
          schema: semantic_layer_exports
          export_as: table  # or 'view'
```

---

## Key Patterns

**DRY Principle**: Define metric once in saved query -> exports cascade updates automatically. Change metric definition once, all export tables reflect it.

**Cache Warming**: Pre-populate BI tool caches by running `dbt sl export-all` before reporting periods.

**Cost Tracking**: Exports count toward queried metrics usage. Querying the resulting tables does NOT count.

---

## Saved Query Performance (Measured)

| Query Type | Duration | Improvement |
|-----------|----------|-------------|
| Uncached Ad-Hoc | ~10s | Baseline |
| Saved Query (Cached) | ~2s | 80% faster |
| Direct Export Query | <1s | >90% faster |

**Source**: Performance validation session 2025-01-03
