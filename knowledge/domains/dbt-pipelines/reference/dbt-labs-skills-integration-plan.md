---
title: "Unified Skills Integration: dbt-labs Official + Ours"
status: open
priority: 0
tags: [skills, architecture, integration, dbt-labs]
created: 2026-02-07
---

# Unified Skills Integration Plan

## Goal

Merge dbt-labs' 9 official skills (37 files) into our 30+ skill set, producing **one unified superset** that combines their universal best practices with our enterprise-grade operational depth. No two parallel systems.

## Design Principles

1. **Framework from them, execution from us.** Their methodology becomes the "what to do." Our MCP-enabled patterns become the "how to do it."
2. **Behavioral guardrails are additive.** Their "Rationalizations to Resist" and "Iron Rules" are defensive patterns we lack. Pull them in wholesale.
3. **Preserve our unique innovations.** Decision traces, anti-pattern registry, join library, controlled vocabulary, forensic sample trace, grain integrity mandate, volume tracing — these don't exist in their skills.
4. **Eliminate the `dbt-official-*` prefix.** After integration, there's no "theirs" and "ours." One skill set.
5. **Execution order = highest daily impact first.** Discovery and QA run on every pipeline. Improve those first.

---

## The Integration Map

### How Their 9 Skills Map to Our Skills

```
dbt-labs Official                          Our Skills (target)
─────────────────────                      ──────────────────
using-dbt-for-analytics-engineering        SPLIT ACROSS 6 SKILLS:
  ├─ references/discovering-data.md    →   dbt-data-discovery (ABSORB)
  ├─ references/writing-data-tests.md  →   dbt-qa (ABSORB)
  ├─ references/debugging-dbt-errors.md →  dbt-qa + troubleshooting KB (ABSORB)
  ├─ references/planning-dbt-models.md →   dbt-migration Step 3A (ABSORB)
  ├─ references/evaluating-impact.md   →   dbt-lineage + dbt-migration (ABSORB)
  ├─ references/writing-documentation  →   dbt-standards (ABSORB)
  └─ references/managing-packages.md   →   dbt-fundamentals (ABSORB)

troubleshooting-dbt-job-errors         →   dbt-qa + dbt-decision-trace (ABSORB)
adding-dbt-unit-test                   →   dbt-sql-unit-testing (MERGE - cross-reference)
running-dbt-commands                   →   dbt-fundamentals (ABSORB)
building-dbt-semantic-layer            →   dbt-semantic-layer-developer (MERGE - update spec)
fetching-dbt-docs                      →   KEEP STANDALONE (unique utility)
answering-nl-questions-with-dbt        →   KEEP STANDALONE (different use case)
configuring-dbt-mcp-server             →   KEEP STANDALONE (setup/onboarding)
migrating-dbt-core-to-fusion           →   KEEP STANDALONE (one-time migration)
```

### Decision Rationale for Each Category

**ABSORB (7 reference files + 2 skills → merged into our existing skills)**
- These have 30-70% overlap with our skills
- Their unique content is methodology/frameworks that enhance our execution patterns
- Keeping them separate creates confusion about which skill to use

**MERGE (2 skills → combined with ours into upgraded skills)**
- `building-dbt-semantic-layer` has the new 1.11+ spec we need; we have operational wisdom they lack
- `adding-dbt-unit-test` covers dbt-native tests; we cover pytest+DuckDB. Both valid, cross-reference

**KEEP STANDALONE (4 skills → remain as-is, just rename)**
- `fetching-dbt-docs` — pure utility, no overlap. Rename: `dbt-docs-lookup`
- `answering-nl-questions-with-dbt` — analyst use case, not developer. Rename: `dbt-nl-queries`
- `configuring-dbt-mcp-server` — setup/onboarding. Rename: `dbt-mcp-setup`
- `migrating-dbt-core-to-fusion` — one-time migration. Rename: `dbt-fusion-migration`

---

## Execution Plan: 5 Phases

### Phase 1: Foundation (Discovery + QA)
**Why first:** Every pipeline starts with discovery, every model gets QA'd. These two skills have the highest daily usage. Improving them improves everything downstream.

**Estimated effort:** 1-2 hours
**Skills touched:** `dbt-data-discovery`, `dbt-qa`

#### 1A. Enhance `dbt-data-discovery` with Iron Rule Framework

**Source:** `dbt-official-using-dbt-for-analytics-engineering/references/discovering-data.md`

