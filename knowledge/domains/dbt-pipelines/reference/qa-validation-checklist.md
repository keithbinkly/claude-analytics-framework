<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/reference/qa-validation-checklist.md
-->

> analytics-workspace migration note: this is a promoted copy from `dbt-agent`. Prefer this analytics-workspace path first. If a referenced companion doc has not been promoted yet, fall back to `dbt-agent`.

# QA Validation Checklist

**Purpose**: Systematic validation workflow to catch issues early and reduce QA iterations

**Target**: 1-2 QA cycles per model (down from 3-4)

---

## Phase 1: Pre-Migration Analysis (5-10 min)

### 1.1 Complexity Assessment
- [ ] Count UNION/UNION ALL statements (>3 = high complexity)
- [ ] Count window functions (ROW_NUMBER, DENSE_RANK, etc.)
- [ ] Count GROUPING SETS (indicates multi-grain aggregation)
- [ ] Identify CASE statements with complex logic
- [ ] Check for nested subqueries (>2 levels = refactoring candidate)

**Score**: Simple (0-3 points) | Medium (4-7 points) | Complex (8+ points)
- Each UNION: +1
- Each window function: +1
- GROUPING SETS present: +2
- Complex CASE logic: +1
- Nested >2 levels: +2

### 1.2 Field Mapping Check
- [ ] Cross-reference field names with `quick-reference/field-mappings.md`
- [ ] Identify any auth_reason vs combined_reason_codes usage
- [ ] Check for portfolio vs product_stack naming
- [ ] Verify merchant_nm vs merchant_cleaned usage
- [ ] Note any date field variations (calendar_date, week_end_date, etc.)

### 1.3 Business Logic Discovery
- [ ] Does script have comments explaining business rules?
- [ ] Are there filters that seem arbitrary? (e.g., `auth_reason NOT IN ('SUCCESS')`)
- [ ] Check for processor-specific logic (ACI, GBOS, etc.)
- [ ] Identify any hardcoded values that need explanation

**Action**: If business logic is unclear, **ASK keith-gd BEFORE coding**

---

## Phase 2: Model Development (20-40 min)

### 2.0 Dependency Analysis (NEW - MANDATORY)
**🚨 BEFORE writing or building ANY model:**

**Option A - Manifest Parser (Recommended - Instant)**:
- [ ] Use manifest-parser skill: `get_model_lineage('target_model_name')`
- [ ] Review parent_count and children_count
- [ ] Check parent models list for missing/outdated dependencies

**Option B - dbt ls (Fallback)**:
- [ ] Run `dbt ls --select +target_model_name --resource-type model`

**Then (Both Options)**:
- [ ] Check warehouse: Which dependencies already exist?
- [ ] Identify dependencies needing schema changes (new columns, etc.)
- [ ] Build missing/modified dependencies FIRST before target model
- [ ] Verify critical columns exist in warehouse

**Time**: 30 seconds (manifest) or 5-10 minutes (dbt ls) → saves 60-90 minutes of error-driven iteration

