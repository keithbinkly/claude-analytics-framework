# dbt-agent Skills Registry

**Last Updated**: 2026-02-12
**Architecture**: Skills-First (v2.0) + Parallelized Sub-Agent Orchestration
**Total Skills**: 25 active + learner + 4 dbt-official (renamed) + 1 reference + 4 absorbed into core + 2 archived
**Pipeline Commands**: 6 (`/pipeline-new`, `-resume`, `-gate`, `-status`, `-close`, `-docs`)

---

## 🏗️ Skills-First Architecture (READ THIS FIRST)

### Philosophy

**Skills are the primary organizational unit.** Everything else (commands, guardrails, tools, knowledge) is colocated with or referenced from skills.

```
OLD (Fragmented):
├── skills/           # Knowledge only
├── commands/         # Orphaned from skills
├── shared/reference/ # Scattered guardrails
└── CLAUDE.md         # Giant trigger table

NEW (Skills-First):
└── skills/
    └── [domain]/
        ├── SKILL.md           # Knowledge + triggers + tool refs
        ├── workflows/         # Agent commands (nested)
        ├── tools.yml          # MCP tools + references declared
        └── guardrails/        # Domain checks (future)
```

### Key Principles

1. **Skills Own Their Domain** — All knowledge, workflows, and tool configs for a domain live together
2. **Progressive Disclosure** — Load skill metadata at startup, full content on trigger
3. **Plan-First Execution** — Orchestrator generates plans before work begins
4. **Workflows Replace Commands** — Agent commands nest under their parent skill as `workflows/*.md`

### Skill Structure

Each skill follows this structure:

```
skills/[name]/
├── SKILL.md              # Required: knowledge + triggers in frontmatter
├── tools.yml             # Declares MCP tools, references, guardrails
├── workflows/            # Optional: agent commands that use this skill
│   ├── implement.md
│   └── qa.md
├── guardrails/           # Optional: domain-specific checks
│   └── preflight.md
└── resources/            # Optional: supplementary docs
    └── patterns.md
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name
version: 1.0.0
description: What this skill does
tags: [relevant, tags]
entry_point: true

triggers:
  - "keyword 1"
  - "keyword 2"
  - "intent pattern"
---
```

### tools.yml Format

```yaml
mcp_tools:
  required:
    - compile
    - run
  optional:
    - get_model_health

references:
  mandatory:
    - shared/knowledge-base/migration-quick-reference.md
  check_before_sql:
    - shared/reference/anti-pattern-impact.yml

guardrails:
  required:
    - compile_before_run
```

### Where Knowledge Lives

| Type | Location | Example |
|------|----------|---------|
| Domain knowledge | `skills/[domain]/SKILL.md` | Migration patterns |
| Shared reference | `shared/reference/` | Anti-pattern list, join registry |
| Shared knowledge base | `shared/knowledge-base/` | Canonical models, folder structure |
| Decision traces | `shared/decision-traces/` | Past QA resolutions |
| Pipeline plans | `handoffs/[pipeline]/PLAN.md` | Active work tracking |

### When Adding New Knowledge

**From external sources (articles, docs, learnings):**

1. **Identify the domain** — Which skill does this belong to?
2. **Check for existing coverage** — Use `get_context()` or search skill
3. **Add to appropriate location:**
   - Domain-specific → skill's SKILL.md or resources/
   - Cross-cutting → `shared/knowledge-base/` or `shared/reference/`
   - QA pattern → `shared/decision-traces/traces.json`
4. **Update skill's MANDATORY section** if it's a critical reference

**When creating new capabilities:**

1. **Prefer enhancing existing skills** over creating new ones
2. **If new skill needed**, follow the structure above
3. **Add workflow** if it's an agent command pattern
4. **Add to this registry** with triggers and purpose

### Activation Flow

```
User message arrives
       ↓
Skill-activation hook scans for keywords/intent
       ↓
Suggests relevant skills to load
       ↓
Agent loads SKILL.md + tools.yml
       ↓
MANDATORY references loaded
       ↓
Work begins with full context
```

### Cross-References

- Epic tracking this migration: `.dots/dbt-agent-skills-architecture-migration.md`
- Skill activation hook: `.claude/hooks/skill-activation.py`
- Skill rules config: `.claude/hooks/skill-rules.json`
- Tool-skill mapping: `shared/reference/tool-skill-mapping.md`

---

## Skill Inventory

### Consolidation Summary (2025-12-31)

Skills consolidated from 36 to 17 for clarity and reduced overlap:

