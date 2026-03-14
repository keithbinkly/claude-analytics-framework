# Metric Reference: Merchant Auth/Decline Analytics

## Semantic Model Overview

| Property | Value |
|----------|-------|
| **Model Name** | `merchant_auth_decline_analytics` |
| **Base Table** | `mrt_merchant_auth_decline__semantic_base` |
| **Grain** | Daily × Merchant × Dimensions |
| **Data Freshness** | Updated daily |
| **Date Range** | 2025-05-21 to present |

---

## Available Metrics (13 total)

### Volume Metrics (6)

| Metric Name | Label | Type | Description |
|-------------|-------|------|-------------|
| `spend_total_auth_attempts` | Total Authorization Attempts | simple | Count of all auth attempts (approved + declined) |
| `spend_total_auth_attempt_amount` | Total Authorization Amount ($) | simple | Dollar value of all auth attempts |
| `spend_total_declines` | Total Declined Transactions | simple | Count of declined transactions |
| `spend_total_decline_amount` | Total Declined Amount ($) | simple | Dollar value of declines |
| `spend_total_approvals` | Total Approved Transactions | simple | Count of approved transactions |
| `spend_total_approval_amount` | Total Approved Amount ($) | simple | Dollar value of approvals |

### Ratio Metrics (7)

| Metric Name | Label | Formula | Format |
|-------------|-------|---------|--------|
| `spend_decline_rate_by_count` | Decline Rate (%) | decline_cnt / attempt_cnt | percent |
| `spend_decline_rate_by_amount` | Decline Rate by Amount (%) | decline_amt / attempt_amt | percent |
| `spend_approval_rate_by_count` | Approval Rate (%) | approve_cnt / attempt_cnt | percent |
| `spend_approval_rate_by_amount` | Approval Rate by Amount (%) | approve_amt / attempt_amt | percent |
| `spend_avg_decline_transaction_size` | Avg Decline Size ($) | decline_amt / decline_cnt | currency |
| `spend_avg_approval_transaction_size` | Avg Approval Size ($) | approve_amt / approve_cnt | currency |
| `spend_avg_attempt_transaction_size` | Avg Transaction Size ($) | attempt_amt / attempt_cnt | currency |

---

## Available Dimensions (9)

### Time Dimension

| Dimension | Supported Grains | Example |
|-----------|------------------|---------|
| `metric_time` | DAY, WEEK, MONTH, QUARTER, YEAR | `{"name": "metric_time", "grain": "WEEK", "type": "time_dimension"}` |

### Categorical Dimensions

| Dimension | Description | Cardinality | Sample Values |
|-----------|-------------|-------------|---------------|
| `product_stack` | Product portfolio | ~10 | 'Ceridian Dayforce', 'Amazon Flex Rewards', 'Uber' |
| `merchant` | Normalized merchant name | High | 'WALMART', 'AMAZON', 'GOOGLE' |
| `responsecode` | Authorization response | ~20 | 'APPROVED', 'Insufficient Funds', 'Card in Pause Status' |
| `card_present` | Card physically present | 2 | 'true', 'false' |
| `pos_entry_mode` | POS entry method | ~10 | 'Chip', 'Contactless', 'ECOM', 'Magnetic Stripe' |
| `pin_sig` | PIN vs Signature | 2 | 'true' (PIN), 'false' (signature) |
| `mcc_category` | Merchant category (high-level) | ~15 | 'Retail', 'Dining', 'Travel', 'Gas' |
| `mcc_desc` | Merchant category (granular) | ~100 | 'Fast food restaurants', 'Grocery stores' |

---

## Query Patterns

### Pattern 1: Time Series Trend

**Question:** "What is the weekly decline rate trend?"

```python
mcp__dbt__query_metrics(
    metrics=["spend_decline_rate_by_count"],
    group_by=[{"name": "metric_time", "grain": "WEEK", "type": "time_dimension"}],
    order_by=[{"name": "metric_time", "descending": True}],
    limit=12
)
```

### Pattern 2: Top N Analysis

**Question:** "Which merchants have the highest decline counts?"

```python
mcp__dbt__query_metrics(
    metrics=["spend_total_declines"],
    group_by=[{"name": "merchant", "grain": None, "type": "dimension"}],
    order_by=[{"name": "spend_total_declines", "descending": True}],
    limit=10
)
```

### Pattern 3: Dimension Comparison

**Question:** "Compare decline rates across product portfolios"

```python
mcp__dbt__query_metrics(
    metrics=["spend_decline_rate_by_count", "spend_total_declines"],
    group_by=[{"name": "product_stack", "grain": None, "type": "dimension"}],
    order_by=[{"name": "spend_decline_rate_by_count", "descending": True}]
)
```

### Pattern 4: Filtered Query

**Question:** "What are the top decline reasons (excluding approved)?"

```python
mcp__dbt__query_metrics(
    metrics=["spend_total_declines"],
    group_by=[{"name": "responsecode", "grain": None, "type": "dimension"}],
    where="{{ Dimension('responsecode') }} != 'APPROVED'",
    order_by=[{"name": "spend_total_declines", "descending": True}],
    limit=10
)
```

### Pattern 5: Time-Filtered Comparison

**Question:** "Monthly decline trend for last 3 months"

```python
mcp__dbt__query_metrics(
    metrics=["spend_decline_rate_by_count", "spend_total_auth_attempts"],
    group_by=[{"name": "metric_time", "grain": "MONTH", "type": "time_dimension"}],
    order_by=[{"name": "metric_time", "descending": True}],
    limit=3
)
```

---

## Known Data Quality Notes

### Anomaly: October 6-12, 2025

| Issue | Details |
|-------|---------|
| **Date Range** | 2025-10-06 to 2025-10-12 |
| **Symptom** | 92.4% decline rate (vs normal ~30%) |
| **Impact** | Weekly aggregations including this period are skewed |
| **Recommendation** | Filter to dates after Oct 15, 2025 for demos |

### High-Cardinality Dimensions

| Dimension | Note |
|-----------|------|
| `merchant` | ALWAYS use `limit` to prevent large result sets |
| `mcc_desc` | May have NULLs for historical data (pre-Nov 2025) |

---

## Metric Relationships

```
                    ┌─────────────────────┐
                    │ spend_total_auth_   │
                    │ attempts            │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           ▼                                       ▼
┌─────────────────────┐               ┌─────────────────────┐
│ spend_total_        │               │ spend_total_        │
│ declines            │               │ approvals           │
└──────────┬──────────┘               └──────────┬──────────┘
           │                                     │
           ▼                                     ▼
┌─────────────────────┐               ┌─────────────────────┐
│ spend_decline_rate_ │               │ spend_approval_rate_│
│ by_count            │               │ by_count            │
└─────────────────────┘               └─────────────────────┘

Key: decline_rate + approval_rate = 100% (for count-based metrics)
```
