# Linked Repos

`repos/` is the local visibility layer for linked analytics repos.

These repos are not CAF-owned content. They are separate repositories that CAF needs to coordinate with:

- `dbt-enterprise`
- `dbt-agent`
- `data-centered`

## Purpose

This directory exists to make CAF-root work easier for humans and coding agents by giving them one place to look for linked repositories.

Use it for:

- local symlinks or other local visibility helpers
- bootstrap notes for teammates
- explaining how CAF-root sessions should discover the linked repos

## Important

- Do not assume every teammate will have the same local paths.
- Do not rewrite promoted CAF assets to depend on machine-specific absolute paths.
- If local symlinks are used, they should be treated as convenience infrastructure, not hidden required behavior.

## Canonical Sources Of Truth

Use these files for the authoritative routing model:

- `../AGENT_ENTRYPOINT.md`
- `../.claude/manifests/workspace-manifest.yaml`
- `../.claude/manifests/repo-adapters.yaml`
- `../.claude/manifests/workflow-contracts.yaml`

## Current Linked Repos

The current intended linked repos are:

- `/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise`
- `/Users/kbinkly/git-repos/dbt-agent`
- `/Users/kbinkly/git-repos/data-centered`

Those paths may later be replaced by a more team-safe bootstrap mechanism, but the workflow model stays the same:

- CAF is the shared control plane
- `dbt-enterprise` is the dbt execution target
- `dbt-agent` is the intact migration source and fallback reference
- `data-centered` is the content and visualization project

## Bootstrap

If you want local convenience links from CAF root, use:

```bash
./scripts/bootstrap-linked-repos.sh
```

This creates symlinks for the current local repo locations described in the workspace manifest.

## Notes

- `repos/*` is gitignored except for this README.
- The symlinks are a convenience layer, not the canonical routing model.
- Agents should still use the manifests and repo adapters as the source of truth.