| Consolidated Skill | Replaces | Purpose |
|-------------------|----------|---------|
| **dbt-fundamentals** | dbt-architecture, dbt-modeling, dbt-testing, dbt-commands, dbt-materializations, dbt-core | All foundational dbt knowledge |
| **dbt-qa** | dbt-qa-execution, dbt-qa-strategy-designer, dbt-sql-unit-testing | Unified QA workflow |
| **dbt-standards** | dbt-model-placement-advisor, dbt-style-evaluator, dbt-schema-documenter, dbt-canonical-model-finder | Placement, style, docs, reuse |
| **dbt-lineage** | dbt-manifest-parser, dbt-dependency-mapper | Lineage and dependency analysis |

New skills added:
- **dbt-decision-trace** - Case-based reasoning from past QA
- **dbt-preflight** - Cost estimation before runs

Archived skills are in `_archived/` directory for reference.

---

## Core dbt Skills

### dbt-fundamentals
**Purpose**: Comprehensive dbt foundation covering architecture, modeling, testing, materializations, commands, and project setup
**Triggers**: project structure, folder organization, medallion, write model, CTE pattern, add test, materialization, incremental, dbt run, dbt build
**Consolidates**: dbt-architecture, dbt-modeling, dbt-testing, dbt-commands, dbt-materializations, dbt-core

### dbt-migration
**Purpose**: Phase 4 implementation - builds dbt models from approved tech specs
**Triggers**: migrate, legacy script, MSTR, Microstrategy, convert to dbt, pipeline migration
**Dependencies**: Requires tech-spec.md from Phase 3

### dbt-qa
**Purpose**: Unified QA workflow - strategy design, execution, and SQL unit testing
**Triggers**: qa strategy, validation plan, variance analysis, execute qa, unit test, mock data
**Consolidates**: dbt-qa-execution, dbt-qa-strategy-designer, dbt-sql-unit-testing

### dbt-standards
**Purpose**: Model placement, style evaluation, schema documentation, and canonical model reuse
**Triggers**: where should I put, folder, style, format, document, schema.yml, canonical, reusable
**Consolidates**: dbt-model-placement-advisor, dbt-style-evaluator, dbt-schema-documenter, dbt-canonical-model-finder

### dbt-lineage
**Purpose**: Dependency mapping, manifest parsing, and impact analysis
**Triggers**: lineage, upstream, downstream, dependencies, manifest, compiled sql
**Consolidates**: dbt-manifest-parser, dbt-dependency-mapper

### dbt-redshift-optimization
**Purpose**: SQL analysis and optimization for Redshift
**Triggers**: optimize, performance, slow query, DISTKEY, SORTKEY, query plan
**Status**: Unchanged (specialized)
**Note**: README.md moved to resources/

### dbt-semantic-layer-developer
**Purpose**: dbt Semantic Layer, MetricFlow, semantic models, metrics
**Triggers**: semantic layer, MetricFlow, metrics, dimensions, entities
**Status**: Unchanged (specialized)
**Note**: README.md moved to resources/

### dbt-jinja-sql-optimizer
**Purpose**: Jinja macros and templating patterns
**Triggers**: jinja, macro, template, dynamic sql, dbt-utils
**Status**: Unchanged (specialized)
**Note**: README.md moved to resources/

---

## New Skills (2025-12-29, updated 2025-12-31)

### dbt-decision-trace (v2.0)
**Purpose**: Case-based reasoning + rule synthesis from past QA resolutions
**Triggers**: log trace, search traces, past resolution, similar issue, synthesize rules, get rules
**Key Operations**:
- `log_trace()` - Log completed QA trace
- `search_traces()` - Find similar past cases
- `match_rules()` - Match symptom against synthesized rules (NEW v2.0)
- `synthesize_rules()` - Generate rules from trace patterns (NEW v2.0)
- `get_rules()` - Get synthesized rules by confidence (NEW v2.0)
**Command**: `/synthesize-traces` - Run synthesis, generate/update rules
**Storage**: `shared/decision-traces/` (traces.json, rules.json, index.json)

### dbt-preflight
**Purpose**: Pre-execution cost estimation
**Triggers**: preflight, cost estimate, how long, should I sample, before running
**Key Checks**:
- Historical runtime from stl_query
- Upstream row counts from svv_table_info
- Join risk analysis
- Stats freshness

---

## 4-Agent Workflow Skills (Parallelized)

### Pipeline Commands

