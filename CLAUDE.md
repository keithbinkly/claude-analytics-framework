don't look at the full .env file. Only search for the var names up to the equals sign.

# Analytics & Insights Team Workspace

This is the shared analytics control plane and team entrypoint. It coordinates shared workflow docs, manifests, commands, skills, and team knowledge across linked repos while preserving `dbt-enterprise` as the execution target and `dbt-agent` as the intact migration source/reference.

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

analytics-workspace coordinates three important locations:

1. `analytics-workspace`
   Shared control plane, team knowledge, migration planning, promoted shared assets.

2. `dbt-enterprise`
   Production dbt project. This is where dbt CLI commands run.

3. `dbt-agent`
   Current operational reference and migration source. It remains fully usable while assets are copied into analytics-workspace over time.

## Critical Rules

### dbt Execution

- Do not run dbt CLI from analytics-workspace root.
- Route dbt execution into `dbt-enterprise`.
- Use analytics-workspace for control-plane context and promoted shared assets.
- Use `dbt-agent` as fallback reference until analytics-workspace has replaced the needed capability.

### Migration Safety

- `dbt-agent` remains fully usable throughout migration.
- Prefer copy-promote over move-delete.
- Do not archive legacy analytics-workspace assets until working replacements exist.
- Do not hide unresolved dependencies behind machine-specific absolute paths.
- Every promoted asset should declare ownership metadata and CCV3/global dependency metadata.

### Global Layer

- Global agent memory remains in `~/.claude/agent-memory/`.
- Analytics-specific global dependencies must be explicit in `.claude/manifests/ccv3-dependencies.yaml`.
- No promoted analytics-workspace asset should rely on undocumented `~/.claude` behavior.

## How To Route Work

Use `.claude/manifests/repo-adapters.yaml` as the routing contract.

- Shared platform behavior, manifests, team knowledge, workflow design:
  Stay in analytics-workspace.

- dbt models, project-local dbt QA, dbt execution, production dbt constraints:
  Route into `dbt-enterprise`.

- Not-yet-promoted commands, skills, reference behavior, legacy shared workflows:
  Consult `dbt-agent`.

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

Shared team-facing knowledge belongs in analytics-workspace, especially under:

- `knowledge/domains/`
- `knowledge/platform/`
- `.claude/manifests/`
- promoted shared commands and skills in `.claude/`

Project-local delivery code does not belong in analytics-workspace. Keep:

- dbt models/tests/YAML in `dbt-enterprise`
- historical and migration-source reference content in `dbt-agent`

See `CONTRIBUTING.md` for the contribution model.

## Skill Activation (Auto-Load on Keywords)

| Keywords | Skill | Path |
|----------|-------|------|
| migrate, legacy, refactor, pipeline | Migration | `.claude/skills/dbt-migration/` |
| optimize, slow, DISTKEY, SORTKEY, performance | Redshift Optimization | `.claude/skills/dbt-redshift-optimization/` |
| QA, validate, test, verify, variance | QA | `.claude/skills/dbt-qa/` |
| style, format, where should, folder, canonical | Standards | `.claude/skills/dbt-standards/` |
| dependencies, lineage, upstream, downstream | Lineage | `.claude/skills/dbt-lineage/` |
| semantic layer, MetricFlow, metrics | Semantic Layer | `.claude/skills/dbt-semantic-layer-developer/` |
| start migration, new pipeline, workflow | Orchestrator | `.claude/skills/dbt-orchestrator/` |
| business context, requirements, transcript | Business Context | `.claude/skills/dbt-business-context/` |
| data discovery, profile, source profiling | Data Discovery | `.claude/skills/dbt-data-discovery/` |
| tech spec, architecture design | Tech Spec Writer | `.claude/skills/dbt-tech-spec-writer/` |
| preflight, cost estimate | Preflight | `.claude/skills/dbt-preflight/` |
| jinja, macro, dbt-utils | Jinja SQL | `.claude/skills/dbt-jinja-sql-optimizer/` |
| echarts, rich text, chart config, visual map | ECharts Reference | `.claude/skills/echarts/` |
| interactive dashboard, keyboard dashboard, deep dive, data story | Interactive Dashboard | `.claude/skills/interactive-dashboard-builder/` |
| dbt unit test, TDD, test-driven | dbt Native Unit Test Reference | `.claude/skills/dbt-native-unit-test-reference/` |
| business question, what were, how many, total sales | NL Queries | `.claude/skills/dbt-nl-queries/` |
| dbt docs, dbt documentation, look up dbt | dbt Docs Lookup | `.claude/skills/dbt-docs-lookup/` |
| MCP server, configure MCP, MCP setup | MCP Setup | `.claude/skills/dbt-mcp-setup/` |
| Fusion, migrate to Fusion, Fusion engine | Fusion Migration | `.claude/skills/dbt-fusion-migration/` |
| CI/CD, slim CI, deploy, state:modified | CI/CD Patterns | `.claude/skills/dbt-fundamentals/` |
| /analyze, ensemble, multi-analyst, compare perspectives | Analyst Ensemble | `.claude/skills/ai-analyst-ensemble/` |
| data story, storytelling page, data narrative, tell the story of | Data Storytelling | `.claude/skills/data-storytelling/` |
| decision trace, past QA, have we seen this before | Decision Trace | `.claude/skills/dbt-decision-trace/` |
| dbt artifacts, execution metadata, run history | dbt Artifacts | `.claude/skills/dbt-artifacts/` |
| SQL unit test, pytest, DuckDB mock | SQL Unit Testing | `.claude/skills/dbt-sql-unit-testing/` |
| outlier detection, Benford, gaps islands, GROUPING SETS | SQL Hidden Gems | `.claude/skills/sql-hidden-gems/` |
| contribute, share finding, add to knowledge, save for team | Contribute Knowledge | `.claude/skills/contribute-knowledge/` |

Full registry: `.claude/skills/SKILLS_REGISTRY.md`

## Anti-Patterns (Auto-Blocked)

| Pattern | Impact | Fix |
|---------|--------|-----|
| `NOT IN (subquery)` | 4.18x slower | `NOT EXISTS` |
| `OR` in JOIN | 4.07x slower | `UNION ALL` |
| Deep nesting 3+ | 3.06x slower | CTEs |
| `SELECT *` | 2.08x slower | Explicit columns |

Full list: `knowledge/domains/redshift/reference/anti-pattern-impact.yml`

## Current Status

analytics-workspace is the shared team entrypoint with 27 promoted skills, 24+ commands, 26 agent definitions, and 21 operating rules. Core pipeline workflows are fully supported from the workspace root. Consult `dbt-agent` for capabilities not yet promoted.
