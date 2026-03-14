---
name: ai-analyst-profile
version: 1.0.0
description: |
  AI Analyst guardrails for conversational BI using dbt's Semantic Layer. This skill should be
  used when responding to business questions about data, metrics, or analytics. It enforces
  dbt MCP Semantic Layer API-only queries to ensure certified, governed metric responses and prevents
  direct SQL queries that could produce incorrect answers.

tags: [semantic-layer, dbt-mcp, analytics, guardrails, conversational-bi, data-analyst]
entry_point: true

triggers:
  - "what is the"
  - "show me"
  - "how many"
  - "what's our"
  - "analyze"
  - "compare"
  - "trend"
  - "top 10"
  - "decline rate"
  - "metrics"
  - "business question"

capabilities:
  metric_querying:
    - query_certified_metrics
    - list_available_metrics
    - get_metric_dimensions
    - execute_saved_queries

  insight_generation:
    - interpret_metric_results
    - identify_trends
    - compare_dimensions
    - explain_anomalies

resources:
  core:
    - path: resources/guardrails.md
      description: "Mandatory rules for Semantic Layer API-only querying"
    - path: resources/metric-reference.md
      description: "Available metrics and dimensions from semantic models"
    - path: resources/example-conversations.md
      description: "Business Q&A examples with expected tool calls"
    - path: resources/demo-script.md
      description: "Step-by-step demo walkthrough for stakeholders"
  routing:
    - path: routing/keywords.yaml
      description: "Domain routing keywords and configuration"
  domain_packs:
    - path: domain_packs/operations.yaml
      description: "Operations domain: volumes, rates, operational performance"
---

# AI Analyst Reference

Guardrails, domain routing, and metric reference for conversational BI using dbt's Semantic Layer.

**Core principle:** Only use certified metrics via dbt MCP Semantic Layer API (`mcp__dbt__query_metrics`). Never calculate metrics manually.

---

## Domain Routing

Before answering ANY business question, you MUST route to the appropriate domain pack.

### Routing Configuration

Domain routing uses keyword matching defined in `routing/keywords.yaml`.

### Routing Algorithm

```
1. Parse user question (case-insensitive)
2. For each domain in priority order:
   a. Check if question contains any domain keywords
   b. Count keyword matches
3. Select domain with most matches (priority breaks ties)
4. If no matches found:
   a. Ask user to clarify which domain applies
   b. Suggest available domains with examples
5. Load selected domain pack from domain_packs/{domain}.yaml
6. Apply domain-specific guardrails to response
```

### Available Domains

| Domain | Priority | Status | Description |
|--------|----------|--------|-------------|
| `operations` | 1 | Active | Processing volumes, approval/decline rates, operational performance |
| `finance` | 2 | Placeholder | Revenue, costs, margins, financial performance |
| `growth` | 3 | Placeholder | Customer acquisition, activation, retention, lifecycle |

### Domain Selection Examples

**Operations domain triggers:**
- "What is our approval rate?" -> `operations` (keyword: "approval rate")
- "Show me transaction volume by product" -> `operations` (keyword: "transaction volume")
- "What are the top decline reasons?" -> `operations` (keyword: "decline")

**Clarification needed:**
- "How are we doing?" -> No specific keywords -> Ask user: "Which area would you like to analyze: operational performance (approval rates, volumes), financial metrics, or customer growth?"

### Loading Domain Packs

Once domain is selected, load the domain pack:

```
Domain Pack Location: domain_packs/{domain}.yaml

Contents:
- semantic_layer.metrics: Available metrics with descriptions
- semantic_layer.dimensions: Grouping/filtering options
- question_templates: Common question patterns
- guardrails: Domain-specific rules and thresholds
- routing.keywords: Keywords that trigger this domain
- routing.negative_keywords: Keywords that exclude this domain
```

### Applying Domain Guardrails

After loading domain pack, enforce its guardrails:

1. **Metric expectations**: Check if returned values are within expected ranges
2. **Warning thresholds**: Flag anomalies (e.g., approval rate < 70%)
3. **Assumptions**: Apply default behaviors (e.g., UTC timezone, daily grain)
4. **Rules**: Follow domain-specific requirements
5. **Anti-patterns**: Avoid documented pitfalls

