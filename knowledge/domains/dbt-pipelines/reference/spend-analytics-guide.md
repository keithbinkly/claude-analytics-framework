# Spend Analytics Pipeline — Analyst Guide

Last verified: 2026-03-11 via dbt Semantic Layer API

---

## What This Pipeline Contains

The spend analytics pipeline tracks **authorization-level transaction data** across all BaaS partner portfolios. It covers purchase/spend transactions only (excludes ACH, ATM, P2P).

**Grain:** One row per merchant × date × product_stack × POS entry mode × card present flag × response code combination.

**Time range:** Data available from April 2025 forward. **Reliable data starts November 2025** (see Data Quality Notes below).

---

## How to Query: Semantic Layer

All spend metrics are queryable through the dbt Semantic Layer. You can use:
- **dbt MCP tools** in Claude Code (`query_metrics`, `list_metrics`, `get_dimensions`)
- **dbt Cloud Semantic Layer API** (GraphQL endpoint)
- **Tableau** via the Semantic Layer connector

### Quick Start Examples

**Monthly volume trend:**
```
metrics: [spend_total_auth_attempts, spend_total_approvals, spend_total_declines]
group_by: metric_time (MONTH)
order_by: metric_time DESC
```

**Approval rate by partner:**
```
metrics: [spend_total_auth_attempts, spend_approval_rate_by_count]
group_by: product_stack, metric_time (MONTH)
```

**Decline reason breakdown:**
```
metrics: [spend_total_declines]
group_by: responsecode
order_by: spend_total_declines DESC
```

**eWallet adoption trend:**
```
metrics: [spend_ewallet_share_by_count, spend_apple_pay_cnt, spend_google_pay_cnt]
group_by: metric_time (MONTH)
```

---

## Available Metrics (53 total)

### Core Volume Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `spend_total_auth_attempts` | count | Total purchase auth attempts (approved + declined) |
| `spend_total_approvals` | count | Approved transaction count |
| `spend_total_declines` | count | Declined transaction count |
| `spend_total_auth_attempt_amount` | $ | Total dollar volume of all attempts |
| `spend_total_approval_amount` | $ | Total approved dollar volume |
| `spend_total_decline_amount` | $ | Total declined dollar volume |

### Rate Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `spend_approval_rate_by_count` | ratio | Approved / Total attempts (by txn count) |
| `spend_approval_rate_by_amount` | ratio | Approved / Total attempts (by $ volume) |
| `spend_decline_rate_by_count` | ratio | Declined / Total attempts |
| `spend_decline_rate_by_amount` | ratio | Declined / Total attempts (by $) |
| `spend_avg_attempt_transaction_size` | ratio | Avg $ per attempt |
| `spend_avg_approval_transaction_size` | ratio | Avg $ per approval |
| `spend_avg_decline_transaction_size` | ratio | Avg $ per decline |

### Channel Metrics (Card Present vs Card Not Present)
| Metric | Type | Description |
|--------|------|-------------|
| `spend_cp_approval_rate` | derived | Card-present approval rate |
| `spend_cnp_approval_rate` | derived | Card-not-present approval rate |
| `spend_cp_share_of_volume` | derived | % of total that is card-present |
| `spend_approval_rate_gap_cp_vs_cnp` | derived | CP minus CNP approval rate (pp) |
| `spend_cp_attempt_cnt` / `approve_cnt` / `decline_cnt` | count | CP breakdown |
| `spend_cnp_attempt_cnt` / `approve_cnt` / `decline_cnt` | count | CNP breakdown |

### POS Entry Mode Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `spend_chip_attempt_cnt` / `approve_cnt` | count | Chip (EMV) transactions |
| `spend_chip_approval_rate` | derived | Chip approval rate |
| `spend_contactless_attempt_cnt` / `approve_cnt` | count | NFC/tap transactions |
| `spend_contactless_approval_rate` | derived | Contactless approval rate |
| `spend_contactless_share_of_cp` | derived | Contactless as % of card-present |
| `spend_manual_entry_attempt_cnt` / `approve_cnt` | count | Keyed transactions |
| `spend_manual_entry_approval_rate` | derived | Manual entry approval rate |

