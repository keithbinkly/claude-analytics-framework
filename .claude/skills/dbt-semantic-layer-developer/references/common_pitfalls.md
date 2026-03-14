# Common Pitfalls (Verified Against MetricFlow 0.11 Source)

These are actual bugs caught in production. Check BEFORE `dbt parse`.

---

## 1. Cumulative: `window` vs `grain_to_date` (MTD/YTD)

| Want | Use | NOT |
|------|-----|-----|
| Month-to-date (resets each month) | `grain_to_date: month` | `window: 1 month` (rolling!) |
| Year-to-date (resets each year) | `grain_to_date: year` | `window: 1 year` |
| Rolling 7-day window | `window: 7 days` | `grain_to_date: week` |
| All-time running total | Omit window entirely | - |

```yaml
# WRONG — rolling window, does NOT reset at month boundary
type_params:
  measure: completed_amount
  window: 1 month

# CORRECT — resets at start of each calendar month
type_params:
  measure: completed_amount
  grain_to_date: month
```

**Source:** `dbt/artifacts/resources/v1/metric.py` — `CumulativeTypeParams` class.
Note: `grain_to_date` also accepted under `cumulative_type_params:` (preferred in 1.11+).

---

## 2. Redshift: `concat()` Only Takes 2 Args

MetricFlow generates `concat()` calls. Redshift's `concat()` only accepts 2 arguments.
**Always use `||`** in entity `expr` and measure `expr` fields.

```yaml
# WRONG — fails on Redshift
expr: concat(col_a, '-', col_b, '-', col_c)

# CORRECT
expr: col_a || '-' || col_b || '-' || col_c
```

---

## 3. `create_metric: true` + Explicit Metric = Duplication Error

If a measure has `create_metric: true`, MetricFlow auto-generates a simple metric.
Defining the same metric explicitly causes: `Metric 'X' defined multiple times`.

**Rule:** Use `create_metric: true` for simple pass-throughs, OR define explicit metrics. Never both.

---

## 4. Ratio Metrics Need Metric References, Not Measure References

Ratio `numerator`/`denominator` reference **metric names**, not measure names.
You need a simple metric wrapping each measure before creating a ratio.

```yaml
# WRONG — measures don't work as ratio inputs
type_params:
  numerator: my_measure    # This is a measure, not a metric
  denominator: total_measure

# CORRECT — reference simple metrics
type_params:
  numerator: my_metric     # Simple metric wrapping my_measure
  denominator: total_metric
```

---

## 5. GROUPING SETS Models: Filter to Single Grain

If base model uses GROUPING SETS (Day/Week/Month rows), every measure MUST filter:
```yaml
expr: "CASE WHEN time_period = 'Day' THEN column_name ELSE 0 END"
```
Without this, MetricFlow sums across all grain rows → triple-counted values.

---

## 6. Redundant `expr` Warning

If measure `name` matches the column name, omit `expr`. MetricFlow infers it.
```yaml
# WRONG — triggers warning
- name: attempt_amt
  agg: sum
  expr: attempt_amt      # redundant

# CORRECT
- name: attempt_amt
  agg: sum               # expr inferred from name
```