| Command | Purpose |
|---------|---------|
| `/pipeline-new [name]` | Start new pipeline (creates PLAN.md, dot, registry) |
| `/pipeline-resume [name]` | Resume pipeline (loads phase context, agents, next action) |
| `/pipeline-gate [keyword]` | Approve gate (requirements, discovery, architecture, deploy) |
| `/pipeline-status [name]` | Check status of one or all pipelines |
| `/pipeline-close [name]` | Complete pipeline, extract learnings, archive |
| `/pipeline-docs [name]` | Generate docs (diagrams, blog, PPTX) from artifacts |

### Parallelized Phase Model

```
Phase 1: Requirements (1 agent)
  └─ dbt-business-context
  → GATE 1: /pipeline-gate requirements

Phase 2: Data Discovery (3 PARALLEL agents)
  ├─ Source Profiler (dbt-data-discovery) — execute_sql for profiling (no VPN)
  ├─ Lineage Analyst (dbt-lineage)
  └─ Legacy Analyst (dbt-migration Step 1)
  → GATE 2: /pipeline-gate discovery

Phase 3: Architecture (2 PARALLEL + 1 SEQUENTIAL)
  ├─ Canonical Search (dbt-standards) [PARALLEL]
  ├─ Standards Validation (dbt-standards) [PARALLEL]
  └─ Tech Spec Writer (dbt-tech-spec-writer) [AFTER A+B]
  → GATE 3: /pipeline-gate architecture

Phase 4: Implementation (multi-step)
  ├─ 4.1: Preflight — 4.2: Model Build — 4.3: Testing (3 PARALLEL) — 4.4: QA — 4.5: Handoff
  → GATE 4: /pipeline-gate deploy
```

**3 workflow types**: Full Migration, Enhancement (E1-E4), Semantic Layer (C1-C5)

**Master agent spec**: `.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md`
Defines exact skills, KBs (MUST/MAY), tools (API/CLI), and parallel/sequential flow per phase.

### dbt-orchestrator
**Purpose**: Central coordinator — manages state, gates, handoffs, agent loading
**Triggers**: start migration, new pipeline, workflow, 4-agent, gate, phase
**Key Resources**:
- `resources/agent-loading-specs.md` — Master agent config per phase
- `resources/workflow-state-machine.md` — State definitions + transitions
- `resources/gate-enforcement-rules.md` — 4 gate checkpoints
- `resources/handoff-protocols.md` — Inter-agent artifact formats

### dbt-business-context
**Purpose**: Phase 1 - Requirements capture from transcripts/docs
**Triggers**: business context, requirements, stakeholder, transcript
**Output**: `handoffs/[pipeline]/business-context.md`

### dbt-data-discovery
**Purpose**: Phase 2 - Source profiling, schema validation
**Triggers**: data discovery, profile data, source profiling, suppression
**Tools**: `execute_sql` (API — no VPN), `get_source_details`, `get_column_lineage`
**Output**: `handoffs/[pipeline]/data-discovery-report.md`

### dbt-tech-spec-writer
**Purpose**: Phase 3 - Architecture design, model inventory
**Triggers**: tech spec, technical specification, architecture design
**Output**: `handoffs/[pipeline]/tech-spec.md`

---

## SYNQ Framework Skills

### synq-data-product-architect
**Purpose**: Data product definition and priority assignment
**Triggers**: data product, priority, P1, P2, SLA, critical data

### synq-sla-monitor-designer
**Purpose**: SLA monitoring and coverage metrics
**Triggers**: SLA monitoring, coverage, quality score, observability

---

## Creative Output Skills

### mviz-full (NEW 2026-01-18)
**Purpose**: Generate static HTML dashboards and reports from data using ECharts
**Triggers**: mviz, visualize, chart, dashboard, report, bar chart, line chart, scatter plot, heatmap
**Location**: `.claude/skills/mviz-full/extracted/`
**Key Capabilities**:
- Compact JSON specs → professional HTML visualizations
- 16-column grid layout system for dashboards
- 17 chart types (bar, line, area, pie, scatter, funnel, sankey, etc.)
- 8 UI components (big_value, delta, table with sparklines, notes)
- Static output printable to PDF
- Works with dbt MCP data via `dbt show --inline`
**Usage**: Query data → "use mviz to report on this analysis"
**Generator**: `python3 chart_generator.py [spec.json|dashboard.md]`
**Note**: mviz (original) archived to `_archived/`

### architecture-diagram-creator
**Purpose**: HTML architecture diagrams with data flows
**Triggers**: create architecture diagram, system overview

### pptx-powerpoint-generator
**Purpose**: Presentation creation and editing
**Triggers**: create presentation, edit powerpoint

### blog-post-writer
**Purpose**: Transform brain dumps into polished blog posts
**Triggers**: write blog post, blog ideas