**What to pull in:**
- **"The Iron Rule"** — "Complete all 6 steps for every table you will build models on." Add as opening section.
- **"Rationalizations That Mean STOP"** — 7 excuse→reality pairs. Add as defensive table immediately after the Iron Rule.
  - "I don't have time for full discovery" → "You don't have time for wrong models"
  - "47 tables is too many" → "Prioritize which you'll use, do FULL discovery on those"
  - "I'll do proper discovery later" → "You won't. Document now or create technical debt"
  - "Standard patterns, I know this data" → "You know the pattern. This instance might vary."
- **"Red Flags" list** — 7 behavioral indicators the agent is about to skip discovery. Add after Rationalizations.
- **Large Scope Strategy** — "When facing 20+ tables" guidance. Integrate into our existing workflow section.

**What to keep (ours):**
- MCP tools integration (they have none)
- Volume tracing + suppression detection (they have none)
- Prevention tests (dbt-agent-36/37/38)
- Pre-discovery reference loading (EDW dictionary, join registry)

**Structure of merged skill:**
```
## The Iron Rule (opening — from dbt-labs)
## Rationalizations That Mean STOP (from dbt-labs)
## Red Flags (from dbt-labs)
## MCP-Powered Discovery Workflow (ours — enhanced)
  └── Large Scope Strategy (from dbt-labs, with our MCP execution)
## Volume Trace Patterns (ours)
## Suppression Detection (ours)
## Prevention Tests (ours)
## Discovery Report Template (merged — their checklist + our MCP outputs)
```

**Why this order:** Their framework sets the mindset. Our tools execute it. Agent reads the "why" first, then the "how."

#### 1B. Enhance `dbt-qa` with Test Priority + Error Classification

**Sources:**
- `references/writing-data-tests.md` (test priority framework)
- `references/debugging-dbt-errors.md` (error classification)
- `troubleshooting-dbt-job-errors/SKILL.md` (never-modify-test rule)

**What to pull in:**
- **4-tier test priority framework** — Tier 1 (PK unique/not_null) through Tier 4 (avoid). Insert as "Pre-QA: dbt Test Strategy" section.
- **Cost-conscious testing** — `where` clauses for large tables, avoid testing pass-through columns. Add to test strategy section.
- **3-type error classification** — YAML/parsing, SQL/compilation, data/test failures. Add as opening taxonomy.
- **"Never modify a test to make it pass"** — Iron rule from job troubleshooting. Add as prominent callout.

**What to keep (ours):**
- Templates 1-4 (granular variance analysis)
- Variance thresholds (<0.1% critical, <0.5% derived, <1.0% edge)
- Decision trace integration
- 5 common variance root causes
- Quality-adjusted pass classification

**Structure of merged skill:**
```
## Error Classification Taxonomy (from dbt-labs — opening)
## The Iron Rule: Never Modify a Test to Pass (from dbt-labs)
## Pre-QA: dbt Test Strategy (from dbt-labs)
  ├── Tier 1-4 Priority Framework
  └── Cost-Conscious Testing Patterns
## QA Layers (ours)
  ├── Layer 0: Compilation
  ├── Layer 1: Unit Tests
  └── Layer 2: Reconciliation (Templates 1-4)
## Variance Root Causes (ours)
## Decision Trace Integration (ours)
## Quality-Adjusted Pass Classification (ours)
```

**Why this order:** Their classification and test strategy are "Layer -1" — structural foundations before our operational QA workflow kicks in.

---

### Phase 2: Planning & Learning (Migration + Decision Trace)
**Why second:** Every new model goes through migration workflow. Better planning = fewer iterations = faster pipelines.

**Estimated effort:** 1 hour
**Skills touched:** `dbt-migration`, `dbt-decision-trace`

#### 2A. Enhance `dbt-migration` with Mock-First Planning + Impact Analysis

**Sources:**
- `references/planning-dbt-models.md` (mock-first methodology)
- `references/evaluating-impact-of-a-dbt-model-change.md` (impact classification)

**What to pull in:**
- **Mock-first methodology** — "Design output table BEFORE writing SQL." 7-step backward process. Insert as new Step 3A in our 6-step workflow.
  - Mock final output → Mock SQL → Identify gaps → Mock upstream → Update SQL → Edge cases → Implement
- **TDD with unit tests** — Create failing unit tests as acceptance criteria BEFORE implementation. Add to Step 3A.
- **Impact classification** — Low (1-5 downstream), Medium (6-15), High (16+). Insert as Step 5.0 (Pre-Execution Impact Check).
- **Column-level impact grep** — Search for column references in downstream SQL. Add to Step 5.0.

