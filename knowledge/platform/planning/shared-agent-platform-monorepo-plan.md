# Analytics & Insights Team Workspace Plan

**Authors:** Keith + Claude (System Architect)
**Date:** 2026-03-13 (revised from 2026-03-11 draft)
**Status:** Approved for Phase 1 execution. System Architect evaluation complete (3 passes + team fitness assessment).

**Related documents:**
- `system-architect-evaluation.md` — 3-pass architectural review with Builder/QA impact analysis
- `caf-team-fitness-assessment.md` — team readiness evaluation and scorecard
- `ai-team-workspace-spec.md` — full specification for teammates
- `dbt-agent-decomposition-inventory.md` — prerequisite inventory for Phase 3
- `global-to-caf-migration-inventory.md` — classification of `~/.claude/` assets

---

## Summary

`claude-analytics-framework` becomes the **Analytics & Insights Team Workspace** — the shared control plane for the analytics team's AI-assisted work. It is where agents, skills, knowledge, and workflows live so everyone on the team benefits from them.

The intended model is:
- **Analytics & Insights Team Workspace** (this repo) is the shared brain — agents, skills, commands, team knowledge
- **dbt-enterprise** stays intact as the production dbt project — where dbt commands run
- **data-centered** stays intact as the content/visualization project
- **dbt-agent** stays intact as the operational reference — proven skills and knowledge are copied from here into the workspace over time
- Global agent memory remains in `~/.claude/agent-memory/`

### Why this matters
- Reduces agent confusion across multiple roots, manifests, and memory locations
- Makes shared team workflows portable across dbt, notebooks, analysis, and content work
- Gives teammates (data science, TPG) a place to contribute domain knowledge
- Preserves domain depth and operational continuity from dbt-agent

---

## Critical Finding: dbt Execution Decoupling Is Already Solved

The control-plane / execution-target split is **already production-proven**. Every pipeline session today:
1. Loads context from dbt-agent's `.claude/` (skills, commands, rules)
2. Runs dbt CLI commands by `cd`-ing to dbt-enterprise
3. Uses `execute_sql` via MCP API (path-independent)

The Analytics & Insights Team Workspace does not change this relationship. It just moves the control plane up one level. Builder and QA workflows don't change mechanically — they already `cd` to dbt-enterprise for dbt CLI.

| Component | Today | End state | Change? |
|-----------|-------|-----------|---------|
| **Control plane** (skills, commands, rules) | dbt-agent | Analytics & Insights Team Workspace | Yes — promotes up |
| **dbt execution** (`compile/run/test`) | dbt-enterprise (via `cd`) | dbt-enterprise (via `cd`) | **No change** |
| **MCP API** (`execute_sql`) | Path-independent | Path-independent | **No change** |
| **Agent memory** | `~/.claude/agent-memory/` | `~/.claude/agent-memory/` | **No change** |

---

## Design Decisions

### Decision 1: Three repos, not one

dbt skills stay in the workspace (promoted from dbt-agent), **not** in dbt-enterprise. The separation between "where agents think" and "where dbt runs" is proven and working. Mixing `.claude/` config into dbt-enterprise PRs adds noise to model review.

| Repo | Role | Why separate |
|------|------|-------------|
| Analytics & Insights Team Workspace | Shared brain | Changes here improve everyone's workflow |
| dbt-enterprise | Production dbt code | Strict CI/CD, branch protection, team review |
| dbt-agent | Migration source | Battle-tested reference, stays intact |

### Decision 2: Two-tier agent model

Our agent model is **two-tier**: domain agents (Opus, persistent memory, judgment) and task agents (Sonnet, stateless, execution).

This replaces the original framework architecture (9 roles + 15 specialists with confidence-based delegation, built for Snowflake/AWS by Graniterock). The original agent files will be archived.

Domain agents: System Architect, Builder, QA, Analyst, Designer, Context Builder
Task agents: Orchestrator, SQL Builder, Data Discoverer, QA Analyst, Learner, Architect

### Decision 3: Copy-promote migration from dbt-agent

Assets are **copied** from dbt-agent into the workspace. dbt-agent stays fully intact — nothing is deleted from it. Every copied asset carries ownership metadata:
- `source_of_truth: dbt-agent` or `source_of_truth: caf`
- `mirrored_from: dbt-agent`
- `deprecated_copy: true`

