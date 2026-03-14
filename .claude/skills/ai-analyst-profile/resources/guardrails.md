# AI Analyst Guardrails

## MANDATORY RULES

These rules are non-negotiable. Violating them produces incorrect, ungoverned answers.

### Rule 1: dbt MCP Semantic Layer API Only

**ALWAYS** query using dbt MCP Semantic Layer API tools:
- `mcp__dbt__query_metrics` - Execute metric queries
- `mcp__dbt__list_metrics` - Discover available metrics
- `mcp__dbt__get_dimensions` - Get groupable dimensions
- `mcp__dbt__list_saved_queries` - Find pre-built queries

**NEVER** use:
- `mcp__dbt__execute_sql` with raw table queries
- `mcp__dbt__show` with custom aggregations
- Any tool that bypasses the semantic layer

### Rule 2: No Manual Calculations

**NEVER** calculate metrics manually, even if it seems simple:

```python
# WRONG - Do not do this
execute_sql("SELECT SUM(decline_cnt) / SUM(attempt_cnt) FROM table")

# CORRECT - Use certified metric
query_metrics(metrics=["spend_decline_rate_by_count"])
```

**Why?** Manual calculations:
- May use wrong filters (e.g., missing exclusions)
- May aggregate at wrong grain
- Are not certified or validated
- May change without notice

### Rule 3: Respect Metric Definitions

Each metric has a certified definition. Do not:
- Redefine metrics with different logic
- Combine metrics in ways not validated
- Apply filters that change the metric's meaning

**Example:** `spend_decline_rate_by_count` is defined as `decline_cnt / attempt_cnt`. Do not manually recalculate this as `decline_amt / attempt_amt` (that's a different metric).

### Rule 4: Acknowledge Limitations

If a question cannot be answered with available metrics:
1. State clearly that no certified metric exists
2. Suggest related metrics that are available
3. Do NOT attempt to answer with raw SQL

---

## APPROVED TOOLS

### Primary Tools

| Tool | Use Case | Example |
|------|----------|---------|
| `mcp__dbt__query_metrics` | Query one or more metrics | Decline rate trends |
| `mcp__dbt__list_metrics` | Find available metrics | "What can I measure?" |
| `mcp__dbt__get_dimensions` | Get grouping options | "How can I slice this?" |
| `mcp__dbt__list_saved_queries` | Find common queries | Pre-built analyses |

### Supporting Tools

| Tool | Use Case | When to Use |
|------|----------|-------------|
| `mcp__dbt__get_model_details` | Understand metric source | Explaining metric logic |
| `mcp__dbt__get_model_health` | Check data freshness | Before answering time-sensitive questions |

---

## FORBIDDEN PATTERNS

### Pattern 1: Direct Table Queries

```python
# FORBIDDEN
execute_sql("""
    SELECT merchant, SUM(decline_cnt)
    FROM dbt_keithgd.mrt_merchant_auth_decline__semantic_base
    GROUP BY merchant
""")
```

**Why forbidden?** Bypasses metric definitions, may apply wrong filters.

### Pattern 2: Manual Aggregations

```python
# FORBIDDEN
execute_sql("SELECT COUNT(*) / SUM(attempts) * 100 as rate FROM ...")
```

**Why forbidden?** May calculate differently than certified metric.

### Pattern 3: Raw Table Joins

```python
# FORBIDDEN
execute_sql("""
    SELECT a.*, b.product_name
    FROM transactions a
    JOIN products b ON a.product_id = b.id
""")
```

**Why forbidden?** May produce incorrect grain or fan-out.

### Pattern 4: Uncertified Derived Metrics

```python
# FORBIDDEN - Creating new metric on the fly
query_metrics(
    metrics=["spend_total_declines"],
    # Then manually dividing by something not in semantic layer
)
```

**Why forbidden?** Derived calculations are not validated.

---

## RESPONSE PATTERNS

### When Question CAN Be Answered

```
## Answer

[Direct answer using certified metrics]

## Details

[Table with metric results]

## Data Source

Metrics: [list of metrics used]
Semantic Model: [model name]
```

### When Question CANNOT Be Answered

```
I cannot answer this question with certified metrics.

**Reason:** [explanation]

**Available alternatives:**
1. [Related metric that exists]
2. [Another approach]

Would you like me to answer using one of these alternatives?
```

---

## ESCALATION TRIGGERS

Escalate to human data team when:

1. **Metric seems wrong** - Values far outside expected range
2. **Missing dimensions** - Needed grouping not available
3. **Data freshness issues** - Stale data detected
4. **Conflicting metrics** - Two metrics give inconsistent answers

**Escalation format:**
```
⚠️ DATA QUALITY FLAG

Issue: [description]
Metric: [metric name]
Expected: [what was expected]
Actual: [what was found]

Recommendation: Review with data engineering before using this result.
```
