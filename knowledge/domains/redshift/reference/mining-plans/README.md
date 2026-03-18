# Enterprise SQL Corpus Mining Package

**A multi-model AI workflow for extracting institutional knowledge from legacy SQL repositories.**

**Status:** v4.0 - Unified Syntactic + Physical Analysis (CONSOLIDATED)

> **New in v4.0:** Granular execution mining adds physical anti-pattern detection (Skewed Worker, Disk Spiller, Ghost Scanner) alongside existing syntactic patterns. See [INDEX.md](INDEX.md) for navigation.

---

## Quick Start

```bash
# 1. Start with the index (navigation guide)
cat docs/research/mining/INDEX.md

# 2. For analysts wanting to improve queries:
cat docs/research/mining/UNIFIED_ANTI_PATTERN_GUIDE.md
cat docs/research/mining/COPILOT_SELF_SERVICE.md

# 3. For engineers doing systematic optimization:
cat docs/research/mining/OPPORTUNITY_SIZING.md      # Where's the ROI?
cat docs/research/mining/OFFENDER_REGISTRY.md       # Specific queries to fix

# 4. For AI tool integration:
#    - Claude Code / Cursor: Use prompts/ORCHESTRATOR.md
#    - GitHub Copilot: Use prompts/COPILOT_INSTRUCTIONS.md
#    - ChatGPT / Gemini: Use prompts/STANDALONE_REVIEW.md
```

---

## What This Package Does

Mines SQL from **three complementary sources** to build **semantic infrastructure**:

### Source 1: Query Log Mining (Syntactic Patterns)
- **Input:** 474,000 queries from `stl_querytext`
- **Output:** 6 anti-patterns with measured slowdowns (up to 4.18x)
- **Use:** Code review, CI/CD checks, static analysis

### Source 2: Granular Execution Mining (Physical Patterns) - NEW
- **Input:** 186,448 queries from `svl_query_metrics`
- **Output:** 5 physical patterns (Skew, Spilling, Ghost Scans)
- **Use:** Production monitoring, capacity planning
- **Key finding:** 98.5% of runtime is problematic, 327+ hrs recoverable

### Source 3: SQL Corpus Mining (Business Context)
- **Input:** 5,998 actionable files from OneDrive/GitHub
- **Output:** Join patterns, business concepts, shadow assets
- **Use:** Knowledge graph, analyst onboarding

### Combined Artifacts
- **Join patterns** → Which tables connect, how, and how often (+ dbt lineage context)
- **Business concepts** → Pattern-to-meaning bridge (what filters MEAN, not just syntax)
- **Column aliases** → Canonical naming conventions (linked to controlled vocabulary)
- **Logic specifications** → Structured documentation of business logic
- **dbt test candidates** → Business rules that should become automated tests
- **Physical signatures** → Runtime detection rules for bad queries

### Target Corpus (Validated Scope)

**89% reduction from raw corpus (42K → 4.6K actionable files)**

| Source | Files | Priority | Content |
|--------|-------|----------|---------|
| MSTR SQL | 435 | P0 | MicroStrategy report queries |
| BIA Library/Current | 352 | P0 | Curated reusable scripts |
| BIA RPT_tickets | 239 | P0 | Ad-hoc requests + business context (GOLD - has requestor metadata) |
| greendot/master | 1,742 | P1 | Production views, data transforms |
| bau/ | 1,671 | P1 | Partner data feeds, operational logic |
| **Excluded** | 37,600 | — | `greendot/releases` (2015-2017 snapshots), archives |

---

## Package Structure

```
docs/research/mining/
├── INDEX.md                     # START HERE - Navigation guide
├── README.md                    # Overview (you are here)
├── EXECUTIVE_SUMMARY.md         # Business overview with key findings
│
├── # Unified Anti-Pattern System
├── UNIFIED_ANTI_PATTERN_GUIDE.md  # Combined syntactic + physical patterns
├── ANTI_PATTERN_DIRECTORY.md      # Physical pattern signatures (runtime)
│
├── # Granular Execution Mining (NEW Jan 23)
├── GRANULAR_PERFORMANCE_MINING_PLAN.md  # Methodology
├── MINED_OPPORTUNITIES.md               # Prioritized optimization targets
├── OFFENDER_REGISTRY.md                 # Top 50 bad queries (by ID)
├── OPPORTUNITY_SIZING.md                # ROI quantification (327 hrs recoverable)
├── COPILOT_SELF_SERVICE.md              # User self-service guide
│
├── # Case Studies
├── CASE_STUDY_GBOS_EAV_OPTIMIZATION.md  # EAV pivot pattern
├── gbos_fail_reason_analysis.md         # Timestamp tie-breaker bug
│
├── # Optimization Gallery
├── optimization_gallery/
│   ├── README.md
│   ├── 01_mega_case_distinct/   # Disk Spiller before/after
│   ├── 02_skewed_join_card_apps/ # Skewed Worker before/after
│   └── 03_heavy_scanner_mstr/    # Heavy Scanner before/after
│
├── # Original Corpus Mining Infrastructure
├── INTEGRATED_PLAN_v3.md        # Full technical plan
├── PLAN_FOR_REVIEW.md           # For adversarial review
├── prompts/                     # AI-ready instruction sets
├── outputs/                     # Generated artifacts (phase1-3)
├── tools/                       # Helper scripts
└── schemas/                     # JSON schemas for validation
```

