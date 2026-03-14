---
name: dbt-semantic-layer-developer
description: |
  Expert-level assistance with dbt Semantic Layer, MetricFlow, semantic models, metrics,
  dimensions, entities, measures, grain definitions, and BI tool integrations. Use this skill
  when building semantic models, creating metrics (simple, ratio, cumulative, derived,
  conversion), defining grain, debugging MetricFlow validation errors, writing semantic YAML,
  or integrating with BI tools. Also use when asked to "add a metric", "create a semantic
  model", "define measures", "fix MetricFlow error", "semantic layer YAML", or "write
  sem_*.yml". Extracted from official dbt documentation and optimized for data practitioners.
---

# dbt Semantic Layer Developer Skill

## Your Role

You are a dbt Semantic Layer architect specializing in MetricFlow, metric governance, and semantic modeling. Your expertise includes defining semantic models, creating metrics across all types, debugging validation errors, and integrating the Semantic Layer with BI tools and APIs.

## When NOT to Use This Skill

**Check this first** - the Semantic Layer adds abstraction overhead. Consider alternatives if:

- **Single tool, simple metrics** - Just aggregating from one table with basic SUM/COUNT? Use a simple dbt model
- **Pre-processed metrics** - Metrics already calculated and persisted? Standard dbt models suffice
- **Ad hoc queries only** - No persistent definitions or BI integrations needed? Direct SQL is simpler
- **Small team, simple use case** - Ensure the benefits justify the complexity
- **High-cardinality grouping** - GROUP BY returning 100s+ rows? MetricFlow may timeout; use direct SQL

**Decision criteria:** Use Semantic Layer when you need centralized metric definitions serving multiple downstream consumers (BI tools, notebooks, APIs). Skip it for single-purpose aggregations.

---

## Core Principles

**Never speculate about code or schema you haven't read.** If you're uncertain about:
- A semantic model's structure (entities, dimensions, measures)
- Entity relationships or join logic
- Metric definitions or their underlying measures
- Time spine configuration

**Stop and read the relevant YAML file first.** It's better to say "Let me check the semantic model definition" than to guess and provide incorrect guidance.

---

## Pre-Development References

Skipping these causes metric name collisions, stale workarounds, and naming drift.

| Resource | Path | Check Before | Why |
|----------|------|--------------|-----|
| **MetricFlow Status** | `shared/knowledge-base/metricflow-connectivity-status.md` | Any MF work | Known issues/workarounds |
| **Semantic Candidates** | `shared/reference/baas-semantic-candidates.yml` | New metrics | What should be in semantic layer |
| **Controlled Vocab** | `shared/reference/controlled-vocabulary.yml` | Naming | Consistent metric/dimension names |

---

## Naming Conventions

MetricFlow requires **globally unique** measure and metric names across ALL semantic models in the project. Collisions cause `dbt parse` failures. The linter rule MF002 catches these, but following conventions prevents them.

### Measures

Prefix with **domain abbreviation** when multiple semantic models exist for related data:

| Pattern | Example | When |
|---------|---------|------|
| `{concept}` | `transaction_count` | Only ONE semantic model for this domain |
| `{domain}_{concept}` | `oct_transaction_count` | Multiple semantic models share similar columns |

The `expr` field always points to the **actual column name** — only the `name` field gets the prefix.

```yaml
# CORRECT: name is prefixed, expr is the real column
- name: oct_transaction_count
  agg: sum
  expr: transaction_count

# WRONG: same name as another semantic model's measure
- name: transaction_count   # collides with disbursement_daily_metrics!
  agg: sum
  expr: transaction_count
```

### Metrics

| Type | Pattern | Example |
|------|---------|---------|
| Simple | `{domain}_{concept}` | `disbursement_transaction_count` |
| Ratio | `{domain}_{kpi_name}` | `disbursement_success_rate` |
| Cumulative | `{domain}_{window}_{concept}` | `disbursement_mtd_completed_amount` |
| Derived | `{domain}_{calculation}` | `disbursement_net_amount` |

### Semantic Models

`{domain}_{grain}_metrics` — e.g., `disbursement_daily_metrics`, `oct_daily_metrics`

### Cross-File Validation

Always run cross-file lint before committing semantic YAML:
```bash
python3 tools/lint/metricflow_lint.py --cross-file path/to/semantic/dir/
```

---

## DEV vs PROD Environments

**Understanding which environment you're querying is essential for accurate results.**

### Two Query Paths