**What to keep (ours):**
- 6-step pipeline workflow (Steps 1-6)
- 75-90% canonical reuse target
- Mandatory 3-part codebase scan
- Progressive resource loading (10K→32K tokens)
- Preflight cost estimation integration

**Where it fits:**
```
STEP 1: Requirements (ours)
STEP 2: Canonical Mapping (ours)
STEP 3: Design Transformations (ours)
  └── NEW: STEP 3A: Mock-First Design (from dbt-labs)
         ├── Mock final output table
         ├── Mock SQL query
         ├── Create failing unit tests (TDD)
         └── Iterate until gaps resolved
STEP 4: Pre-flight (ours)
  └── NEW: STEP 4.5: Impact Analysis (from dbt-labs)
         ├── Count downstream models
         ├── Classify: Low/Medium/High
         └── Column-level grep
STEP 5: Execute & Validate (ours)
STEP 6: Documentation (ours)
```

#### 2B. Enhance `dbt-decision-trace` with Investigation Framework

**Source:** `troubleshooting-dbt-job-errors/SKILL.md`

**What to pull in:**
- **"Never modify a test to pass" iron rule** — Cross-reference from QA skill, add as principle.
- **Investigation documentation template** — When root cause is NOT found, create structured findings doc. This fills a gap — we currently only log resolved traces.
- **Rationalizations to Resist** — 5 troubleshooting rationalizations. Add as defensive table.
  - "Just make the test pass" → "Test is telling you something is wrong. Investigate first."
  - "There's a board meeting in 2 hours" → "Rushing creates bigger problems."
  - "It's probably just a flaky test" → "Flaky means there's an issue. Find it."

**What to keep (ours):**
- Everything. This is our unique innovation.
- Trace schema (problem → triage_path → resolution)
- Rule synthesis (traces → generalized rules)
- Two-tier lookup (rules first, traces fallback)
- Automatic synthesis every 5 traces

**Enhancement:** Add "unresolved trace" template for cases that couldn't be solved (currently a gap).

---

### Phase 3: Semantic Layer & Testing (Specialized Domains)
**Why third:** Spec updates are important but lower daily usage than discovery/QA/migration.

**Estimated effort:** 45 min
**Skills touched:** `dbt-semantic-layer-developer`, `dbt-sql-unit-testing`

#### 3A. Update `dbt-semantic-layer-developer` with 1.11+ Spec

**Source:** `dbt-official-building-dbt-semantic-layer/SKILL.md`

**What to pull in:**
- **New 1.11+ semantic model spec** — `semantic_model: enabled: true` under models, column-level `entity:` and `dimension:` properties, `agg_time_dimension:` at model level.
- **Measures → column-level metrics migration** — How to move from old spec to new.
- **`dbt-autofix deprecations --semantic-layer`** — Automated migration command.

**What to keep (ours):**
- Naming conventions (domain prefixes for uniqueness)
- MF002 linter rule awareness
- DEV vs PROD environment disclosure
- High-cardinality timeout workarounds
- Redshift compatibility warnings
- Dual dbt install setup (Core 1.10 for `mf`, Fusion for `dbt`)

**Structure:** Add "1.11+ Spec" section BEFORE our operational sections. Their spec is the canonical format; our sections are "here's what you'll actually run into."

#### 3B. Cross-Reference `dbt-sql-unit-testing` with Native Tests

**Source:** `dbt-official-adding-dbt-unit-test/SKILL.md`

**What to pull in:**
- **Decision matrix** — When to use sql-testing-library (Python) vs dbt native unit tests (YAML).
- **Brief overview** of dbt native test format (Model-Given-Expect pattern).
- **Cross-reference** to the full `dbt-official-adding-dbt-unit-test` skill for YAML details.

**What to keep (ours):**
- sql-testing-library patterns (pytest + DuckDB)
- VPN-independent iteration
- Integration with QA workflow (Layer 1)
- Mock data patterns

**No merge needed** — these are genuinely different tools. Just add a "Which approach?" decision section at the top.

---

### Phase 4: Standards & Fundamentals (Polish)
**Why fourth:** Lower-frequency skills. Still worth enhancing but lower daily impact.

**Estimated effort:** 30 min
**Skills touched:** `dbt-standards`, `dbt-fundamentals`

#### 4A. Enhance `dbt-standards` with Documentation Patterns

**Source:** `references/writing-documentation.md`

