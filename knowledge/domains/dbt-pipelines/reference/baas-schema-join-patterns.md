# BaaS Schema Join Patterns Reference

**Source:** 30-day Redshift query log mining (474K queries, Dec 2025)
**Focus:** EDW, ODS, GBOS schemas for BaaS division reporting
**Usage:** Consult when writing dbt models that join across these schemas

---

## Schema Distribution

| Schema | References | % of Total | Focus |
|--------|------------|------------|-------|
| TPG | 533,156 | 61.5% | Tax Products (separate BU) |
| **EDW** | 104,639 | 12.1% | 🎯 BaaS - Star schema |
| **GBOS** | 88,665 | 10.2% | 🎯 BaaS - Source system |
| greendot_share | 70,629 | 8.1% | Shared tables |
| **ODS** | 68,001 | 7.8% | 🎯 BaaS - Operational |

**BaaS Total:** 261,305 references (30.1%)

---

## EDW Schema (Star Schema - Reporting Layer)

### Core Dimension Tables

| Table | Query Count | Purpose |
|-------|-------------|---------|
| `dim_date` | 23,981 | Calendar dimension |
| `dim_account` | 22,040 | Account master |
| `dim_product` | 13,376 | Product dimension |
| `dim_acct_bin_product_attr` | 3,734 | Account-BIN-Product bridge |
| `dim_bank` | 2,804 | Bank dimension |
| `dim_bin` | 2,053 | BIN dimension |
| `dim_txn_type_hierarchy` | 2,672 | Transaction classification |

### Core Fact Tables

| Table | Query Count | Purpose |
|-------|-------------|---------|
| `fct_posted_transaction` | 4,148 | Posted transactions |
| `fct_dly_acct_txn_summary` | 2,788 | Daily account summaries |
| `fct_ach` | 1,731 | ACH transactions |
| `fct_daily_acct_actives` | 1,206 | Daily active accounts |
| `fct_deposit_acct_bal_dtl_hist` | 859 | Balance history |

### Canonical Join Patterns

```sql
-- Account enrichment (most common pattern)
FROM edw.fct_posted_transaction pt
JOIN edw.dim_account da ON pt.acct_uid = da.acct_uid
JOIN edw.dim_product dp ON dp.product_uid = da.product_uid
JOIN edw.dim_acct_bin_product_attr dabp ON da.acct_uid = dabp.acct_uid
JOIN edw.dim_bank dba ON dabp.bank_uid = dba.bank_uid

-- Date dimension join
JOIN edw.dim_date dd ON pt.posted_dt_key = dd.date_key
-- OR calendar date version:
JOIN edw.dim_date dd ON TRUNC(pt.posted_dttm) = dd.calendar_date

-- Transaction type hierarchy (with business rules)
JOIN edw.txn_type_hier_txn_type_xref ttx ON pt.txn_type_uid = ttx.txn_type_uid
JOIN edw.dim_txn_type_hierarchy tth ON ttx.txn_type_hierarchy_key = tth.txn_type_hierarchy_key
-- NOTE: Check hier_business_rule_1 for MCC-based classification

-- Account holder (primary only)
JOIN edw.dim_account_holder dah ON da.acct_uid = dah.acct_uid
  AND dah.primary_ind = true
JOIN edw.dim_consumer_profile dcp ON dah.consumer_profile_uid = dcp.consumer_profile_uid
```

### Key Filters

```sql
-- Legacy vs BaaS filter
AND da.sor_uid = 1  -- Legacy only
AND da.sor_uid = 24 -- GBR (Go2Bank/BaaS)

-- Account type exclusions
AND da.acct_link_type <> 'VAULT'

-- Standard date range
AND pt.posted_dttm_local >= DATEADD('year', -1, DATE_TRUNC('year', current_date))
```

---

## ODS Schema (Operational Data Store)

### Core Tables

| Table | Query Count | Purpose |
|-------|-------------|---------|
| `business_division` | 7,309 | Business hierarchy |
| `business_channel` | 6,528 | Channel classification |
| `product_channel` | 5,698 | Product-channel bridge |
| `product_sub_channel` | 5,623 | Sub-channel detail |
| `business_sub_channel` | 5,605 | Business sub-channel |
| `business_segment` | 5,371 | Segment classification |
| `transaction_type` | 3,279 | Transaction types |
| `account` | 2,364 | ODS account table |
| `posted_transaction` | 2,274 | ODS posted transactions |

