<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/knowledge-base/canonical-models-registry.md
-->

> analytics-workspace migration note: this is a promoted copy from `dbt-agent`. Prefer this analytics-workspace path first. If a referenced companion doc has not been promoted yet, fall back to `dbt-agent`.

# Canonical Models Registry

**Purpose**: Quick reference for reusable foundation models to avoid duplication during legacy migrations

**Last Updated**: December 2, 2025

---

## 🎯 What is a Canonical Model?

A **canonical model** is a universal building block that:
- ✅ Provides comprehensive enrichment for a specific domain (transactions, accounts, etc.)
- ✅ Used by **2+ downstream models** across different pipelines
- ✅ Follows DRY principle - single source of truth
- ✅ Well-tested and production-validated

**When building a new pipeline, ALWAYS check this registry first to avoid rebuilding existing logic.**

---

## 🏛️ Conformed Dimensions Principle

**Source**: dbt Labs - Modeling Success blog, Kimball methodology

### What are Conformed Dimensions?

**Conformed dimensions** are dimension tables built ONCE and shared across the entire organization. They ensure everyone uses the same definition for core business entities.

### Why Conformed Dimensions Matter

| Without Conformed | With Conformed |
|-------------------|----------------|
| Finance: "Active customer = 30-day activity" | **One definition** shared by all |
| Marketing: "Active customer = 90-day activity" | Cross-functional metrics align |
| "Why don't our numbers match?" | Single source of truth |

### Core Conformed Dimensions (Build Once, Use Everywhere)

| Dimension | Canonical Model | Grain | Key Attributes |
|-----------|-----------------|-------|----------------|
| **Customer/Account** | `int_edw_kpi__account_base` | Account | lifecycle, product, segment |
| **Product** | Product hierarchy in account_base | Product | brand, portfolio, channel |
| **Time/Calendar** | `int_wonderwall_calendar` | Date | fiscal periods, YoY flags |
| **Merchant** | Merchant mapping in txn models | Merchant | cleaned name, MCC |

### Rules for Conformed Dimensions

1. **Build once** - Never create `finance_customers` and `marketing_customers`
2. **Share always** - Every pipeline refs the same canonical
3. **Extend carefully** - Add attributes to canonical, don't create variants
4. **Document thoroughly** - Full coverage in this registry

### When to Extend vs. Create New

| Scenario | Action |
|----------|--------|
| Need new attribute on existing dimension | **Extend** canonical model |
| New grain needed (account-month vs account) | **Create** new canonical at that grain |
| Department needs custom calc | **Create mart** that refs canonical + adds calc |
| Fundamentally different entity | **Create** new canonical (rare) |

**Anti-pattern**: Creating `int_customers__marketing` when `int_edw_kpi__account_base` exists. Instead, create `mrt_marketing__customer_attribution` that refs the canonical.

---

## 📊 Transactions Domain

### `int_transactions__posted_all`
**Location**: `models/intermediate/intermediate_NEW/transactions/int_transactions__posted_all.sql`

**Grain**: Transaction-level (one row per `posted_txn_uid`)

**Coverage**:
- ✅ Base posted transaction details (edw.fct_posted_transaction)
- ✅ Account enrichment (product, brand, portfolio, business division)
- ✅ Product hierarchy (product_uid, product name, product channel)
- ✅ Merchant normalization (merchant_cleaned via merchant_mapping)
- ✅ Transaction type hierarchy (txn_type_desc, purchase_txn_ind, atm_txn_ind, etc.)
- ✅ FPA group dimensions (fpa_group_level_1, fpa_group_level_2)
- ✅ Calendar date enrichment (calendar_date derived from processor_business_dt)

**Materialization**: Incremental (merge strategy, 3-day lookback)

**Use Cases**:
- Revenue analytics (interchange, GDV)
- Merchant analysis (top merchants, decline patterns)
- Transaction monitoring (fraud, volume tracking)
- Product performance (purchase patterns by product)

**When to Extend**:
- Adding new universal dimensions (BIN ranges, card brand, network)
- Adding derived indicators used across multiple pipelines (international_txn_ind, etc.)

**When NOT to Extend**:
- Pipeline-specific calculations (interchange revenue formulas)
- Aggregations that change grain (product-month summaries)

---

### `int_transactions__auth_all`
**Location**: `models/intermediate/intermediate_NEW/transactions/int_transactions__auth_all.sql`