**What to pull in:**
- **"Why not what" principle** — Document WHY a column exists and its business meaning, not just "this is the customer ID."
- **"Inspect data before writing docs"** — Don't document from column names alone.

**What to keep (ours):** All existing content (folder structure, naming conventions, canonical reuse, CTE patterns).

#### 4B. Enhance `dbt-fundamentals` with CLI Patterns

**Sources:** `running-dbt-commands/SKILL.md`, `references/managing-packages.md`

**What to pull in:**
- **MCP-first preference** — Prefer MCP tools over CLI when available.
- **`--warn-error-options`** — For catching selector typos in automation.
- **Fusion vs Core detection logic** — Check which CLI flavor is active.
- **`dbt list --output json --output-keys`** — Programmatic output parsing.
- **Hub.getdbt.com API** — Programmatic package discovery.

**What to keep (ours):** Medallion architecture, modeling templates, materialization guidance.

---

### Phase 5: Cleanup & Unification
**Why last:** Depends on all content being merged first.

**Estimated effort:** 45 min

#### 5A. Rename 4 Standalone Skills (remove `dbt-official-` prefix)

| Current Name | New Name | Rationale |
|-------------|----------|-----------|
| `dbt-official-fetching-dbt-docs` | `dbt-docs-lookup` | Utility, short name |
| `dbt-official-answering-natural-language-questions-with-dbt` | `dbt-nl-queries` | Analyst use case |
| `dbt-official-configuring-dbt-mcp-server` | `dbt-mcp-setup` | Setup/onboarding |
| `dbt-official-migrating-dbt-core-to-fusion` | `dbt-fusion-migration` | One-time migration |

For each: rename directory, update SKILL.md frontmatter `name:` field, update CLAUDE.md activation table.

#### 5B. Archive 5 Absorbed Skills

After content is merged, archive these directories (content now lives in our skills):

| Archive | Content Now In |
|---------|---------------|
| `dbt-official-using-dbt-for-analytics-engineering/` | Split across 6 skills |
| `dbt-official-troubleshooting-dbt-job-errors/` | `dbt-qa` + `dbt-decision-trace` |
| `dbt-official-adding-dbt-unit-test/` | `dbt-sql-unit-testing` (cross-ref) |
| `dbt-official-running-dbt-commands/` | `dbt-fundamentals` |
| `dbt-official-building-dbt-semantic-layer/` | `dbt-semantic-layer-developer` |

**Exception:** Keep `dbt-official-adding-dbt-unit-test` as a reference resource (14 warehouse-specific reference files) even after cross-referencing. Rename to `dbt-native-unit-test-reference/`.

#### 5C. Update Configuration Files

1. **CLAUDE.md Skill Activation Table** — Remove all `dbt-official-*` entries. Add renamed standalone skills.
2. **CLAUDE.md dbt Skills Index** — Add standalone skills to compact index.
3. **SKILLS_REGISTRY.md** — Update full registry to reflect merged state.
4. **`.claude/skills/` directory** — Verify no orphaned directories.

#### 5D. Attribution

Add to each merged skill's frontmatter:
```yaml
attribution:
  - author: dbt-labs
    source: https://github.com/dbt-labs/dbt-agent-skills
    content: [list of specific sections pulled in]
```

---

## What's New After Integration (Unique Patterns Adopted)

### Behavioral Guardrails (from dbt-labs)
These patterns don't exist in our current skills:

| Pattern | Where It Goes | Why It Matters |
|---------|---------------|----------------|
| **"Rationalizations to Resist"** | `dbt-data-discovery`, `dbt-decision-trace` | Defends against the agent's own tendency to rationalize shortcuts |
| **"Red Flags — STOP and Reconsider"** | `dbt-data-discovery`, `dbt-qa` | Behavioral pattern recognition for the agent |
| **"The Iron Rule"** | `dbt-data-discovery`, `dbt-qa` | Forcing function that prevents half-measures |
| **"Common Mistakes" tables** | Throughout | Structured as Mistake → Why Wrong → Fix |

### Methodological Enhancements
| Enhancement | Where It Goes | What It Adds |
|-------------|---------------|--------------|
| **Mock-first planning** | `dbt-migration` Step 3A | Design output before writing SQL |
| **4-tier test priority** | `dbt-qa` Pre-QA section | Systematic test selection |
| **Impact classification** | `dbt-migration` Step 4.5 | Low/Medium/High downstream assessment |
| **Investigation doc template** | `dbt-decision-trace` | Structure for unresolved cases |
| **1.11+ semantic layer spec** | `dbt-semantic-layer-developer` | Future-proof format |