### Canonical Join Patterns

```sql
-- Business hierarchy (product_channel is the hub)
FROM ods.product_channel pc
LEFT JOIN ods.business_division bd ON pc.business_division_uid = bd.business_division_uid
LEFT JOIN ods.business_channel bc ON pc.business_channel_uid = bc.business_channel_uid
LEFT JOIN ods.business_sub_channel bsc ON pc.business_sub_channel_uid = bsc.business_sub_channel_uid
LEFT JOIN ods.product_sub_channel psc ON pc.product_sub_channel_uid = psc.product_sub_channel_uid
LEFT JOIN ods.business_segment bs ON pc.business_segment_uid = bs.business_segment_uid

-- ODS account holder (primary only)
FROM ods.account_holder ah
WHERE ah.primary_ind = true

-- Consumer profile chain
JOIN ods.account_holder ah ON ai.acct_uid = ah.acct_uid
  AND ai.sor_uid = ah.sor_uid
  AND ah.primary_ind = 1
JOIN ods.consumer_profile cp ON ah.consumer_profile_uid = cp.consumer_profile_uid

-- Transaction type classification
FROM ods.posted_transaction pt
JOIN ods.transaction_type tt ON pt.txn_type_uid = tt.txn_type_uid

-- Service type (exclude eCash)
JOIN ods.service_type svc_typ ON svc_ods.svc_type_uid = svc_typ.svc_type_uid
  AND svc_typ.svc_type_uid <> 4 -- exclude eCash
```

### ODS-to-EDW Bridge Pattern

```sql
-- When linking ODS to EDW
FROM edw.dim_account da
JOIN ods.product_channel pc ON da.product_channel_uid = pc.product_channel_uid

-- Legacy account lookup
FROM ods.account oacct
WHERE oacct.sor_uid = 24 AND oacct.sor_acct_id = acct.accountkey
```

---

## GBOS Schema (Go2Bank Source System)

### Core Tables

| Table | Query Count | Purpose |
|-------|-------------|---------|
| `account` | 17,834 | GBOS accounts |
| `product` | 9,715 | GBOS products |
| `accountholder` | 4,125 | Account holders |
| `postinternaltransaction` | 3,944 | Internal transactions |
| `program` | 3,930 | Program definitions |
| `transclass` | 3,585 | Transaction classes |
| `accountbalance` | 2,426 | Current balances |
| `accountstatus` | 2,268 | Account status |
| `posttransaction` | 2,184 | Posted transactions |
| `fundtransfer` | 1,631 | Fund transfers |

### Canonical Join Patterns

```sql
-- Account to product (most common)
FROM gbos.account ac
JOIN gbos.product pd ON ac.productkey = pd.productkey

-- Account holder (primary only)
JOIN gbos.accountholder ah ON ac.accountkey = ah.accountkey
  AND ac.sor_uid = ah.sor_uid
  AND ah.isprimaryaccountholder = true

-- Account status
JOIN gbos.accountstatus acts ON ac.accountstatuskey = acts.accountstatuskey

-- Transaction class
FROM gbos.posttransaction pt
JOIN gbos.transclass tc ON pt.transclasskey = tc.transclasskey

-- Payment identifier chain
FROM gbos.accountholder ah
JOIN gbos.accountholder_paymentidentifier ahp ON ah.accountholderkey = ahp.accountholderkey
  AND ah.sor_uid = ahp.sor_uid
JOIN gbos.paymentidentifier pi ON ahp.paymentidentifierkey = pi.paymentidentifierkey
  AND ahp.sor_uid = pi.sor_uid

-- Fund transfer with details
FROM gbos.fundtransfer ft
JOIN gbos.fundtransferdetail ftd ON ft.fundtransferkey = ftd.fundtransferkey
  AND ft.sor_uid = ftd.sor_uid

-- Verification request chain
FROM gbos.verificationrequest vr
JOIN gbos.verificationtriggertype vtt ON vr.verificationtriggertypekey = vtt.verificationtriggertypekey
JOIN gbos.verificationstatus vs ON vr.verificationstatuskey = vs.verificationstatuskey
JOIN gbos.consumerprofileidentity cpi ON vr.consumerprofilekey = cpi.consumerprofilekey
  AND vr.sor_uid = cpi.sor_uid
```

