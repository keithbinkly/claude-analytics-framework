---
title: Canonical dbt Flow Audit — Skills, Agents, Commands
status: open
priority: 0
tags: [architecture, skills, audit, canonical-flow]
created: 2026-02-08
---

# Canonical dbt Development Flow vs Our Skills: Full Audit

**Source of truth**: 3 research reports from 90+ official dbt Labs sources (2,400 lines total)
- `.claude/cache/agents/oracle/output-2026-02-08-dbt-lifecycle-research.md`
- `.claude/cache/agents/oracle/output-2026-02-08T20-30-42.md`
- `.claude/cache/agents/oracle/output-2026-02-08-semantic-layer-deep-research.md`

**What we're auditing**: Skills registry, agent-loading-specs, pipeline commands, resource checks, ordering

---

## Part 1: The Canonical Flow (Synthesized from Research)

This is the end-to-end lifecycle as defined by dbt Labs official documentation — the independent source of truth.

```
PHASE 0: PROJECT INIT
  └─ dbt init → project scaffold
  └─ Configure profiles.yml, dbt_project.yml
  └─ Install packages (dbt-utils, audit_helper, dbt-expectations)

PHASE 1: SOURCE ONBOARDING
  └─ Define source YAML (source name, database, schema, tables)
  └─ Configure source freshness (loaded_at_field, warn_after, error_after)
  └─ Add source-level tests (PK unique+not_null, accepted_values)
  └─ Use {{ source() }} exclusively — never raw table refs downstream

PHASE 2: DATA DISCOVERY & PROFILING
  └─ Grain analysis (what makes each row unique?)
  └─ Null audit (% null per column, what null means)
  └─ Uniqueness verification (COUNT vs COUNT DISTINCT)
  └─ Value distributions (min/max, cardinality, outliers)
  └─ Referential integrity (do FK joins actually work? fanout?)
  └─ Temporal patterns (cadence, gaps, date ranges)

PHASE 3: STAGING LAYER
  └─ 1:1 mapping with source tables
  └─ Renaming, type casting, soft delete filtering, column selection
  └─ NO aggregations, NO joins, NO business logic, NO window functions
  └─ Materialize as views
  └─ Named stg_<source>__<entity>
  └─ CTE structure: source → renamed → select * from renamed
  └─ ADD TESTS: PK unique+not_null, accepted_values on cleaned fields
  └─ ADD DOCS: YAML descriptions on model + columns

PHASE 4: INTERMEDIATE MODELS
  └─ Re-graining (fan out or collapse)
  └─ Complex joins with clear purpose
  └─ Isolating difficult logic
  └─ Named int_<entity>__<verb>
  └─ Not exposed to end users
  └─ Materialized as ephemeral or views
  └─ ADD TESTS: PK on re-grained models, join validation
  └─ ADD DOCS: YAML descriptions

PHASE 5: MARTS (CRITICAL ARCHITECTURAL FORK)
  └─ DECISION: Normalized (with Semantic Layer) vs Denormalized (without)
  └─ If SL: Stay normalized, star schema — MetricFlow does the denormalization
  └─ If no SL: Wide and denormalized — pack everything needed per concept
  └─ Named fct_<entity> (facts) or dim_<entity> (dimensions)
  └─ Grouped by business domain (models/marts/finance/, etc.)
  └─ Materialization progression: view → table → incremental
  └─ ADD TESTS: Unit tests on complex logic, PK tests, business rule validation
  └─ ADD DOCS: Full descriptions, doc blocks for complex concepts
  └─ ADD CONTRACTS: enforced:true on stable marts consumed by SL or BI

PHASE 6: TESTING STRATEGY (CONTINUOUS, NOT A PHASE)
  └─ Sources: freshness + existence (PK, not_null)
  └─ Staging: data quality gates (range, format, accepted_values)
  └─ Intermediate: join integrity (PK on re-grained, fanout checks)
  └─ Marts: business logic (unit tests, expression_is_true, net-new columns only)
  └─ Severity config: error for critical, warn for nice-to-know
  └─ DON'T re-test passthrough columns from upstream layers

PHASE 7: SEMANTIC LAYER (if applicable)
  └─ Time spine model (materialized as table, daily grain minimum)
  └─ Semantic models: entities → dimensions → measures (this order)
  └─ Metrics: simple first → then ratio, cumulative, derived, conversion
  └─ Validate: dbt parse → mf validate-configs → mf query --limit 1
  └─ Saved queries (declarative caching)
  └─ Exports (materialize for non-native BI tools)

PHASE 8: CI/CD
  └─ Slim CI: state:modified+ --defer --state ./target-prod
  └─ Clone incremental models before CI build (dbt clone)
  └─ --fail-fast, --empty for schema-only contract checks
  └─ Semantic validation in CI (dbt parse + mf validate --skip-dw)

PHASE 9: DEPLOYMENT & BI SERVING
  └─ Production deploy job triggered by merge
  └─ Source freshness runs in production (severity: error on critical)
  └─ BI tool connection: native SL integration OR exports OR JDBC
  └─ Monitor with dbt Artifacts / dbt Cloud

CROSS-CUTTING (applies at every phase):
  └─ SQL style: lowercase, trailing commas, 4-space indent, import CTEs
  └─ Documentation: as you go, not at the end
  └─ Compile before run (always)
  └─ audit_helper for migration reconciliation
```

