# GBOS Wallet & Tokenization Patterns

**Created:** December 17, 2025
**Source:** Phase 0 eWallet Deep Dive (merchant-spend-feature-expansion)
**Validated:** 181K transactions tested, 100% match rate

---

## Quick Reference

### When to Use This Guide
- Building eWallet / digital wallet metrics
- Working with tokenized transaction data
- Joining `gbos.paymentidentifierdevice` or `gbos.wallettype`
- Distinguishing Apple Pay vs Google Pay vs merchant tokens

### Key Tables

| Table | Purpose | Key Column |
|-------|---------|------------|
| `gbos.posttransaction` | Transaction facts | `paymentidentifierdevicekey` |
| `gbos.paymentidentifierdevice` | **History table** - device→wallet mappings over time | `paymentidentifierdevicekey`, `wallettypekey`, `createdate` |
| `gbos.wallettype` | Wallet type dimension | `wallettypekey`, `wallettype`, `ismerchant` |

---

## Critical Knowledge

### 1. `paymentidentifierdevice` is a HISTORY TABLE

**⚠️ One device key can have MULTIPLE wallet type records over time.**

Real example from production:
```
paymentidentifierdevicekey: 2068051
├── Record 1: wallettype='Unknown'        createdate=2023-03-03
├── Record 2: wallettype='Google Inc.'    createdate=2022-05-09
└── Record 3: wallettype='Google Inc - Ecomm' createdate=2021-09-20
```

**Scale of fan-out:**
- 7.8M devices have different wallet types across records
- 1.5M devices have same wallet, multiple records

### 2. Point-in-Time Join Pattern (VALIDATED)

**Always use `createdate` for point-in-time filtering:**

```sql
SELECT
    pt.posttransactionkey,
    pt.sor_uid,
    wt.wallettype,
    wt.ismerchant
FROM gbos.posttransaction pt
JOIN gbos.paymentidentifierdevice pid
    ON pid.paymentidentifierdevicekey = pt.paymentidentifierdevicekey
    AND pid.createdate <= pt.createdate  -- Exclude future device records
JOIN gbos.wallettype wt
    ON pid.wallettypekey = wt.wallettypekey
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY pt.posttransactionkey, pt.sor_uid
    ORDER BY pid.createdate DESC  -- Pick latest valid record
) = 1
```

**Why this works:**
- `createdate` tracks when the device-wallet association was created
- Filter `createdate <= pt.createdate` excludes future updates
- `ORDER BY createdate DESC` picks the most recent valid state

**Why NOT `changedate`:**
- `changedate` can be in the FUTURE relative to transaction date
- Using `changedate` would incorrectly attribute future wallet states to past transactions

### 3. ismerchant Classification

The `ismerchant` boolean on `gbos.wallettype` determines transaction type:

```
paymentidentifierdevicekey IS NOT NULL → Tokenized transaction
├── ismerchant = 0 → Digital Wallet (Apple Pay, Google Pay, Samsung Pay)
└── ismerchant = 1 → Merchant Token (stored card - Netflix, Amazon subscriptions)

paymentidentifierdevicekey IS NULL → Not tokenized (regular card swipe/dip)
```

**Production distribution (7 days, Dec 2025):**

| ismerchant | Type | Example | Volume |
|------------|------|---------|--------|
| 0 | Digital Wallet | Apple Pay | 410K |
| 0 | Digital Wallet | Google Inc. | 88K |
| 1 | Merchant Token | Unknown | 530K |
| 1 | Merchant Token | Amazon | 106K |

### 4. Wallet Type Consolidation Map

Raw values need consolidation for reporting:

```sql
CASE
    WHEN wt.wallettype IN ('Apple Pay', 'Apple Inc.') THEN 'Apple Pay'
    WHEN wt.wallettype IN ('Google Pay', 'Google Inc.', 'Google Inc - Ecomm') THEN 'Google Pay'
    WHEN wt.wallettype IN ('Paypal', 'PayPal') THEN 'PayPal'
    WHEN wt.wallettype = 'SAMSUNG CORPORATION' THEN 'Samsung Pay'
    WHEN wt.wallettype = 'Venmo' THEN 'Venmo'
    WHEN wt.wallettype = 'Unknown' THEN 'Unknown'
    ELSE 'Other'
END as ewallet_type_normalized
```

