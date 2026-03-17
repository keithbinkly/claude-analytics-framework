# Analytics & Insights Team Workspace — Specification

**Authors:** Keith + Claude (System Architect)
**Date:** 2026-03-13
**Status:** Draft spec — ready for team review

---

## What This Is

The **Analytics & Insights Team Workspace** is our customized version of the `claude-analytics-framework` repo. It serves as the shared control plane for the analytics team's AI-assisted work — the one place where agents, skills, knowledge, and workflows live so that everyone on the team can benefit from them.

It is **not** where dbt code lives. It is **not** where data stories or articles live. It is the brain that coordinates work across all of those projects.

---

## The Three-Repo Model

```
┌─────────────────────────────────────────────────────────┐
│  Analytics & Insights Team Workspace (this repo)                          │
│  ─────────────────────────────                          │
│  The shared brain. Agents, skills, knowledge,           │
│  commands, and team coordination.                       │
│                                                         │
│  .claude/          ← agents, skills, commands, rules    │
│  knowledge/        ← domain knowledge, patterns, refs   │
│  repos/            ← symlinks to sibling repos          │
│                                                         │
│  Linked repos (external, intact, never absorbed):       │
│  ├── dbt-enterprise    ← production dbt project         │
│  ├── data-centered     ← content/visualization site     │
│  └── dbt-agent         ← legacy control plane (ref)     │
└─────────────────────────────────────────────────────────┘
```

### Why three repos, not one?

| Repo | What it does | Why it's separate |
|------|-------------|-------------------|
| **Analytics & Insights Team Workspace** | Shared control plane — agents, skills, knowledge | Shared across the team; changes here improve everyone's workflow |
| **dbt-enterprise** | Production dbt models, tests, seeds, configs | Production code with strict CI/CD, branch protection, and team review. Mixing `.claude/` config noise into PRs slows down model review |
| **dbt-agent** | Current operational reference | Battle-tested skills and knowledge base. Stays intact as migration source — we copy from it, never delete from it |

The separation between "where agents think" and "where dbt runs" is already proven in production. Every pipeline session today loads skills from dbt-agent and runs dbt commands in dbt-enterprise via `cd`. This workspace just moves the thinking layer up one level so the whole team can share it.

---

## Who This Is For

| Person | What they get from this workspace |
|--------|----------------------------------|
| **Pipeline builders** (dbt) | Shared skills for migration, QA, preflight, optimization. Decision traces from past QA investigations. Canonical model registry. Pipeline lifecycle commands |
| **Data scientists** (feature store) | A place to document feature store patterns, domain knowledge, and tooling preferences. Shared analyst ensemble for ad-hoc questions |
| **TPG pipeline builders** | Domain knowledge folder for TPG-specific patterns. Shared dbt fundamentals and Redshift optimization skills |
| **Anyone on the analytics team** | One starting point for AI-assisted work. Cross-repo search. Shared commands. Team coordination |

---

## Architecture

### Layer 1: Agent System (`.claude/`)

Our agent model is **two-tier**: domain agents (Opus-class, persistent memory, judgment) and task agents (Sonnet-class, stateless, execution).

```
Domain Agents (Opus)          Task Agents (Sonnet)
┌──────────────────┐          ┌──────────────────┐
│ Builder          │─spawns──▶│ SQL Builder       │
│ QA               │─spawns──▶│ QA Analyst        │
│ Analyst          │─spawns──▶│ Data Discoverer   │
│ Designer         │─spawns──▶│ Architect         │
│ System Architect │          │ Learner           │
│ Context Builder  │          │ Orchestrator      │
└──────────────────┘          └──────────────────┘
```

**Key properties:**
- Domain agents have persistent memory in `~/.claude/agent-memory/` (global, not repo-bound)
- Task agents are disposable — clean context each time
- Domain agents coordinate; task agents execute
- Model selection: Opus for judgment, Sonnet for extraction. Never Haiku

**What this replaces:** The original framework shipped with a 9-role + 15-specialist confidence-based delegation model built for Snowflake/AWS. Our model is simpler, proven, and Redshift-native.

### Layer 2: Skills (`.claude/skills/`)

Skills are reusable capability modules loaded on demand by keyword matching.

**Core skills (promoted from dbt-agent):**