---

## Final State: Unified Skill Set

After all 5 phases, the skill set looks like this:

### Core Development Skills (8)
| Skill | Key Enhancement from Integration |
|-------|----------------------------------|
| `dbt-fundamentals` | + MCP-first CLI, warn-error-options, Fusion detection |
| `dbt-standards` | + "Why not what" documentation principle |
| `dbt-data-discovery` | + Iron Rule, Rationalizations to Resist, Red Flags |
| `dbt-migration` | + Mock-first planning (3A), impact classification (4.5) |
| `dbt-qa` | + 4-tier test priority, error classification, never-modify-test rule |
| `dbt-decision-trace` | + Investigation template, troubleshooting rationalizations |
| `dbt-semantic-layer-developer` | + 1.11+ spec, column-level properties |
| `dbt-sql-unit-testing` | + Cross-reference to dbt native tests, decision matrix |

### Utility Skills (4, renamed from official)
| Skill | Purpose |
|-------|---------|
| `dbt-docs-lookup` | Fetch dbt documentation mid-session |
| `dbt-nl-queries` | Answer business questions via semantic layer |
| `dbt-mcp-setup` | MCP server configuration/onboarding |
| `dbt-fusion-migration` | One-time Core → Fusion migration |

### Reference Resources (1, archived from official)
| Resource | Purpose |
|----------|---------|
| `dbt-native-unit-test-reference/` | 14 warehouse-specific unit test guides |

### Unchanged Skills (18+)
All other skills remain as-is: `dbt-lineage`, `dbt-redshift-optimization`, `dbt-preflight`, `dbt-orchestrator`, `dbt-business-context`, `dbt-tech-spec-writer`, `dbt-jinja-sql-optimizer`, `dbt-artifacts`, `sql-hidden-gems`, etc.

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Merged skills become too long (token bloat) | Use reference file pattern: core SKILL.md stays concise, detailed content in `references/` |
| Attribution unclear | Add `attribution:` frontmatter to every merged skill |
| dbt-labs updates their skills | Pin to commit SHA in attribution; periodic sync check (quarterly) |
| Breaking existing workflows | Phase 5 cleanup happens LAST, only after all content verified |
| Losing content during merge | Archive, don't delete. `dbt-official-*` dirs moved to `docs/archive/skills/` |

---

## Success Criteria

- [ ] Zero `dbt-official-*` prefixed skills in active use (all absorbed/renamed/archived)
- [ ] All "Rationalizations to Resist" tables present in relevant skills
- [ ] All "Iron Rules" documented in relevant skills
- [ ] Mock-first planning integrated into `dbt-migration` workflow
- [ ] 1.11+ semantic layer spec in `dbt-semantic-layer-developer`
- [ ] Test priority framework in `dbt-qa`
- [ ] CLAUDE.md activation table reflects unified set
- [ ] SKILLS_REGISTRY.md updated
- [ ] Attribution in every merged skill

---

## Quick Reference: What Content Goes Where

| dbt-labs Source File | Target Skill | Specific Sections to Pull |
|---------------------|-------------|---------------------------|
| `discovering-data.md` | `dbt-data-discovery` | Iron Rule (lines 14-50), Rationalizations (17-27), Red Flags (29-37), Large Scope (41-50) |
| `writing-data-tests.md` | `dbt-qa` | Tier 1-4 framework (82-115), cost-conscious testing (151-165) |
| `debugging-dbt-errors.md` | `dbt-qa` | Error classification taxonomy (18-78) |
| `planning-dbt-models.md` | `dbt-migration` | Mock-first methodology (14-151), TDD unit tests (141-147) |
| `evaluating-impact.md` | `dbt-migration` | Impact classification (76-82), column-level grep (62-74) |
| `writing-documentation.md` | `dbt-standards` | "Why not what" principle, inspect-before-documenting |
| `managing-packages.md` | `dbt-fundamentals` | Hub API for programmatic discovery |
| `troubleshooting-dbt-job-errors` | `dbt-decision-trace` | Never-modify-test rule (22-37), Rationalizations (5 pairs), investigation template (236-276) |
| `running-dbt-commands` | `dbt-fundamentals` | MCP-first preference, warn-error-options, Fusion detection, output-keys |
| `building-dbt-semantic-layer` | `dbt-semantic-layer-developer` | 1.11+ spec, column-level properties, dbt-autofix command |
| `adding-dbt-unit-test` | `dbt-sql-unit-testing` | Cross-reference section, decision matrix (when to use each approach) |