### eWallet Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `spend_ewallet_total_amt` / `cnt` | count/$ | All digital wallet transactions |
| `spend_ewallet_share_by_count` / `by_amount` | ratio | eWallet as % of total |
| `spend_apple_pay_amt` / `cnt` | count/$ | Apple Pay volume |
| `spend_google_pay_amt` / `cnt` | count/$ | Google Pay volume |
| `spend_samsung_pay_amt` / `cnt` | count/$ | Samsung Pay volume |
| `spend_apple_pay_share` | ratio | Apple Pay as % of eWallet |

### Cardholder-Level Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `spend_distinct_cardholders` | count | Unique cardholders who attempted txns |
| `spend_distinct_cardholders_with_declines` | count | Cardholders with 1+ decline |
| `spend_pct_cardholders_affected_by_declines` | ratio | % of cardholders who experienced declines |
| `spend_declines_per_affected_cardholder` | ratio | Avg declines per declined cardholder |
| `spend_cardholder_total_attempts` / `approvals` / `declines` | count | Cardholder-grain totals |
| `spend_cardholder_decline_rate` | ratio | Cardholder-grain decline rate |

### 90-Day Active Cardholder Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `spend_active_90d_amt` / `cnt` | count/$ | Volume from 90-day active cardholders |
| `spend_active_90d_share_by_amount` / `by_count` | ratio | Active cardholder share |

---

## Available Dimensions (9)

| Dimension | Type | Values |
|-----------|------|--------|
| `metric_time` | Time | DAY, WEEK, MONTH, QUARTER, YEAR |
| `product_stack` | Categorical | Ceridian Dayforce, Amazon Flex Rewards, Intuit QuickBooks, Intuit Turbo, Wealthfront, TaxSlayer, TaxHawk, Green Dot Classic, Toast Wallet, others |
| `card_present` | Categorical | Card present vs not present flag |
| `pos_entry_mode` | Categorical | Chip, Magnetic Stripe, Contactless, Manual Entry, NULL (CNP) |
| `mcc_category` | Categorical | Services, Retail, Dining, Gas, Groceries & Warehouses, Transportation, Entertainment, Health & Drugstore, Automotive, Travel, Other |
| `mcc_desc` | Categorical | Granular MCC descriptions (e.g., "Fast food restaurants") |
| `merchant` | Categorical | Normalized merchant names |
| `responsecode` | Categorical | Auth response codes (APPROVED, INSUFFICIENT FUNDS, etc.) |
| `pin_sig` | Categorical | PIN vs signature verification |

---

## Known Baselines (Feb 2026, full month)

Use these as sanity checks when running queries:

| Metric | Value |
|--------|-------|
| Total auth attempts | 13.8M txn count |
| Total approved | 9.2M txn count |
| Total declined | 4.5M txn count |
| Attempt dollar volume | $607M |
| Approved dollar volume | $386M |
| Approval rate (count) | 67.0% |
| Approval rate (amount) | 63.5% |
| Avg transaction size | $44.10 |
| CP approval rate | 96.1% |
| CNP approval rate | 46.2% |
| CP share of volume | 41.8% |
| Distinct cardholders | 500K |
| % cardholders with declines | 77.0% |
| eWallet share (count) | 8.7% |
| Apple Pay txn count | 244K |

### Top Partners by Volume (Feb 2026)
| Partner | Auth Attempts | Approval Rate |
|---------|--------------|---------------|
| Ceridian Dayforce | 7.1M (52%) | 65.5% |
| Amazon Flex Rewards | 3.4M (25%) | 74.0% |
| Intuit Turbo | 1.5M (11%) | 56.4% |
| Intuit QuickBooks | 1.1M (8%) | 68.3% |
| Wealthfront | 365K (3%) | 83.3% |

### Top MCC Categories (Feb 2026)
| Category | Auth Attempts | Approved $ |
|----------|--------------|------------|
| Services | 3.8M | $146M |
| Retail | 2.8M | $67M |
| Dining | 2.4M | $39M |
| Gas | 1.7M | $30M |
| Groceries & Warehouses | 1.2M | $46M |

