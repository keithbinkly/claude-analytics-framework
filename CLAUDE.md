don't look at the full .env file. Only search for the var names up to the equals sign.

# Claude Analytics Framework

CAF is the shared analytics control plane and planned team entrypoint. It coordinates shared workflow docs, manifests, commands, skills, and team knowledge across linked repos while preserving `dbt-enterprise` as the execution target and `dbt-agent` as the intact migration source/reference.

## Read First

For a fresh session, read these in order:

1. `AGENT_ENTRYPOINT.md`
2. `README.md`
3. `CLAUDE.md`
4. `.claude/manifests/workspace-manifest.yaml`
5. `.claude/manifests/repo-adapters.yaml`
6. `.claude/manifests/workflow-contracts.yaml`
7. `.claude/manifests/ccv3-dependencies.yaml`
8. `knowledge/platform/planning/shared-agent-platform-monorepo-plan.md`

If you are not Claude or do not support slash commands/skills natively, start with `AGENT_ENTRYPOINT.md`.

## Workspace Model

CAF coordinates four important locations:

1. `claude-analytics-framework`
   Shared control plane, team knowledge, migration planning, promoted shared assets.

2. `dbt-enterprise`
   Production dbt project. This is where dbt CLI commands run.

3. `dbt-agent`
   Current operational reference and migration source. It remains fully usable while assets are copied into CAF over time.

4. `data-centered`
   Content and visualization project.

## Critical Rules

### dbt Execution

- Do not run dbt CLI from CAF root.
- Route dbt execution into `dbt-enterprise`.
- Use CAF for control-plane context and promoted shared assets.
- Use `dbt-agent` as fallback reference until CAF has replaced the needed capability.

### Migration Safety

- `dbt-agent` remains fully usable throughout migration.
- Prefer copy-promote over move-delete.
- Do not archive legacy CAF assets until working replacements exist.
- Do not hide unresolved dependencies behind machine-specific absolute paths.
- Every promoted asset should declare ownership metadata and CCV3/global dependency metadata.

### Global Layer

- Global agent memory remains in `~/.claude/agent-memory/`.
- Analytics-specific global dependencies must be explicit in `.claude/manifests/ccv3-dependencies.yaml`.
- No promoted CAF asset should rely on undocumented `~/.claude` behavior.

## How To Route Work

Use `.claude/manifests/repo-adapters.yaml` as the routing contract.

- Shared platform behavior, manifests, team knowledge, workflow design:
  Stay in CAF.

- dbt models, project-local dbt QA, dbt execution, production dbt constraints:
  Route into `dbt-enterprise`.

- Not-yet-promoted commands, skills, reference behavior, legacy shared workflows:
  Consult `dbt-agent`.

- Publishing, storytelling, visualization product work:
  Route into `data-centered`.

## Core Workflow References

Use these files for the canonical workflow definitions:

- Agent-neutral bootstrap: `AGENT_ENTRYPOINT.md`
- Machine-readable workflows: `.claude/manifests/workflow-contracts.yaml`
- Workspace topology and policy: `.claude/manifests/workspace-manifest.yaml`
- Repo routing: `.claude/manifests/repo-adapters.yaml`
- Global dependency declarations: `.claude/manifests/ccv3-dependencies.yaml`

## MCP

dbt Cloud MCP remains important for this workspace.

Suggested setup flow:

```bash
cp .env.example .env
./scripts/validate-mcp.sh
```

After changing MCP configuration, restart Claude Code before expecting the MCP server list to refresh.

## Team Contribution

Shared team-facing knowledge belongs in CAF, especially under:

- `knowledge/domains/`
- `knowledge/platform/`
- `.claude/manifests/`
- promoted shared commands and skills in `.claude/`

Project-local delivery code does not belong in CAF. Keep:

- dbt models/tests/YAML in `dbt-enterprise`
- content/site product code in `data-centered`
- historical and migration-source reference content in `dbt-agent`

See `CONTRIBUTING.md` for the contribution model.

## Current Status

CAF is the planned team entrypoint, but not every capability has been re-homed yet. Use CAF first, then consult `dbt-agent` where the promoted replacement does not yet exist.
