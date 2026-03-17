# Posted Transactions Pipeline — Analyst Guide

Last verified: 2026-03-12 via dbt Cloud API

---

## Who This Is For

Analysts, data scientists, and BI developers who query the warehouse directly. You don't need to know dbt to use these tables — just SQL and Redshift.

---

## How to Connect

All tables live in **Redshift** under the `greendot` database:

```sql
-- Pattern:
SELECT * FROM dbt.<table_name> LIMIT 10;
```

The `dbt` schema contains all dbt-managed tables. No special access beyond standard Redshift credentials.

---

## The Two-Tier Architecture

There are two ways to get transaction data. Use the right one:

### Tier 1: Summary Table (fast, pre-aggregated)

**`dbt.stg_edw__fct_dly_acct_txn_summary`**

| Property | Value |
|----------|-------|
| Grain | One row per **account × date** |
| Columns | 115 (pre-aggregated counts and amounts) |
| Best for | Executive KPIs, account-level reporting, GDV totals, quick aggregates |
| History | Full history |
| Update frequency | Daily batch |

Pre-computed columns include: `purchase_txn_cnt`, `purchase_txn_amt`, `ach_txn_cnt`, `direct_deposit_txn_cnt`, `atm_withdrawal_txn_cnt`, `gdv_txn_cnt`, `card_present_purchase_txn_cnt`, and many more.

**Example — Monthly GDV by product:**
```sql
SELECT
    DATE_TRUNC('month', s.acct_txn_posted_dt_pt) AS month,
    p.product,
    SUM(s.gdv_txn_amt) AS gdv_dollars,
    SUM(s.gdv_txn_cnt) AS gdv_txn_count
FROM dbt.stg_edw__fct_dly_acct_txn_summary s
JOIN dbt.int_baas_account_details_core p ON s.acct_uid = p.acct_uid
WHERE s.acct_txn_posted_dt_pt >= '2025-01-01'
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC;
```

**When NOT to use:** If you need merchant name, MCC code, individual transaction amounts, or any dimension not in the 115 pre-agg columns → use Tier 2.

---

### Tier 2: Detail Tables (granular, event-level)

Two tables — one for **posted** (settled) transactions, one for **authorization** (attempted) transactions.

#### `dbt.int_transactions__posted_all`

| Property | Value |
|----------|-------|
| Grain | One row per **posted transaction** (`posted_txn_uid`) |
| Columns | 58 |
| Best for | Merchant-level analysis, MCC breakdowns, transaction classification, funds flow |
| History | 2021-01-01 forward |
| Update frequency | Daily incremental (3-day lookback) |
| Distribution key | `acct_uid` (queries filtering on account are fastest) |
| Sort key | `calendar_date, posted_txn_uid` |

**Key columns for analysts:**

| Column | Type | Description |
|--------|------|-------------|
| `posted_txn_uid` | bigint | Unique transaction ID (primary key) |
| `acct_uid` | bigint | Account ID — join to account tables on this |
| `calendar_date` | date | Transaction posted date |
| `calendar_month` | date | First of month (for monthly aggregation) |
| `total_post_amt` | numeric(20,4) | Transaction dollar amount |
| `credit_or_debit` | varchar(10) | 'CREDIT' or 'DEBIT' |
| `merchant_nm` | varchar(100) | Merchant name (raw, not normalized) |
| `mcc` | varchar(4) | Merchant category code |
| `card_present_ind` | boolean | True = in-store, False = online/CNP |
| `pin_used_ind` | boolean | True = PIN transaction |
| `product` | varchar(50) | Product name (e.g., "Ceridian Dayforce") |
| `portfolio` | varchar(50) | Partner portfolio name |
| `brand` | varchar(50) | Card brand |
| `baas_analytics_ind` | integer | 1 = BaaS partner program |
| `is_90_day_active` | integer | 1 = cardholder was active in last 90 days |
| `card_brand` | varchar(10) | Derived: 'Visa', 'Mastercard', or 'Other' |
| `transaction_flow` | varchar(18) | 'Funds In', 'Funds Out', or 'Transactions Other' |
| `transaction_category` | varchar(21) | High-level: 'Purchase', 'ACH', 'ATM Withdrawal', etc. |
| `transaction_subcategory` | varchar(255) | Granular: 'ACH In (Push)', 'ATM Withdrawal In-Network', etc. |
| `is_fee` | boolean | True = fee transaction |
| `is_adjustment` | boolean | True = adjustment/internal credit |
| `net_post_amt` | numeric(31,4) | Signed amount (positive = expected direction) |
| `net_post_cnt` | integer | Signed count (+1 or -1) for netting |
| `reversal_ind` | boolean | True = reversal of a prior transaction |
| `pos_entry_mode_desc` | varchar(255) | How the card was read (chip, swipe, etc.) |
| `network_lvl1` | varchar(50) | Payment network (Visa, Mastercard, etc.) |