---

## Part 2: Mapping Our Skills to the Canonical Flow

### Coverage Matrix

| Canonical Phase | Our Skill(s) | Coverage | Gap Assessment |
|----------------|-------------|----------|----------------|
| **0. Project Init** | dbt-fundamentals | Partial | Covers concepts but not packages install guidance (audit_helper, dbt-expectations) |
| **1. Source Onboarding** | dbt-data-discovery (partial) | **WEAK** | We profile data but don't have explicit source YAML generation or freshness config |
| **2. Data Discovery** | dbt-data-discovery | **STRONG** | Comprehensive profiling — grain, nulls, distributions, suppression detection |
| **3. Staging Layer** | dbt-fundamentals + dbt-standards | Moderate | CTE patterns and naming covered. Missing: explicit test+doc addition at staging time |
| **4. Intermediate Models** | dbt-fundamentals | Moderate | Concepts covered. Missing: re-graining test guidance, fan-out detection protocols |
| **5. Marts** | dbt-standards + dbt-tech-spec-writer | **WEAK on key decision** | No explicit "normalized vs denormalized" fork. No model contracts. No materialization progression guidance |
| **6. Testing by Layer** | dbt-qa + dbt-fundamentals | **MISARCHITECTED** | Testing is a Phase 4.3 blob, not continuous per-layer. No "don't re-test passthrough" rule. No severity config guidance |
| **7. Semantic Layer** | dbt-semantic-layer-developer | **STRONG** | Comprehensive MetricFlow coverage. Has naming conventions, validation, all metric types |
| **8. CI/CD** | **NONE** | **MISSING** | No skill, no workflow, no guidance for Slim CI, state:modified+, dbt clone |
| **9. Deployment/BI** | dbt-semantic-layer-developer (partial) | Moderate | SL connection covered. No production monitoring, no source freshness in prod |
| **Migration/Refactoring** | dbt-migration | **STRONG** | 4-phase migration, legacy analysis, but audit_helper underused |
| **SQL Style** | dbt-standards | **STRONG** | CTE patterns, anti-patterns, naming conventions |
| **Documentation** | dbt-standards (doc section) | **WEAK on timing** | Capability exists but not invoked until Phase 4. Should be continuous |

### Skill-by-Skill Fitness Assessment

