# Shared Agent Platform Monorepo Plan

**Authors:** Keith + Claude  
**Date:** 2026-03-11  
**Status:** Draft  

## Summary
`claude-analytics-framework` should become the top-level shared agent platform for the workspace. It is the right long-term canonical root, but it has not earned that status yet.

The intended model is:
- `dbt-enterprise` stays intact as its own repo/project and may later live inside CAF, but physical nesting is not required for the control-plane migration
- `data-centered` stays intact as its own repo/project and may later live inside CAF, but physical nesting is not required for the control-plane migration
- `dbt-agent` is the one repo whose reusable contents get absorbed into CAF over time
- analytics-specific global commands, manifests, and selected skills are brought down into CAF
- truly global agent memory remains in `~/.claude/agent-memory/`

The core move is to centralize the agentic control plane here: agents, skills, commands, workstream state, team memory patterns, and platform docs. This gives agents one canonical home while preserving current delivery workflows for the production dbt project and the content/site project.

This design matters because it:
- Reduces agent confusion across multiple roots, manifests, and memory locations
- Makes shared team workflows portable across dbt, notebooks, analysis projects, and content work
- Preserves domain depth from `dbt-agent` while moving the reusable platform up a level
- Avoids high-risk git/process changes in production repos until the platform layer is stable

## Scope
### In Scope
- Define `claude-analytics-framework` as the canonical agent platform root
- Define the target folder and ownership model
- Identify what moves from `dbt-agent` first
- Define how `dbt-enterprise` and `data-centered` participate in the CAF workspace while remaining intact
- Define what should migrate from `~/.claude/` into CAF
- Provide a phased migration and cutover plan

### Out of Scope
- Extracting `dbt-enterprise` contents out of its existing project structure
- Extracting `data-centered` contents out of its existing project structure
- Moving truly universal non-analytics personal tooling into CAF
- Rewriting all existing commands or agents in one pass
- Production dbt workflow changes inside dbt Cloud IDE
- Immediate deprecation of existing repos

## Design Overview
### Recommendation
Adopt a **CAF-centered shared control plane** model:

- One platform monorepo: `claude-analytics-framework`
- `dbt-enterprise` remains an intact production project, referenced through CAF manifests and adapters
- `data-centered` remains an intact content/product project, referenced through CAF manifests and adapters
- `dbt-agent` is progressively decomposed and absorbed into CAF
- analytics-specific commands, manifests, and selected skills currently living in `~/.claude/` are progressively relocated into CAF
- truly global memory remains in `~/.claude/agent-memory/`
- Shared control plane lives in CAF

### Why this shape
Today the workspace already behaves like a monorepo from the agent's perspective, but without monorepo clarity. Agents must infer:
- which manifest is canonical
- where global vs local memory lives
- which commands are shared
- where workstream state belongs
- whether analytics behavior lives in CAF, `dbt-agent`, `data-centered`, or `~/.claude`

The fix is not "put every file together immediately." The fix is "make one repo the canonical operating system."

## Target Topology
```text
claude-analytics-framework/
  .claude/
    agents/                  # shared/global agents
    skills/                  # shared/platform skills
    commands/                # shared slash commands
    rules/                   # always-on operating rules
    manifests/               # agent, skill, repo, workspace manifests
  knowledge/
    platform/                # operating model, planning, ops, training
    domains/
      dbt/                   # reusable dbt/domain guidance promoted from dbt-agent
      analytics/             # notebooks, analysis patterns, experiments
      storytelling/          # presentation, dashboard, article patterns
  workstreams/
    active/
    archive/
  telemetry/
    chatops/
    learning/
  domains/
    dbt-agent/               # temporary migration landing area while content is absorbed
  projects/
    notebooks/
    analyses/
    prototypes/
  templates/
  scripts/

External but workspace-linked repos:
  /Users/kbinkly/git-repos/dbt_projects/dbt-enterprise
  /Users/kbinkly/git-repos/data-centered
  /Users/kbinkly/git-repos/dbt-agent

Global layer retained:
  ~/.claude/agent-memory/    # canonical memory for truly global agents
```