**Example — Purchase volume by merchant category:**
```sql
SELECT
    mcc,
    merchant_nm,
    COUNT(*) AS txn_count,
    SUM(total_post_amt) AS total_dollars
FROM dbt.int_transactions__posted_all
WHERE calendar_date >= '2026-01-01'
  AND transaction_category = 'Purchase'
  AND baas_analytics_ind = 1
GROUP BY 1, 2
ORDER BY 4 DESC
LIMIT 20;
```

**Example — Funds flow (in vs out) by partner:**
```sql
SELECT
    portfolio,
    transaction_flow,
    SUM(net_post_amt) AS net_dollars,
    SUM(net_post_cnt) AS net_txn_count
FROM dbt.int_transactions__posted_all
WHERE calendar_date BETWEEN '2026-02-01' AND '2026-02-28'
GROUP BY 1, 2
ORDER BY 1, 2;
```

---

#### `dbt.int_transactions__auth_all`

| Property | Value |
|----------|-------|
| Grain | One row per **authorization attempt** (`auth_uid`) |
| Columns | 55 |
| Best for | Decline analysis, approval rates, auth reason codes, spend analytics |
| History | 2021-01-01 forward |
| Update frequency | Daily incremental (3-day lookback) |
| Distribution key | `acct_uid` |
| Sort key | `calendar_date, auth_uid` |

**Auth-specific columns (not in posted):**

| Column | Type | Description |
|--------|------|-------------|
| `auth_uid` | bigint | Unique authorization ID (primary key) |
| `total_auth_amt` | numeric(20,4) | Authorization attempt dollar amount |
| `auth_reason_desc` | varchar(255) | EDW auth reason (e.g., 'Success', 'Insufficient Funds') |
| `is_success` | boolean | True = approved |
| `is_decline` | boolean | True = declined |
| `gbos_responsedescription` | varchar(800) | GBOS-level decline reason (more granular) |
| `auth_attempt_amt` | numeric(31,4) | Signed attempt amount |
| `auth_attempt_cnt` | integer | Signed attempt count |
| `decline_amt` | numeric(31,4) | Decline amount (0 if approved) |
| `decline_cnt` | integer | Decline count (0 if approved) |
| `approve_amt` | numeric(32,4) | Approved amount (0 if declined) |
| `approve_cnt` | integer | Approved count (0 if declined) |

**Example — Approval rate by partner (monthly):**
```sql
SELECT
    DATE_TRUNC('month', calendar_date) AS month,
    portfolio,
    COUNT(*) AS total_auths,
    SUM(approve_cnt) AS approvals,
    SUM(decline_cnt) AS declines,
    ROUND(SUM(approve_cnt)::DECIMAL / NULLIF(COUNT(*), 0), 4) AS approval_rate
FROM dbt.int_transactions__auth_all
WHERE calendar_date >= '2025-11-01'
  AND purchase_txn_ind = true
  AND baas_analytics_ind = 1
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC;
```

**Example — Top decline reasons:**
```sql
SELECT
    gbos_responsedescription,
    COUNT(*) AS decline_count,
    SUM(ABS(decline_amt)) AS decline_dollars
FROM dbt.int_transactions__auth_all
WHERE calendar_date >= '2026-02-01'
  AND is_decline = true
  AND purchase_txn_ind = true
GROUP BY 1
ORDER BY 2 DESC
LIMIT 15;
```

---

## eWallet Data

Digital wallet (Apple Pay, Google Pay, Samsung Pay) attribution lives in **separate tables**:

- `dbt.int_transactions__posted_ewallet` — eWallet flag for posted transactions
- `dbt.int_transactions__auth_ewallet` — eWallet flag for auth transactions