### Top Decline Reasons (Feb 2026)
| Reason | Count | % of Declines |
|--------|-------|---------------|
| INSUFFICIENT FUNDS | 2.6M | 57.5% |
| Insufficient Balance | 521K | 11.5% |
| Expiration Date Mismatch | 327K | 7.2% |
| Card in Pause Status | 296K | 6.5% |
| Unusual transaction | 167K | 3.7% |

---

## Caveats & Limitations

### 1. Pre-November 2025 volume spike is real (Card in Pause Status)
Data before November 2025 shows much higher attempt volumes (21-38M vs 14-15M post-Nov) and lower approval rates. This is **not a data quality issue** — it's a genuine business event. The cause was "Card in Pause Status" declines on Amazon Flex Rewards, which ramped from 1.7M/month (Jun 2025) to 9.0M/month (Oct 2025) before dropping 99% to 86K in November 2025 when the issue was resolved. All other decline reasons remained stable at 600-900K/month throughout. When analyzing long-term trends, be aware of this regime change and consider filtering by response code or using approved transaction metrics (which are smooth across the entire period).

### 2. POS entry mode is NULL for 76% of transactions
Most CNP (card-not-present) transactions have `pos_entry_mode = NULL`. The non-null values (Chip, Magnetic Stripe, Contactless, Manual Entry) only cover the ~42% that are card-present. When filtering by POS entry mode, be aware you're excluding the majority of volume.

### 3. Contactless volume appears near zero
Only 70-300 transactions/month are classified as "Contactless" — far below industry norms (20-40% of CP). Apple Pay transactions (200-400K/month) exist but are likely classified under Chip or NULL. **Do not use `spend_contactless_*` metrics for digital wallet analysis — use the `spend_ewallet_*` and `spend_apple_pay_*` metrics instead.**

### 4. CNP approval rate is 45-49% (below industry benchmark)
Industry benchmark for CNP is 70-85%, but this portfolio is BaaS prepaid cards where 69% of declines are balance-related (INSUFFICIENT FUNDS + Insufficient Balance). This is expected behavior for prepaid, not a performance issue.

### 5. Some small partners show 0% or 100% approval rates
- **TaxHawk** (26-94K attempts): 0% approval — likely expired tax refund cards with $0 balance
- **Credibly** (90-290 attempts): 0% approval — minimal volume
- **Green Dot Classic** (30-76K attempts): 100% approval — may only include posted transactions
- **Toast** (3-52 attempts): near-zero volume, ignore

### 6. Manual Entry shows 100% approval (suspicious)
127K manual entry transactions in Feb 2026 show 100% approval rate (industry benchmark: 70-85%). Likely a classification issue where only approved manual entries get POS entry mode tagged; declined ones fall to NULL.

### 7. Ratio metrics return decimals, not percentages
`spend_approval_rate_by_count` returns `0.67`, not `67`. Multiply by 100 for percentage display.

---

## Where This Data Lives

| Layer | Table | Grain |
|-------|-------|-------|
| Semantic Model | `mart_merchant_spend__auth_daily_metrics` | merchant × date × product_stack × pos_entry_mode × card_present × response_code |
| Semantic Model | `mart_merchant_spend__cardholder_auth_daily_metrics` | cardholder-level daily metrics |
| Mart | `mrt_merchant_spend__auth_daily_metrics` | Same as semantic model |
| Mart | `mrt_merchant_spend__cardholder_auth_daily_metrics` | Cardholder grain |

---

## Query Tips

1. **Always specify a date filter** for large queries — unfiltered queries scan the full history
2. **Use `limit` first** — test with `limit: 5` before running full queries
3. **Merchant dimension is high cardinality** — always use with `limit` or a `where` filter
4. **Weekly grain uses ISO weeks** (Monday start) — add 6 days for Saturday week-end dates
5. **`where` syntax uses Jinja**: `{{ Dimension('product_stack') }} = 'Amazon Flex Rewards'`
6. **Time filters**: `{{ TimeDimension('metric_time', 'MONTH') }} >= '2025-11-01'`