### design-document-writer
**Purpose**: Write design documents from PRDs
**Triggers**: design document, write design
**Note**: Now has proper frontmatter (activated 2026-02)

### frontend-design
**Purpose**: Production-grade frontend interfaces
**Triggers**: build web component, create web page

### echarts (NEW 2026-02)
**Purpose**: ECharts configuration reference for building rich interactive charts
**Triggers**: echarts, rich text, chart config, visual map, chart options
**Location**: `.claude/skills/echarts/`
**Key Capabilities**:
- 20-section ECharts reference covering all major chart types and features
- Configuration patterns for advanced visualizations
- Integration with interactive dashboard builder skill
**Note**: Now has proper frontmatter (activated 2026-02)

### interactive-dashboard-builder (NEW 2026-02)
**Purpose**: Build keyboard-navigable interactive HTML dashboards with deep-dive analytics
**Triggers**: interactive dashboard, keyboard dashboard, deep dive, data story
**Location**: `.claude/skills/interactive-dashboard-builder/`
**Key Capabilities**:
- Power BI-style ribbon charts via custom ECharts series
- Keyboard navigation and multi-level drill-down
- Works with dbt semantic layer data
**Note**: Now has proper frontmatter (activated 2026-02)

### data-storytelling (NEW 2026-02)
**Purpose**: End-to-end workflow from business question to narrative data storytelling page — chains ensemble analysis, viz spec design, chart comparison, critic review, semantic layer queries, and narrative page build
**Triggers**: data story, storytelling page, data narrative, tell the story of, analysis to visualization, end-to-end analysis
**Location**: `.claude/skills/data-storytelling/`
**Key Capabilities**:
- 11-step reproducible workflow (question → ensemble → viz spec → comparison → critics → selection → data → narrative → deploy)
- FT Visual Vocabulary chart type selection with genuine alternatives
- 3-critic review pattern (Encoding Accuracy, Visual Design, Communication)
- Semantic layer data integration via dbt MCP tools
- Dark-theme design system (Space Grotesk/Mono, slate palette)
**Reference implementations**: `docs/visualizations/ewallet-*` (alternatives catalog, comparison page, data story)

### samwho-interactive-viz (NEW 2026-02)
**Purpose**: Create samwho-style interactive web visualizations with scroll-driven animations
**Triggers**: samwho, interactive viz, scroll animation
**Location**: `.claude/skills/samwho-interactive-viz/`
**Note**: Now has proper frontmatter (activated 2026-02)

### hypercontext (NEW 2026-02)
**Purpose**: Manages hypercontext sessions for rich contextual linking across conversations
**Triggers**: hypercontext, context linking, session context
**Location**: `.claude/skills/hypercontext/`
**Note**: Description added to frontmatter (activated 2026-02)

---

## Meta/Utility Skills

### autonomous-planning (NEW 2026-01-25)
**Purpose**: Transform complex projects into executable task graphs with dependency-aware decomposition
**Triggers**: plan this, break this down, create task graph, autonomous execution, orchestrate this, swarm this, parallelize
**Key Capabilities**:
- Hierarchical task decomposition with blockedBy dependencies
- Parallel sub-agent execution (7-10 agents)
- Skill/knowledge/recall routing for each task
- Cross-session persistence via CLAUDE_CODE_TASK_LIST_ID
- Prompting patterns for triggering autonomous execution
**Resources**:
- `resources/decomposition-patterns.md` - Diamond, Pipeline, Fork-Join, etc.
- `resources/skill-routing-guide.md` - Agent type selection
- `resources/prompting-patterns.md` - How to trigger planning
**Based on**: Claude Code task system (v2.0.64+)

### skill-creator
**Purpose**: Guide for creating new skills
**Triggers**: create skill, new skill, update skill

### anthropic-docs-consultant
**Purpose**: Consult official Claude Code documentation
**Triggers**: Claude Code feature, how to hook, MCP server

### ai-analyst-profile
**Purpose**: AI analyst demo and stakeholder walkthrough
**Triggers**: demo, stakeholder presentation

### dbt-knowledge-integrity-check
**Purpose**: Knowledge base consistency validation
**Triggers**: integrity check, validate knowledge

### dbt-artifacts
**Purpose**: dbt Artifacts package for execution monitoring
**Triggers**: execution history, run patterns, dbt_artifacts

