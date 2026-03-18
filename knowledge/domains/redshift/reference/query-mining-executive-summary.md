# Enterprise SQL Mining: Executive Summary

**Project:** Institutional Knowledge Extraction from Legacy SQL Corpus
**Date:** January 2026 (Updated: Jan 23, 2026)
**Owner:** Keith Binkley, Analytics & Insights
**Version:** 4.0 - Unified Syntactic + Physical Analysis

---

## TL;DR

| Mining Stream | Queries Analyzed | Key Finding |
|---------------|------------------|-------------|
| **Query Log (Syntactic)** | 474,000 | `NOT IN` is 4.18x slower than alternatives |
| **Granular Execution (Physical)** | 186,448 | **98.5% of runtime is problematic** |
| **SQL Corpus** | 5,998 files | 210 shadow assets need dbt sources |

**Bottom line:** We can recover **327+ hours of compute time** every 3 days by fixing distribution keys and sort key alignment.

---

## The Challenge

Institutional knowledge locked in:
- 42,000+ legacy SQL files across OneDrive and GitHub
- Analyst heads (walks out the door when they leave)
- Undocumented join patterns, naming conventions, business rules

**Impact:** AI agents hallucinate joins. New analysts take months to ramp. Same problems get re-solved.

---

## What We Did

### Two Complementary Mining Operations

| Mining Project | Source | Records | Output |
|----------------|--------|---------|--------|
| **Query Log Mining** | Redshift STL_QUERYTEXT | 474,000 queries | Behavioral specification |
| **SQL Corpus Mining** | Legacy files (OneDrive, GitHub) | 5,998 files | Institutional knowledge |

### Why Both?

- **Query logs** = what actually runs in production (proven patterns)
- **SQL corpus** = business context, ticket history, analyst intent

Together, they answer: *"What works?"* AND *"Why was it built this way?"*

---

## Results: Query Log Mining

**From 474,000 Redshift queries, extracted:**

| Artifact | Count | Value |
|----------|-------|-------|
| **Controlled Vocabulary** | 103 terms | Resolved naming conflicts before they cause bugs |
| **Join Library** | 89 verified paths | Performance metrics + orphan risk flags |
| **Anti-Pattern Impact** | 4 patterns | Quantified slowdowns with auto-substitution |

### Anti-Pattern Impact (Measured)

| Pattern | Avg Slowdown | Fix |
|---------|-------------|-----|
| NOT IN (subquery) | 4.18x | NOT EXISTS |
| OR in JOIN | 4.07x | UNION ALL |
| Deep nesting (3+) | 3.06x | Flat CTEs |
| SELECT * | 2.08x | Explicit columns |

**Paper:** `query-log-mining-institutional-knowledge.md`

---

## Results: SQL Corpus Mining

**From 5,998 actionable SQL files, extracted:**

| Output | Count | Value |
|--------|-------|-------|
| **Shadow Assets** | 210 | Tables with no dbt source definition (highest priority gaps) |
| **Business Concepts** | 16 | Pattern-to-meaning bridge (e.g., "owned product filter") |
| **New Joins** | 50 | Join patterns not in existing registry |
| **Test Candidates** | 10 | Business rules extractable as dbt tests (2 auto-ready) |
| **KG Chunks** | 66 | Knowledge Graph entries for AI agent context |

### Files Processed by Source

| Source | Files | Parse Success | Description |
|--------|-------|---------------|-------------|
| MSTR SQL | 435 | 100% | MicroStrategy report backing SQL |
| BIA Library | 352 | 100% | Curated analyst scripts |
| RPT Tickets | 239 | 100% | Ad-hoc analyses with business context |
| greendot/master | 1,307 | 100% | Production views and transforms |
| bau | 1,847 | 100% | Partner feeds and operations |
| ods | 1,818 | 100% | ODS layer objects |

### Top Shadow Assets (Need dbt Sources)

| Table | Usage Frequency | Priority |
|-------|----------------|----------|
| etl.ods_configuration | 2,153 | High |
| gbos.account | 1,431 | High |
| ods.account | 1,148 | High |
| etl.configuration | 647 | High |
| ods.payment_identifier | 487 | High |

---

## Results: Granular Execution Mining (NEW - Jan 23)

**From 186,448 queries over 3 days, discovered:**

| Metric | Value |
|--------|-------|
| Total Runtime | 339.9 hours |
| **Wasted Runtime** | **334.8 hours (98.5%)** |
| Estimated Recoverable | **327.6 hours** |

### Physical Anti-Patterns Detected

| Anti-Pattern | Prevalence | Impact |
|--------------|------------|--------|
| **Skewed Worker** | 25.8% of queries | CPU saturation (one core at 100%) |
| **Heavy Scanner** | 10.7% of queries | I/O saturation (full table reads) |
| **Disk Spiller** | 2.8% of queries | Memory overflow to disk |

### Top Offenders by User

