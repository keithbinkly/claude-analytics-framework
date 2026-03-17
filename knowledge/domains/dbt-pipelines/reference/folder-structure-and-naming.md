# 📁 Folder Structure and Naming Conventions

## Critical Pre-Migration Checklist

**BEFORE creating any new models**, always verify:

1. ✅ **Correct folder location** per intermediate_structure_guide.md and marts_structure_guide.md
2. ✅ **Environment-aware date limits** for dev/CI environments (6-month limit pattern)
3. ✅ **Naming conventions** match existing patterns in target folder
4. ✅ **Materialization strategy** appropriate for model type and layer

---

## Intermediate Layer Structure

**Location**: `models/intermediate/intermediate_NEW/`

### Subfolder Organization

```
intermediate_NEW/
├── foundations/              # Core building blocks (account base, product hierarchy)
│   ├── edw_account_base/    # Account enrichment and product classification
│   └── product/             # Product hierarchies
├── transactions/            # Transaction data from all sources
│   ├── gbos_based/         # GBOS source-direct transactions
│   ├── gss_based/          # GSS source-direct transactions
│   └── ods_based/          # ODS source-direct transactions (e.g., interchange_transaction)
├── balances/               # Balance data from multiple sources
├── registrations/          # Customer onboarding & registration data (if needed)
└── metrics/                # **REUSABLE METRIC CALCULATIONS**
    ├── edw_based/          # EDW-derived metrics
    └── gbos_based/         # **GBOS-derived metrics (registration, verification, etc.)**
```

### Where Does Registration Go?

**Registration metrics belong in**: `intermediate_NEW/metrics/gbos_based/`

**Rationale**:
- Registration is a **metric calculation** (counts, aggregations)
- Not a foundation (account base) or transaction (auth/posted events)
- GBOS-sourced data → `gbos_based/` subfolder

---

## Marts Layer Structure

**Location**: `models/marts/marts_NEW/`

### Subfolder Organization

```
marts_NEW/
├── executive/              # C-suite & board reporting (strategic KPIs)
├── operational/            # **Day-to-day operations (registration monitoring, transaction health)**
│   ├── customer_service/
│   ├── risk_management/
│   └── transaction_monitoring/
├── analytics/              # Deep-dive analysis (segmentation, behavior)
└── regulatory/             # Compliance & mandatory reporting
```

### Where Does Registration Mart Go?

**Registration views belong in**: `marts_NEW/operational/`

**Rationale**:
- Used for day-to-day BaaS operations monitoring
- Not executive-level strategic KPIs
- Not deep-dive analytics or regulatory compliance

---

## Environment-Aware Date Limiting

### Critical Pattern for Dev/CI Environments

**Authoritative Pattern:** See `shared/knowledge-base/migration-quick-reference.md` → "ENVIRONMENT-AWARE DATE LIMITS"

**All intermediate models with date filters MUST include the environment-aware pattern.**

### Why This Matters

- **Dev environment**: Limited warehouse resources, faster iteration
- **CI environment**: Automated testing, needs to complete quickly
- **Production**: Full data loads for accurate business metrics

### Common Patterns

| Environment Type | Date Limit | Use Case |
|-----------------|------------|----------|
| `ci`, `continuous-integration` | **6 months** | Fast CI/CD testing |
| `development` | **6 months** | Local/dev warehouse testing |
| `production` (default) | **Full range** (365 days or unlimited) | Business reporting |

---

## Materialization Strategy by Layer

### Intermediate Layer

```sql
-- Metrics (aggregated, frequently reused)
{{ config(materialized='table') }}

-- Foundations (core account base, incremental for performance)
{{ config(materialized='incremental', unique_key='acct_uid') }}

-- Transactions (large datasets, incremental)
{{ config(materialized='incremental', unique_key='transaction_uid') }}
```

### Marts Layer

```sql
-- Operational dashboards (frequent access, real-time updates)
{{ config(materialized='table', post_hook="grant select on {{ this }} to svc_dbt_bi;") }}

-- Executive dashboards (small data, frequent access)
{{ config(materialized='table') }}

-- Analytics deep-dives (on-demand, complex queries)
{{ config(materialized='view') }}
```

