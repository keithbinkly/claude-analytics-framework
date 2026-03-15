# CAF Legacy Asset Inventory

Purpose: classify current CAF assets into `keep`, `keep temporarily`, `replace after equivalent exists`, or `archive after replacement exists`.

This document satisfies the CAF-side prerequisite from the migration plan: do not archive legacy CAF content blindly.

## Classification Legend

| Classification | Meaning |
|---|---|
| Keep | Already aligned with the Analytics & Insights Team Workspace direction |
| Keep temporarily | Useful during migration, but may be superseded later |
| Replace after equivalent exists | Legacy asset should be replaced, but only after the new asset is live |
| Archive after replacement exists | Historical/legacy asset that should move out of the active path once replacement is proven |

## Root Bootstrap Files

| Path | Classification | Notes |
|---|---|---|
| `AGENT_ENTRYPOINT.md` | Keep | New agent-neutral bootstrap for all agents |
| `CLAUDE.md` | Keep | Rewritten for CAF workspace model |
| `README.md` | Keep temporarily | Now points toward the new model, but may need another pass as CAF evolves |
| `CONTRIBUTING.md` | Keep | Rewritten for CAF contribution model |

## Manifests

| Path | Classification | Notes |
|---|---|---|
| `.claude/manifests/workspace-manifest.yaml` | Keep | Core routing/topology contract |
| `.claude/manifests/repo-adapters.yaml` | Keep | Core per-repo routing contract |
| `.claude/manifests/workflow-contracts.yaml` | Keep | Agent-neutral workflow contract |
| `.claude/manifests/ccv3-dependencies.yaml` | Keep | Explicit global dependency inventory |

## Current CAF Agents

| Path Group | Classification | Notes |
|---|---|---|
| `.claude/agents/roles/*` | Replace after equivalent exists | Graniterock-era role architecture; do not archive until replacement agent set exists in CAF |
| `.claude/agents/specialists/*` | Replace after equivalent exists | Legacy specialist model; preserve until the workspace-native replacement is in place |
| `.claude/agents/README.md` | Replace after equivalent exists | Still reflects the older architecture |

## Current CAF Commands

| Path Group | Classification | Notes |
|---|---|---|
| `.claude/commands/build.md` | Archive after replacement exists | Legacy ADLC command |
| `.claude/commands/complete.md` | Archive after replacement exists | Legacy ADLC command |
| `.claude/commands/idea.md` | Archive after replacement exists | Legacy ADLC command |
| `.claude/commands/onboard.md` | Archive after replacement exists | Legacy ADLC command |
| `.claude/commands/pause.md` | Keep temporarily | Could still be useful, but not part of the current workspace-first model |
| `.claude/commands/pr.md` | Keep temporarily | Could remain useful even after migration |
| `.claude/commands/push.md` | Keep temporarily | Could remain useful even after migration |
| `.claude/commands/research.md` | Archive after replacement exists | Legacy workflow framing |
| `.claude/commands/setup.md` | Replace after equivalent exists | May be replaced by workspace bootstrap flow |
| `.claude/commands/start.md` | Archive after replacement exists | Legacy ADLC command |
| `.claude/commands/switch.md` | Keep temporarily | Could remain useful if adapted |

## Current CAF Skills

| Path Group | Classification | Notes |
|---|---|---|
| `.claude/skills/project-setup/` | Keep temporarily | Still useful, but likely needs workspace-aware adaptation |
| `.claude/skills/pr-description-generator/` | Keep temporarily | Generic utility, not harmful to keep active |
| `.claude/skills/dbt-model-scaffolder/` | Keep temporarily | Potentially useful, but not aligned with current dbt-enterprise workflow yet |
| `.claude/skills/documentation-validator/` | Keep temporarily | Generic utility skill |
| `.claude/skills/reference-knowledge/` | Replace after equivalent exists | Mixed legacy reference layer, much of it Snowflake/AWS/ADLC-oriented |
| `.claude/skills/workflows/` | Replace after equivalent exists | Legacy workflow automation set |
| `.claude/skills/README.md` | Replace after equivalent exists | Still describes the older skill layer |

## Scripts

| Path | Classification | Notes |
|---|---|---|
| `scripts/bootstrap-linked-repos.sh` | Keep | New local visibility bootstrap |
| `scripts/check-workspace-readiness.sh` | Keep | New CAF readiness check |
| `scripts/validate-mcp.sh` | Keep | Still useful in the workspace model |
| `scripts/setup-submodules.sh` | Keep temporarily | Retain until repo-linking decision is fully settled |
| `scripts/convert-to-submodules.sh` | Keep temporarily | Historical but still relevant to the topology discussion |
| `scripts/pull-all-repos.sh` | Keep temporarily | May still be useful for linked-repo workflows |
| `scripts/resolve-repo-context.py` | Keep temporarily | Still potentially useful if GitHub repo context remains relevant |
| `scripts/get-repo-owner.sh` | Keep temporarily | Same as above |
| `scripts/idea.sh` | Archive after replacement exists | Legacy ADLC workflow |
| `scripts/research.sh` | Archive after replacement exists | Legacy ADLC workflow |
| `scripts/start.sh` | Archive after replacement exists | Legacy ADLC workflow |
| `scripts/finish.sh` | Archive after replacement exists | Legacy ADLC workflow |
| `scripts/switch.sh` | Keep temporarily | May remain useful if adapted |
| `scripts/work-init.sh` | Keep temporarily | Could be repurposed if workspace workstreams survive |
| `scripts/cleanup-internal-refs.sh` | Keep temporarily | Potentially useful during migration cleanup |

## Platform Knowledge

| Path Group | Classification | Notes |
|---|---|---|
| `knowledge/platform/planning/` | Keep | Current source of migration and workspace design truth |
| `knowledge/platform/README.md` | Keep | Rewritten toward current platform docs |
| `knowledge/platform/architecture/` | Archive after replacement exists | Legacy architecture docs; currently not the primary truth layer |
| `knowledge/platform/development/` | Keep temporarily | Mixed legacy content; some items may still be useful during migration |
| `knowledge/platform/mcp-servers/` | Keep temporarily | Mixed relevance; retain until filtered |
| `knowledge/platform/operations/` | Keep temporarily | Some cross-repo docs may still be useful |
| `knowledge/platform/specialists/` | Archive after replacement exists | Tied to legacy agent model |
| `knowledge/platform/training/` | Keep temporarily | May remain useful independent of the old architecture |

## Domain Knowledge

| Path Group | Classification | Notes |
|---|---|---|
| `knowledge/domains/` | Keep | New shared knowledge landing zone for the team |

## Linked Repo Helper Layer

| Path | Classification | Notes |
|---|---|---|
| `repos/README.md` | Keep | Documents the local linked-repo convenience layer |
| `repos/*` symlinks | Keep temporarily | Local-only convenience, not canonical routing |

## Next Actions

1. Use this inventory before archiving any legacy CAF asset.
2. Promote the first high-leverage `dbt-agent` slice into CAF.
3. Only then archive or replace the legacy CAF agent/command/skill assets that become obsolete.