| User | Anti-Pattern % | Runtime Impact |
|------|---------------:|---------------:|
| **microstrategysvc** | 51.0% | 98.9% of runtime is problematic |
| **svc_dbt_bi** | 48.1% | 97.0% of runtime is problematic |
| **etluser** | 37.5% | 99.1% of runtime is problematic |
| **jupyter (Ad-Hoc)** | 54.9% | 99.3% of runtime is problematic |

### Key Optimization Targets

1. **MicroStrategy Temp Tables** - The "Volt" pattern scans full tables without SORTKEY alignment
2. **dbt Intermediate Models** - `int_transactions__posted_all` shows 64x CPU skew (distribution key issue)
3. **Ad-Hoc Cartesians** - Users joining large tables without adequate filtering

**Details:** See `MINED_OPPORTUNITIES.md`, `OFFENDER_REGISTRY.md`

---

## How It Works

### Multi-Agent Architecture

```
Orchestrator (Claude Opus 4.5)
    ├── Discovery Agent (Gemini 3 Pro) → File inventory + temporal classification
    ├── Extraction Agent (GPT 5.2 Codex) → AST parsing + pattern extraction
    ├── Interpretation Agent (Claude Opus) → Logic specs + business concepts
    └── Consolidation Agent (Claude Opus) → KG integration + conflict resolution
```

### Quality Gates

Each extracted pattern validated against:
- Parse quality (full AST > partial > regex)
- Frequency (high-frequency = consensus)
- Temporal status (active > stale > deprecated)
- Cross-source presence (appears in multiple folders = canonical)

---

## Value Delivered

### For AI Agents

- **Before:** Hallucinate joins, use wrong column names, generate slow queries
- **After:** Query Knowledge Graph for verified patterns, auto-apply substitutions

### For Analysts

- **Before:** 3-6 months to learn undocumented patterns
- **After:** Search KG for "how do we calculate active accounts?"

### For Data Engineering

- **Before:** Re-solve same problems, duplicate logic across pipelines
- **After:** DRY infrastructure with canonical patterns + tests

---

## Outputs Location

```
dbt-agent/
├── docs/research/mining/
│   ├── INDEX.md                           # Start here - navigation guide
│   ├── EXECUTIVE_SUMMARY.md               # ← You are here
│   ├── UNIFIED_ANTI_PATTERN_GUIDE.md      # Combined syntactic + physical patterns
│   │
│   ├── # Granular Execution Mining (NEW)
│   ├── GRANULAR_PERFORMANCE_MINING_PLAN.md
│   ├── ANTI_PATTERN_DIRECTORY.md          # Physical pattern signatures
│   ├── MINED_OPPORTUNITIES.md             # Prioritized optimization targets
│   ├── OFFENDER_REGISTRY.md               # Top 50 bad queries (by ID)
│   ├── OPPORTUNITY_SIZING.md              # ROI quantification
│   ├── COPILOT_SELF_SERVICE.md            # User guide
│   │
│   ├── # Case Studies
│   ├── CASE_STUDY_GBOS_EAV_OPTIMIZATION.md
│   ├── gbos_fail_reason_analysis.md       # Timestamp bug finding
│   │
│   ├── # Optimization Examples
│   ├── optimization_gallery/
│   │   ├── 01_mega_case_distinct/         # Before/after for disk spiller
│   │   ├── 02_skewed_join_card_apps/      # Before/after for skew
│   │   └── 03_heavy_scanner_mstr/         # Before/after for MSTR pattern
│   │
│   ├── # Original Corpus Mining
│   ├── outputs/
│   │   ├── phase1/          # Initial extraction
│   │   ├── phase2/          # Expanded corpus
│   │   └── phase3/          # Consolidated artifacts (KG chunks, tests)
│   │
│   └── INTEGRATED_PLAN_v3.md              # Full technical plan
│
├── shared/reference/
│   ├── baas-join-registry.yml             # 139 verified joins
│   ├── baas-controlled-vocabulary.yml     # 103 canonical terms
│   └── anti-pattern-impact.yml            # Syntactic patterns + substitutions
│
└── docs/research/
    └── query-log-mining-institutional-knowledge.md  # Methodology paper
```

---

## Next Steps

### Immediate (High ROI)
1. **Fix distribution keys** on `int_transactions__posted_all` (64x skew)
2. **Align MSTR queries** with SORTKEY (address "Volt" pattern)
3. **Roll out self-service guide** to ad-hoc users

### Short-term
4. **Integrate KG chunks** into qmd index for AI agent retrieval
5. **Create dbt sources** for top 20 shadow assets
6. **Codify 2 auto-ready tests** from business rule extraction
7. **Human review** of 16 business concept candidates

---

## Methodology Papers

- **Query Log Mining:** `query-log-mining-institutional-knowledge.md`
- **SQL Corpus Mining:** `.dots/dbt-agent-enterprise-sql-mining.md`
- **Integrated Plan:** `docs/research/mining/INTEGRATED_PLAN_v3.md`

---

**Contact:** Keith Binkley | Analytics & Insights