**Grain**: Transaction-level (one row per `auth_txn_uid`)

**Coverage**:
- ✅ Base authorization details (edw.fct_authorization)
- ✅ Account enrichment (same as posted_all)
- ✅ Product hierarchy (same as posted_all)
- ✅ Merchant normalization (merchant_cleaned)
- ✅ Transaction type hierarchy (txn_type_desc, purchase_txn_ind)
- ✅ Decline reason enrichment (decline_reason_desc, decline_category)
- ✅ Network/issuer information
- ✅ POS entry method (chip, contactless, manual)

**Materialization**: Incremental (merge strategy, 3-day lookback)

**Use Cases**:
- Authorization analytics (approval rates, decline analysis)
- Fraud detection (decline patterns, unusual activity)
- Network performance (issuer response times)
- Customer experience (POS entry type analysis)

---

### `int_transaction_pairs__purchase`
**Location**: `models/intermediate/intermediate_NEW/transactions/int_transaction_pairs__purchase.sql`

**Grain**: Matched auth+posted pair (one row per `auth_posted_pair_id`)

**Coverage**:
- ✅ Auth transaction details (from int_transactions__auth_all)
- ✅ Posted transaction details (from int_transactions__posted_all)
- ✅ Pairing logic (matches auth to settlement within 7-day window)
- ✅ Amount variance tracking (auth_amt vs posted_amt)
- ✅ Timing analysis (auth_to_posted_hours)

**Materialization**: Table (depends on both auth_all and posted_all)

**Use Cases**:
- Auth-to-settlement reconciliation
- Merchant authorization performance (decline → retry → approval patterns)
- Amount variance analysis (tip adjustments, currency conversion)

---

## 🏢 Foundations Domain

### `int_edw_kpi__account_base`
**Location**: `models/intermediate/edw_account_base/int_edw_kpi__account_base.sql`

**Grain**: Account-level (one row per `acct_uid`)

**Coverage**:
- ✅ Account lifecycle attributes (open date, close date, status)
- ✅ Product hierarchy (product_uid, product name, brand, portfolio)
- ✅ Customer demographics (age, state, customer segment)
- ✅ Account classification (consumer vs business, prepaid vs credit)
- ✅ Tenure calculations (months_since_open)

**Materialization**: Table (refreshed daily)

**Use Cases**:
- Customer analytics (lifetime value, retention)
- Portfolio reporting (active accounts by product)
- Segmentation analysis (demographics, behavior)

**When to Extend**:
- Adding universal account attributes (risk score, credit limit)
- Adding derived customer segments (RFM, lifecycle stage)

---

### `int_wonderwall_calendar`
**Location**: `models/intermediate/baas_wonderwall_kpi/01_foundations/int_wonderwall_calendar.sql`

**Grain**: Date-level (one row per calendar_date)

**Coverage**:
- ✅ Standard date dimensions (year, quarter, month, week, day)
- ✅ Rolling window indicators (t_minus_days, t_minus_weeks, t_minus_months)
- ✅ Period comparison flags (YoY, MoM, QoQ)
- ✅ Business calendar (holidays, fiscal periods)
- ✅ Time scaffold support (generates continuous date range)

**Materialization**: Table (relatively small, full refresh is fast)

**Use Cases**:
- Time-series analysis (trend detection, seasonality)
- Comparative reporting (YoY growth, MoM variance)
- Snapshot windows (30-day actives, 90-day retention)

---

## 💰 Revenue Domain

### `int_interchange__account_enriched` (Example - To Be Created)
**Location**: `models/intermediate/intermediate_NEW/metrics/interchange/int_interchange__account_enriched.sql`

**Grain**: Account-level

**Coverage**:
- ✅ Account base (from int_edw_kpi__account_base)
- ✅ FPA group dimensions (fpa_group_level_1, fpa_group_level_2)
- ✅ Business division hierarchy
- ✅ Interchange eligibility flags

**Materialization**: Table

**Use Cases**:
- Interchange revenue attribution
- FPA group reporting
- Business division performance

**Status**: 📝 Planned (example for future canonical model)

---

## 🔍 How to Use This Registry

### When Building a New Pipeline:

**Step 1**: Ask User for Suggestions
> "What existing intermediate models enrich [posted transactions / accounts / etc.]?"

**Step 2**: Check This Registry
- Search for models matching your domain (transactions, accounts, revenue)
- Read the "Coverage" section to see what enrichment already exists