**Join pattern:**
```sql
SELECT
    p.*,
    ew.ewallet_type
FROM dbt.int_transactions__posted_all p
LEFT JOIN dbt.int_transactions__posted_ewallet ew
    ON p.posted_txn_uid = ew.posted_txn_uid
WHERE p.calendar_date >= '2026-01-01';
```

---

## Downstream Marts (Pre-Aggregated)

If someone already built the aggregation you need:

| Table | Grain | Use Case |
|-------|-------|----------|
| `dbt.mrt_merchant_spend__auth_daily_metrics` | merchant × date × product × POS × card_present × response | Spend analytics (auth attempts, approvals, declines) |
| `dbt.mrt_merchant_spend__cardholder_auth_daily_metrics` | cardholder × date | Cardholder-level spend metrics |
| `dbt.mrt_merchant_auth_decline_analytics` | decline analytics | Auth decline deep dives |

These marts also have **semantic layer** metrics queryable through Tableau or the dbt Semantic Layer API. See `shared/reference/spend-analytics-guide.md` for the full 53-metric catalog.

---

## Common Filters

### BaaS Partners Only
```sql
WHERE baas_analytics_ind = 1
```

### Purchases Only (excludes fees, ACH, ATM, adjustments)
```sql
WHERE purchase_txn_ind = true
```

### Excluding Fees and Adjustments
```sql
WHERE is_fee = false AND is_adjustment = false
```

### Specific Partner
```sql
WHERE portfolio = 'Amazon Flex Rewards'
-- or
WHERE product = 'Ceridian Dayforce'
```

### Card Present vs Card Not Present
```sql
WHERE card_present_ind = true   -- in-store
WHERE card_present_ind = false  -- online / CNP
```

---

## Performance Tips

1. **Always filter on `calendar_date`** — these tables are sorted by date. Unfiltered queries scan everything.
2. **Filter on `acct_uid` when possible** — tables are distributed by account, so account-specific queries are fastest.
3. **Use `LIMIT` during development** — the detail tables have hundreds of millions of rows.
4. **Prefer the summary table** (`fct_dly_acct_txn_summary`) for simple KPIs — it's ~100x smaller than the detail tables.
5. **Avoid `SELECT *`** — these tables are wide (55-115 columns). Select only what you need.

---

## Caveats

1. **Posted ≠ Auth.** Posted transactions are settled. Auth transactions include both approved and declined attempts. For volume/approval rate analysis, use auth. For actual money movement, use posted.

2. **`net_post_amt` is signed.** Funds In transactions are positive, Funds Out are positive (in their expected direction), reversals are negative. Use `total_post_amt` for unsigned amounts.

3. **`merchant_nm` is raw.** Not normalized — "AMAZON.COM" and "Amazon.com" are different values. For merchant analytics, use the spend marts which have normalized merchant names.

4. **Auth table has no `transaction_subcategory` granularity for PIN/signature.** The `transaction_subcategory` shows "Purchase - Unknown" for all purchases. PIN vs signature splitting is only reliable in the posted table.

5. **3-day lookback means late-arriving data is handled.** Transactions that post 1-2 days late are picked up on the next run. Don't worry about gaps at recent date boundaries.

6. **History starts 2021-01-01** but reliable BaaS partner data starts later (varies by partner onboarding date).

---

## Quick Reference

| Question | Table | Key Columns |
|----------|-------|-------------|
| "What's our total GDV?" | `fct_dly_acct_txn_summary` | `gdv_txn_amt` |
| "Purchase volume by merchant?" | `int_transactions__posted_all` | `merchant_nm`, `total_post_amt`, `purchase_txn_ind` |
| "Approval rate by partner?" | `int_transactions__auth_all` | `approve_cnt`, `decline_cnt`, `portfolio` |
| "Top decline reasons?" | `int_transactions__auth_all` | `gbos_responsedescription`, `is_decline` |
| "Card present vs online split?" | Either detail table | `card_present_ind` |
| "Apple Pay adoption?" | `int_transactions__*_ewallet` | `ewallet_type` |
| "Funds in vs funds out?" | `int_transactions__posted_all` | `transaction_flow`, `net_post_amt` |
| "ATM usage?" | `int_transactions__posted_all` | `transaction_category = 'ATM Withdrawal'` |