| Skill                            | Canonical Alignment       | Key Strengths                                                        | Key Gaps                                                                                                     |
| -------------------------------- | ------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **dbt-business-context**         | Good                      | Captures requirements before building                                | No grain analysis. No "what questions determine grain" prompt                                                |
| **dbt-data-discovery**           | Good                      | Comprehensive profiling                                              | Missing: source YAML generation, freshness config, formal grain documentation template                       |
| **dbt-standards**                | Mixed                     | Strong naming/placement. Good canonical search                       | Missing: model contracts, access modifiers, materialization progression, normalized vs denormalized guidance |
| **dbt-fundamentals**             | Mixed                     | Broad foundation                                                     | Jack-of-all-trades. Testing section doesn't match "test by layer" canonical approach                         |
| **dbt-migration**                | Good                      | Clear 4-phase workflow                                               | Under-uses audit_helper. Phase 1 (migrate unchanged) could reference our existing patterns better            |
| **dbt-qa**                       | Over-engineered           | 7-phase QA is more comprehensive than canonical                      | But it runs too late. Should be woven into model creation, not a separate gate                               |
| **dbt-preflight**                | Good                      | Cost estimation is unique to us (not in canonical)                   | But it's step 4.1 — could be merged into tech-spec step for earlier cost awareness                           |
| **dbt-lineage**                  | Good                      | Dependency mapping well-covered                                      | No CI/CD state comparison integration                                                                        |
| **dbt-semantic-layer-developer** | Excellent                 | Most aligned skill. Naming conventions, all metric types, validation | Missing: explicit "start with simple metrics, build up" guidance in workflow                                 |
| **dbt-tech-spec-writer**         | Good                      | Creates architecture docs                                            | Missing: the normalized vs denormalized fork as a mandatory decision point                                   |
| **dbt-decision-trace**           | Novel (not in canonical)  | Unique to us — case-based reasoning. High value                      | No gap — this is additive                                                                                    |
| **dbt-redshift-optimization**    | Novel (platform-specific) | Our anti-pattern list is evidence-based with measured impact         | No gap — this is additive                                                                                    |
| **dbt-jinja-sql-optimizer**      | Good                      | Jinja/macro patterns                                                 | Underused in workflow — not loaded until complex macros appear                                               |

---

## Part 3: Ordering Analysis

### Current Pipeline Order vs Canonical

```
OUR ORDER                          CANONICAL ORDER
─────────                          ──────────────
Phase 1: Requirements              Phase 0: Project init ← WE SKIP
  └─ business-context              Phase 1: Source onboarding ← WE DELAY TO Phase 2
                                   Phase 2: Data discovery
Phase 2: Discovery (3 parallel)    Phase 3: Staging
  ├─ Source profiler                Phase 4: Intermediate
  ├─ Lineage analyst                Phase 5: Marts (NORMALIZED vs DENORMALIZED FORK)
  └─ Legacy analyst                 Phase 6: Testing (continuous, not a phase!)
                                   Phase 7: Semantic Layer
Phase 3: Architecture              Phase 8: CI/CD ← WE'RE MISSING
  ├─ Canonical search               Phase 9: Deployment ← WE'RE MISSING
  ├─ Standards validation
  └─ Tech spec writer              CROSS-CUTTING:
                                     - Documentation (as you go)
Phase 4: Implementation              - Style (enforced always)
  ├─ 4.1 Preflight                   - Compile before run
  ├─ 4.2 Model build
  ├─ 4.3 Testing (3 parallel)
  ├─ 4.4 QA
  └─ 4.5 Handoff
```

### Ordering Issues Identified

#### ISSUE 1: Source freshness is discovered too late (HIGH IMPACT)
**Canonical**: Configure freshness at source onboarding time (Phase 1)
**Us**: Data discovery (Phase 2) profiles data but doesn't set freshness thresholds
**Impact**: Stale source data goes undetected until QA (Phase 4.4), causing rework
**Fix**: Add freshness configuration to dbt-data-discovery's output. Agent should propose `loaded_at_field`, `warn_after`, `error_after` values based on profiling results.

#### ISSUE 2: Testing is a phase, not continuous (HIGH IMPACT)
**Canonical**: Add tests PER LAYER as you build — source tests at source time, staging tests at staging time
**Us**: All testing happens in Phase 4.3, after ALL models are built
**Impact**: Errors compound across layers. A staging PK violation propagates to intermediates and marts before being caught.
**Fix**: Restructure Phase 4.2 (model build) to be: write model → add tests → compile → run → repeat per layer. Testing agents should fire per-layer, not after all layers.