**Step 3**: Calculate Overlap %
- List columns needed by legacy script
- Compare with columns available in canonical model
- Calculate overlap percentage

**Step 4**: Make Reuse Decision
| Overlap | Action |
|---------|--------|
| **≥80%** | ✅ Reuse canonical model, create thin wrapper |
| **50-80%** | ⚠️ Extend canonical model OR create intermediate layer |
| **<50%** | ❌ Build new model (but follow canonical patterns) |

### When to Add a New Canonical Model:

**Criteria for Canonical Status:**
- ✅ Used by **3+ pipelines** (not just 1-2 use cases)
- ✅ Provides **universal value** (not pipeline-specific logic)
- ✅ Stable enrichment pattern (not experimental)
- ✅ Performance-tested (incremental strategy validated)

**Process**:
1. Build model following existing canonical patterns
2. Validate with QA process (compare to legacy)
3. Document in this registry with full coverage details
4. Get user approval before marking as "canonical"

---

## 📝 Registry Maintenance

**When to Update**:
- ✅ New canonical model created (add full entry)
- ✅ Canonical model extended with new columns (update "Coverage" section)
- ✅ Deprecated canonical model (mark as DEPRECATED, note replacement)

**Ownership**: Data Engineering team maintains this registry
**Review Cadence**: Quarterly review to identify new canonical candidates

---

## 🚀 Future Candidates

Models being evaluated for canonical status:

### `int_merchant_mapping` (Under Review)
**Status**: 🔍 Evaluating for canonical status
**Coverage**: Merchant normalization (merchant_cleaned), MCC enrichment
**Usage**: Currently used by auth_all and posted_all
**Decision Needed**: Should merchant mapping be a standalone canonical, or remain as enrichment within transaction models?

### `int_balance_snapshots` (Planned)
**Status**: 📝 Planned canonical for balance analytics
**Coverage**: Daily balance snapshots, net ledger balance, available balance
**Use Cases**: Balance trending, liquidity analysis, regulatory reporting

### `int_transaction_pairs__purchase` + `int_transaction_pairs__purchase_detail` (New - 2025-11-11)
**Status**: ✅ Production ready - Two-tier architecture pattern
**Domain**: Transaction Pairs
**Location**: `models/intermediate/intermediate_NEW/transactions/edw_based/transaction_pairs/`

**Pattern**: Two-tier architecture supporting both operational performance and cardholder-level analysis

#### Detail Tier: `int_transaction_pairs__purchase_detail`
- **Grain**: Transaction-level with `acct_uid` preserved
- **Materialization**: `incremental`
- **Unique Key**: `sor_uid || acct_uid || posted_txn_uid || auth_txn_uid`
- **Use Cases**: Cardholder-level concentration analysis, behavioral patterns, account-level metrics
- **Performance**: ~10-20x more rows than aggregated tier
- **Downstream Models**: `mrt_merchant_auth_decline__cardholder_base`

#### Aggregated Tier: `int_transaction_pairs__purchase`
- **Grain**: Daily × Product × Merchant × Dimensions (no `acct_uid`)
- **Materialization**: `incremental`
- **Unique Key**: Date + dimensional attributes
- **Use Cases**: Fast operational queries, decline rate trends, merchant analytics
- **Performance**: Sub-second query response for dashboards
- **Downstream Models**: `mrt_merchant_auth_decline__semantic_base`

**Critical Implementation Pattern**:
Both tiers MUST exclude auth approvals using:
```sql
WHERE auth_reason_desc NOT IN ('Success', 'Transaction Approved', 'Partial Approval')
```
This prevents double-counting with posted transactions. Failure to exclude 'Success' (the actual value in data) causes 50%+ variance in attempt metrics.

**When to Use Which Tier**:
- Use **detail tier** when: Need account-level analysis, cardholder concentration, behavioral segmentation
- Use **aggregated tier** when: Need operational dashboards, trend analysis, merchant performance (no PII needed)

**Learnings**: During 2025-11-11 QA session, discovered that actual auth_reason_desc value is 'Success' (not 'Transaction Approved' as documented). Filter checking only for 'Transaction Approved' caused 56% variance in cardholder metrics. See `field-mappings.md` for auth response code values.

---

**Questions or Suggestions?**
- To propose a new canonical model, document use cases + overlap analysis
- To request extension of existing canonical, specify new enrichment needed
- User: Keith Binkly has final approval on canonical model additions