## Repository Roles After Migration
### `claude-analytics-framework`
Becomes the shared team repo and canonical control plane:
- agent manifests
- shared commands
- shared skills
- analytics-domain commands and manifests that currently live in `~/.claude/`
- workstream state
- team documentation
- cross-repo coordination
- reusable analytics/dbt/notebook patterns

### `dbt-agent`
Is the primary source repo for migration into CAF:
- reusable agentic content is promoted into CAF
- dbt-specific domain knowledge is split into either shared platform content or retained dbt-domain content
- over time, this repo stops being the primary control plane
- eventually it may remain only as an archive, a source reference, or a much smaller dbt-domain package

### `data-centered`
Remains intact as its own project:
- site, articles, visualizations, showcase work
- consumes the shared platform, but does not define it
- keeps its own project structure and delivery concerns

### `dbt-enterprise`
Remains intact as the production delivery project:
- dbt models, YAML, tests, seeds, project configs
- accessed through dbt Cloud and controlled workflows
- is not unpacked or absorbed into CAF content-wise
- remains the operational dbt project while CAF becomes the control-plane root

### `~/.claude`
Retains the truly global layer:
- global agent memory for agents invoked from 2+ repos
- universal non-analytics helpers
- editor/runtime preferences
- generic experimentation not owned by the analytics platform

CAF should absorb analytics-specific operating assets, but not break the clean residency rule for global memory.

## Key Design Decisions
### Decision 1: Shared root, selective absorption
**Recommendation:** Make CAF the shared control plane, absorb `dbt-agent` content over time, and pull analytics-specific global commands/manifests into CAF.

Why:
- fastest relief for current agent-navigation pain
- lowest operational risk
- preserves dbt Cloud workflow expectations
- preserves `data-centered` and `dbt-enterprise` as intact projects
- focuses migration effort on the repo that is actually duplicating the platform role
- removes ambiguity between "global analytics platform" and "repo-local analytics platform"

### Decision 2: Move reusable agentic content up, keep delivery projects intact
**Promote to framework now:**
- shared manifests and bootstrap docs
- shared slash-command patterns
- workstream load/save model
- cross-repo memory/residency rules
- learning-loop and telemetry patterns
- notebook and analysis project scaffolds
- generic dbt skills that are team-reusable
- analytics-related global commands from `~/.claude/commands/`
- analytics-related global manifest logic from `~/.claude/AGENTS.md`
- analytics-related global skills from `~/.claude/skills/`

**Keep in intact project folders:**
- `dbt-enterprise` delivery code and dbt configs
- `data-centered` site/content files
- project-specific handoffs and active artifacts where local ownership matters
- warehouse/domain-specific troubleshooting tied tightly to one production environment

### Decision 3: Repo boundaries must still be explicit inside CAF
Even once these projects live under CAF, agents still need a manifest that says:
- this path is a production dbt project
- this path is a content/site project
- this path is shared platform infrastructure
- this path is legacy material still being migrated
- this path used to be global but is now CAF-owned analytics infrastructure

Do not rely on folder names alone.

### Decision 4: Keep global agent memory global
**Recommendation:** Keep `~/.claude/agent-memory/` as the canonical location for global agent memory.

Why:
- it preserves the clean residency rule
- it avoids coupling agent identity to CAF checkout location
- it matches the current architecture decision already encoded in the global manifest

CAF should reference global memory explicitly through manifests and commands rather than relocating it.

### Decision 5: CAF becomes canonical by capability replacement, not declaration
**Recommendation:** CAF is a planned canonical root until it can replace dbt-agent's operational depth.

`dbt-agent` remains authoritative for dbt-agent-specific operations until CAF has equivalent coverage for:
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

Move into CAF when the asset is:
- analytics-team specific
- used across the CAF/dbt/data-centered workspace
- part of the shared operating model
- something another analytics teammate would need

Leave in `~/.claude` when the asset is:
- personal rather than team/platform level
- broadly generic across unrelated domains
- not meaningfully part of the analytics operating system