| Method | Data Source | Use Case |
|--------|-------------|----------|
| **MCP Semantic Layer API** | **PROD** (deployed environment) | Consumption, stakeholder demos, production analytics |
| **MetricFlow CLI** (local) | **DEV** (local profiles.yml target) | Development, validation, testing |

### When Building (DEVELOPER Role)
- Use **MetricFlow CLI** (`mf query`, `mf validate-configs`)
- Queries hit your **DEV target** from `profiles.yml`
- Perfect for iterating on semantic model definitions
- Changes don't affect production

### When Consuming (ANALYST Role)
- Use **MCP tools** (`mcp__dbt-mcp__query_metrics`, etc.)
- Queries hit **PROD environment** via dbt Cloud Semantic Layer API
- Required for stakeholder demos and production analytics
- Always disclose if falling back to DEV data

### DEV Data Staleness Warning

DEV schemas may lag PROD by days or weeks. If you see zeros or anomalies in recent dates, first run:
```sql
SELECT MAX(calendar_date) FROM dev_schema.model_name;   -- DEV
SELECT MAX(calendar_date) FROM prod_schema.model_name;  -- PROD
```

### MCP Multi-Cell URL Format

`https://<ACCOUNT_PREFIX>.semantic-layer.<REGION>.dbt.com/api/graphql` — e.g., `https://sb340.semantic-layer.us1.dbt.com/api/graphql`. Common mistake: wrong segment order (`semantic-layer.sb340.us1.dbt.com`).

---

## When to Use MetricFlow vs Direct SQL

**Decision Tree:**
```
Is this a defined metric?
  YES → Use MetricFlow
  NO  → Use dbt show / direct SQL

Will GROUP BY return > 100 rows?
  YES → Use dbt show (avoid timeout)
  NO  → MetricFlow is fine
```

| Use Case | Tool | Reason |
|----------|------|--------|
| Low-cardinality dimensions (product, region) | MetricFlow | Sub-second, consistent with semantic layer |
| High-cardinality dimensions (merchant, account_id) | `dbt show --inline` | MetricFlow times out at 1000s of values |
| Ad-hoc data profiling | `dbt show --inline` | Direct SQL, no overhead |
| Metric validation | MetricFlow | Uses same calculation logic as BI tools |

---

## Ontological Grounding for Metrics

**Source:** Knowledge Engineering Research Synthesis (2026-01-12)

`spend_total` without context could mean cardholder spend, merchant processing volume, or platform fee revenue. Ontological grounding encodes semantic boundaries so metrics can't be silently misused.

For each metric, embed these in the `description`:

| Element | What to State |
|---------|--------------|
| **Entity** | What this metric measures (not what it sounds like) |
| **Valid Dimensions** | Groupings that produce meaningful results |
| **Invalid Dimensions** | Groupings that produce nonsense (explicit prohibition) |
| **Temporal Context** | Which date field applies and why |

```yaml
metrics:
  - name: total_customer_spend
    description: >
      Sum of posted transaction amounts at merchant POS.
      ENTITY: Cardholder spend (not merchant revenue, not platform fees)
      VALID DIMENSIONS: product, merchant_category, geography, time
      INVALID: Do not group by internal cost center or account type
      TEMPORAL: Uses posted_date (when funds settled), not txn_date
    type: simple
    type_params:
      measure: posted_amount
```

AI agents misuse certified metrics by grouping by invalid dimensions, filtering the wrong population, or combining dimensionally incompatible metrics. Explicit description fields prevent silent errors.

---

## Local Development Workflow

### Installation & Setup

```bash
# Install MetricFlow with adapter
pip install "dbt-metricflow[snowflake]"  # Or: bigquery, redshift, databricks

# Configure shell for template wrappers (zsh)
echo "setopt BRACECCL" >> ~/.zshrc
source ~/.zshrc

# Or use automated script
bash scripts/setup_shell_config.sh
```

**See:** [Local Development Guide](references/guide_local_development.md)

### 5-Step Development Loop

1. **EDIT** - Modify semantic models or metrics
2. **PARSE** - Run `dbt parse` to validate YAML
3. **VALIDATE** - Run `mf validate-configs` to check semantic graph
4. **QUERY** - Test with `mf query --metrics <metric>`
5. **ITERATE** - Refine and repeat

**See:** [Validation Workflow](references/guide_validation_workflow.md)

### CLI Quick Commands

```bash
# List metrics
mf list metrics

# List dimensions for a metric
mf list dimensions --metrics total_revenue

# Query metric
mf query --metrics total_revenue

# Query with time dimension
mf query --metrics total_revenue --group-by metric_time__day --limit 10

# Query with filter (note: quoted!)
mf query --metrics total_revenue \
  --where "{{ Dimension('order__status') }} == 'completed'"

# Compile without executing
mf query --metrics total_revenue --compile
```

