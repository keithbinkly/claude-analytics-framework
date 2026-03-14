<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/knowledge-base/migration-quick-reference.md
-->

> CAF migration note: this is a promoted copy from `dbt-agent`. Prefer this CAF path first. If a referenced companion doc has not been promoted yet, fall back to `dbt-agent`.

# 🚀 Migration Quick Reference
**Critical patterns and checklists for all migrations**

## ⚠️ MANDATORY PRE-FLIGHT CHECKLIST
**Read these BEFORE starting any migration:**

✅ [ ] **Legacy Script Analysis** (if provided): Read FIRST to understand:
  - Metric definitions (especially Started, Passed, Failed, Active, etc.)
  - Source table choices for product/merchant mappings
  - Aggregation grain (account vs event vs transaction)
  - Business rules and filters (commented or in CASE logic)
✅ [ ] **Canonical Models**: Load `canonical-models-registry.md` - ask user for overlap
✅ [ ] **Macros**: Load `knowledge/domains/dbt-pipelines/reference/macros-registry.md` - check for reusable logic patterns
✅ [ ] **Folder Structure**: Load `folder-structure-and-naming.md` - verify correct location
✅ [ ] **QA Methodology**: Load `shared/reference/qa-validation-checklist.md` - use proper templates
✅ [ ] **Environment Limits**: Apply 6-month dev/CI limit pattern to all date-filtered models
✅ [ ] **Materialization**: Choose correct strategy per layer (incremental for intermediate)

## 🚨 ZERO-TOLERANCE EXECUTION RULES

### Rule #1: Check Dependencies BEFORE Build
**Pattern**: Use manifest-parser skill OR `dbt ls --select +model_name`

**Option A - Manifest Parser (Recommended - Instant)**:
```python
# Use manifest-parser skill (after dbt compile/run exists)
from manifest_parser import get_model_lineage

lineage = get_model_lineage('target_model_name')
print(f"Parents: {lineage['parent_count']}")
print(f"Children: {lineage['child_count']}")
# Shows full upstream/downstream instantly
```

**Option B - dbt ls (Fallback)**:
```bash
dbt ls --select +model_name --resource-type model
```

**Process**:
- ALWAYS check dependencies first
- Identify missing upstream models
- Build dependencies in correct order
- Prevents 60-90 min of error-driven iteration

**Reference**: `.claude/skills/manifest-parser/SKILL.md`

### Rule #2: Compile After EVERY Change
**Pattern**: `dbt compile → dbt run` (never skip compile)
- ROI: 12-30x time savings per error
- Catches syntax, JOIN, GROUP BY, SORTKEY errors instantly
- See: `shared/reference/MANDATORY_COMPILE_RULE.md`

### Rule #3: Define Grain BEFORE Building
**"Wrong granularity creates substantial technical debt."** - dbt Labs

**What is grain?** The level of detail for each row (transaction, account, day, month)

**Why it matters:**
- Aggregating UP is easy (daily → monthly)
- Disaggregating DOWN is expensive/impossible (monthly → daily)
- Wrong grain = rebuild entire pipeline

**Process**:
1. **Ask first:** "What's the grain of the legacy report?"
2. **Start lowest:** Choose the most granular level needed
3. **Document explicitly:** Add grain comment in model header

```sql
-- Grain: One row per posted_txn_uid (transaction-level)
-- Downstream aggregation: product × calendar_month in mart layer
```

**Common grain mismatches:**
| Legacy Says | Likely Grain | Watch For |
|-------------|--------------|-----------|
| "Monthly metrics by product" | Account-month OR Transaction aggregated | Check if they track individual transactions |
| "Active accounts" | Account-level snapshot | Daily vs monthly snapshot |
| "Transaction summary" | Could be txn-level or daily aggregate | Check for txn_id columns |

**KEY ASSUMPTION**: Legacy QA datasets (`analytics.*_views`, etc.) powering business reports are maintained current through present date unless user states otherwise.

---

## 🏗️ DATA WAREHOUSE ARCHITECTURE CONTEXT

### EDW vs ODS Relationship

**ODS (Operational Data Store)**:
- First intake layer of unified data warehouse
- Raw operational data from source systems
- Less optimized for analytics use cases

**EDW (Enterprise Data Warehouse)**:
- Optimized views built for analytics use cases
- Better performance, richer dimensions, pre-computed hierarchies
- Preferred source for analytics workloads

**Preference Rule**: **ALWAYS prefer EDW table over ODS table where available** (vast majority of cases)

**Canonical Models**: For posted transactions, prefer enriched canonical `int_transactions__posted_all` over `stg_edw__fct_posted_transaction` or `stg_ods__posted_transaction`

**Exception**: Some tables only exist in ODS (e.g., `ods.interchange_transaction` has no EDW equivalent) → use ODS staging

---

## 📁 CORRECT FOLDER PLACEMENT