---

## Multi-Model Strategy

Different AI models excel at different tasks. Use this guide:

| Task | Best Model | Why | Prompt File |
|------|-----------|-----|-------------|
| **Bulk indexing** | Gemini 3 Pro | 1M token context, cheap | `DISCOVERY_AGENT.md` |
| **Pattern extraction** | GPT-5.2-Codex | Best code accuracy, low hallucination | `EXTRACTION_AGENT.md` |
| **Logic interpretation** | Claude Opus 4.5 | Nuanced reasoning | `INTERPRETATION_AGENT.md` |
| **Adversarial review** | All models | Cross-validation | `STANDALONE_REVIEW.md` |
| **Orchestration** | Claude Opus 4.5 | Multi-step coordination | `ORCHESTRATOR.md` |

---

## For GitHub Copilot Users

1. Copy `prompts/COPILOT_INSTRUCTIONS.md` to your `.github/copilot-instructions.md`
2. Or paste directly into Copilot Chat as context
3. Point Copilot at the target directories (see PLAN_FOR_REVIEW.md for paths)

---

## For Claude Code / Cursor Users

1. Open this directory in your IDE
2. Start a session with: "Read prompts/ORCHESTRATOR.md and begin Phase 1"
3. The orchestrator will coordinate sub-agents as needed

---

## For ChatGPT / Gemini Users

1. Copy contents of `prompts/STANDALONE_REVIEW.md`
2. Paste into a new chat session
3. Attach or paste SQL files you want analyzed
4. Save outputs to `outputs/` directory

---

## Output Formats

### Inventory (JSON)
```json
{
  "source": "BI_Library",
  "generated_at": "2026-01-14T20:00:00Z",
  "files": [...],
  "summary": {
    "total_files": 364,
    "sql_files": 352,
    "top_tables": [...]
  }
}
```

### Patterns (YAML)
```yaml
joins:
  - left_table: fct_posted_transaction
    right_table: dim_account
    join_key: account_key
    frequency: 245
    sources: [file1.sql, file2.sql]

aliases:
  - canonical: transaction_amount
    variants: [txn_amt, amount, trans_amt]
    frequency: 500
```

### Logic Spec (Markdown)
```markdown
# Logic Spec: Monthly Active Accounts

## Business Purpose
Counts accounts with at least one transaction in the trailing 30 days.

## Key Logic
1. Filter: calendar_date >= DATEADD('day', -30, CURRENT_DATE)
2. Aggregation: COUNT(DISTINCT account_uid)
...
```

---

## Contributing

1. Run your mining session
2. Save outputs to appropriate `outputs/` subfolder
3. If you discover new patterns, update `examples/`
4. Submit PR with your findings

---

## Key Findings Summary

| Mining Stream | Key Finding | Action |
|---------------|-------------|--------|
| **Syntactic** | `NOT IN` is 4.18x slower | Use `NOT EXISTS` |
| **Physical** | 98.5% of runtime is problematic | Fix DISTKEY/SORTKEY |
| **Corpus** | 210 shadow assets | Create dbt sources |

---

## Related Resources

**In this package:**
- [INDEX.md](INDEX.md) - Navigation guide
- [UNIFIED_ANTI_PATTERN_GUIDE.md](UNIFIED_ANTI_PATTERN_GUIDE.md) - Complete pattern reference
- [optimization_gallery/](optimization_gallery/) - Before/after examples

**Elsewhere in repo:**
- `../../query-log-mining-institutional-knowledge.md` - Methodology paper
- `../../../shared/reference/anti-pattern-impact.yml` - Syntactic patterns + substitutions
- `../../../shared/reference/baas-join-registry.yml` - Verified join documentation
- `../../../tools/kg/` - Knowledge Graph infrastructure

---

## Questions?

Open an issue or ping the Analytics Engineering team.
