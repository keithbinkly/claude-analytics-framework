# SQL & MetricFlow Pattern Library

Reference for Data-Puller. Load at canvas start.

## Entity Prefix Rules

All dimension names require entity prefixes when used in `group_by` or `where`:

```
WRONG: group_by=["partner_name"]
RIGHT: group_by=["transaction__partner_name"]
```

The prefix is the entity name from the semantic model, not the table name.
Use `mcp__dbt-mcp__get_dimensions` to discover exact prefixed names.

## Common Query Patterns

### Single metric, all dimensions
```python
query_metrics(
    metrics=["metric_name"],
    group_by=["dim1", "dim2", "dim3"],
    order_by=["-metric_name"],
    limit=100
)
```

### Time series with grain
```python
query_metrics(
    metrics=["metric_name"],
    group_by=["metric_time__day"],  # or __week, __month
    where=["{{ TimeDimension('metric_time', 'DAY') }} >= '2025-01-01'"],
    order_by=["metric_time__day"]
)
```

### Cross-dimensional comparison
```python
query_metrics(
    metrics=["metric_a", "metric_b"],
    group_by=["shared_dimension"],
    where=["{{ TimeDimension('metric_time', 'MONTH') }} >= '2025-01-01'"],
    order_by=["-metric_a"]
)
```

### Filtered aggregation
```python
query_metrics(
    metrics=["metric_name"],
    group_by=["dimension_a"],
    where=[
        "{{ TimeDimension('metric_time', 'DAY') }} >= '2025-06-01'",
        "{{ Dimension('entity__dimension_b') }} = 'value'"
    ]
)
```

## Canvas Optimization

| Dataset Size | Strategy |
|---|---|
| Small (<500 rows) | Query all dimensions at once |
| Medium (500-5000) | Query top dimensions first, drill on signal |
| Large (>5000) | Pre-filter by time range, then dimension sweeps |

## Known Gotchas

- `metric_time` requires TimeDimension wrapper in WHERE, not Dimension
- Derived metrics may not support all group_by combinations — check with get_dimensions first
- `order_by` uses string prefix `-` for descending, no prefix for ascending
- `limit` applies AFTER grouping, not before
- Empty result = likely wrong entity prefix, not missing data

## Rate/Ratio Metrics

When querying rate metrics (e.g., success_rate, approval_rate):
- These are pre-computed ratios — do NOT divide component metrics yourself
- The semantic layer handles the numerator/denominator relationship
- Verify by querying both the rate metric AND its components separately

## Canvas Pre-Query Checklist

1. `list_metrics()` — get all available metrics
2. `get_dimensions(metrics=[...])` — get all dimensions with entity prefixes
3. Query each low-cardinality dimension individually to get value distributions
4. For high-cardinality dimensions (>50 values), query top 20 by volume
5. Record all dimension values exactly as returned (case-sensitive)
