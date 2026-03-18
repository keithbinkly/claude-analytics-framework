# Redshift Query Log Mining Report

**Date:** 2025-12-26
**Data Source:** 30 days of Redshift query logs (Nov 21 - Dec 25, 2025)
**Total Queries Analyzed:** 474,260
**File:** `greendot_analytics_mtegysvc_compute_stats.xlsx` (122MB)

---

## Executive Summary

Mining 30 days of Redshift query logs revealed:

| Finding | Impact | Action |
|---------|--------|--------|
| **One query pattern consumes 666 CPU hours/month** | $$$$ cost, 30-min execution | Pre-aggregate or materialize |
| **20% of queries have >50% CPU skew** | Poor parallelization | Optimize DISTKEY |
| **6,635 SELECT * patterns** | Wasted I/O | Column pruning |
| **TPG tables are the "de facto semantic layer"** | Tax products = core business | Prioritize in dbt models |
| **transactionamount is THE metric** | Most aggregated column | Ensure in semantic layer |

---

## 🔥 Critical Finding: The 666-Hour Query

### The Problem

One query pattern (`#legacy_od_trans2`) consumes **666 CPU hours per month**:

```sql
CREATE TABLE #legacy_od_trans2 AS
SELECT
  lot.*,
  TRUNC(a.deposit_acct_bal_dtl_hist_dt) AS balance_date,
  a.ledger_bal_amt AS NextDayBalance
FROM #legacy_od_trans lot
LEFT JOIN edw.dim_account da
  ON da.sor_acct_id = lot.accountkey
  AND da.sor_uid = 1
LEFT JOIN edw.v_fct_deposit_acct_bal_dtl_hist a
  ON da.acct_uid = a.acct_uid
  AND TRUNC(a.deposit_acct_bal_dtl_hist_dt) = TRUNC(DATE_ADD('day', 1, lot.customerpostingdateandtime))
WHERE
  da.acct_link_type <> 'VAULT'
  AND lot.ODP_subscription ilike '%Premier%'
  AND lot.ledgerbalance <= -10
  AND lot.transactionamount >= 5
```

### Metrics

| Metric | Value |
|--------|-------|
| Executions/month | 136 |
| CPU time per execution | 77,309 seconds |
| Wall clock per execution | 30 minutes |
| Rows scanned per execution | 759 billion |
| **Total CPU hours/month** | **666 hours** |

### Business Logic (Overdraft Detection)

This query identifies **Premier tier customers with overdraft transactions**:
- Balance goes negative by >$10
- Transaction amount >$5
- Joins to historical balance table to get next-day balance

### Recommended Fix

1. **Create dbt incremental model**: `int_overdraft__premier_transactions`
   - Materialize daily, only process new transactions
   - Pre-join to balance history once, not 136 times

2. **DISTKEY optimization**:
   - `edw.v_fct_deposit_acct_bal_dtl_hist` should have `DISTKEY(acct_uid)`
   - Enables co-located joins without redistribution

3. **Estimated savings**: 90%+ reduction (666 → ~60 CPU hours/month)

---

## 📊 De Facto Semantic Layer (What People Actually Query)

### Most Queried Tables

These tables represent the **actual business priorities** (not what documentation says is important):

| Rank | Table | Query Count | Domain |
|------|-------|-------------|--------|
| 1 | `tpg.controlaccount` | 4,490 | Tax Products |
| 2 | `tpg.partnerproduct` | 3,329 | Tax Products |
| 3 | `tpg.application` | 3,084 | Tax Products |
| 4 | `tpg.journaltransactiontype` | 1,967 | Tax Products |
| 5 | `greendot_share.tpg` | 1,926 | Tax Products |
| 6 | `tpg.disbursement` | 1,369 | Tax Products |
| 7 | `tpg.cashreceiptsubledger` | 1,043 | Tax Products |
| 8 | `gbos.account` | 1,035 | Core Banking |
| 9 | `edw.dim_account` | 855 | EDW |
| 10 | `ods.business_division` | 844 | ODS |

**Insight:** TPG (Tax Product Group) tables dominate. This should inform model prioritization in dbt.

### Most Aggregated Metrics

The "de facto metrics" being calculated repeatedly:

| Pattern | Count | Business Meaning |
|---------|-------|------------------|
| `SUM(transactionamount)` | 919+ | **Core revenue metric** |
| `COUNT(DISTINCT acct_uid)` | 267 | Customer counts |
| `SUM(crsl.transactionamount)` | 436 | Cash receipt amounts |
| `SUM(cdsl.TransactionAmount)` | 406 | Cash disbursement amounts |
| `SUM(amount)` | 224 | Generic amounts |

**Recommendation:** These should be first-class metrics in the dbt Semantic Layer.

### Most Common Business Rules (CASE WHEN patterns)

| Pattern | Count | Meaning |
|---------|-------|---------|
| `processdate > createdate` | 5,450 | Lag detection |
| `year % 2 = 0` | 3,714 | Even/odd year logic |
| `cdsl.isdebit` | 218 | Debit/credit classification |
| `achcategorykey = 1/2` | 276 | ACH type classification |
| `ProgramCode = 'gbr'` | 104 | Program filtering |

---

## ⚠️ Anti-Patterns Detected

### Prevalence (in 100K query sample)

| Anti-Pattern | Count | Impact | Fix |
|--------------|-------|--------|-----|
| **SELECT *** | 6,635 | Scans all columns | Explicit column list |
| **DISTINCT in aggregation** | 6,307 | Memory-intensive | Pre-dedupe in CTE |
| **OR in JOIN condition** | 3,850 | Prevents merge join | Refactor to UNION |
| **Nested subqueries (3+ levels)** | 2,992 | Hard to optimize | Flatten to CTEs |
| **NOT IN (subquery)** | 1,964 | Can't use hash join | Use NOT EXISTS |
| **CROSS JOIN** | 449 | Cartesian explosion | Add join conditions |

### Performance Distribution

| Metric | Value |
|--------|-------|
| Mean execution time | 22.5 sec |
| Median execution time | 2.0 sec |
| 95th percentile | 84 sec |
| 99th percentile | 435 sec (7+ min) |
| Slow queries (>60 sec) | 20,028 (4.2%) |
| Very slow (>5 min) | 4,738 (1.0%) |
| **High CPU skew (>50%)** | **94,966 (20%)** |

**Critical:** 20% of queries have poor parallelization. This suggests DISTKEY/SORTKEY optimization opportunities.

---

## 🔗 Canonical Model Candidates

These table pairs are frequently joined together and should be **pre-joined in dbt models**:

| Table Pair | Join Count | Canonical Model |
|------------|------------|-----------------|
| TPG tables + TPG tables | 8,643+ | `int_tpg__base` |
| GBOS + various | 1,482+ | `int_accounts__gbos_enriched` |
| EDW + various | 1,632+ | Already have `dim_account` |
| ODS + TPG | 3,059+ | `int_tpg__ods_enriched` |

---

## 📈 Recommendations Summary

### Immediate Actions (This Week)

1. **Optimize the legacy_od_trans2 pattern**
   - Create `int_overdraft__premier_transactions` incremental model
   - Expected savings: 600+ CPU hours/month

2. **Add TPG tables to canonical registry**
   - These are queried 15,000+ times but may not be in dbt yet

3. **Create `transactionamount` as semantic layer metric**
   - It's the #1 aggregated column

### Short-Term (This Month)

4. **Address SELECT * patterns**
   - Grep for `SELECT *` in MicroStrategy reports
   - Replace with explicit columns

5. **Fix OR in JOIN patterns**
   - Refactor to UNION ALL + specific conditions

6. **Review DISTKEY assignments**
   - Tables with high skew need DISTKEY(acct_uid) or similar

### Long-Term (Next Quarter)

7. **Build "Query Pattern Registry"**
   - Track common patterns, auto-generate dbt models
   - This is the "Figma moment" for semantic infrastructure

8. **Implement query log monitoring**
   - Weekly reports on expensive queries
   - Alert on new patterns >X CPU seconds

---

## Files Changed

```
Created:
  docs/updates/2025-12-26-redshift-query-log-mining.md     # This report
  shared/reference/baas-schema-join-patterns.md            # Schema-specific guidance for BaaS

Experience Store:
  5 patterns logged for cross-agent retrieval
  - EDW account enrichment join pattern
  - GBOS account-product join pattern
  - ODS business hierarchy pattern
  - SOR_UID reference values
  - Primary account holder filter
```

---

*Generated by Query Log Mining analysis, 2025-12-26*
*Methodology: pandas analysis of 474K queries from Redshift STL tables*
