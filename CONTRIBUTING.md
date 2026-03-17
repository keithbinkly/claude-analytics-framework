# Contributing to analytics-workspace

analytics-workspace is the shared analytics control plane. Contribute here when the change improves team-shared workflows, manifests, knowledge, commands, or skills across repos. Keep delivery code in its owning repo.

## What Belongs Where

### Put it in analytics-workspace when it is:

- shared team knowledge
- workflow documentation
- manifests and routing metadata
- shared commands or skills
- migration planning
- cross-repo coordination logic
- team-contributed patterns that should outlive one project

### Put it in `dbt-enterprise` when it is:

- dbt models
- schema YAML
- tests
- seeds
- project-local dbt docs and runbooks
- anything that should ship with the production dbt project

### Put it in `dbt-agent` when it is:

- still the current reference source during migration
- historical or operational content that has not yet been promoted into analytics-workspace
- deeper dbt-agent-native logic you are consulting but not yet re-homing

### Put it in `data-centered` when it is:

- articles
- site code
- visualization product work
- storytelling deliverables

## Common Contribution Types

### Shared knowledge

Add team-facing reference material under `knowledge/`, especially:

- `knowledge/domains/`
- `knowledge/platform/`

Use domain folders for reusable knowledge. Do not create shared reference content inside `dbt-enterprise` just because a pipeline happened to need it first.

### Shared commands and skills

Add or update:

- `.claude/commands/`
- `.claude/skills/`
- `.claude/manifests/`

These are shared control-plane assets. They should be understandable from workspace root and should not assume undocumented local setup.

### Migration copy-promote work

When copying an asset from `dbt-agent` into analytics-workspace:

1. Keep `dbt-agent` intact.
2. Add ownership metadata.
3. Add CCV3/global dependency metadata if the asset depends on `~/.claude` or another external layer.
4. Prefer natural analytics-workspace destinations over shadow folders.

Allowed ownership labels:

- `source_of_truth: dbt-agent`
- `source_of_truth: analytics-workspace`
- `mirrored_from: dbt-agent`
- `deprecated_copy: true`

Dependency declarations belong in:

- `.claude/manifests/ccv3-dependencies.yaml`

## How To Start

```bash
git checkout -b feature/your-change
```

Make the smallest useful change that improves analytics-workspace as the shared team entrypoint.

If your change affects workflow routing, also update the relevant manifest or planning doc.

## Linked Repos

analytics-workspace often needs visibility into linked repos. Read:

- `AGENT_ENTRYPOINT.md`
- `.claude/manifests/workspace-manifest.yaml`
- `.claude/manifests/repo-adapters.yaml`
- `repos/README.md`

Do not hardcode machine-specific absolute paths into promoted assets just to make them work locally.

## Pull Request Expectations

Before opening a PR:

- confirm the change belongs in analytics-workspace
- update docs if behavior changed
- update manifests if routing or dependencies changed
- preserve `dbt-agent` usability if doing migration work
- avoid introducing hidden global-layer dependencies

PR description should cover:

- what changed
- why it belongs in analytics-workspace
- whether it affects analytics-workspace only or linked repos too
- how you verified it

## Commit Style

Use conventional commit style when practical:

```text
feat: add agent-neutral workflow contracts
docs: rewrite workspace bootstrap docs for team workspace
chore: add CCV3 dependency manifest
```

## Current Priority

The current migration priority is:

1. make analytics-workspace readable and usable from root
2. support non-Claude agents as first-class readers
3. promote the highest-leverage `dbt-agent` assets by copy
4. archive legacy analytics-workspace content only after replacements exist
