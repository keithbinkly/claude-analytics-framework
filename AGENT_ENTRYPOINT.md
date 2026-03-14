# Agent Entrypoint

Tool-agnostic bootstrap for coding agents working in `claude-analytics-framework`.

This file is for agents that do not use Claude-specific slash commands, skills, or memory conventions as their primary interface. Read this first if you are starting from the CAF root and need to understand how to navigate the workspace safely.

## What This Workspace Is

`claude-analytics-framework` is the shared analytics control plane. It is the team-facing root for:
- shared workflow docs
- shared manifests
- shared commands and skills as they are promoted into CAF
- cross-repo coordination
- team-contributed domain knowledge

It is not the production dbt project itself.

## The Three Linked Repos

This workspace coordinates three linked repositories:

1. `claude-analytics-framework`
   The shared control plane and team entrypoint.

2. `dbt-enterprise`
   The production dbt project. This is where dbt CLI commands run.

3. `dbt-agent`
   The current operational reference and migration source. It stays intact while useful assets are copied into CAF over time.

There is also `data-centered`, which is the content and visualization project.

## Read Order

For a fresh session, read these in order:

1. `AGENT_ENTRYPOINT.md`
2. `README.md`
3. `CLAUDE.md`
4. `.claude/manifests/workspace-manifest.yaml`
5. `.claude/manifests/repo-adapters.yaml`
6. `.claude/manifests/workflow-contracts.yaml`
7. `.claude/manifests/pipeline-state-schema.yaml`
8. `.claude/manifests/ccv3-dependencies.yaml`
9. `knowledge/platform/planning/shared-agent-platform-monorepo-plan.md`

If you want local convenience links for the linked repos, run:

```bash
./scripts/bootstrap-linked-repos.sh
```

## Canonical Routing

Use these rules unless a more specific local repo rule overrides them:

- If the task is about shared platform behavior, manifests, shared knowledge, or cross-repo coordination, stay in CAF.
- If the task is about dbt models, dbt QA, or dbt project behavior, route into `dbt-enterprise`.
- If the task is about reference workflows, legacy shared logic, or not-yet-promoted analytics agent behavior, consult `dbt-agent`.
- If the task is about publishing, storytelling, or visualization product work, route into `data-centered`.

## Critical Constraint

For dbt pipeline work:
- use CAF for control-plane context
- use `dbt-enterprise` for dbt CLI execution
- use `dbt-agent` as fallback reference until CAF has replaced the needed capability

Do not assume dbt commands run from CAF root.

## Current Migration Model

The migration is non-destructive:
- `dbt-agent` remains fully usable
- assets are promoted into CAF by copy
- promoted assets should declare ownership metadata
- promoted assets should declare CCV3/global dependencies explicitly

CAF is the planned team entrypoint, but not every capability has been re-homed yet.

## Current State Locations

Look in these places for active state:

- CAF shared state:
  - `workstreams/active`
  - `workstreams/archive`
  - `knowledge/platform`
  - `.claude/manifests/`

- `dbt-agent` state:
  - `handoffs/`
  - `.dots/` if a pipeline-specific dot exists
  - `.claude/`
  - `shared/`

For pipeline lifecycle state during migration, prefer:

- `dbt-agent/handoffs/PIPELINE_REGISTRY.yaml`
- `dbt-agent/handoffs/[pipeline]/PLAN.md`

Treat `dbt-agent/.dots/pipeline-[name].md` as optional auxiliary state, not guaranteed state.

- `dbt-enterprise` state:
  - local project docs
  - `models/`
  - `tests/`
  - `analyses/`

If local convenience symlinks exist, they will appear under `repos/`.

## How To Perform Common Workflows

Use `.claude/manifests/workflow-contracts.yaml` for the machine-readable version. In plain terms:

### Build or resume a dbt pipeline
- read CAF manifests and planning docs
- consult CAF dbt references under:
  - `knowledge/domains/dbt-pipelines/reference/`
  - `knowledge/reference/standards/`
  - `knowledge/reference/tools/`
  - `.claude/skills/dbt-tech-spec-writer/`
  - `.claude/skills/dbt-preflight/`
  - `.claude/skills/dbt-migration/`
  - `.claude/skills/dbt-fundamentals/`
  - `.claude/skills/dbt-lineage/`
  - `.claude/skills/dbt-sql-unit-testing/`
  - `.claude/skills/sql-hidden-gems/`
- consult promoted CAF assets if available
- consult `dbt-agent` if the capability is not yet promoted
- run dbt CLI from `dbt-enterprise`

### Run QA on a dbt model
- locate QA workflow guidance in CAF under `knowledge/domains/dbt-pipelines/reference/qa-validation-checklist.md`
- use CAF troubleshooting and reusable-rule guidance under:
  - `knowledge/domains/dbt-pipelines/reference/troubleshooting.md`
  - `knowledge/domains/dbt-pipelines/decision-traces/rules.json`
- use `knowledge/reference/tools/dbt-mcp-tools-reference.md` for tool routing
- inspect the target model in `dbt-enterprise`
- apply project-local dbt constraints from `dbt-enterprise`

### Contribute shared team knowledge
- add or update content in CAF under `knowledge/domains/`
- do not modify `dbt-enterprise` just to add shared reference material

### Investigate cross-repo workflow behavior
- start in CAF manifests
- then route into the relevant repo using `.claude/manifests/repo-adapters.yaml`

## Non-Claude Agents

If you do not support Claude slash commands or Claude skill loading:
- treat `.claude/commands/*.md` as workflow docs, not executable primitives
- treat `.claude/skills/*/SKILL.md` as SOP/reference material
- rely on the manifests and this file for routing decisions
- prefer machine-readable manifests over Claude-specific conventions

## Do Not Assume

- Do not assume `~/.claude` is your primary interface.
- Do not assume all useful workflows are already promoted into CAF.
- Do not assume machine-specific absolute paths are portable.
- Do not assume a CAF asset is team-ready unless its dependencies are explicit.

## Immediate Goal

A non-Claude coding agent should be able to:
- understand the workspace structure
- route to the correct repo
- identify the correct files to read
- perform core dbt workflow navigation without depending on Claude-only runtime features