#### ISSUE 3: Documentation is an afterthought (MEDIUM IMPACT)
**Canonical**: "As you go, not at the end." Add descriptions in the same YAML where you declare tests.
**Us**: dbt-standards has documentation capability but it's only invoked reactively on "document" trigger
**Impact**: Models ship without descriptions. Documentation debt accumulates.
**Fix**: Make dbt-standards' doc-generation a mandatory sub-step of model creation. When Phase 4.2 writes a `.sql` file, it should also write/update the corresponding `.yml` with descriptions.

#### ISSUE 4: The normalized vs denormalized decision is invisible (HIGH IMPACT)
**Canonical**: This is THE architectural fork. If using Semantic Layer → normalized marts. If not → denormalized.
**Us**: dbt-tech-spec-writer creates architecture docs but doesn't force this decision
**Impact**: We may build denormalized marts and then try to put a Semantic Layer on top (wrong approach). Or normalize when we don't need SL.
**Fix**: Add to dbt-tech-spec-writer's MANDATORY checklist: "Will this pipeline use the Semantic Layer? If yes → normalize. If no → denormalize." This must be answered before any mart design.

#### ISSUE 5: No model contracts or governance (MEDIUM IMPACT)
**Canonical**: `contract: enforced: true` on stable marts. Access modifiers (public/protected/private). Versioning.
**Us**: Zero concept of model contracts in any skill
**Impact**: Schema drift in marts breaks downstream BI/SL without warning
**Fix**: Add contracts section to dbt-standards. When a mart is consumed by Semantic Layer or BI tool, recommend `contract: enforced: true`.

#### ISSUE 6: CI/CD is completely missing (HIGH IMPACT)
**Canonical**: Slim CI, state:modified+, deferred builds, --empty, --fail-fast, dbt clone for incrementals
**Us**: No skill, no workflow, no guidance
**Impact**: We deploy without CI validation. No automated detection of breaking changes.
**Fix**: Create a `dbt-cicd` skill or add a CI section to dbt-fundamentals. At minimum, document the Slim CI pattern and how to integrate semantic validation.

#### ISSUE 7: audit_helper is underused in migration QA (LOW-MEDIUM IMPACT)
**Canonical**: compare_relations, compare_column_values, compare_queries — structured, consistent output
**Us**: dbt-qa uses custom SQL queries for comparison
**Impact**: Inconsistent QA output format. Manual effort to build comparison queries each time.
**Fix**: Add audit_helper macros as the PRIMARY tool in dbt-qa Phase 4 (Comparative QA). Keep custom SQL as fallback.

---

## Part 4: Early Deflection Opportunities

These are things that, if moved earlier in the pipeline, would prevent downstream rework.

### 1. Grain Analysis at Requirements Time (save 30-60 min per pipeline)

**Current**: Grain is discovered during Phase 2 data discovery
**Proposed**: Ask about grain during Phase 1 requirements capture

**Why it deflects work**: If the business stakeholder says "I need one row per customer per month" and the source data is one row per transaction, you know immediately you need an intermediate model with aggregation. Without this, you design staging → discover the grain mismatch → redesign architecture.

**Implementation**: Add to dbt-business-context's output template:
```
## Data Grain Requirements
- Expected grain of final output: [one row per ___]
- Known source grain: [one row per ___]
- Grain mismatch detected: [yes/no → implications for intermediate models]
```

### 2. Source Freshness Config at Discovery Time (prevent stale-data rework)

**Current**: Not configured until models are built and QA discovers stale data
**Proposed**: dbt-data-discovery agent proposes freshness thresholds as part of discovery report

**Implementation**: Add to data-discovery-report.md output:
```
## Recommended Source Freshness Configuration
| Source | Table | loaded_at_field | warn_after | error_after | Rationale |
|--------|-------|----------------|------------|-------------|-----------|
```

