# Architecture Validation Checklist
**Purpose:** Ensure models are placed in correct locations per documented architecture
**Created:** 2025-11-11 (Lesson from dbt-agent-13)

---

## 🎯 When to Use This Checklist

Use BEFORE:
- Creating any new intermediate or mart models
- Migrating legacy scripts to dbt
- Recommending folder placement to users
- Approving model placement in code reviews

**Why:** Prevents misplaced models that violate architecture standards (path depth, wrong folders, duplicate concepts)

---

## ✅ Validation Steps

### Step 1: Load Architecture Documentation

**MANDATORY: Read these files from dbt-enterprise project:**

```bash
# Intermediate layer guides
/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise/models/intermediate/intermediate_NEW/intermediate_structure_guide.md
/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise/models/intermediate/intermediate_NEW/transactions/transactions_structure_guide.md
/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise/models/intermediate/intermediate_NEW/foundations/edw_account_base/foundations_structure_guide.md

# Marts layer guide
/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise/models/marts/marts_NEW/marts_structure_guide.md
```

**DO NOT rely on:**
- Generic dbt guidance alone
- Memory of folder structure
- Assumptions based on model name

**Key Principle:** "Reality (architecture docs) beats theory (generic guidance)"

---

### Step 2: Identify Model Purpose

**Ask these questions:**

1. **What does this model do?**
   - Transaction processing (auth, posted, pairing)
   - Account enrichment (customer dimensions, product hierarchy)
   - Metric calculations (aggregations, KPIs)
   - Balance data processing
   - Registration/onboarding data

2. **What are the inputs?**
   - Staging models (source tables)
   - Other intermediate models
   - Multiple sources combined

3. **Who consumes this?**
   - Other intermediate models (building block)
   - Mart models (business-ready output)
   - BI tools directly (dashboard)

4. **What's the grain?**
   - Event-level (transactions, registrations)
   - Account-level (customer enrichment)
   - Aggregated (daily, merchant-level)
   - Business entity (final mart)

---

### Step 3: Match to Architecture Pattern

| Model Purpose | Correct Location | Anti-Pattern (NEVER) | Architecture Doc |
|--------------|------------------|----------------------|------------------|
| **Transaction processing** (auth, posted, pairs) | `transactions/edw_based/` | ❌ `foundations/product/metrics/edw_based/` | `transactions_structure_guide.md` |
| **Account enrichment** (customer dims, product hierarchy) | `foundations/edw_account_base/` | ❌ `transactions/` | `foundations_structure_guide.md` |
| **Metric calculations** (aggregations, KPIs) | `metrics/[source]_based/` | ❌ `foundations/` or `transactions/` | `intermediate_structure_guide.md` |
| **Balance data** | `balances/` | ❌ `metrics/` or `transactions/` | `intermediate_structure_guide.md` |
| **Registration data** | `registrations/` or `metrics/gbos_based/` | ❌ `foundations/` | `folder-structure-and-naming.md` |
| **Operational marts** | `marts/operational/[use_case]/` | ❌ `marts/analytics/` | `marts_structure_guide.md` |
| **Executive marts** | `marts/executive/` | ❌ `marts/operational/` | `marts_structure_guide.md` |

---

### Step 4: Validate Against Anti-Patterns

**🚫 CHECK FOR THESE VIOLATIONS:**

#### Anti-Pattern 1: Transaction Models in Foundations

```
❌ WRONG: intermediate_NEW/foundations/product/metrics/edw_based/enriched_auth/
✅ RIGHT: intermediate_NEW/transactions/edw_based/enriched_auth/

Reason: Foundations = static enrichment (accounts, products)
        Transactions = event processing (auth, posted)
```

#### Anti-Pattern 2: Path Depth > 4 Levels

```
❌ WRONG: intermediate_NEW/foundations/product/metrics/edw_based/transaction_pairs/
          ^ Level 1    ^ Level 2  ^ L3    ^ L4     ^ L5       ^ L6

✅ RIGHT: intermediate_NEW/transactions/edw_based/transaction_pairs/
          ^ Level 1    ^ Level 2       ^ L3       ^ L4

Guideline: Max 4 levels for human discoverability
```

#### Anti-Pattern 3: Duplicate Folder Concepts

```
❌ WRONG: Both transactions/ AND foundations/product/metrics/edw_based/ containing transaction models

✅ RIGHT: ONE location: transactions/edw_based/ for all transaction processing

Reason: Single source of truth per content type
```

#### Anti-Pattern 4: Mixed Layer in Folder Name

```
❌ WRONG: foundations/product/metrics/
          (Confuses "foundation" vs "metrics")

✅ RIGHT: foundations/product/ OR metrics/product/
          (Clear single purpose)

Reason: Folder name should match single purpose
```

#### Anti-Pattern 5: Business Logic in Wrong Mart

```
❌ WRONG: Operational monitoring in marts/analytics/
✅ RIGHT: Operational monitoring in marts/operational/transaction_monitoring/

❌ WRONG: Deep-dive analysis in marts/operational/
✅ RIGHT: Deep-dive analysis in marts/analytics/customer_behavior/

Reason: Marts organized by consuming team/use case
```

---

### Step 5: Calculate Path Depth

