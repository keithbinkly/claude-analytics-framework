# Demo Script: Conversational BI with Semantic Layer

## Overview

This demo showcases how an AI Analyst can answer business questions accurately using dbt's Semantic Layer via the dbt MCP API. The demonstration emphasizes **governed, certified metrics** that prevent incorrect answers from ad-hoc SQL.

**Target Audience:** Business stakeholders
**Duration:** 15-20 minutes
**Semantic Model:** Merchant Authorization & Decline Analytics

---

## Demo Setup

### Pre-Demo Checklist

- [ ] Verify MCP connection to dbt semantic layer
- [ ] Confirm data freshness (check last update date)
- [ ] Load `ai-analyst-profile` skill
- [ ] Have metric reference open for backup

### Recommended Date Filter

Use **November 1-12, 2025** for clean data. Avoid October dates due to known anomaly.

---

## Demo Script

### Opening (2 min)

**Talking Point:**
> "Today I'll show you how we've enabled AI-powered analytics using certified business metrics. Instead of writing SQL that could produce incorrect numbers, the AI uses our governed semantic layer - the same metrics we use in dashboards and reports."

### Question 1: High-Level Trend (3 min)

**Ask the AI:**
> "What's our weekly decline rate for the last month?"

**Expected Response:**
- AI calls `query_metrics` with weekly time grain
- Shows ~30% decline rate with weekly breakdown
- Notes stability in trend

**Talking Point:**
> "Notice the AI used our certified 'decline rate by count' metric. It didn't try to calculate this from raw tables - it used the same definition as our dashboards."

---

### Question 2: Product Comparison (3 min)

**Ask the AI:**
> "How do decline rates compare across our product portfolios?"

**Expected Response:**
- Shows product_stack dimension breakdown
- Highlights Ceridian (~28%) vs Amazon Flex (~32%) difference
- Provides volume context

**Talking Point:**
> "The AI grouped by our 'product stack' dimension and gave us both the rate AND the volume. Notice it interpreted my question and chose appropriate metrics automatically."

---

### Question 3: Root Cause Analysis (3 min)

**Ask the AI:**
> "What are the main reasons cards are getting declined?"

**Expected Response:**
- Filters to non-APPROVED response codes
- Shows "Insufficient Funds" at 55%
- Provides actionable insight

**Talking Point:**
> "This is operational intelligence - 55% of declines are insufficient funds. That's actionable for our product team to consider balance alerts or spending insights features."

---

### Question 4: Channel Analysis (3 min)

**Ask the AI:**
> "How do in-person and online transactions compare?"

**Expected Response:**
- Uses card_present dimension
- Shows CNP has higher decline rate (~34% vs ~26%)
- Explains typical reasoning

**Talking Point:**
> "The AI didn't just give numbers - it provided context. Online transactions typically have higher decline rates due to fraud screening. That's domain knowledge embedded in how it interprets results."

---

### Question 5: Guardrails Demo (3 min)

**Ask the AI:**
> "Can you calculate the fraud rate by merchant?"

**Expected Response:**
- AI acknowledges no "fraud rate" metric exists
- Suggests alternatives (response code filtering)
- Does NOT attempt raw SQL

**Talking Point:**
> "This is critical - the AI didn't make something up. It acknowledged the limitation and suggested what we CAN do. This prevents incorrect 'answers' that could mislead decisions."

---

### Closing (2 min)

**Key Messages:**

1. **Accuracy:** Uses certified metrics, not ad-hoc SQL
2. **Consistency:** Same numbers as dashboards and reports
3. **Guardrails:** Won't produce ungoverned metrics
4. **Accessibility:** Natural language, no SQL required
5. **Transparency:** Shows what metric was used

**Next Steps:**
- "We can extend this to other semantic models"
- "Users can ask their own questions"
- "Metrics are maintained by the data team"

---

## FAQ / Objection Handling

### "Can it handle any question?"

> "It can answer questions that map to our certified metrics. If a metric doesn't exist, it will say so and suggest alternatives. We prefer this to making up numbers."

### "How accurate is it?"

> "It uses the exact same metric definitions as our dashboards. The numbers will match because they come from the same semantic layer."

### "Can it access sensitive data?"

> "It only has access to aggregated metrics at the level we've defined. It cannot query individual customer records or sensitive PII."

### "What if the metric definition changes?"

> "The semantic layer is maintained by the data team. When we update a metric, the AI automatically uses the new definition - no retraining needed."

---

## Backup Queries

If something goes wrong, these are known-good queries:

### Basic Health Check
```python
mcp__dbt__list_metrics()
```

### Simple Volume Query
```python
mcp__dbt__query_metrics(
    metrics=["spend_total_auth_attempts"],
    limit=1
)
```

### Weekly Trend
```python
mcp__dbt__query_metrics(
    metrics=["spend_decline_rate_by_count"],
    group_by=[{"name": "metric_time", "grain": "WEEK", "type": "time_dimension"}],
    order_by=[{"name": "metric_time", "descending": True}],
    limit=4
)
```

---

## Post-Demo Notes

After the demo, document:
- [ ] Questions asked that we couldn't answer
- [ ] Metrics requested that don't exist
- [ ] Unexpected responses or errors
- [ ] Stakeholder feedback

This feedback informs future semantic model enhancements.