### 3. PK Tests During Model Creation (prevent compound errors)

**Current**: All tests run after all models built (Phase 4.3)
**Proposed**: After writing each model, immediately add PK test and run it

**Why it deflects work**: A staging model with a duplicate PK will cause every intermediate and mart that references it to produce wrong results. Catching it at staging means you fix 1 model, not 5.

**Implementation**: Modify Phase 4.2 build order:
```
CURRENT: Write all stg_ → Write all int_ → Write all fct_/dim_ → Test everything
PROPOSED: Write stg_ + test stg_ → Write int_ + test int_ → Write fct_/dim_ + test fct_/dim_
```

### 4. Documentation Concurrent with Model Creation (eliminate doc debt)

**Current**: Documentation is a separate, optional step
**Proposed**: Schema YAML generation is automatic when writing any model

**Implementation**: In Phase 4.2, after writing `stg_stripe__payments.sql`, the agent should also write/update `_stripe__models.yml` with at minimum:
```yaml
models:
  - name: stg_stripe__payments
    description: "[auto-generated stub — needs human review]"
    columns:
      - name: payment_id
        description: "Primary key"
        data_tests:
          - unique
          - not_null
```

### 5. Normalized vs Denormalized Decision in Tech Spec (prevent architectural rework)

**Current**: Decision is implicit or never made
**Proposed**: dbt-tech-spec-writer's template includes mandatory field:

```
## Semantic Layer Decision
- Will this pipeline feed the Semantic Layer? [YES/NO]
- If YES: Marts will be NORMALIZED (star schema). MetricFlow handles denormalization.
- If NO: Marts will be DENORMALIZED (wide tables for direct BI consumption).
- Decision rationale: [why]
```

### 6. Anti-Pattern Scan at Architecture Time (prevent costly rewrites)

**Current**: Anti-patterns caught during code review or never
**Proposed**: When tech spec references specific join patterns or SQL approaches, run anti-pattern check against `anti-pattern-impact.yml`

**Implementation**: Agent C (Tech Spec Writer) in Phase 3 should reference anti-pattern-impact.yml and flag any proposed patterns that match known anti-patterns (NOT IN subquery, OR in JOIN, etc.)

---

## Part 5: Integration Recommendations (Revised)

Based on this audit, the original integration plan at `.dots/dbt-agent-skills-integration-plan.md` should be revised. Here's the updated priority:

### Priority 1: Fix the Testing Architecture (HIGHEST IMPACT)

**Problem**: Testing as a blob in Phase 4.3
**Solution**:
1. Split dbt-qa into "per-layer test generation" and "comparative QA"
2. Per-layer test generation: fires DURING Phase 4.2, per layer
3. Comparative QA: stays at Phase 4.4 for migration validation
4. Absorb dbt-official-adding-dbt-unit-test's TDD workflow into per-layer testing

### Priority 2: Add Source Onboarding to Discovery (EARLY DEFLECTION)

**Problem**: Source freshness and source YAML not generated during discovery
**Solution**: Enhance dbt-data-discovery to output:
1. Recommended source YAML with freshness thresholds
2. Recommended source-level tests (PK, accepted_values)
3. Grain documentation per source table

Absorb dbt-official-using-dbt-for-analytics-engineering's source definition guidance.

### Priority 3: Make the SL Decision Explicit in Architecture (ARCHITECTURAL)

**Problem**: Normalized vs denormalized is never explicitly decided
**Solution**: Add to dbt-tech-spec-writer's mandatory template:
1. "Semantic Layer: YES/NO?" decision point
2. If YES → load dbt-semantic-layer-developer guidance for mart design
3. If NO → load dbt-standards' denormalized mart patterns

### Priority 4: Add CI/CD Skill (MISSING COVERAGE)

**Problem**: No CI/CD concept in our workflow
**Solution**: Create `dbt-cicd` section in dbt-fundamentals or standalone skill covering:
1. Slim CI setup (state:modified+ --defer)
2. Incremental clone strategy (dbt clone)
3. Semantic validation in CI (dbt parse + mf validate --skip-dw)
4. --fail-fast and --empty patterns