**See:** [CLI Commands Complete](references/cli_commands_complete.md) | [Query Syntax Guide](references/guide_query_syntax.md)

### Template Wrapper Syntax

MetricFlow uses special syntax for filters:

```bash
# Dimension filter
--where "{{ Dimension('entity__dimension_name') }} == 'value'"

# Time dimension filter
--where "{{ TimeDimension('entity__time_dim', 'day') }} >= '2024-01-01'"

# Combined filters
--where "{{ Dimension('customer__segment') }} == 'enterprise' AND {{ TimeDimension('order__order_date', 'day') }} >= '2024-01-01'"
```

**Important:** Always quote the entire `--where` clause to prevent shell interpretation errors.

**See:** [Query Syntax Guide](references/guide_query_syntax.md)

---

## Quick Reference

### Common Semantic Model Pattern

```yaml
semantic_models:
  - name: orders
    description: Order fact table
    model: ref('fct_orders')

    entities:
      - name: order_id
        type: primary
      - name: customer_id
        type: foreign

    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
      - name: order_status
        type: categorical

    measures:
      - name: order_total
        agg: sum
      - name: order_count
        agg: count
        expr: order_id
```

### Common Metric Patterns

```yaml
metrics:
  # Simple metric
  - name: total_revenue
    description: Sum of all order totals
    type: simple
    label: Total Revenue
    type_params:
      measure: order_total

  # Ratio metric
  - name: average_order_value
    description: Revenue per order
    type: ratio
    label: Average Order Value
    type_params:
      numerator: total_revenue
      denominator: order_count

  # Cumulative metric
  - name: cumulative_revenue
    description: Running total of revenue
    type: cumulative
    label: Cumulative Revenue
    type_params:
      measure: order_total
```

### Latest Metrics Spec (dbt 1.11+)

The new spec moves semantic model definitions inline with `models:` blocks and deprecates `measures:` in favor of column-level `metrics:`. Key changes: `type_params` promoted to direct keys, `input_metrics` replaces `type_params.metrics`, ratio/cumulative/conversion params are unnested.

For old format → new format examples, migration command, and derived semantics (1.12+), see [`references/migration_guide_1_11.md`](references/migration_guide_1_11.md).

---

### Metric Verification Checklist

After creating any metric, verify before querying:

1. **Measure exists** - `type_params.measure` is in the semantic model; ratio metrics need both numerator and denominator metrics defined
2. **Filter dimensions exist** - dimension names match semantic model; use entity qualification (`order__status`)
3. **Time spine configured** - model exists in `dbt_project.yml`; cumulative metrics may need `join_to_timespine: true`
4. **No circular dependencies** - ratio/derived metrics reference defined metrics
5. **Test query passes** - `mf query --metrics <your_metric> --limit 5`

### Common Pitfalls

These are verified production bugs. Full details in [`references/common_pitfalls.md`](references/common_pitfalls.md).

| Pitfall | One-Line Description |
|---------|---------------------|
| `window` vs `grain_to_date` | Rolling window ≠ month-to-date; use `grain_to_date: month` for MTD |
| Redshift `concat()` limit | Redshift accepts only 2 args; use `\|\|` operator instead |
| `create_metric` duplication | Auto-generated and explicit metric with same name causes parse error |
| Ratio measure vs metric refs | Ratio numerator/denominator must reference metrics, not measures |
| GROUPING SETS triple-count | Filter each measure to single grain or values sum across all grain rows |
| Redundant `expr` warning | Omit `expr` when measure name matches the column name |

### Semantic Layer Exports

Exports write saved query results to warehouse tables/views — useful for BI tools without native SL integration and cache warming before reporting periods. Key commands: `dbt sl export --saved-query <name>`, `dbt sl export-all`.

Full configuration examples and performance benchmarks in [`references/semantic_layer_exports.md`](references/semantic_layer_exports.md).

### MetricFlow Time Spine Setup

```sql
-- models/metricflow_time_spine.sql
{{ config(
    materialized='table'
) }}

with days as (
    {{ dbt.date_spine(
        datepart="day",
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2030-12-31' as date)"
    ) }}
),

final as (
    select cast(date_day as date) as date_day
    from days
)

select * from final
```

**Python SDK examples:** [`references/api_reference.md`](references/api_reference.md)

---

## Debugging

### 3-Layer Validation Architecture

**When debugging validation errors, think step by step:**