### Decision 4: Capability replacement, not declaration

The workspace is authoritative only for capabilities it actually provides. dbt-agent stays authoritative until all 10 capabilities are replaced:

1. MCP tool routing
2. Preflight rules
3. QA standards and templates
4. Skill activation table
5. Pipeline orchestration commands
6. Agent loading specs
7. Anti-pattern enforcement
8. Decision trace lookup
9. Learning loop infrastructure
10. Workstream state management

### Decision 5: Global agent memory stays global

`~/.claude/agent-memory/` remains canonical for global agents (System Architect, Designer). Agent identity shouldn't depend on checkout location.

### Decision 6: Native placement, not shadow structure

Promoted assets go into their natural locations (`knowledge/domains/dbt/`, `.claude/skills/`, `.claude/commands/`), **not** into a `promoted/dbt-agent/` shadow directory. Ownership metadata tracks provenance.

### Decision 7: Gitignored nested repos (supersedes symlinks)

Team repos are cloned directly inside the workspace directory and gitignored. Each repo keeps its own `.git/`, branches, remotes, and CI/CD — the workspace git never sees them. This gives every teammate identical relative paths with zero configuration. No symlinks, no bootstrap script, no hardcoded personal paths.

Full plan: `nested-repos-restructure.md`

### Decision 8: Compound routing for pipeline work

Pipeline building is the most common daily task and requires both repos:
- **dbt-enterprise** as execution target (where dbt commands run)
- **dbt-agent** (later: workspace) as skill/knowledge reference

This is the existing proven pattern, made explicit in routing rules.

---

## Target Topology

```text
Analytics & Insights Team Workspace (claude-analytics-framework)/
  .claude/
    agents/                  # two-tier agent definitions (replaces Graniterock roles/specialists)
    skills/                  # promoted from dbt-agent + team-contributed
    commands/                # pipeline lifecycle + analysis + coordination
    rules/                   # always-on operating rules
    manifests/               # workspace, repo adapters, agent inventory
  knowledge/
    platform/
      planning/              # migration plans, evaluations (this folder)
      operations/            # team operating model, runbooks
      training/              # onboarding, how-tos
    domains/
      dbt-pipelines/         # canonical models, migration patterns, QA methodology
      feature-store/         # [team-contributed] feature engineering, ML pipelines
      tpg-pipelines/         # [team-contributed] TPG-specific patterns
      semantic-layer/        # MetricFlow, metrics, saved queries
      redshift/              # optimization patterns, table design
      data-storytelling/     # visualization patterns, dashboard templates
    reference/
      tools/                 # MCP setup, dbt CLI, external tool guides
      standards/             # SQL style, naming conventions, folder structure
  dbt-enterprise/              # full repo clone (gitignored, own .git/)
  dbt-agent/                   # full repo clone (gitignored, own .git/)
  data-centered/               # full repo clone (gitignored, own .git/)
  workstreams/
    active/
    archive/
  telemetry/
    chatops/
    learning/
  scripts/
  templates/

Global layer retained:
  ~/.claude/agent-memory/    # canonical memory for truly global agents
```

---

## Repository Roles

### Analytics & Insights Team Workspace (this repo)
Shared control plane and team knowledge hub:
- Agent definitions (two-tier model)
- Shared skills (promoted from dbt-agent + team-contributed)
- Pipeline lifecycle and analysis commands
- Team domain knowledge (dbt, feature store, TPG, semantic layer)
- Cross-repo coordination and workstream state
- Learning loop and telemetry patterns

### dbt-agent
Stays intact as operational reference and migration source:
- Battle-tested skills and knowledge base (source for copy-promote)
- Enterprise-specific dbt operating knowledge
- Current workflows remain usable throughout migration
- Authority shrinks only as workspace replaces specific capabilities

### dbt-enterprise
Stays intact as production dbt project:
- dbt models, YAML, tests, seeds, project configs
- Accessed via dbt Cloud and `cd` from workspace
- No `.claude/` config mixed into production code

### data-centered
Stays intact as content/visualization project:
- Site, articles, visualizations, showcase
- Consumes the shared platform but does not define it

### ~/.claude
Retains the truly global layer:
- Global agent memory for agents invoked from 2+ repos
- Universal non-analytics helpers
- Editor/runtime preferences