**Formula:** Count directories from `models/` to model filename

```bash
# Example path
models/intermediate/intermediate_NEW/transactions/edw_based/enriched_auth/int_transactions__auth_all.sql

# Path depth calculation
models/              # (not counted - root)
  intermediate/      # Level 1
    intermediate_NEW/  # Level 2
      transactions/    # Level 3
        edw_based/     # Level 4
          enriched_auth/  # Too deep! (5 levels)

# This is acceptable if enforced by project structure
# but ideally should be 4 or fewer
```

**Guidelines:**
- ✅ **3-4 levels:** Optimal for discoverability
- ⚠️ **5 levels:** Acceptable if project structure enforces
- ❌ **6+ levels:** Too deep, restructure needed

---

### Step 6: Document Validation Result

**Include in recommendation/approval:**

```markdown
## ✅ Architecture Validation

**Model Purpose:** Transaction processing (auth/posted pairs)
**Recommended Path:** `intermediate_NEW/transactions/edw_based/transaction_pairs/`

**Validated Against:** `transactions_structure_guide.md`
**Compliance:** ✅ Matches documented structure

**Alternatives Considered:**
- ❌ `foundations/product/metrics/edw_based/` - Rejected (transactions don't belong in foundations)
- ❌ `metrics/edw_based/` - Rejected (not a metric calculation, it's event processing)

**Path Depth:** 4 levels (within guidelines)

**Anti-Pattern Check:**
- ✅ No transaction models in foundations
- ✅ Path depth acceptable
- ✅ No duplicate folder concepts
- ✅ Single clear purpose
```

---

## 🎓 Real-World Example: dbt-agent-13

### The Problem

**Models placed incorrectly:**
```
❌ intermediate_NEW/foundations/product/metrics/edw_based/enriched_auth/
❌ intermediate_NEW/foundations/product/metrics/edw_based/enriched_posted/
❌ intermediate_NEW/foundations/product/metrics/edw_based/transaction_pairs/
```

**Issues:**
1. Transaction processing in `foundations/` (wrong layer)
2. Path depth: 6 levels (too deep)
3. Duplicate concept: `transactions/` folder exists but unused
4. Non-intuitive: "Where are transactions?" → hard to find

### The Fix

**Moved to correct location:**
```
✅ intermediate_NEW/transactions/edw_based/enriched_auth/
✅ intermediate_NEW/transactions/edw_based/enriched_posted/
✅ intermediate_NEW/transactions/edw_based/transaction_pairs/
```

**Benefits:**
- Aligns with `transactions_structure_guide.md`
- Path depth reduced: 6 → 4 levels
- Human-intuitive: "transactions" in `transactions/` folder
- Consistent with marts: `operational/transaction_monitoring/`

### Root Cause

**Validation step was skipped:**
- Assumed generic guidance was sufficient
- Didn't load actual architecture docs
- Didn't check for anti-patterns
- No validation before model creation

### Prevention

**Use this checklist:**
1. Load architecture docs FIRST
2. Match model purpose to documented structure
3. Check for anti-patterns
4. Document validation result
5. Get user approval with explicit validation

---

## 📋 Quick Validation Template

Copy/paste for quick validation:

```markdown
## 🔍 Model Placement Validation

### Model Details
- **Name:** [model_name]
- **Purpose:** [transaction/enrichment/metric/mart]
- **Layer:** [staging/intermediate/marts]

### Architecture Validation
- [ ] Loaded architecture docs from dbt-enterprise
- [ ] Matched purpose to documented structure
- [ ] Checked anti-patterns (none found)
- [ ] Path depth ≤ 4 levels
- [ ] Folder name matches purpose

### Recommendation
**Path:** `[full_path]`
**Validated Against:** `[architecture_doc_name]`
**Compliance:** ✅ Matches documented structure

### Alternatives Rejected
- ❌ `[alternative_path_1]` - Reason: [why rejected]
- ❌ `[alternative_path_2]` - Reason: [why rejected]
```

---

## 🚀 Usage in Workflows

### For Claude Code (dbt-developer)

**BEFORE creating models:**
```
1. Load this checklist
2. Load architecture docs from dbt-enterprise
3. Run through Steps 1-6
4. Present validation to user for approval
5. Only create models after approval
```

**Include in model recommendation:**
- Show validation result
- Reference specific architecture doc
- List anti-patterns checked
- Get explicit user approval

### For Code Reviews

**Reviewer checks:**
```
1. Does model location match architecture docs?
2. Path depth ≤ 4 levels?
3. No anti-patterns present?
4. Consistent with similar models?
5. User approved placement explicitly?
```

**If violations found:**
- Reference this checklist
- Point to correct location
- Explain anti-pattern violated
- Request restructure

---

## 📚 Related Documentation

- **`shared/knowledge-base/folder-structure-and-naming.md`** - Folder conventions and patterns
- **`docs/analysis/dbt-agent-13_folder_structure_analysis.md`** - Case study of misplacement
- **`.claude/skills/model-placement-advisor/SKILL.md`** - Automated placement recommendations

---

**Last Updated:** 2025-11-11
**Lesson Learned From:** dbt-agent-13 (transaction model restructure)
**Key Principle:** "Validate against reality (architecture docs), not theory (generic guidance)"