Absorb relevant pieces from dbt-official-running-dbt-commands.

### Priority 5: Add Model Contracts to Standards (GOVERNANCE)

**Problem**: No concept of contracts, access, or versioning
**Solution**: Add section to dbt-standards covering:
1. When to use `contract: enforced: true` (stable marts consumed by SL/BI)
2. Access modifiers (public for marts, private for intermediates)
3. Versioning for breaking changes

### Priority 6: Integrate audit_helper into QA (EFFICIENCY)

**Problem**: Custom SQL for migration comparison
**Solution**: Make audit_helper macros the default in dbt-qa Phase 4:
1. `compare_relations` for row-level diff
2. `compare_column_values` for column-level drill-down
3. Keep our variance thresholds (<0.1%)

---

## Part 6: Proposed Revised Pipeline Flow

```
Phase 1: Requirements + Grain Analysis (1 agent)
  └─ dbt-business-context
  └─ NEW: Grain requirements template
  └─ NEW: "Will this use Semantic Layer?" decision
  → GATE 1: /pipeline-gate requirements

Phase 2: Data Discovery + Source Config (3 PARALLEL agents)
  ├─ Agent A: Source Profiler (dbt-data-discovery)
  │   └─ NEW OUTPUT: Recommended source YAML with freshness thresholds
  │   └─ NEW OUTPUT: Recommended source-level tests
  │   └─ NEW OUTPUT: Grain documentation per source
  ├─ Agent B: Lineage Analyst (dbt-lineage)
  └─ Agent C: Legacy Analyst (dbt-migration Step 1)
      └─ NEW: Anti-pattern pre-scan against anti-pattern-impact.yml
  → GATE 2: /pipeline-gate discovery

Phase 3: Architecture + Design Decisions (2 PARALLEL + 1 SEQUENTIAL)
  ├─ Agent A: Canonical Search (dbt-standards) [PARALLEL]
  ├─ Agent B: Standards + Contracts Validation (dbt-standards) [PARALLEL]
  │   └─ NEW: Model contract recommendations
  │   └─ NEW: Normalized vs denormalized decision enforcement
  └─ Agent C: Tech Spec Writer (dbt-tech-spec-writer) [AFTER A+B]
      └─ NEW: Mandatory SL decision field
      └─ NEW: Anti-pattern flag on proposed patterns
  → GATE 3: /pipeline-gate architecture

Phase 4: Implementation (per-layer build+test, not blob)
  ├─ 4.1: Preflight (unchanged)
  ├─ 4.2: REVISED Model Build (per-layer with inline testing)
  │   ├─ Layer 1: Write stg_* → Add PK tests → Add YAML docs → Compile → Test → Run
  │   ├─ Layer 2: Write int_* → Add PK+join tests → Add YAML docs → Compile → Test → Run
  │   └─ Layer 3: Write fct_*/dim_* → Add unit tests + PK → Add YAML + contracts → Compile → Test → Run
  ├─ 4.3: REVISED Testing (reduced scope — only cross-cutting)
  │   ├─ Agent A: SQL Unit Tests for complex business logic [PARALLEL]
  │   ├─ Agent B: Linter (MetricFlow YAML + SQL anti-patterns) [PARALLEL]
  │   └─ (per-layer tests already ran in 4.2)
  ├─ 4.4: QA (unchanged + audit_helper)
  │   └─ NEW: audit_helper as primary comparison tool
  └─ 4.5: Handoff (unchanged)
  → GATE 4: /pipeline-gate deploy

Phase 5: Semantic Layer (if SL decision = YES in Phase 3) ← NEW EXPLICIT PHASE
  ├─ 5.1: Time spine model
  ├─ 5.2: Semantic model YAML (entities → dimensions → measures)
  ├─ 5.3: Metrics (simple first → ratio/cumulative/derived/conversion)
  ├─ 5.4: Validation (3 parallel: lint, parse+validate, query smoke)
  ├─ 5.5: Saved queries + exports
  └─ 5.6: Documentation
  → GATE 5: /pipeline-gate semantic ← NEW GATE

Phase 6: CI/CD + Deploy ← NEW PHASE
  ├─ 6.1: Configure Slim CI job
  ├─ 6.2: Validate CI with --empty + semantic validation
  └─ 6.3: Production deployment
  → GATE 6: /pipeline-gate deploy
```