### Key GBOS Filters

```sql
-- Go2Bank program filter
AND pd.programkey = 5  -- Go2bank
AND pd.productcode = 4000

-- GBR (Go2Bank Retail) SOR
AND ac.sor_uid = 24

-- BIN product join
JOIN gbos.binproduct bp ON pd.productkey = bp.productkey
```

---

## Cross-Schema Patterns

### EDW ↔ GBOS Bridge

```sql
-- Link via sor_acct_id
FROM edw.dim_account da
WHERE da.sor_uid = 24  -- GBR
  AND da.sor_acct_id = gbos_account.accountkey

-- Alternative via account identifier
FROM edw.dim_account da
JOIN gbos.account ga ON da.sor_acct_id = ga.accountkey AND da.sor_uid = ga.sor_uid
```

### EDW ↔ ODS Bridge

```sql
-- Via product_channel_uid
FROM edw.dim_account da
JOIN ods.product_channel pc ON da.product_channel_uid = pc.product_channel_uid

-- Via account_uid
FROM edw.dim_account da
JOIN ods.account_holder oah ON da.acct_uid = oah.acct_uid AND oah.primary_ind = true
```

---

## Business Rules from Production Queries

### Date Filtering Patterns

```sql
-- Pacific Time conversion (critical for daily reports)
TRUNC(DATE_ADD('hour', -8, GETDATE()))  -- Current PT date
TRUNC(DATE_ADD('hour', -8, DATE_ADD('day', -1, GETDATE())))  -- Yesterday PT

-- Year-over-year pattern
pt.posted_dttm_local >= DATEADD('year', -1, DATE_TRUNC('year', current_date))
```

### Account Filtering

```sql
-- Exclude test/internal accounts
AND da.acct_link_type <> 'VAULT'

-- Primary account holder only (appears in 80%+ of queries)
AND ah.primary_ind = true
AND ah.isprimaryaccountholder = true  -- GBOS spelling

-- Registration complete filter
AND da.registration_complete_ind = 1
AND initial_funding_ind = 1
```

### Transaction Filtering

```sql
-- Exclude fees
AND creditdebit = -1
AND pt.ledgerbalance < 0

-- Exclude eCash (nets to zero)
AND svc_typ.svc_type_uid <> 4

-- ODP (Overdraft) specific
AND pit.ProcessorTransactionDate >= '2021-01-28'  -- OD Fee Engine launch
AND tc.transclass = '1-008'  -- ODP transaction class
```

### SOR_UID Reference

| SOR_UID | System | Notes |
|---------|--------|-------|
| 1 | Legacy | Pre-Go2Bank systems |
| 21 | Wire | Wire transfer system |
| 24 | GBR | Go2Bank Retail (BaaS) |

---

## Anti-Patterns to Avoid

From query log analysis:

1. **Always specify sor_uid** - Multi-tenant tables require this filter
2. **Always use primary_ind = true** for account holders
3. **Avoid SELECT *** - Found in 6,635 queries, wastes I/O
4. **Pre-join product_channel** - Business hierarchy is 5+ tables deep

---

## Usage in dbt Models

When building BaaS models:

```sql
-- Reference this document for join conditions
-- Example: Account enrichment intermediate model

WITH account_base AS (
    SELECT
        da.acct_uid,
        da.sor_acct_id,
        da.product_uid,
        dp.product_name,
        dba.bank_name,
        dabp.bin_uid
    FROM {{ ref('stg_edw__dim_account') }} da
    JOIN {{ ref('stg_edw__dim_product') }} dp
        ON dp.product_uid = da.product_uid
    JOIN {{ ref('stg_edw__dim_acct_bin_product_attr') }} dabp
        ON da.acct_uid = dabp.acct_uid
    JOIN {{ ref('stg_edw__dim_bank') }} dba
        ON dabp.bank_uid = dba.bank_uid
    WHERE da.sor_uid = 24  -- BaaS only
)
```

---

*Generated from query log mining, 2025-12-26*
*Source: 474K Redshift production queries*