1. **PARSE Layer** - Is the YAML syntactically correct?
   - Check indentation, quotes, special characters
   - Run `dbt parse` to validate structure
   - Look for: "Compilation Error", "YAML syntax error"

2. **SEMANTIC Layer** - Is the logic valid?
   - Check measure/dimension/entity references
   - Verify join paths and entity relationships
   - Run `mf validate-configs` to check semantic graph
   - Look for: "Measure not found", "Unknown dimension", "No join path"

3. **DATA PLATFORM Layer** - Can the query execute?
   - Check SQL compilation and warehouse execution
   - Verify table/column existence
   - Run `mf query --compile` to see generated SQL
   - Look for: "Column does not exist", "Table not found"

### Common Validation Errors

| Error | Layer | Fix |
|-------|-------|-----|
| `Compilation Error: YAML syntax` | PARSE | Fix indentation, quotes |
| `Measure not found` | SEMANTIC | Check measure name in semantic model |
| `Unknown dimension` | SEMANTIC | Verify dimension name and entity prefix |
| `No join path` | SEMANTIC | Check entity relationships |
| `Column does not exist` | DATA PLATFORM | Verify column in base model |
| `Table not found` | DATA PLATFORM | Run `dbt run` on upstream models |

### Metric Duplication Error

**Symptom:**
```
Error: Metric 'decline_rate' defined multiple times
```

**Root Cause**: Setting `create_metric: true` in the semantic model YAML while ALSO defining the metric in a separate `metrics.yml` file.

**Solution**: Set `create_metric: false` in the semantic model YAML if you are defining complex metrics (like ratios) externally.

### Proxy Metric `expr` Warning

**Symptom:** `Warning: Metric 'attempt_amt' should not have an expr set if it's proxy from measures`

**Fix**: Omit `expr` on a measure when the measure name matches the column name — MetricFlow infers it. Keep `expr` only when name differs from column, you need a SQL expression, or you're using `count_distinct`. Fixed 16 prod warnings in `sem_merchant_auth_decline_analytics.yml` (2026-01-29). See [`references/common_pitfalls.md`](references/common_pitfalls.md) pitfall #6.

---

## Pre-Flight: Downstream Impact Analysis

**BEFORE replacing or refactoring semantic base models:**

1. **Check semantic model refs:**
   ```bash
   grep -r "ref('model_name')" **/*.yml
   ```

2. **List downstream consumers:**
   Use lineage tools to find all models that depend on your target.

3. **Design migration strategy:**

| Strategy | When to Use | Pros | Cons |
|----------|-------------|------|------|
| **Backward-compat view** | Many downstream consumers | Zero ref changes | Extra layer |
| **Update all refs** | Few consumers, simple refs | Clean architecture | Coordination |
| **Deprecation period** | External consumers | Safe transition | Temp duplication |

**Red Flag**: Creating new optimized models without planning downstream integration leads to "orphaned lineage" bugs where new models aren't consumed and old broken models keep running.

---

## Reference Files

| File | Contents |
|------|----------|
| [guide_local_development.md](references/guide_local_development.md) | Installation, shell config, dev workflow |
| [guide_validation_workflow.md](references/guide_validation_workflow.md) | CI/CD integration, validation errors, testing |
| [guide_query_syntax.md](references/guide_query_syntax.md) | Template wrappers, entity qualification, time granularity |
| [cli_commands_complete.md](references/cli_commands_complete.md) | Full command reference, all flags, examples |
| [metrics.md](references/metrics.md) | YAML metric definitions, Python SDK, query API |
| [api_reference.md](references/api_reference.md) | GraphQL, JDBC, Python SDK sync/async, lazy loading |
| [migration_guide_1_11.md](references/migration_guide_1_11.md) | Old → new format examples, migration command, derived semantics |
| [common_pitfalls.md](references/common_pitfalls.md) | 6 verified production bugs with full code examples |
| [semantic_layer_exports.md](references/semantic_layer_exports.md) | Export config, when to use vs API, performance benchmarks |
| [stack_specific.md](references/stack_specific.md) | Redshift warnings, dual dbt install, internal metric inventory |
| [guide_bi_tool_integrations.md](references/guide_bi_tool_integrations.md) | Tableau, Power BI, Looker, Mode, Hex |
| [guide_enterprise_patterns.md](references/guide_enterprise_patterns.md) | Enterprise patterns, iterative migration, naming conventions |

---

## External Links

- [dbt Semantic Layer Docs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl)
- [MetricFlow Documentation](https://docs.getdbt.com/docs/build/about-metricflow)
- [Python SDK Repository](https://github.com/dbt-labs/semantic-layer-sdk-python)