### context-graph-expert (NEW 2026-01-11)
**Purpose**: Context graph thought leadership, TrustGraph patterns, reification, Context Cores architecture
**Triggers**: context graph, context engineering, knowledge graph for AI, agent memory architecture, decision trace, reification, TrustGraph, context cores, systems of context
**Key Capabilities**:
- Synthesize thought leadership (Foundation Capital, Glean, TrustGraph)
- Apply context graph patterns to dbt-agent infrastructure
- Stay current via web search
- Create perspective pieces when warranted
- Advise on context/memory tool adoption
**Analysis**: `docs/updates/2026-01-11-context-graphs-trustgraph-analysis.md`
**Sources**: 23 synthesized articles (see `context-graph-expert` skill resources)
**Note**: Now has proper frontmatter (activated 2026-02)

---

## Archived Skills (in `_archived/`)

Skills consolidated into unified skills:

- dbt-architecture → dbt-fundamentals
- dbt-modeling → dbt-fundamentals
- dbt-testing → dbt-fundamentals
- dbt-commands → dbt-fundamentals
- dbt-materializations → dbt-fundamentals
- dbt-core → dbt-fundamentals
- dbt-qa-execution → dbt-qa
- dbt-qa-strategy-designer → dbt-qa
- dbt-sql-unit-testing → dbt-qa
- dbt-model-placement-advisor → dbt-standards
- dbt-style-evaluator → dbt-standards
- dbt-schema-documenter → dbt-standards
- dbt-canonical-model-finder → dbt-standards
- dbt-manifest-parser → dbt-lineage
- dbt-dependency-mapper → dbt-lineage
- dbt-developer → dbt-migration (overlapped)

Skills archived (2026-02):

- mviz → replaced by mviz-full
- manual-adversarial-review → archived

---

## dbt-Official Skills (Integrated from dbt-labs/dbt-agent-skills)

Original 9 skills from `dbt-labs/dbt-agent-skills` have been integrated:
- **4 absorbed** into core skills (content merged, originals archived to `docs/archive/skills/`)
- **4 renamed** as standalone utilities (removed `dbt-official-` prefix)
- **1 renamed** as reference resource

### Standalone (Renamed)

| Skill | Triggers | Formerly |
|-------|----------|----------|
| `dbt-docs-lookup` | dbt docs, look up dbt | `dbt-official-fetching-dbt-docs` |
| `dbt-nl-queries` | business question, how many, total sales | `dbt-official-answering-natural-language-questions-with-dbt` |
| `dbt-mcp-setup` | MCP server, configure MCP | `dbt-official-configuring-dbt-mcp-server` |
| `dbt-fusion-migration` | Fusion, migrate to Fusion | `dbt-official-migrating-dbt-core-to-fusion` |

### Reference Resource (Renamed)

| Resource | Triggers | Formerly |
|----------|----------|----------|
| `dbt-native-unit-test-reference` | dbt unit test, TDD | `dbt-official-adding-dbt-unit-test` |

### Absorbed (Archived to `docs/archive/skills/`)

| Archived Skill | Content Now In |
|---------------|----------------|
| `dbt-official-using-dbt-for-analytics-engineering` | Iron Rule → `dbt-data-discovery`, Test priority → `dbt-qa`, Investigation template → `dbt-decision-trace` |
| `dbt-official-troubleshooting-dbt-job-errors` | Never-modify-test rule → `dbt-qa`, Rationalizations → `dbt-decision-trace` |
| `dbt-official-running-dbt-commands` | MCP-first, --warn-error-options, Fusion detection → `dbt-fundamentals` |
| `dbt-official-building-dbt-semantic-layer` | Derived semantics (1.12+) → `dbt-semantic-layer-developer` |

---

## Quick Reference

| Need | Skill / Resource |
|------|-----------------|
| **Start a pipeline** | **`/pipeline-new [name]`** |
| **Resume a pipeline** | **`/pipeline-resume [name]`** |
| **Approve a gate** | **`/pipeline-gate [keyword]`** |
| **Agent loading per phase** | **`agent-loading-specs.md`** |
| dbt basics (architecture, modeling, testing) | dbt-fundamentals |
| Migrate legacy SQL | dbt-migration |
| QA validation | dbt-qa |
| Where to put a model | dbt-standards |
| SQL style/formatting | dbt-standards |
| Find canonical models | dbt-standards |
| Check dependencies | dbt-lineage |
| Optimize slow query | dbt-redshift-optimization |
| Semantic layer/metrics | dbt-semantic-layer-developer |
| Past QA resolutions | dbt-decision-trace |
| Estimate run cost | dbt-preflight |
| VPN-free data profiling | `execute_sql` (API path — see MCP tools ref) |
| Context graphs / agent memory | context-graph-expert |
| Data visualization / dashboards | mviz |