---

## Workspace Fitness: What We Keep vs Replace

The original repo was built by Dylan Morrish at Graniterock for a Snowflake/AWS stack. Our environment is Redshift/dbt Cloud.

| Component | Action | Notes |
|-----------|--------|-------|
| Directory structure | **Keep** | `knowledge/` hierarchy well-designed |
| `repos/` symlink infrastructure | **Keep** | Ready for cross-repo search |
| MCP configuration | **Keep** | dbt Cloud MCP already correct |
| Detection/analysis libraries | **Keep** | Generic, warehouse-agnostic |
| Agent architecture (9 roles + 15 specialists) | **Archive** | Replace with two-tier model |
| ADLC commands (`/idea`, `/research`, `/build`) | **Archive** | Replace with pipeline lifecycle |
| Snowflake-specific skills | **Archive** | Replace with Redshift-native skills |
| CLAUDE.md | **Rewrite** | Team analytics bootstrap, not Snowflake setup |

---

## Migration Phases

### Phase 1: Establish the workspace (current)
- Create symlinks in `repos/` for cross-repo search
- Archive Graniterock agent/command/skill files
- Create `knowledge/domains/` skeleton with README templates
- Update manifests and bootstrap docs
- Write contribution guide for teammates

**Output:** One obvious starting place. Teammates can browse and contribute knowledge.

### Phase 2: Inventory dbt-agent assets
- File-by-file classification of `dbt-agent/.claude/`, `shared/`, `tools/`
- Classify each as: Promote / Keep in dbt-domain / Archive / Already duplicated
- Determine target location and ownership for each promoted asset

**Output:** Concrete input list for Phase 3.

### Phase 3: Promote highest-leverage content
- Copy skills, commands, knowledge into native workspace locations
- Each copied asset carries ownership metadata
- Prioritize: assets teammates can immediately use, assets that improve workspace bootstrapping

**Output:** Workspace has useful capabilities without breaking dbt-agent.

### Phase 4: Add project adapters
- Per-repo routing rules and integration metadata
- Add compound routing rule for pipeline building (dbt-enterprise + dbt-agent reference)
- Define safe commands, environment constraints, local vs shared assets per repo

**Output:** Agents route correctly across repos.

### Phase 5: Migrate analytics globals from ~/.claude
- Analytics-specific commands (system-architect, designer, load/save, visual-explainer)
- Analytics-specific skills
- Keep global agent memory global

**Output:** Analytics platform logic in workspace, not scattered in home directory.

### Phase 6: Unify live state
- Shared workstream system in workspace
- Local repos keep local artifacts, indexed centrally
- Cross-repo session continuity

**Output:** Cross-repo work stops feeling like context teleportation.

### Phase 7: Stabilize ownership
- Decide what remains mirrored vs re-owned
- Shrink dbt-agent authority only where workspace has full replacement
- Keep historical/reference value available in dbt-agent

---

## Environment

| Component | Technology | Notes |
|-----------|-----------|-------|
| Data warehouse | Amazon Redshift | VPN for CLI, MCP API works without |
| dbt | dbt Cloud + Fusion 2.0 locally | CLI runs in dbt-enterprise |
| Semantic layer | MetricFlow (Core 1.10 `.venv`) | `mf query/validate` only |
| AI models | Opus (domain agents), Sonnet (task agents) | Never Haiku |
| MCP server | `dbt@dbt-agent-marketplace` | Already configured |

---

## Success Criteria

- [ ] A new teammate can start in this workspace and find relevant domain knowledge
- [ ] Pipeline building works end-to-end from workspace root
- [ ] Cross-repo search finds files in dbt-enterprise and data-centered
- [ ] At least 2 team-contributed domain folders exist (feature store, TPG)
- [ ] Shared skills are accessible without reading dbt-agent directly
- [ ] No degradation in pipeline delivery speed during migration
- [ ] Ownership of promoted assets is explicit (no silent drift)
- [ ] dbt-agent remains fully usable throughout
- [ ] Global memory residency stays clean

---

## Bottom Line

The Analytics & Insights Team Workspace is the shared brain for the analytics team. dbt-enterprise is the hands. dbt-agent is the proven reference we copy from. The separation between thinking and executing is already production-proven — this plan just moves the thinking layer up one level so the whole team can share it.
