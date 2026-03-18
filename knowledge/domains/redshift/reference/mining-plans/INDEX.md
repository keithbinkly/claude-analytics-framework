# Redshift Performance Mining: Comprehensive Index

**Status:** v4.0 - Unified Syntactic + Physical Analysis
**Last Updated:** 2026-01-23

---

## Quick Navigation

| If you need... | Go to |
|----------------|-------|
| **Executive overview** | [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) |
| **What patterns to avoid** | [UNIFIED_ANTI_PATTERN_GUIDE.md](UNIFIED_ANTI_PATTERN_GUIDE.md) |
| **Real optimization examples** | [optimization_gallery/](optimization_gallery/) |
| **Specific offending queries** | [OFFENDER_REGISTRY.md](OFFENDER_REGISTRY.md) |
| **Quantified ROI** | [OPPORTUNITY_SIZING.md](OPPORTUNITY_SIZING.md) |
| **Self-service tuning** | [COPILOT_SELF_SERVICE.md](COPILOT_SELF_SERVICE.md) |
| **Full technical plan** | [INTEGRATED_PLAN_v3.md](INTEGRATED_PLAN_v3.md) |

---

## Two Complementary Mining Approaches

This package contains **two complementary detection systems** that together provide complete coverage:

### 1. Syntactic Pattern Detection (Query Text Analysis)

**Source:** Query log text parsing
**File:** `shared/reference/anti-pattern-impact.yml`
**Method:** Regex/AST analysis of SQL syntax

| Pattern | Impact | Detection Method |
|---------|--------|------------------|
| `NOT IN (subquery)` | **4.18x** slower | Text pattern match |
| `OR in JOIN` | **4.07x** slower | Text pattern match |
| Deep nesting (3+) | **3.06x** slower | Subquery depth count |
| `SELECT *` | **2.08x** slower | Text pattern match |

**When to use:** Code review, pre-commit checks, static analysis.

### 2. Physical Execution Detection (Runtime Metrics)

**Source:** `svl_query_metrics` (Redshift system tables)
**File:** [ANTI_PATTERN_DIRECTORY.md](ANTI_PATTERN_DIRECTORY.md)
**Method:** Runtime metric thresholds

| Pattern | Signature | Detection Method |
|---------|-----------|------------------|
| **Disk Spiller** | `temp_blocks > 0` | Runtime metric |
| **Skewed Worker** | `cpu_skew > 0.95` | Runtime metric |
| **Ghost Scanner** | `scan_rows > 10M, return < 100` | Runtime metric |
| **Cartesian Bomb** | `join_rows > inputs * 10` | Runtime metric |
| **Serial Leader** | High CPU on aggregation | Runtime metric |

**When to use:** Production monitoring, post-execution analysis, capacity planning.

### Combined Detection Strategy

```
┌─────────────────────────────────────────────────────────────────────┐
│                    UNIFIED DETECTION PIPELINE                        │
├──────────────────────────────────┬──────────────────────────────────┤
│       PRE-EXECUTION              │       POST-EXECUTION             │
│       (Syntactic)                │       (Physical)                 │
├──────────────────────────────────┼──────────────────────────────────┤
│ 1. Parse SQL text                │ 1. Query completes               │
│ 2. Match anti-pattern regex      │ 2. Check svl_query_metrics       │
│ 3. Flag before execution         │ 3. Flag runtime issues           │
│                                  │                                  │
│ Catches: NOT IN, OR JOIN,        │ Catches: Skew, Spilling,         │
│ SELECT *, Deep nesting           │ Full scans, Cartesians           │
└──────────────────────────────────┴──────────────────────────────────┘
```

---

## Key Findings (Quantified)

### From Query Log Mining (474K queries)

| Metric | Value |
|--------|-------|
| Queries analyzed | 474,144 |
| Unique syntactic patterns | 6 |
| Worst pattern | `NOT IN` (4.18x slowdown) |
| Files inventoried | 5,998 actionable |

### From Granular Execution Mining (186K queries, 3 days)