---

## ⚠️ EDW Data Quality Warning

**DO NOT use EDW tables for wallet type attribution from GBOS source.**

### The Problem
Investigation found EDW incorrectly maps wallet types:
- GBOS record `14291281` = "Google Inc." → EDW maps to "Apple Pay"
- GBOS record `13989860` = "GoGoGrandparent GC" → EDW maps to "Apple Pay"
- **Zero** Google Pay records exist in EDW for GBOS source (`sor_uid=3`)

### Tables to Avoid for This Use Case
- `edw.dim_wallet_type` - Shared dimension, but data is mismatched
- `edw.dim_payment_identifier_device` - Links exist but values are wrong

### Correct Approach
**Always use GBOS tables directly** for wallet attribution:
- `gbos.posttransaction` → `gbos.paymentidentifierdevice` → `gbos.wallettype`

---

## Complete Implementation Pattern

```sql
-- eWallet attribution with full logic
WITH tokenized_transactions AS (
    SELECT
        pt.posttransactionkey,
        pt.sor_uid,
        pt.processorbusinessdate,
        pt.transactionamount,

        -- Wallet attribution
        wt.wallettype as wallet_type_raw,
        wt.ismerchant,

        -- Normalized wallet type
        CASE
            WHEN wt.wallettype IN ('Apple Pay', 'Apple Inc.') THEN 'Apple Pay'
            WHEN wt.wallettype IN ('Google Pay', 'Google Inc.', 'Google Inc - Ecomm') THEN 'Google Pay'
            WHEN wt.wallettype IN ('Paypal', 'PayPal') THEN 'PayPal'
            WHEN wt.wallettype = 'SAMSUNG CORPORATION' THEN 'Samsung Pay'
            WHEN wt.wallettype = 'Venmo' THEN 'Venmo'
            WHEN wt.wallettype = 'Unknown' THEN 'Unknown'
            ELSE 'Other'
        END as ewallet_type,

        -- Token classification
        CASE
            WHEN wt.ismerchant = 0 THEN 'Digital Wallet'
            WHEN wt.ismerchant = 1 THEN 'Merchant Token'
            ELSE 'Unknown'
        END as token_type,

        -- Boolean flags for aggregation
        CASE WHEN wt.ismerchant = 0 THEN TRUE ELSE FALSE END as is_digital_wallet,
        CASE WHEN wt.ismerchant = 1 THEN TRUE ELSE FALSE END as is_merchant_token

    FROM gbos.posttransaction pt
    JOIN gbos.paymentidentifierdevice pid
        ON pid.paymentidentifierdevicekey = pt.paymentidentifierdevicekey
        AND pid.createdate <= pt.createdate
    JOIN gbos.wallettype wt
        ON pid.wallettypekey = wt.wallettypekey
    WHERE pt.paymentidentifierdevicekey IS NOT NULL  -- Only tokenized transactions
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY pt.posttransactionkey, pt.sor_uid
        ORDER BY pid.createdate DESC
    ) = 1
)

SELECT * FROM tokenized_transactions
```

---

## Validation Results

| Metric | Result |
|--------|--------|
| Transactions tested | 181,383 |
| Match rate with point-in-time logic | 100% |
| QUALIFY dedup effectiveness | 158 → 100 rows (1:1 achieved) |
| Fan-out devices (different wallets) | 7.8M |
| Fan-out devices (same wallet) | 1.5M |

---

## Related Resources

- **Discovery Results:** `handoffs/interchange_revenue_migration/phase0-ewallet-deep-dive-results.md`
- **Parent Plan:** `handoffs/interchange_revenue_migration/merchant-spend-feature-expansion-plan.md`
- **QA Methodology:** `shared/reference/qa-validation-checklist.md` (Phase 4.4 Sample Trace)

---

## Keywords for Search
`ewallet`, `digital wallet`, `tokenization`, `apple pay`, `google pay`, `samsung pay`, `ismerchant`, `paymentidentifierdevice`, `wallettype`, `gbos`, `point-in-time`, `fan-out`, `history table`
