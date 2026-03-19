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

## Common Contribution Types

### Shared knowledge

Add team-facing reference material under `knowledge/`, especially:

- `knowledge/domains/`
- `knowledge/platform/`

Use domain folders for reusable knowledge. Do not create shared reference content inside `dbt-enterprise` just because a pipeline happened to need it first.

### When you learn something

The test: **did you solve a problem or learn something that a teammate could use when they hit something similar?** If yes, commit it. If it's just a personal preference or a one-off note, keep it local.

| What you learned | Where it goes | Example |
|-----------------|--------------|---------|
| A fact about our data | `knowledge/domains/<domain>/reference/` | "ODS posted_transaction has BaaS + Legacy" |
| A pattern that works | `knowledge/domains/<domain>/patterns/` | "Use delete+insert for composite keys on Redshift" |
| A decision with rationale | `knowledge/domains/<domain>/decisions/` | "Why we exclude POS mode X from this pipeline" |
| A QA resolution | `knowledge/domains/dbt-pipelines/decision-traces/` | "Amount inflation caused by merge strategy at month boundaries" |
| An agent anti-pattern | `.claude/agent-memory/<agent>/napkin.md` | "Don't trust row counts as QA validation" |

Don't overthink the format. A few sentences with context is better than nothing. The knowledge graph and agents will find it.

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
3. Add global-layer dependency metadata if the asset depends on `~/.claude` or another external layer.
4. Prefer natural analytics-workspace destinations over shadow folders.

Allowed ownership labels:

- `source_of_truth: dbt-agent`
- `source_of_truth: analytics-workspace`
- `mirrored_from: dbt-agent`
- `deprecated_copy: true`

Dependency declarations belong in:

- `.claude/manifests/global-dependencies.yaml`

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
chore: add global dependency manifest
```

## Current Priority

The current migration priority is:

1. make analytics-workspace readable and usable from root
2. support non-Claude agents as first-class readers
3. promote the highest-leverage `dbt-agent` assets by copy
4. archive legacy analytics-workspace content only after replacements exist