---

## Naming Conventions

### Intermediate Models

**Pattern**: `int_<source>__<business_entity>_<detail>.sql`

Examples:
- `int_gbos__new_registrations.sql` (core entity)
- `int_gbos__registration_start_end.sql` (aggregated view)
- `int_gbos__registration_metrics_daily.sql` (metrics calculation)

### Mart Models

**Pattern**: `mart_<business_area>__<report_name>.sql`

Examples:
- `mart_operational__registration_views.sql`
- `mart_executive__kpi_dashboard.sql`
- `mart_analytics__customer_segmentation.sql`

---

## Post-Hook Standards

### Operational Marts (BI Tool Access)

```sql
{{ config(
    materialized='table',
    post_hook=[
        "analyze {{ this }};",
        "grant select on {{ this }} to svc_dbt_bi;"
    ]
) }}
```

### Internal Intermediate Models (No External Access)

```sql
{{ config(
    materialized='table',
    post_hook="analyze {{ this }};"
) }}
```

---

## Common Mistakes to Avoid

❌ **Don't do this**:
- Creating custom folders like `models/intermediate/gbos_registration/`
- Skipping environment-aware date limits
- Forgetting post-hook grants for BI-facing marts
- Using `getdate()` instead of `current_date` (Redshift-specific)

✅ **Do this instead**:
- Use established folder structure: `intermediate_NEW/metrics/gbos_based/`
- Add `{% if env_var('DBT_CLOUD_ENVIRONMENT_TYPE'...) %}` date filters
- Include `grant select` post-hooks for marts
- Use `current_date` for date comparisons

---

## Quick Reference: Where Should My Model Go?

| Model Type | Intermediate Location | Mart Location |
|-----------|----------------------|---------------|
| Account enrichment | `foundations/edw_account_base/` | N/A |
| GBOS registration metrics | `metrics/gbos_based/` | `operational/` |
| Transaction auth/posted | `transactions/gbos_based/` | `operational/transaction_monitoring/` |
| Revenue calculations | `metrics/edw_based/` | `executive/financial_summary/` |
| Customer segmentation | N/A (built in mart) | `analytics/customer_behavior/` |
| Regulatory reporting | N/A (built in mart) | `regulatory/financial_reporting/` |

---

## 🎓 Key Learning: Transaction Model Placement (2025-11-11)

**CRITICAL:** Transaction processing models belong in `transactions/edw_based/`, NOT `foundations/product/metrics/edw_based/`

### Why This Matters (dbt-agent-13)

**Wrong Location:**
```
❌ intermediate_NEW/foundations/product/metrics/edw_based/
   ├── enriched_auth/
   ├── enriched_posted/
   └── transaction_pairs/
```

**Correct Location:**
```
✅ intermediate_NEW/transactions/edw_based/
   ├── enriched_auth/
   ├── enriched_posted/
   └── transaction_pairs/
```

### Rationale

1. **`foundations/`** = Account enrichment, product hierarchy, time scaffolding (NOT transaction processing)
2. **`transactions/`** = Transaction processing (auth, posted, pairs) - explicit purpose
3. **Deeply nested paths** (6+ levels) are non-intuitive and violate architecture docs
4. **Follow `transactions_structure_guide.md`** for proper placement
5. **Consistency** - Marts use `operational/transaction_monitoring/`, intermediate should use `transactions/edw_based/`

### Architecture Principle

**"Folder name should match content purpose"**
- Transactions → `transactions/` folder
- Foundations → `foundations/` folder
- Don't nest transactions inside foundations/product/metrics

**Violation Pattern to Avoid:**
- Creating deeply nested folder hierarchies based on legacy pipeline concepts
- Mixing transaction processing with foundational building blocks
- Ignoring documented architecture guides

---

**Last Updated**: 2025-11-11
**Learned From**:
- GBOS registration views migration (built in wrong location, missing env limits)
- dbt-agent-13: Transaction model restructure (aligned with architecture docs)