### Intermediate Layer (`models/intermediate/intermediate_NEW/`)
```
foundations/          # Account base, product hierarchies
transactions/         # Auth/posted transactions (gbos_based/, gss_based/, ods_based/)
balances/             # Balance data
registrations/        # Customer registration data
metrics/              # REUSABLE metric calculations
  ├── edw_based/      # EDW metrics
  └── gbos_based/     # GBOS metrics (registration, verification, etc.)
```

### 2-Layer Intermediate Pattern (for Revenue/Transaction Models)
**Following OCT disbursements pattern** (`int_oct__transfer_details` → `int_oct__aggregated_transfers`):

**Layer 1: Detailed Enriched Model**
- **Grain**: Transaction-level (most granular - `interchange_txn_uid` or `posted_txn_uid`)
- **Purpose**: Full enrichment with all dimensions, no aggregations
- **Materialization**: Incremental table
- **Location**: `intermediate_NEW/transactions/ods_based/` or `intermediate_NEW/metrics/edw_based/`

**Layer 2: Aggregated Metrics Model**
- **Grain**: Aggregated (removes transaction-level identifiers)
- **Purpose**: Pre-calculated metrics with status-specific transformations (e.g., `failed_amount = CASE WHEN status = 'Failed' THEN amount ELSE 0 END`)
- **Materialization**: View (fast aggregation from Layer 1)
- **Location**: Same folder as Layer 1

**Example**: `int_interchange__revenue_details` (Layer 1) → `int_interchange__revenue_aggregated` (Layer 2)

### Backward-Compatibility VIEW Pattern (for Model Replacements)
**When replacing a model that has downstream consumers:**

**Problem**: Creating new optimized models without planning downstream integration leads to "orphaned lineage" where old broken models keep running.

**Solution**: Convert old model to a VIEW that reads from new optimized model:

```sql
-- mrt_old_model.sql (was TABLE, now VIEW)
{{ config(
    materialized='view'
) }}

-- Backward-compatibility view reading from new EAV model
-- Pivots new format back to wide format for existing consumers
select
    product_stack,
    registration_start_date,
    MAX(CASE WHEN metric_name = 'Cohort Size' THEN cumulative_count END) as cohort_size,
    MAX(CASE WHEN metric_name = 'Passed' THEN cumulative_count END) as cumulative_passed,
    MAX(CASE WHEN metric_name = 'Failed' THEN cumulative_count END) as cumulative_failed
from {{ ref('mrt_new_optimized_model') }}
group by 1, 2
```

**When to use:**
- Many downstream consumers (semantic models, views, dashboards)
- Changing from wide format to EAV or vice versa
- Significant performance optimization with schema change

**Benefits:**
- Zero ref changes in downstream models
- Transparent migration path
- Easy rollback if issues

**Example (GBOS 2026-01-15):**
```
int_gbos_registration_enriched
    ↓
int_gbos_registration_metrics_daily (new Layer 1)
    ↓
mrt_gbos_registration_cohort_metrics (new Layer 2, EAV format)
    ↓
mrt_gbos_registration_cohort_progress (VIEW, backward-compat wide format)
    ↓
[semantic model, downstream views - unchanged]
```

### Marts Layer (`models/marts/marts_NEW/`)
```
executive/            # C-suite KPIs
operational/          # Day-to-day operations (registration monitoring)
  ├── customer_service/
  ├── risk_management/
  └── transaction_monitoring/
analytics/            # Deep-dive analysis
regulatory/           # Compliance reporting
```

### Where Registration Goes:
- **Metrics**: `intermediate_NEW/metrics/gbos_based/`
- **Views**: `marts_NEW/operational/`

---

## 🎯 SEMANTIC LAYER PATTERNS

### Metric Type Hierarchy
**Critical**: Ratio metrics must reference METRICS, not MEASURES

```yaml
# ❌ WRONG: References measures directly
- name: decline_rate
  type: ratio
  type_params:
    numerator: decline_cnt  # This is a MEASURE - will fail!
    denominator: attempt_cnt  # This is a MEASURE - will fail!

# ✅ CORRECT: Create simple metrics first, then reference them
- name: metric_decline_cnt
  type: simple
  type_params:
    measure: decline_cnt

- name: metric_attempt_cnt
  type: simple
  type_params:
    measure: attempt_cnt

- name: decline_rate
  type: ratio
  type_params:
    numerator: metric_decline_cnt  # References METRIC ✓
    denominator: metric_attempt_cnt  # References METRIC ✓
```

**Why**: MetricFlow requires explicit metric definitions for ratio calculations  
**When**: Any ratio, derived, or conversion metric type  
**Error if wrong**: `The metric 'X' does not exist but was referenced`

### Semantic Manifest Generation
**Critical**: `dbt parse` and `dbt compile` do NOT generate `semantic_manifest.json`

```bash
# ❌ WRONG: These don't create semantic_manifest.json
dbt parse --target dev
dbt compile --target dev

# ✅ CORRECT: Use build or run
dbt build --target dev --select <semantic_model_base_table>
dbt run --target dev --select <semantic_model_base_table>
```

