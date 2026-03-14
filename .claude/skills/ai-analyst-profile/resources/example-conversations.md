# Example Conversations

This document contains example business questions and the expected AI Analyst responses using the dbt MCP Semantic Layer API.

---

## Example 1: Decline Rate Trend

### User Question
> "What's our weekly decline rate for the last month?"

### AI Analyst Response

First, query the certified metric:

```python
mcp__dbt__query_metrics(
    metrics=["spend_decline_rate_by_count"],
    group_by=[{"name": "metric_time", "grain": "WEEK", "type": "time_dimension"}],
    order_by=[{"name": "metric_time", "descending": True}],
    limit=4
)
```

**Answer:**

The weekly decline rate has been relatively stable around 30-32% over the past month:

| Week | Decline Rate |
|------|--------------|
| Nov 10 | 30.85% |
| Nov 3 | 29.57% |
| Oct 27 | 31.86% |
| Oct 20 | 31.75% |

**Insight:** Decline rates are consistent with no significant trending. The slight uptick on Oct 27 is within normal variance.

---

## Example 2: Top Merchants by Volume

### User Question
> "Which merchants have the most declines this month?"

### AI Analyst Response

```python
mcp__dbt__query_metrics(
    metrics=["spend_total_declines", "spend_decline_rate_by_count"],
    group_by=[{"name": "merchant", "grain": None, "type": "dimension"}],
    where="{{ TimeDimension('metric_time', 'MONTH') }} = '2025-11-01'",
    order_by=[{"name": "spend_total_declines", "descending": True}],
    limit=10
)
```

**Answer:**

Top 10 merchants by decline volume in November:

| Merchant | Declines | Decline Rate |
|----------|----------|--------------|
| GOOGLE | 45,230 | 28.4% |
| APPLE.COM/BILL | 38,102 | 31.2% |
| AMAZON | 32,891 | 25.8% |
| CASH APP | 28,445 | 35.1% |
| DOORDASH | 24,112 | 29.7% |

**Insight:** CASH APP has the highest decline rate (35.1%) among top merchants, suggesting potential investigation into insufficient funds patterns for that merchant.

---

## Example 3: Product Portfolio Comparison

### User Question
> "How do decline rates compare across our product portfolios?"

### AI Analyst Response

```python
mcp__dbt__query_metrics(
    metrics=["spend_decline_rate_by_count", "spend_total_auth_attempts"],
    group_by=[{"name": "product_stack", "grain": None, "type": "dimension"}],
    order_by=[{"name": "spend_total_auth_attempts", "descending": True}]
)
```

**Answer:**

Decline rates by product portfolio (sorted by volume):

| Product Stack | Auth Attempts | Decline Rate |
|---------------|---------------|--------------|
| Ceridian Dayforce | 2.8M | 28.3% |
| Amazon Flex Rewards | 1.4M | 32.1% |
| Intuit Turbo | 588K | 29.7% |
| Uber | 412K | 31.5% |

**Insight:** Amazon Flex Rewards has a notably higher decline rate (32.1%) compared to Ceridian Dayforce (28.3%). This may warrant investigation into cardholder spending patterns or merchant acceptance.

---

## Example 4: Card Present Analysis

### User Question
> "How do in-person transactions compare to online for declines?"

### AI Analyst Response

```python
mcp__dbt__query_metrics(
    metrics=["spend_decline_rate_by_count", "spend_total_auth_attempts"],
    group_by=[{"name": "card_present", "grain": None, "type": "dimension"}]
)
```

**Answer:**

| Channel | Auth Attempts | Decline Rate |
|---------|---------------|--------------|
| Card Present (In-Person) | 2.1M | 26.4% |
| Card Not Present (Online) | 3.4M | 33.8% |

**Insight:** Online transactions have a 7.4 percentage point higher decline rate than in-person. This is typical due to higher fraud screening on CNP transactions and insufficient funds at e-commerce merchants.

---

## Example 5: Decline Reasons

### User Question
> "What are the main reasons cards are getting declined?"

### AI Analyst Response

```python
mcp__dbt__query_metrics(
    metrics=["spend_total_declines"],
    group_by=[{"name": "responsecode", "grain": None, "type": "dimension"}],
    where="{{ Dimension('responsecode') }} != 'APPROVED'",
    order_by=[{"name": "spend_total_declines", "descending": True}],
    limit=5
)
```

**Answer:**

Top 5 decline reasons:

| Response Code | Declines | % of Total |
|---------------|----------|------------|
| INSUFFICIENT FUNDS | 912,340 | 55% |
| Insufficient Balance | 214,567 | 13% |
| Card in Pause Status | 115,890 | 7% |
| Exceeds Withdrawal Limit | 89,234 | 5% |
| Invalid Card Number | 45,678 | 3% |

**Insight:** Over half (55%) of all declines are due to "Insufficient Funds." This suggests opportunity for balance management features or cardholder education.

---

## Example 6: Cannot Answer (Proper Handling)

### User Question
> "What's our fraud rate by merchant?"

### AI Analyst Response

I don't have a certified fraud rate metric in the current semantic model.

**Available related metrics:**
- `spend_decline_rate_by_count` - Overall decline rate (includes fraud declines)
- `responsecode` dimension - Can filter for fraud-related response codes

**Alternative approach:**
I can show you declines by response code to identify fraud-related declines:

```python
mcp__dbt__query_metrics(
    metrics=["spend_total_declines"],
    group_by=[{"name": "responsecode", "grain": None, "type": "dimension"}],
    where="{{ Dimension('responsecode') }} IN ('Suspected Fraud', 'Pick Up Card', 'Lost Card', 'Stolen Card')"
)
```

Would you like me to run this alternative analysis?

---

## Conversation Best Practices

### DO

1. **Start with the metric** - Lead with the certified metric name
2. **Show the query** - Transparency builds trust
3. **Provide context** - What does this number mean?
4. **Highlight insights** - What should the user notice?
5. **Acknowledge limitations** - If data has known issues, say so

### DON'T

1. **Guess at metrics** - If unsure, ask or check `list_metrics()`
2. **Calculate manually** - Even simple math should use certified metrics
3. **Over-interpret** - State what the data shows, not speculation
4. **Hide anomalies** - Flag data quality issues prominently

---

## Placeholder: User-Specific Questions

*[This section will be populated with specific operational and financial questions provided by the user]*

### Operational Monitoring Questions
- TBD

### Financial Performance Questions
- TBD

### Trend Analysis Questions
- TBD