**References**:
- `.claude/skills/manifest-parser/SKILL.md`
- `session-logs/2025-11-06_interchange_qa_learnings.md` (Mistake #1)

### 2.0.1 Downstream Impact Analysis (MANDATORY for replacements/refactors)
**🚨 BEFORE designing architecture for model replacements:**

**Why this matters**: Creating new optimized models without planning downstream integration leads to "orphaned lineage" bugs where new models aren't consumed and old broken models keep running.

**Step 1: Inventory downstream consumers of target model**
```bash
# Using dbt-mcp (preferred):
mcp__dbt__get_model_lineage_dev --model_name "model_being_replaced"

# Check children list - these ALL need a migration plan
```

**Step 2: Check for semantic model dependencies**
```bash
# Find semantic models that ref the target:
grep -r "ref('model_name')" models/**/*.yml --include="sem_*.yml"
```

**Step 3: Design migration strategy BEFORE writing code**

| Strategy | When to Use | Pros | Cons |
|----------|-------------|------|------|
| **Backward-compat view** | Many downstream consumers | Zero ref changes needed | Extra layer |
| **Update all refs** | Few consumers, simple refs | Clean architecture | Coordination needed |
| **Deprecation period** | External consumers | Safe transition | Temporary duplication |

**Step 4: Document in architecture plan**
- [ ] List all downstream consumers found
- [ ] Chosen migration strategy with rationale
- [ ] Semantic model compatibility check (columns match?)
- [ ] Deployment sequence (what order to run models)

**Red Flag**: If you're creating new models without a documented plan for downstream consumers, STOP and complete this analysis first.

**Example Failure (GBOS Cohort 2026-01-15)**:
```
❌ What happened: Created new EAV models, marked old model "deprecated"
❌ Result: Semantic model + 3 views still ref'd old model → merge job failures
✅ Fix: Converted old model to VIEW reading from new model
✅ Lesson: Analyze downstream BEFORE architecture design
```

**Time**: 5-10 minutes upfront → saves hours of post-deployment debugging

### 2.1 Type-Safe Development
- [ ] Use explicit type casting for all UNION columns
- [ ] Cast hardcoded values to match source column types
- [ ] Use `NULL::TYPE` instead of arbitrary defaults (0, -1, etc.)
- [ ] Verify TIMESTAMP vs TIMESTAMP WITH TIME ZONE in date functions

**Reference**: `quick-reference/type-casting-cheatsheet.md`

### 2.2 Common Pattern Application
- [ ] For multi-grain (daily/weekly/monthly): Use GROUPING SETS pattern
- [ ] For time period detection: Aggregate by grain FIRST, then UNION with labels
- [ ] For merchant normalization: LEFT JOIN + NVL fallback pattern
- [ ] For transaction type joins: Use certified business rule logic

**Reference**: `quick-reference/field-mappings.md` → Transaction Type Hierarchies

### 2.3 Config Validation (NEW)
- [ ] SORTKEY references OUTPUT column names (after AS alias), not source columns
- [ ] GROUP BY counts only dimensions, excludes aggregates (COUNT, SUM, etc.)
- [ ] For aggregations: Add inline comment `group by 1, 2, ..., N  -- N dimensions`
- [ ] DISTKEY matches unique_key for incremental models

**Reference**: session-logs/2025-11-06_interchange_qa_learnings.md (Mistakes #2, #3)

### 2.4 Pre-Compilation Check (MANDATORY)
**🚨 ZERO TOLERANCE - Compile after EVERY script change:**
- [ ] Run `dbt compile --select model_name` (NEVER skip this)
- [ ] Review `target/compiled/.../model_name.sql` for obvious issues
- [ ] Check UNION column counts match across all CTEs
- [ ] Verify GROUP BY column counts match dimension count
- [ ] ONLY if compile succeeds → proceed to `dbt run`

**ROI**: 12-30x time savings per error (5-10 sec compile vs 2-5 min failed run)

**Reference**: shared/reference/MANDATORY_COMPILE_RULE.md

---

## Phase 3: Initial Validation (5-10 min)

### 3.1 Parse & Compilation (MANDATORY - ALWAYS RUN FIRST)
**🚨 ZERO TOLERANCE - Run in this exact order:**

- [ ] **STEP 1: Parse** → `dbt parse` (validates YAML syntax, refs, configs)
- [ ] Review parse warnings (missing models, deprecated syntax, etc.)
- [ ] **STEP 2: Compile** → `dbt compile --select model_name` (validates SQL logic)
- [ ] No warnings about missing columns or refs
- [ ] Compiled SQL looks reasonable (spot check in `target/compiled/`)
- [ ] **ONLY AFTER BOTH PASS** → Proceed to `dbt run`

**Why This Order**:
- Parse catches: Invalid refs, YAML syntax errors, config issues
- Compile catches: SQL syntax, JOIN errors, GROUP BY mismatches, type issues
- Running without parse/compile wastes 2-5 minutes per error

**ROI**: 12-30x time savings per error (10 sec parse + 5 sec compile vs 2-5 min failed run)

### 3.2 Temp Filter Scan (MANDATORY - Before ANY QA)
**🚨 Prevent "forgotten filter" debugging (saves 30-60 min)**

- [ ] **BEFORE starting QA**, scan for leftover temp filters:
```bash
# Scan all models for temp filters
grep -r "TEMP_FILTER\|TODO: REMOVE" models/ --include="*.sql"

# Alternative: Find suspicious recent date filters
grep -r "dateadd('day', -[7-9]\|dateadd('day', -[1-3][0-9]" models/ --include="*.sql" \
  | grep -v "{% if is_incremental"
```

- [ ] If found: Review if still needed, document in handoff, or remove immediately
- [ ] No temp filters found: ✅ Proceed to execution

**Why This Matters**: Forgotten 7-day filter caused 0 approvals before Nov 6 (Session 2025-11-13), wasted 60 min debugging

**Full Prevention Strategy**: See `shared/knowledge-base/troubleshooting.md` → Temporary Development Filters

### 3.3 Execution
**🚨 For QA Speed: Use temp date filters (WITH TRACKING)**
- [ ] Add 7-day temp filter to model: `WHERE calendar_month >= dateadd('day', -7, current_date)`
- [ ] Add standardized comment: `-- ⚠️ TEMP_FILTER: Fast QA iteration - Added 2025-MM-DD by [initials]`
- [ ] Add removal reminder: `-- ⚠️ TODO: REMOVE before final QA sign-off`
- [ ] **Track in handoff package**: List ALL temp filters for removal checklist
- [ ] Run: `dbt run --select model_name` (or `--full-refresh` if DISTKEY/SORTKEY changed)
- [ ] Note runtime (flag if >60s for a mart model)
- [ ] Check for warnings (data type coercion, etc.)

**Time Savings**: 80-90% faster builds during QA iteration

**⚠️ CRITICAL**: Before final build, remove all temp filters (use scan command above)

**Reference**: session-logs/2025-11-06_interchange_qa_learnings.md (Success #1, Mistake #4)

### 3.3 Basic Smoke Tests
- [ ] Row count > 0
- [ ] No unexpected NULLs in critical fields
- [ ] Date range covers expected period

**Quick Queries**:
```sql
-- Row count
SELECT COUNT(*) FROM {{ ref('model_name') }};

-- Null check on critical fields
SELECT 
  COUNT(*) AS total,
  COUNT(critical_field_1) AS field1_non_null,
  COUNT(critical_field_2) AS field2_non_null
FROM {{ ref('model_name') }};

-- Date range
SELECT MIN(calendar_date), MAX(calendar_date) 
FROM {{ ref('model_name') }};
```

### 3.4 Grain Integrity Check (MANDATORY after ANY model change)
**🚨 ALWAYS RUN after modifying a model — catches fan-out from ANY join**

**Purpose**: Verify the model's declared grain is still 1:1. A single extra join with overlapping keys silently inflates every downstream SUM.

```sql
-- Replace unique_key with the model's grain column (e.g., posted_txn_uid)
SELECT
    COUNT(*) as total_rows,
    COUNT(DISTINCT unique_key) as distinct_grain,
    COUNT(*) - COUNT(DISTINCT unique_key) as duplicate_rows,
    ROUND(
        (COUNT(*)::FLOAT / NULLIF(COUNT(DISTINCT unique_key), 0) - 1) * 100,
        2
    ) as inflation_pct
FROM {{ ref('model_name') }};
```

**Pass criteria**: `inflation_pct < 0.1%` (effectively zero duplicates)

**Red Flags**:
- `duplicate_rows > 0` → Fan-out from a JOIN producing 1:M instead of 1:1
- `inflation_pct > 1%` → STOP. Identify which join causes it before proceeding

**Diagnosis** (when fan-out detected):
```sql
-- Find which rows have duplicates
SELECT unique_key, COUNT(*) as row_count
FROM {{ ref('model_name') }}
GROUP BY unique_key
HAVING COUNT(*) > 1
ORDER BY row_count DESC
LIMIT 20;
```

**Why This Matters**: The eWallet extraction (Jan 28) QA verified the eWallet join was 1:1 but did NOT check the overall model grain. The `fct_acct_actives` SCD-2 fan-out (~20% inflation) went undetected because QA was scoped to the change, not the model.

**Rule**: QA the MODEL, not just the CHANGE.

### 3.5 Volume Trace (Multi-Stage Pipelines Only)
**When to use**: Pipeline has 3+ intermediate models before final mart
**Purpose**: Detect data suppression OR inflation between stages

**Quick Query** (Run at EACH stage):
```sql
-- Run at each pipeline stage to detect suppression or fan-out
SELECT
    'stage_name' as stage,
    COUNT(*) as total_rows,
    COUNT(DISTINCT unique_key) as distinct_keys,
    COUNT(*) - COUNT(DISTINCT unique_key) as fanout_rows,
    MIN(date_field) as min_date,
    MAX(date_field) as max_date
FROM {{ ref('model_at_this_stage') }}
WHERE product_stack = 'Target Product';
```

**Red Flags**:
- Stage N has <50% rows of Stage N-1 (unexpected suppression)
- `total_rows > distinct_keys` at any stage (fan-out — rows being duplicated)
- Distinct key count drops >20% between stages
- Date range narrows unexpectedly

**Action**: If variance >50% between stages OR fan-out detected, STOP and investigate THAT stage's filter/join logic before continuing QA

---

## Phase 4: Comparative QA (10-15 min)

### 4.1 Seed Data Comparison (if available)
- [ ] Load QA seed: `dbt seed --select qa_seed_name`
- [ ] Use Template 1 from `common-qa-queries.md`
- [ ] Calculate variance % for all key metrics
- [ ] Document variance in comments or QA analysis file

**Acceptance Criteria** (confirm with keith-gd):
- <1%: ✅ PASS (expected minor differences)
- 1-5%: ⚠️ REVIEW (acceptable if explainable)
- >5%: ❌ INVESTIGATE (likely logic error)

### 4.2 Grain Validation
- [ ] Check for unexpected duplicates on unique_key
- [ ] Verify time series has no gaps (if daily data)
- [ ] Confirm merchant count matches expectation

**Use**: Template 6 & Template 5 from `common-qa-queries.md`

### 4.3 Top N Validation (for ranking models)
- [ ] Compare top 25 merchants between legacy and new
- [ ] Check if rankings are consistent
- [ ] Verify ranking column values (1-25, no gaps)

**Use**: Template 4 from `common-qa-queries.md`

### 4.4 Row-Level Sample Trace (CRITICAL for complex pipelines)
**When to use**: Any model with 3+ joins, or when aggregate QA shows unexpected variance
**Purpose**: Build concrete understanding of data flow at atomic level

**Sample Selection** (pick 3-5 transactions):
- [ ] 1 "happy path" transaction (all joins succeed, typical values)
- [ ] 1 edge case (NULL in optional field, boundary date, etc.)
- [ ] 1 from the problematic population (if investigating variance)
- [ ] 1-2 random samples for variety

**Trace Query Pattern**:
```sql
-- Trace a single transaction through every CTE/join stage
WITH sample_txn AS (
    SELECT 'YOUR_TRANSACTION_ID' as target_id
),

-- Stage 1: Source table
stage_1_source AS (
    SELECT * FROM {{ ref('stg_source_table') }}
    WHERE unique_id = (SELECT target_id FROM sample_txn)
),

-- Stage 2: After first join (check for fan-out or suppression)
stage_2_after_join AS (
    SELECT s.*, j.new_field
    FROM stage_1_source s
    LEFT JOIN {{ ref('join_table') }} j ON s.key = j.key
),

-- Continue for each CTE/join in the model...

-- Final: Summary showing row count at each stage
SELECT 'stage_1_source' as stage, COUNT(*) as rows, 'Expected: 1' as note FROM stage_1_source
UNION ALL SELECT 'stage_2_after_join', COUNT(*), 'Fan-out if >1' FROM stage_2_after_join
-- Add all stages
ORDER BY stage;
```

**What to Document**:
- [ ] Row count at each stage (1 → 1 = good, 1 → 2+ = fan-out, 1 → 0 = suppression)
- [ ] Which join caused fan-out (if any)
- [ ] Key field values that explain the behavior
- [ ] Screenshot or save query results for handoff

**Red Flags**:
| Pattern | Meaning | Action |
|---------|---------|--------|
| 1 → 2+ rows | Fan-out from join | Add QUALIFY dedup or fix join key |
| 1 → 0 rows | Suppression from INNER JOIN or filter | Check if intentional, switch to LEFT JOIN |
| NULL in unexpected field | Join didn't match | Verify join keys, check for data quality issue |

**Example Investigation** (RTP duplicates):
```sql
-- Trace one of the 4 duplicate GlobalFundTransferIDs
WITH sample AS (SELECT 'DUPLICATE_ID_HERE' as gft_id),

transfers AS (
    SELECT * FROM stg_azuresql_gss_gft__globalfundtransfer
    WHERE GlobalFundTransferID = (SELECT gft_id FROM sample)
),

after_ledger_join AS (
    SELECT t.*, tl.IsDebit
    FROM transfers t
    LEFT JOIN stg_azuresql_gss_gft__globalfundtransferledger tl
        ON t.GlobalFundTransferKey = tl.GlobalFundTransferKey
),

after_profile_join AS (
    SELECT alj.*, tp.GlobalFundTransferProfileKey
    FROM after_ledger_join alj
    INNER JOIN stg_azuresql_gss_gft__globalfundtransferprofile tp
        ON tp.GlobalFundTransferProfileKey = alj.TargetGlobalFundTransferProfileKey
)

SELECT 'transfers' as stage, COUNT(*) as rows FROM transfers
UNION ALL SELECT 'after_ledger_join', COUNT(*) FROM after_ledger_join
UNION ALL SELECT 'after_profile_join', COUNT(*) FROM after_profile_join;
-- If any stage shows >1 row, that's where the fan-out happens
```

**Time**: 10-15 min per model (but saves hours of aggregate-level guessing)

---

### 4.5 Impact Validation & Human Approval Gate (MANDATORY)
**🚨 STOP - Do NOT implement fixes without completing this section**

After identifying root cause and proposed fix from row-level trace:

#### Step 1: Run Impact Validation Queries
**Purpose**: Quantify exactly how much data is affected by the proposed fix

```sql
-- TEMPLATE: Impact assessment for deduplication fix
-- Quantify: How many records affected? How many accounts? What time range?

-- Query 1: Count affected records
SELECT
    'affected_records' as metric,
    COUNT(*) as value,
    MIN(date_field) as earliest,
    MAX(date_field) as latest
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY unique_key ORDER BY tiebreaker DESC) as rn
    FROM {{ ref('model_name') }}
)
WHERE rn > 1;  -- Records that WOULD BE removed by dedup

-- Query 2: Check for value differences in duplicates (CRITICAL)
SELECT
    unique_key,
    COUNT(*) as duplicate_count,
    COUNT(DISTINCT amount_field) as distinct_amounts,
    CASE
        WHEN COUNT(DISTINCT amount_field) > 1 THEN '⚠️ DIFFERENT VALUES'
        ELSE '✅ Safe to dedup'
    END as assessment
FROM {{ ref('model_name') }}
GROUP BY unique_key
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC
LIMIT 20;

-- Query 3: Account/entity impact
SELECT
    COUNT(DISTINCT account_id) as affected_accounts,
    COUNT(DISTINCT customer_id) as affected_customers,
    SUM(amount_field) as total_amount_in_duplicates
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY unique_key ORDER BY tiebreaker DESC) as rn
    FROM {{ ref('model_name') }}
)
WHERE rn > 1;
```

#### Step 2: Document Findings for Human Review
- [ ] **Root cause identified**: Which CTE/join causes the issue?
- [ ] **Records affected**: Exact count (e.g., "4 duplicate GlobalFundTransferIDs")
- [ ] **Value consistency**: Do duplicates have same or different values?
- [ ] **Account impact**: How many unique accounts/entities affected?
- [ ] **Time range**: When did this start? Recent or historical?
- [ ] **Proposed fix**: Specific code change (e.g., "Add QUALIFY clause to transfer_ledger CTE")
- [ ] **Risk assessment**: Safe to dedup vs needs business review

#### Step 3: Human Approval Gate
**🛑 STOP HERE - Present to user before implementing**

Present findings in this format:
```
## QA Investigation Complete - Approval Required

### Root Cause
[Which CTE/join, why it happens]

### Impact Assessment
- Records affected: X
- Accounts affected: Y
- Value differences: None / X cases with different values
- Time range: [date range]

### Proposed Fix
[Specific code change with line numbers]

### Risk Level
- ✅ LOW: All duplicates have identical values, safe to dedup
- ⚠️ MEDIUM: Some value differences, may lose data
- 🔴 HIGH: Significant value differences, needs business review

### Recommendation
[Your recommendation: proceed / needs discussion / escalate]

**Awaiting your approval to implement fix.**
```

**Only proceed to implementation after explicit user approval.**

#### Step 4: Document Join Behavior in Folder README (MANDATORY after fix)
**Purpose**: Capture data model knowledge permanently so it doesn't need to be re-discovered

After implementing fix, create or update `README.md` in the model folder:

```markdown
# [Pipeline Name] Documentation

## Models

### `model_name`
- **Grain**: One row per [unique_key]
- **Purpose**: [Brief description]
- **Key Logic**:
  - **[Pattern Name]**: [Why this exists]
    - *Note*: [Critical gotcha or business rule]
  - **Deduplication**: [If applicable] The join to [table] uses a `QUALIFY` clause
    to select [criteria] for each [key]. This handles [root cause] preventing
    [consequence].
  - **Verification**: Analysis confirms [validation finding].
```

**What to Document**:
- [ ] Join behavior that caused issues (fan-out sources, dedup logic)
- [ ] Business rules discovered during investigation
- [ ] Filter gotchas (e.g., "INNER JOIN alone won't filter X")
- [ ] Verification findings (e.g., "duplicates always have same amount")

**Why This Matters**:
- Next developer/agent won't re-discover the same issue
- Business logic is localized with the code
- Done once, persists forever

**Example** (RTP pipeline):
> "The join to `globalfundtransferledger` uses QUALIFY...ORDER BY CreateDate DESC
> because the source system creates multiple ledger revisions for status updates."

### 4.6 Materialization-Change QA (Template 5)
**When to use**: DIST/SORT changes, view-to-table, table-to-incremental, or any materialization-only change where data content is NOT expected to change.

**Why a separate template**: Templates 1-4 assume data content changes. Materialization changes need physical validation + runtime comparison, not content variance. A 30-day variance check on a materialization change compares unlike scopes and produces misleading results.

**Step 1: Physical Layout Validation (MANDATORY)**
```sql
-- Confirm DISTKEY, SORTKEY applied correctly
SELECT
    "schema", "table", diststyle, sortkey1, sortkey_num,
    size AS size_mb, tbl_rows, unsorted, skew_rows
FROM svv_table_info
WHERE "table" = 'your_model_name';
```

**Pass criteria:**
- `diststyle` matches your config
- `sortkey1` matches expected column
- `skew_rows` < 2.0 (< 4.0 is warning)
- `unsorted` < 20% (run VACUUM if high)

**Step 2: Skew Check**
```sql
-- Verify no single slice holds disproportionate data
SELECT
    slice, COUNT(*) AS row_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM your_schema.your_model_name
GROUP BY slice
ORDER BY row_count DESC;
```

**Pass criteria:** No single slice > 40% of total rows.

**Step 3: Runtime Comparison (Controlled Probe)**
```sql
-- Run identical query on old vs new materialization
-- Use the SAME filter shape that BI tools use
SELECT COUNT(*), SUM(metric_column)
FROM your_model_name
WHERE date_column >= DATEADD('month', -3, CURRENT_DATE)
  AND dimension_column = 'common_value';
```

Run against both old (if available) and new materialization. Compare elapsed time.
**Gate:** >= 30% improvement for performance-motivated changes.

**Step 4: Data Integrity Verification**
```sql
-- Confirm content is identical (pivot consistency with NULL-safe comparison)
SELECT
    dimension_column,
    COALESCE(SUM(metric_column), 0) AS total_metric,
    COUNT(*) AS row_count
FROM your_model_name
GROUP BY 1
ORDER BY 1;
```

Compare output against a snapshot taken before the materialization change.

**Step 5: dbt Tests**
- [ ] Run `dbt test --select your_model_name` — all tests must pass
- [ ] No new warnings or errors

---

## Phase 5: Pre-PR Readiness Check (2-5 min)

**🚨 MANDATORY before opening PR - prevents CI iteration loops**

### 5.1 State:Modified Selection Check
**Purpose**: Preview exactly which models CI will build/test

```bash
# Run from dbt project root (requires production manifest in target/)
dbt ls --select state:modified+1 --state target --target-path target_run --defer --favor-state
```

**Review Output**:
- [ ] Only expected models appear (the ones you actually changed)
- [ ] No unrelated models flagged (e.g., TPG models when PR is about merchant analytics)
- [ ] Downstream +1 dependencies are correct

**If Unexpected Models Flagged**:
1. Check `git diff origin/main --name-only` for unintended file changes
2. Check `packages.yml` for version bumps (cascade to all models using those packages)
3. Check source YAMLs for freshness/config changes (cascade to all downstream models)
4. Add `--exclude` for legitimately unrelated models if needed

**Common Exclusions** (add to CI command if needed):
```bash
--exclude path:models/staging/tpg path:models/intermediate/tpg path:models/intermediate/tpg_operations path:models/marts/tpg_operations
```

### 5.2 CI Command Validation
- [ ] Verify CI command includes `--target-path target_run` (prevents manifest overwrite)
- [ ] Verify exclusions are appropriate for this PR
- [ ] Test full CI command locally if possible

**Reference**: `docs/dbt-cloud-ci-slim-ci-mechanics.md`

### 5.3 Lineage Verification (MANDATORY for model replacements/refactors)
**🚨 CRITICAL: Prevents "orphaned lineage" bugs where new models aren't wired up**

**When to run**: Any time you:
- Create new models that replace existing ones
- Refactor model architecture (e.g., table → view, single → multi-layer)
- Modify models referenced by semantic layer

**Step 1: Verify new model has downstream consumers**
```bash
# Using dbt-mcp (preferred - instant):
mcp__dbt__get_model_lineage_dev --model_name "new_model_name"

# Check: children_count > 0 (unless intentionally a leaf model)
# Check: children list includes expected consumers
```

**Step 2: Verify old model (if being replaced) is properly rewired**
```bash
# Check old model's lineage - should now read from new model:
mcp__dbt__get_model_lineage_dev --model_name "old_model_name"

# Check: parents list includes new optimized model
# Check: children still intact (views, semantic models, etc.)
```

**Step 3: Verify semantic model references**
```bash
# Find semantic models referencing this domain:
grep -r "ref('model_name')" models/**/*.yml --include="sem_*.yml"

# For each semantic model found:
# - Verify it points to correct model
# - Verify all dimensions/measures use columns that exist in new model
```

**Step 4: Document lineage changes in PR/handoff**
- [ ] List models created
- [ ] List models modified (table → view, etc.)
- [ ] List downstream consumers verified
- [ ] Confirm semantic model compatibility

**Red Flags**:
| Pattern | Problem | Fix |
|---------|---------|-----|
| New model has 0 children | Not wired up | Create backward-compat view or update refs |
| Old model still has old parents | Replacement incomplete | Update old model to ref new model |
| Semantic model points to deprecated model | Will break in prod | Update semantic model ref |

**Example Investigation (GBOS Cohort 2026-01-15)**:
```
Problem: Created mrt_gbos_registration_cohort_metrics but old model still failing
Root cause: mrt_gbos_registration_cohort_progress still existed as table,
           semantic model still pointed to it
Fix: Converted old model to VIEW that reads from new model
Lesson: Always verify lineage before closing ticket
```

**Reference**: `.dots/dbt-agent-gbos-cohort-optimization.md`

---

## Phase 6: Edge Case Testing (5 min)

### 6.1 Boundary Conditions
- [ ] Check behavior on first/last date in dataset
- [ ] Verify handling of products with minimal data
- [ ] Test single-record products (if applicable)

### 6.2 Known Issues
- [ ] Verify ACI migration logic applied (auth approvals excluded)
- [ ] Check merchant normalization is working (no excessive nulls)
- [ ] Confirm posted reversals are excluded where required

---

## Phase 7: Documentation (5 min)

### 7.1 Inline Documentation
- [ ] Model header explains business purpose
- [ ] Critical business rules documented (e.g., ACI migration)
- [ ] Complex logic has explanatory comments
- [ ] Dependencies noted (upstream models, macros)

### 7.2 QA Results
- [ ] Save comparison query to `analyses/qa_validation/`
- [ ] Document variance findings in analysis file
- [ ] Note any known/acceptable differences

### 7.3 Schema Documentation
- [ ] Add model to appropriate `schema.yml`
- [ ] Document critical columns
- [ ] Add data quality tests where appropriate

---

## Common Failure Modes & Preventions

| Failure Mode | Prevention | Detection | Fix Time |
|--------------|-----------|-----------|----------|
| Type mismatch in UNION | Pre-compilation type check | Runtime error | 5-10 min |
| Double-counting approvals | Check for ACI migration logic | QA variance >50% | 15-20 min |
| NULL merchants | Verify join conditions + fallback | Null check query | 10-30 min |
| Wrong time period logic | Use GROUPING SETS pattern | Row count mismatch | 15-25 min |
| Missing business rules | Ask keith-gd upfront | QA variance >5% | 20-40 min |

---

## Parallelization Readiness

**Can migrate in parallel if**:
- [ ] No shared upstream dependencies being developed
- [ ] Independent business domains (spend vs balance vs registration)
- [ ] Different target schemas
- [ ] QA seeds available for each

**Must be sequential if**:
- Dependencies on other in-progress models
- Shared macros need development
- Same business domain (risk of conflicting logic)

---

## QA Cycle Metrics (Track These)

**Per Migration**:
- Compilation attempts before success
- Runtime errors encountered
- QA iterations before acceptance
- Total time from start to commit

**Session Aggregate**:
- Models completed per session
- Average QA cycles per model
- Most common error type
- Time saved by templates/checklists

---

## Quick Reference: QA Commands

```bash
# MANDATORY SEQUENCE (always run in this order):
dbt parse                                    # 1. Validate YAML/refs/configs
dbt compile --select model_name              # 2. Validate SQL logic
dbt run --select model_name                  # 3. Execute build

# Run model
dbt run --select model_name

# Run with downstream
dbt run --select model_name+

# Run comparison query
dbt show --inline "<paste query from common-qa-queries.md>"

# Load seed for validation
dbt seed --select qa_seed_name

# Check for errors
dbt test --select model_name
```

---

## Checklist Usage

**Before starting**: Review Phase 1 (5-10 min upfront investment)
**During development**: Reference Phase 2 patterns
**After first run**: Execute Phase 3-5 systematically
**Before commit**: Complete Phase 6 documentation

**Goal**: Make validation mechanical, not creative

---

## Last Updated
2026-01-15

**Change Log**:
- 2026-02-21: Added Template 5 (Materialization-Change QA) from registration funnel post-mortem; added NULL-safe comparison standard
- 2026-01-15: Added Phase 2.0.1 Downstream Impact Analysis (pre-implementation) + Phase 5.3 Lineage Verification (post-implementation) - two-gate protection against orphaned lineage bugs discovered in GBOS cohort optimization
- 2026-01-06: Added Phase 5 Pre-PR Readiness Check with state:modified selection validation (prevents CI iteration loops from unexpected model selection)
- 2025-12-11: Added Phase 4.5 Step 4 - Document Join Behavior in Folder README (persist data model knowledge with the code)
- 2025-12-11: Added Phase 4.5 Impact Validation & Human Approval Gate (MANDATORY checkpoint before implementing fixes - quantify affected data + get user approval)
- 2025-12-10: Added Phase 4.4 Row-Level Sample Trace (critical for understanding join behavior at atomic level)
- 2025-10-09: Initial version

**Maintenance**: 
- Update acceptance criteria thresholds as project matures
- Add new failure modes as discovered
- Track metrics to measure improvement