**Why**: Only build/run trigger semantic manifest generation in dbt Fusion  
**Error if wrong**: `ERROR: Unable to load the semantic manifest`

---

## ⚡ ENVIRONMENT-AWARE DATE LIMITS
**ALL intermediate models with dates MUST include:**

```sql
where 1=1
    {% if env_var('DBT_CLOUD_ENVIRONMENT_TYPE', 'development') in ('ci', 'continuous-integration', 'development') %}
    and createdate >= dateadd('month', -6, current_date)  -- Dev/CI: 6-month limit
    {% else %}
    and createdate >= dateadd('day', -365, current_date)  -- Prod: full 365-day lookback
    {% endif %}
```

---

## 🧪 QA VALIDATION METHODOLOGY
**Use Templates 1-4 from qa-validation-checklist.md, NOT row counts**

**Authoritative Source:** `shared/reference/qa-validation-checklist.md`

| Template | Purpose | Section |
|----------|---------|---------|
| Template 1 | Basic Comparison (variance %) | Phase 4.1 |
| Template 4 | Top N Validation (rankings) | Phase 4.3 |
| Template 5 | Time Series Gaps | Phase 4.2 |
| Template 6 | Grain Validation (duplicates) | Phase 4.2 |

**Key Phases:**
- **Phase 4.4**: Row-Level Sample Trace (critical for complex pipelines)
- **Phase 4.5**: Impact Validation & Human Approval Gate (MANDATORY)

**Acceptance Criteria:** <0.1% variance for metrics, explicit user approval before fixes

---

## ⚙️ MATERIALIZATION STRATEGIES

### Intermediate Models
```sql
-- Metrics (aggregated, reusable)
{{ config(materialized='table') }}

-- Foundations/Transactions (large datasets)
{{ config(materialized='incremental', unique_key='unique_id') }}
```

### Mart Models
```sql
-- Operational dashboards (BI access)
{{ config(
    materialized='table',
    post_hook="grant select on {{ this }} to svc_dbt_bi;"
) }}

-- Analytics (complex, on-demand)
{{ config(materialized='view') }}
```

---

## 🔄 INCREMENTAL STRATEGIES

### Merge Strategy (Preferred)
```sql
{{ config(materialized='incremental', unique_key='unique_id') }}

{% if is_incremental() %}
    and updated_at >= (select max(updated_at) from {{ this }})
{% endif %}
```

### Delete+Insert Strategy (Large Lookbacks)
```sql
{{ config(
    materialized='incremental',
    incremental_strategy='delete+insert',
    unique_key='unique_id'
) }}

{% if is_incremental() %}
    and updated_at >= dateadd('day', -7, current_date)  -- 7-day lookback
{% endif %}
```

---

## 🏗️ NAMING CONVENTIONS

### Intermediate Models
`int_<source>__<business_entity>_<detail>.sql`

Examples:
- `int_gbos__new_registrations.sql`
- `int_gbos__registration_metrics_daily.sql`

### Mart Models
`mart_<business_area>__<report_name>.sql`

Examples:
- `mart_operational__registration_views.sql`
- `mart_executive__kpi_dashboard.sql`

---

## ⚠️ COMMON MISTAKES TO AVOID

❌ **Don't**:
- Build without checking dependencies first (`dbt ls --select +model`)
- Run without compiling first (ZERO TOLERANCE rule)
- Create custom folders outside `intermediate_NEW/` or `marts_NEW/`
- Skip environment-aware date limits
- Use row count QA instead of proper templates
- Forget BI grants for operational marts
- Use `getdate()` instead of `current_date`
- Reference source column names in SORTKEY (use output column names after AS)
- Include aggregate columns in GROUP BY (dimensions only)
- Forget to track temp date filters for removal

✅ **Do**:
- Check dependencies: `dbt ls --select +model_name` BEFORE build
- Compile after EVERY change: `dbt compile` → `dbt run`
- Track temp filters: `-- ⚠️ TODO: REMOVE after QA passes`
- Use output column names in SORTKEY config
- Count dimensions separately from aggregates in GROUP BY
- Always ask user for canonical model overlap first
- Use established folder structure
- Apply 6-month dev/CI limits to date-filtered models
- Include `grant select` post-hooks for marts
- Use QA templates 1-4, not basic comparisons

---

## 📋 MIGRATION WORKFLOW

1. **ASK USER**: "What existing models overlap with this script?"
2. **READ**: Canonical models registry, folder structure guide
3. **VERIFY**: Correct folder location with user approval
4. **WRITE**: Models in correct locations with env limits
5. **QA**: Use proper templates, not row counts
6. **HANDOFF**: Create structured package for Copilot

---

## 🚨 STOP AND ASK USER IF

- Can't find canonical models after asking
- Unclear business logic in legacy script
- Multiple valid architectural approaches
- Folder placement uncertain (always verify before writing)

---

**This replaces scattered guidance across 5+ files. Load this BEFORE any migration.**