| Category | Skills |
|----------|--------|
| **Pipeline lifecycle** | Migration, Orchestrator, Preflight, Tech Spec Writer, Business Context |
| **Quality** | QA (4-template system), Decision Traces, SQL Unit Testing, dbt Native Unit Tests |
| **Optimization** | Redshift Optimization, Jinja SQL Optimizer, Anti-Pattern Enforcement |
| **Standards** | dbt Standards, Fundamentals, Lineage, Data Discovery |
| **Semantic layer** | Semantic Layer Developer, Fusion Migration |
| **Analysis** | AI Analyst Ensemble, Data Storytelling, SQL Hidden Gems |
| **Visualization** | ECharts Reference, Interactive Dashboard Builder, samwho Interactive Viz |

**Team-extensible:** Teammates can add skills for their domains (feature store, TPG) by creating a folder in `.claude/skills/` with a `SKILL.md` file.

### Layer 3: Knowledge (`knowledge/`)

Domain-specific knowledge, patterns, and reference material. This is the primary contribution point for teammates.

```
knowledge/
  platform/
    planning/           ← migration plans, evaluations (you're reading one)
    operations/         ← team operating model, runbooks
    training/           ← onboarding, how-tos
  domains/
    dbt-pipelines/      ← canonical models, migration patterns, QA methodology
    feature-store/      ← [team-contributed] feature engineering, ML pipelines
    tpg-pipelines/      ← [team-contributed] TPG-specific patterns and domain knowledge
    semantic-layer/     ← MetricFlow, metrics definitions, saved queries
    redshift/           ← optimization patterns, table design, query tuning
    data-storytelling/  ← visualization patterns, dashboard templates
  reference/
    tools/              ← MCP setup, dbt CLI, external tool guides
    standards/          ← SQL style, naming conventions, folder structure
```

Each domain folder has:
- `README.md` — what this domain covers, who maintains it
- `patterns/` — proven approaches and templates
- `reference/` — external docs, tool guides, cheat sheets
- `decisions/` — why we do things this way (decision traces)

### Layer 4: Commands (`.claude/commands/`)

Slash commands for common workflows.

**Pipeline lifecycle:**
| Command | Purpose |
|---------|---------|
| `/pipeline-new [name]` | Start a new pipeline — creates plan, dot, registry entry |
| `/pipeline-resume [name]` | Resume existing pipeline — loads phase context |
| `/pipeline-gate [keyword]` | Approve a gate checkpoint |
| `/pipeline-status` | Check status of all pipelines |
| `/pipeline-close [name]` | Complete pipeline, extract learnings |

**Analysis:**
| Command | Purpose |
|---------|---------|
| `/analyze` | Multi-analyst ensemble — fans out business questions to 3 specialist analysts |
| `/explore-data` | Systematic data exploration |
| `/data-story` | End-to-end data story creation |

**Coordination:**
| Command | Purpose |
|---------|---------|
| `/save` | Save workstream progress |
| `/load [name]` | Resume from workstream state |
| `/learning-loop` | Distill session learnings into the knowledge base |
| `/morning-review` | Daily status across all workstreams |

### Layer 5: Cross-Repo Search (`repos/`)

Symlinks to sibling repos enable Glob and Grep across the entire workspace from one root.

```
repos/
  README.md             ← explains the pattern
  dbt-enterprise/       ← symlink → /Users/.../dbt-enterprise
  data-centered/        ← symlink → /Users/.../data-centered
  dbt-agent/            ← symlink → /Users/.../dbt-agent
```

`.gitignore` excludes `repos/*` (except README.md) so symlinks are local-only.

---

## How Work Flows

### Pipeline building (most common daily task)

```
1. Start in Analytics & Insights Team Workspace
2. /pipeline-new merchant-spend
   → Creates PLAN.md, dot, registry entry
   → Loads: Migration skill, Business Context skill, Canonical Models registry
3. Phase 1-3: Requirements → Discovery → Architecture
   → Skills, agents, and knowledge load from this workspace
   → Data profiling via execute_sql (MCP API, path-independent)
4. Phase 4: Implementation
   → cd to dbt-enterprise for dbt compile/run/test
   → QA with decision traces from this workspace
5. /pipeline-close merchant-spend
   → Extracts learnings back into the knowledge base
```

### Ad-hoc analysis

```
1. /analyze "What's driving the decline in approval rates for Samsung?"
   → Ensemble dispatches 3 analyst agents (statistical, forensic, synthesizer)
   → Each queries via execute_sql
   → Synthesizer merges findings into a data story
```

### Adding team knowledge

```
1. Create knowledge/domains/feature-store/README.md
2. Add patterns, reference docs, decision traces
3. Commit and push — everyone benefits
```

---

## What We Kept From the Original Framework