---

## Part 7: dbt-Official Skills Integration (Revised Mapping)

Based on the canonical flow audit, here's where each dbt-official skill best integrates:

| Official Skill | Absorb Into | Integration Point | What to Extract |
|----------------|------------|-------------------|-----------------|
| adding-dbt-unit-test | dbt-qa (per-layer testing) | Phase 4.2, Layer 3 (mart unit tests) | TDD workflow, dict/csv/sql format examples, retrospective vs prospective |
| answering-natural-language-questions | dbt-semantic-layer-developer | Phase 5.3+ (post-metric-build) | NL→MetricFlow query patterns |
| building-dbt-semantic-layer | dbt-semantic-layer-developer | Phase 5 (all steps) | Official examples, validation patterns |
| configuring-dbt-mcp-server | Keep standalone | Pre-pipeline (setup) | No change needed |
| fetching-dbt-docs | Keep standalone (utility) | Any phase | Reference lookup tool |
| migrating-dbt-core-to-fusion | Keep standalone | One-time migration | Specialized, rarely used |
| running-dbt-commands | dbt-fundamentals | Cross-cutting | CLI patterns, selectors, --fail-fast |
| troubleshooting-dbt-job-errors | dbt-decision-trace | Phase 4.4 QA | Error patterns → trace database |
| using-dbt-for-analytics-engineering | Split: source guidance → dbt-data-discovery, model guidance → dbt-fundamentals | Phase 2-4 | Source definition, modeling patterns |

---

## Part 8: Summary Scorecard

| Dimension | Score | Detail |
|-----------|-------|--------|
| **Phase ordering** | 7/10 | Requirements → Discovery → Architecture → Implementation is correct. But testing-as-blob and missing CI/CD hurt. |
| **Skill coverage** | 6/10 | Strong on discovery, migration, semantic layer. Weak on source onboarding, CI/CD, governance. |
| **Early deflection** | 4/10 | We miss 4 major opportunities: grain at requirements, freshness at discovery, tests per layer, docs with models |
| **dbt-official integration** | 3/10 | Official skills are listed in registry but not functionally integrated. They sit in `dbt-official-*/` untouched. |
| **Documentation timing** | 3/10 | Capability exists but only fires reactively. Canonical says "as you go." |
| **Testing architecture** | 4/10 | QA is comprehensive but misarchitected as a late blob rather than continuous per-layer |
| **Semantic layer** | 9/10 | Our strongest alignment. Naming conventions, all metric types, validation, linter. |
| **Migration workflow** | 8/10 | Strong 4-phase process. audit_helper underused but workflow is sound. |

**Overall**: We built a system optimized for our specific pipeline migration workflow (legacy → dbt) and did it well. But we didn't fully internalize the canonical dbt development lifecycle, which is broader. The biggest returns come from:

1. **Testing per-layer** (prevents error compounding)
2. **Source freshness at discovery** (prevents stale-data rework)
3. **Explicit SL decision at architecture** (prevents mart redesign)
4. **CI/CD skill** (prevents production surprises)

---

## Next Steps

1. [ ] Revise integration plan at `.dots/dbt-agent-skills-integration-plan.md`
2. [ ] Restructure Phase 4.2 to build+test per layer
3. [ ] Add source freshness output to dbt-data-discovery
4. [ ] Add SL decision + model contracts to dbt-tech-spec-writer
5. [ ] Create CI/CD section (skill or fundamentals addition)
6. [ ] Add grain requirements to dbt-business-context template
7. [ ] Integrate audit_helper into dbt-qa Phase 4
8. [ ] Absorb 6 dbt-official skills into our skills (keep 3 standalone)