| Metric | Value |
|--------|-------|
| Queries analyzed | 186,448 |
| Total runtime | 339.9 hours |
| **Wasted runtime** | **334.8 hours (98.5%)** |
| Estimated saveable | **327.6 hours** |

### By User (Top Offenders)

| User | Anti-Pattern % | Runtime Impact |
|------|---------------:|---------------:|
| microstrategysvc | 51.0% | 98.9% problematic |
| svc_dbt_bi | 48.1% | 97.0% problematic |
| etluser | 37.5% | 99.1% problematic |

---

## Artifact Inventory

### Core Analysis Documents

| File | Purpose | Created |
|------|---------|---------|
| `EXECUTIVE_SUMMARY.md` | Business overview | Jan 20 |
| `INTEGRATED_PLAN_v3.md` | Full technical plan | Jan 20 |
| `GRANULAR_PERFORMANCE_MINING_PLAN.md` | Physical mining methodology | Jan 23 |

### Anti-Pattern Detection

| File | Purpose | Created |
|------|---------|---------|
| `ANTI_PATTERN_DIRECTORY.md` | Physical pattern signatures | Jan 23 |
| `UNIFIED_ANTI_PATTERN_GUIDE.md` | Combined syntactic + physical | Jan 23 |
| `shared/reference/anti-pattern-impact.yml` | Syntactic patterns + substitutions | Jan 20 |

### Actionable Outputs

| File | Purpose | Created |
|------|---------|---------|
| `OFFENDER_REGISTRY.md` | Top 50 bad queries (by query ID) | Jan 23 |
| `MINED_OPPORTUNITIES.md` | Prioritized optimization targets | Jan 23 |
| `OPPORTUNITY_SIZING.md` | ROI quantification | Jan 23 |
| `optimization_gallery/` | Before/after examples | Jan 23 |

### Case Studies

| File | Purpose | Created |
|------|---------|---------|
| `CASE_STUDY_GBOS_EAV_OPTIMIZATION.md` | EAV pivot pattern | Jan 23 |
| `gbos_fail_reason_analysis.md` | Timestamp tie-breaker bug | Jan 23 |

### Tools & Self-Service

| File | Purpose | Created |
|------|---------|---------|
| `COPILOT_SELF_SERVICE.md` | User guide for query tuning | Jan 23 |
| `tools/` | Helper scripts | Jan 20 |
| `schemas/` | JSON validation schemas | Jan 20 |

---

## Integration Points

### Knowledge Graph
- Extracted chunks: `outputs/phase3/kg_chunks.json` (66 chunks)
- Business concepts: `outputs/phase3/business_concepts.yaml` (16 concepts)

### dbt-enterprise
- Test candidates: `outputs/phase3/dbt_test_candidates.yaml` (10 candidates)
- Shadow assets: `outputs/phase3/shadow_inventory.json` (210 assets)

### Existing Reference Files
- Join registry: `shared/reference/baas-join-registry.yml` (139 joins)
- Vocabulary: `shared/reference/baas-controlled-vocabulary.yml` (103 terms)
- Anti-patterns: `shared/reference/anti-pattern-impact.yml` (6 syntactic patterns)

---

## Recommended Reading Order

**For analysts wanting to improve queries:**
1. `COPILOT_SELF_SERVICE.md` - Self-service guide
2. `UNIFIED_ANTI_PATTERN_GUIDE.md` - What to avoid
3. `optimization_gallery/` - Examples

**For engineers doing systematic optimization:**
1. `OPPORTUNITY_SIZING.md` - Where's the ROI?
2. `OFFENDER_REGISTRY.md` - Specific queries to fix
3. `MINED_OPPORTUNITIES.md` - Prioritized action items

**For understanding the methodology:**
1. `EXECUTIVE_SUMMARY.md` - Overview
2. `INTEGRATED_PLAN_v3.md` - Full plan
3. `GRANULAR_PERFORMANCE_MINING_PLAN.md` - Physical mining approach