## Migration Phases
### Phase 1: Establish the control plane
Move or recreate in `claude-analytics-framework`:
- canonical bootstrap docs
- global agent manifest
- workspace/repo manifest
- shared workstream model
- shared command inventory
- inventory of analytics-related assets currently living in `~/.claude/`
- capability cutover checklist against `dbt-agent`

Output:
- one obvious starting place for any agent

### Phase 2: Create the `dbt-agent` decomposition inventory
Create a file-by-file inventory of `dbt-agent/.claude/`, `docs/`, `shared/`, and related control-plane assets.

Classify each asset as:
- Promote to CAF
- Keep in dbt-domain
- Archive
- Already duplicated

Output:
- realistic scope for the actual migration

### Phase 3: Extract reusable content from `dbt-agent`
Promote:
- cross-repo agent memory standards
- general planning and learning-loop patterns
- reusable dbt scaffolding and workflow skills
- agent residency and coordination docs

Keep in `dbt-agent`:
- enterprise-specific dbt operating knowledge
- Redshift-specific troubleshooting and QA depth

Output:
- CAF becomes the primary platform
- `dbt-agent` becomes a migration source rather than a parallel operating system

### Phase 4: Add project adapters
Create per-project integration metadata for:
- `dbt-enterprise`
- `data-centered`
- notebooks / analysis repos
- migrated former-global analytics agents/commands/skills

Each adapter should define:
- repo role
- safe commands
- environment constraints
- where local memory/state lives
- when to use shared vs local skills

Output:
- agents can work across repos without guessing

### Phase 5: Migrate analytics assets from `~/.claude`
Move into CAF:
- analytics-specific global agents such as `system-architect` and `designer` if they are part of the shared analytics platform
- analytics-specific commands such as cross-repo load/save, design-for-analytics commands, and platform recap commands
- analytics-specific supporting docs
- analytics-specific reusable skills

Classify each current global asset as one of:
- move to CAF
- duplicate temporarily and deprecate global copy
- keep global because it is truly universal

Keep global:
- canonical memory for global agents

Output:
- analytics platform command and manifest logic lives in CAF without breaking global memory residency

### Phase 6: Unify live state
Move toward one shared workstream system in `claude-analytics-framework`:
- active workstreams
- project links
- session continuity
- cross-repo tasks

Allow local repos to keep local artifacts, but index them centrally.

Output:
- cross-repo work stops feeling like context teleportation

### Phase 7: Finalize `dbt-agent` absorption
After the platform is stable:
- retire duplicated platform docs from `dbt-agent`
- keep only what still needs to exist as a dbt-domain source or archive
- move canonical agentic content fully into CAF
- shrink `dbt-agent` authority only as CAF replaces specific capabilities

## Proposed Cutover Order
1. Declare `claude-analytics-framework` the canonical platform root
2. Create workspace and repo manifests there
3. Inventory analytics-specific assets in `~/.claude/`
4. Create the `dbt-agent` decomposition inventory
5. Mirror/import the best reusable docs from `dbt-agent`
6. Move analytics-specific global commands, manifests, and selected skills into CAF
7. Update repo bootstraps to point back to framework-first docs
8. Introduce central workstream state
9. Continue `dbt-agent` content absorption only as CAF replaces concrete capabilities

## Success Criteria
- A new agent can bootstrap from CAF without hunting across multiple workspace roots
- Shared commands and skills have one canonical source
- Cross-repo tasks use one workstream/state model
- `dbt-agent` is no longer a parallel platform once CAF has equivalent operational depth
- `dbt-enterprise` remains productive and low-risk during the transition
- `data-centered` remains intact while benefiting from the shared platform
- analytics-specific command and manifest logic no longer depends on `~/.claude` as a primary source of truth
- global memory residency remains clean and consistent

## Bottom Line
Yes, a CAF-centered platform model better suits agents here, but the value comes from consolidating the analytics control plane, not from physically nesting repos. `dbt-enterprise` and `data-centered` can remain intact as linked workspace repos, `dbt-agent` can be decomposed and absorbed over time, and analytics-specific global command/manifest logic can move into CAF while truly global agent memory stays in `~/.claude`.