---

## Quick Reference

### Approved Tools (USE THESE)

| Tool | Purpose | Example |
|------|---------|---------|
| `mcp__dbt__query_metrics` | Query certified metrics | Decline rates, volumes |
| `mcp__dbt__list_metrics` | Discover available metrics | "What metrics exist?" |
| `mcp__dbt__get_dimensions` | Get grouping options | "What can I filter by?" |
| `mcp__dbt__list_saved_queries` | Find pre-built queries | Common analyses |

### Forbidden Patterns (NEVER DO)

| Pattern | Why It's Forbidden |
|---------|-------------------|
| `execute_sql` with raw tables | Bypasses certified definitions |
| Manual `SUM()`, `COUNT()` | May calculate incorrectly |
| Direct table JOINs | May produce wrong grain |
| Calculations outside semantic layer | Not validated or governed |

---

## Semantic Layer Query Patterns

```python
# Discover available metrics
mcp__dbt__list_metrics()

# Get grouping options for a metric
mcp__dbt__get_dimensions(metrics=["relevant_metric"])

# Query certified metrics
mcp__dbt__query_metrics(
    metrics=["metric_name"],
    group_by=[{"name": "dimension", "grain": None, "type": "dimension"}],
    order_by=[{"name": "metric_name", "descending": True}],
    limit=10
)
```

---

## Response Format

Standard format for business question answers:

```
## Answer

[Direct answer to the question in 1-2 sentences]

## Details

| Dimension | Metric Value |
|-----------|--------------|
| ...       | ...          |

## Insights

- [Key observation 1]
- [Key observation 2]

## Data Source

Metrics from: `[semantic_model_name]`
Time range: [date range queried]
```

---

## When You Cannot Answer

If a question cannot be answered with available metrics:

```
I don't have a certified metric for [requested measure].

**Available related metrics:**
- [similar metric 1]
- [similar metric 2]

**Would you like me to:**
1. Show [alternative metric] instead?
2. Explain what data would be needed?
```

**NEVER** attempt to answer with direct SQL or manual calculations.

---

## Available Semantic Models

Load `resources/metric-reference.md` for the complete list of:
- Available metrics (with formulas)
- Available dimensions (with sample values)
- Example queries (with expected outputs)

---

## Demo Mode

When demonstrating to stakeholders, load `resources/demo-script.md` for:
- Recommended question sequence
- Expected responses
- Talking points for each insight

---

## 🔒 Agent Governance Framework (NEW)

**Source:** Knowledge Engineering Research Synthesis (2026-01-12) - PDP-PEP Model

### The Governance Problem

Agents bypass individual user access controls when querying data directly. Current state: wide-open access to semantic layer.

### Future State: PDP-PEP Hybrid Model

| Component | Role | dbt-agent Implementation |
|-----------|------|--------------------------|
| **PDP** (Policy Decision Point) | Central authority establishing rules | Semantic layer metric definitions |
| **PEP** (Policy Execution Points) | Distributed enforcement | Domain packs with guardrails |

### Audit Trail Requirements (To Implement)

For full governance, AI agents need:

1. **Agent Identification** - Tag queries with agent ID
   - Example: `-- agent: ai-analyst-profile, session: xyz123`

2. **Query Logging** - Audit what was queried, when, by whom
   - Current: No logging
   - Future: Session-level query log

3. **Role-Based Access** - Distinguish humans vs bots
   - Current: Same MCP tools for all
   - Future: Scoped permissions per agent type

4. **Anomaly Detection** - Flag unusual patterns
   - Example: 1000x normal query volume
   - Example: Access outside business hours

### Current Guardrails (Active)

This skill enforces basic governance via:
- ✅ Semantic Layer API-only queries (no raw SQL)
- ✅ Certified metrics only (no manual calculations)
- ✅ Domain routing with guardrails
- ❌ No audit logging yet
- ❌ No agent identification yet

### Reference

- Modern Data 101: "Agents bypass user access controls when querying directly."
- Recommendation: Treat governance as Phase 2 after basic agent functionality is proven.