| Component | Status | Notes |
|-----------|--------|-------|
| Directory structure (`knowledge/`, `repos/`, `scripts/`) | **Kept** | Well-designed for team contributions |
| MCP configuration (dbt Cloud) | **Kept** | Already configured correctly |
| `.gitignore` and repo infrastructure | **Kept** | Properly excludes `repos/*`, credentials |
| Detection/analysis libraries | **Kept** | Generic enough for any warehouse |
| Graniterock agent architecture (9 roles + 15 specialists) | **Archived** | Wrong model for our workflow |
| ADLC commands (`/idea`, `/research`, `/build`) | **Archived** | Replaced by pipeline lifecycle commands |
| Snowflake-specific skills | **Archived** | Replaced by Redshift-native skills |
| CLAUDE.md (Snowflake setup wizard) | **Rewritten** | Now serves as team analytics bootstrap |

---

## Environment

| Component | Technology | Access |
|-----------|-----------|--------|
| Data warehouse | Amazon Redshift | VPN required for dbt CLI; MCP API (`execute_sql`) works without VPN |
| dbt | dbt Cloud + Fusion 2.0 locally | `dbt compile/run/test` in dbt-enterprise |
| Semantic layer | MetricFlow (dbt Core 1.10 `.venv`) | `mf query/validate` only |
| AI models | Claude Opus (domain agents), Claude Sonnet (task agents) | Via Claude Code CLI |
| MCP server | `dbt@dbt-agent-marketplace` | Configured in `.claude/settings.json` |

**VPN split architecture:** MCP API tools (`execute_sql`, `get_related_models`, etc.) work without VPN. dbt CLI tools (`dbt compile`, `dbt run`, `dbt test`) require VPN because they hit Redshift directly.

---

## Migration From dbt-agent

The Analytics & Insights Team Workspace grows by **copying** proven assets from dbt-agent. dbt-agent stays fully intact throughout — nothing is deleted from it.

### Migration principles
1. **Copy-promote, never move-delete** — dbt-agent is the rollback safety net
2. **Capability replacement, not declaration** — workspace is authoritative only for capabilities it actually provides
3. **Ownership metadata** — every copied asset records `source_of_truth` or `mirrored_from`
4. **10-item cutover checklist** — dbt-agent stays authoritative until all 10 are replaced:
   MCP routing, Preflight, QA standards, Skill activation, Pipeline commands, Agent loading, Anti-patterns, Decision traces, Learning loop, Workstream state

### Migration phases
1. **Establish** — symlinks, manifests, bootstrap docs (current)
2. **Inventory** — file-by-file classification of dbt-agent assets
3. **Promote** — copy highest-leverage skills, commands, knowledge
4. **Adapt** — per-repo routing rules and integration metadata
5. **Migrate globals** — analytics-specific commands from `~/.claude/`
6. **Unify state** — shared workstream system
7. **Stabilize** — decide what remains mirrored vs re-owned

---

## Contributing

### Adding domain knowledge (easiest entry point)

1. Create a folder: `knowledge/domains/your-domain/`
2. Add a `README.md` explaining what the domain covers
3. Add patterns, reference docs, decision traces as needed
4. Commit and push

### Adding a skill

1. Create a folder: `.claude/skills/your-skill/`
2. Add a `SKILL.md` with frontmatter (name, description, triggers)
3. See `.claude/skills/SKILLS_REGISTRY.md` for format guidance
4. Add activation keywords to CLAUDE.md's skill activation table

### Adding a command

1. Create a markdown file: `.claude/commands/your-command.md`
2. Define the workflow steps
3. Document the command in CLAUDE.md

---

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Three repos, not one | Keeps production dbt code separate from control plane. Avoids `.claude/` noise in dbt PRs |
| dbt skills in dbt-agent, not dbt-enterprise | Proven separation: brain (dbt-agent) and hands (dbt-enterprise). Mixing them undoes working architecture |
| Two-tier agent model | Simpler than role/specialist trees. Opus for judgment, Sonnet for execution. Research-backed (ALMA, SkillsBench) |
| Copy-promote migration | Zero-risk: source repo stays intact. Can always roll back |
| Domain knowledge folders | Low-friction team contribution. No need to understand agent architecture to add knowledge |
| Global agent memory stays global | Agent identity shouldn't depend on checkout location. Clean residency rule |

---

## Success Criteria

- [ ] A new teammate can start in this workspace and find relevant domain knowledge
- [ ] Pipeline building works end-to-end from this workspace root
- [ ] Cross-repo search finds files in dbt-enterprise and data-centered
- [ ] At least 2 team-contributed domain folders exist (feature store, TPG)
- [ ] Shared skills are accessible without reading dbt-agent directly
- [ ] No degradation in pipeline delivery speed during migration
