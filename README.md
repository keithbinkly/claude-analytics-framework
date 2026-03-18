# Analytics & Insights Team Workspace

analytics-workspace is the shared control plane for workflows, manifests, shared commands and skills, and team knowledge across linked repositories.

It is not the production dbt project itself. For dbt execution, the target repo remains `dbt-enterprise`.

## Start Here

For a fresh session, read these in order:

1. `AGENT_ENTRYPOINT.md`
2. `CLAUDE.md`
3. `.claude/manifests/workspace-manifest.yaml`
4. `.claude/manifests/repo-adapters.yaml`
5. `.claude/manifests/workflow-contracts.yaml`
6. `.claude/manifests/ccv3-dependencies.yaml`
7. `knowledge/platform/planning/shared-agent-platform-monorepo-plan.md`

## What analytics-workspace Is

analytics-workspace is the shared analytics control plane. It is where the team should increasingly find:

- shared workflow docs
- machine-readable manifests
- shared commands and skills as they are promoted into analytics-workspace
- cross-repo coordination guidance
- team-contributed domain knowledge

analytics-workspace is also the planned team entrypoint for non-Claude coding agents. That is why the workspace now includes:

- `AGENT_ENTRYPOINT.md`
- `.claude/manifests/workflow-contracts.yaml`
- `.claude/manifests/ccv3-dependencies.yaml`

## Linked Repos

analytics-workspace coordinates work across these linked repos:

1. `analytics-workspace`
   Shared control plane and team-facing root.

2. `dbt-enterprise`
   Production dbt project. Run dbt CLI here, not from workspace root.

3. `dbt-agent`
   Current operational reference and migration source. It remains intact while useful assets are copied into analytics-workspace over time.

## Current Migration Model

The migration is non-destructive:

- `dbt-agent` stays fully usable
- analytics-workspace grows by copy-promoting the highest-leverage shared assets
- legacy analytics-workspace assets should only be archived after replacements exist
- promoted assets should declare ownership metadata
- promoted assets should declare CCV3/global dependencies explicitly

analytics-workspace is the planned team entrypoint, but not every capability has been re-homed yet.

## Local Setup

### 1. Create local convenience links

If you want linked repos visible from workspace root:

```bash
./scripts/bootstrap-linked-repos.sh
```

This creates local `repos/` symlinks for the currently expected linked repos.

### 2. Check workspace readiness

```bash
./scripts/check-workspace-readiness.sh
```

This verifies the key bootstrap docs, manifests, linked repo visibility, and MCP setup hints.

### 3. Validate MCP

If you use the dbt Cloud MCP layer:

```bash
cp .env.example .env
./scripts/validate-mcp.sh
```

After changing MCP configuration, restart Claude Code if you expect MCP server discovery to refresh.

## How To Work From Workspace Root

### Build or resume a dbt pipeline

- start in analytics-workspace for manifests, planning docs, and promoted shared assets
- route into `dbt-enterprise` for dbt CLI execution
- consult `dbt-agent` if the needed capability has not yet been promoted

### Run QA

- use analytics-workspace workflow docs or promoted QA assets if available
- inspect the model and project-local constraints in `dbt-enterprise`
- fall back to `dbt-agent` reference material where needed

### Contribute shared knowledge

Add reusable team knowledge in analytics-workspace, especially under:

- `knowledge/domains/`
- `knowledge/platform/`
- `.claude/manifests/`

Do not put shared reference material in `dbt-enterprise` unless it truly belongs with production dbt code.

## Repository Layout

```text
analytics-workspace/
├── AGENT_ENTRYPOINT.md
├── .claude/
│   ├── manifests/
│   ├── commands/
│   ├── skills/
│   └── agents/
├── knowledge/
│   ├── platform/
│   └── domains/
├── repos/
├── scripts/
└── templates/
```

## Where Things Belong

### analytics-workspace

- shared commands and skills
- workflow contracts and manifests
- migration planning
- cross-repo coordination
- team-shared domain knowledge

### `dbt-enterprise`

- dbt models
- schema YAML
- tests
- seeds
- project-local dbt docs

### `dbt-agent`

- intact migration-source/reference material
- not-yet-promoted agent logic
- historical shared workflow content

## Current Priorities

1. Make analytics-workspace usable as the shared workspace root.
2. Support non-Claude agents as first-class readers.
3. Promote the first high-leverage slice from `dbt-agent`.
4. Archive outdated analytics-workspace content only after replacement exists.

## More Detail

- `AGENT_ENTRYPOINT.md` — tool-agnostic bootstrap
- `CLAUDE.md` — workspace operating contract
- `CONTRIBUTING.md` — where to contribute what
- `knowledge/platform/planning/README.md` — planning index

## License

MIT License - See `LICENSE`.
