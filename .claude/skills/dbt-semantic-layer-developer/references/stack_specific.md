# Stack-Specific Appendix

> **For Public Release:** Remove this file from the distribution.
> Contains learnings specific to our environment (Redshift, dbt Fusion/Core dual install, Green Dot specific patterns).

---

## Redshift Compatibility Warnings

These issues are specific to **Amazon Redshift** and may not apply to Snowflake, BigQuery, or Databricks.

### Boolean Casting Errors

**Symptom:**
```
ERROR: invalid input syntax for type boolean: "true"
```

**Root Cause**: Direct casting `boolean_col::varchar` or `boolean_col::boolean` in views/semantic layer often fails in Redshift due to strict typing in the virtualization layer.

**Solution**: Use explicit `CASE WHEN` pattern:
```sql
-- Wrong
is_active::varchar

-- Correct
CASE WHEN is_active THEN 'true' ELSE 'false' END
```

### Concat Function Errors

**Symptom:**
```
ERROR: function concat(character varying, character varying, ...) does not exist
```

**Root Cause**: MetricFlow generates SQL using `concat()` with multiple arguments, but Redshift's `concat()` only accepts two arguments.

**Solution**: Always use the pipe operator `||` in Semantic Model YAML `expr` fields:
```yaml
# Wrong
expr: concat(col_a, '_', col_b)

# Correct
expr: col_a || '_' || col_b
```

### Schema Drift with SELECT *

**Symptom:**
```
ERROR: column "_fivetran_synced" does not exist
```

**Root Cause**: `SELECT *` on an incremental model includes system columns (like `_fivetran_synced`) that may not exist in the view definition or semantic layer expectation.

**Solution**: Explicitly select columns in intermediate models used by the semantic layer, excluding system columns.

---

## Dual dbt Installation Setup

**Applies to:** dbt-enterprise and similar projects using dbt Fusion + dbt Core together.

### Why Dual Setup?

| Environment | dbt Version | Use Case |
|-------------|-------------|----------|
| **Main** | dbt Fusion 2.0.0-preview | Model dev, `dbt run/build/test` |
| **`.venv`** | dbt Core 1.10.13 + MetricFlow | Semantic layer, `mf` commands |

MetricFlow requires dbt-core>=1.8,<2.0 (incompatible with Fusion).

### Activation Commands

```bash
# Main environment (default)
dbt --version  # Should show: dbt Fusion 2.0.0-preview.65

# Semantic layer environment
source /path/to/project/.venv/bin/activate
dbt --version  # Should show: dbt Core 1.10.13
mf --version   # Should show: MetricFlow 0.11.0
deactivate     # Return to main environment
```

### Version Conflict Troubleshooting

**Symptom:**
```
ERROR: dbt-metricflow requires dbt-core>=1.8,<2.0 but you have dbt-fusion 2.0.0
```

**Solution:** Activate `.venv` first:
```bash
source .venv/bin/activate
dbt parse  # Generate semantic_manifest.json
mf validate-configs
```

---

## Environment-Specific References

**MetricFlow Connectivity Status**: `shared/knowledge-base/metricflow-connectivity-status.md`
- 46 available metrics inventory
- Known issues and workarounds
- Environment-specific query patterns

**Troubleshooting Guide**: `shared/knowledge-base/troubleshooting.md`
- Semantic Layer / MetricFlow Issues section
- High-cardinality timeout workarounds

---

## High-Cardinality Workaround (Measured)

**Source**: Session 2025-12-09 Analyst QA

MetricFlow times out on dimensions with 1000s of values (merchant, account_id).

**Example:**
```bash
# FAILS - MetricFlow timeout
mf query --metrics approved_amt --group-by merchant --limit 10

# WORKS - Direct SQL
dbt show --inline "
SELECT merchant, SUM(approve_amt) as approved_amt
FROM {{ ref('mrt_semantic_base') }}
WHERE calendar_date >= CURRENT_DATE - 7
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10
"
```

---

## Internal Metric Inventory

**46 metrics available** across domains:
- Merchant Auth: `approve_amt`, `decline_amt`, `decline_cnt`, `attempt_cnt`, etc.
- Cardholder: `metric_cardholder_attempt_cnt`, `spend_cardholder_decline_rate`, etc.
- Registration: `cumulative_registrations_passed`, `cohort_activation_rate`, etc.

**Full list**: Run `mf list metrics` in `.venv` environment.

---

*End of stack-specific content. Remove this file for public release.*
