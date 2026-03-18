# Platform Documentation

This directory contains analytics-workspace platform documentation for the shared analytics control plane. During the migration, the most important material lives in planning docs and manifests rather than the older ADLC-oriented structure.

## Start Here

Read these first:

1. `../../AGENT_ENTRYPOINT.md`
2. `../../CLAUDE.md`
3. `../../.claude/manifests/workspace-manifest.yaml`
4. `../../.claude/manifests/repo-adapters.yaml`
5. `../../.claude/manifests/workflow-contracts.yaml`
6. `../../.claude/manifests/ccv3-dependencies.yaml`
7. `planning/shared-agent-platform-monorepo-plan.md`

## Current Planning Docs

- `planning/shared-agent-platform-monorepo-plan.md`
- `planning/ai-team-workspace-spec.md`
- `planning/system-architect-evaluation.md`
- `planning/caf-team-fitness-assessment.md`
- `planning/dbt-agent-decomposition-inventory.md`
- `planning/global-to-caf-migration-inventory.md`
- `planning/README.md`

## Related Manifests

- `../../.claude/manifests/workspace-manifest.yaml`
- `../../.claude/manifests/repo-adapters.yaml`
- `../../.claude/manifests/workflow-contracts.yaml`
- `../../.claude/manifests/ccv3-dependencies.yaml`

## What This Section Is For

Use `knowledge/platform/` for:

- migration planning
- workspace operating model
- shared control-plane documentation
- team-facing runbooks that apply across repos

Do not use this folder for:

- project-local dbt delivery docs that belong in `dbt-enterprise`
- historical reference content that still belongs only in `dbt-agent`

## Migration Note

This repo is being repurposed from an older analytics-workspace/Graniterock framing into the Analytics & Insights Team Workspace model.

That means:

- planning docs and manifests are currently the most trustworthy layer
- some older docs in sibling sections may still reflect the legacy architecture
- legacy content should be archived only after replacement assets exist and are verified