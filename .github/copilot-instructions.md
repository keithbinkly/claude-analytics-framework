# Copilot Instructions — Analytics & Insights Team Workspace

You are working in the shared analytics control plane (`analytics-workspace`). This is NOT the production dbt project — it coordinates shared knowledge, skills, manifests, and workflows across linked repos.

## Read Order

For full context, read these files in order:

1. `AGENT_ENTRYPOINT.md` — tool-agnostic bootstrap, workspace structure, routing rules
2. `README.md` — team overview and quick start
3. `CLAUDE.md` — detailed rules (many apply to any agent, not just Claude)
4. `.claude/manifests/repo-adapters.yaml` — which repo handles which work

## Workspace Layout

| Repo | Role | Where |
|------|------|-------|
| `analytics-workspace` (this repo) | Shared control plane, skills, knowledge | `.` |
| `dbt-enterprise` | Production dbt project — run dbt CLI here | `./dbt-enterprise` |
| `dbt-agent` | Migration source, reference workflows | `./dbt-agent` |

## Critical Rules

### dbt Execution

- **NEVER** run `dbt run`, `dbt build`, or `dbt test` from this repo's root
- Route all dbt CLI execution into `dbt-enterprise`
- **Always** run `dbt compile` before `dbt run` — no exceptions
- Use `dbt-enterprise` project constraints, not generic dbt guidance

### Work Routing

| Task Type | Route To |
|-----------|----------|
| Shared platform, manifests, team knowledge | Stay in `analytics-workspace` |
| dbt models, tests, QA, semantic layer | `dbt-enterprise` |
| Reference workflows, legacy shared logic | Consult `dbt-agent` |

## Skills as Reference Material

This repo contains 27+ skills under `.claude/skills/`. Each skill has a `SKILL.md` with domain knowledge. Treat these as SOPs / reference docs — they contain validated patterns, guardrails, and examples.

### Key Skills by Topic

| Topic | Skill Path | Use When |
|-------|-----------|----------|
| **dbt Fundamentals** | `.claude/skills/dbt-fundamentals/` | Modeling, testing, materializations, commands |
| **Migration** | `.claude/skills/dbt-migration/` | Converting legacy SQL/reports to dbt models |
| **QA & Validation** | `.claude/skills/dbt-qa/` | Variance analysis, data quality, test writing |
| **Standards** | `.claude/skills/dbt-standards/` | Model placement, naming, canonical reuse |
| **Preflight** | `.claude/skills/dbt-preflight/` | Cost estimation, dependency checks before runs |
| **Redshift Optimization** | `.claude/skills/dbt-redshift-optimization/` | DISTKEY, SORTKEY, incremental strategy, slow queries |
| **Semantic Layer** | `.claude/skills/dbt-semantic-layer-developer/` | MetricFlow, metrics, semantic models, grain |
| **Jinja & SQL** | `.claude/skills/dbt-jinja-sql-optimizer/` | Macros, dbt-utils, dynamic SQL generation |
| **Lineage** | `.claude/skills/dbt-lineage/` | Upstream/downstream impact, dependency analysis |
| **Tech Spec** | `.claude/skills/dbt-tech-spec-writer/` | Pipeline architecture, model inventory |
| **Business Context** | `.claude/skills/dbt-business-context/` | Requirements gathering, stakeholder notes |
| **Data Discovery** | `.claude/skills/dbt-data-discovery/` | Source profiling, schema validation |
| **Decision Traces** | `.claude/skills/dbt-decision-trace/` | Past QA resolutions, case-based reasoning |
| **SQL Hidden Gems** | `.claude/skills/sql-hidden-gems/` | Advanced SQL patterns, Redshift-specific |
| **Unit Testing** | `.claude/skills/dbt-sql-unit-testing/` | Mock data, DuckDB-style local tests |
| **ECharts** | `.claude/skills/echarts/` | Chart configuration, rich interactive visuals |

Full registry: `.claude/skills/SKILLS_REGISTRY.md`

## Knowledge Base

Domain knowledge is organized under `knowledge/`:

| Path | Contents |
|------|----------|
| `knowledge/domains/dbt-pipelines/reference/` | QA checklists, troubleshooting, anti-patterns |
| `knowledge/domains/redshift/reference/` | Anti-pattern impact data, optimization patterns |
| `knowledge/reference/standards/` | Coding standards, naming conventions |
| `knowledge/reference/tools/` | MCP tool reference, dbt Cloud tools |
| `knowledge/platform/planning/` | Architecture plans, migration inventory |

## SQL Anti-Patterns (Auto-Block)

These patterns are validated as significantly slower on Redshift. Avoid them:

| Pattern | Impact | Fix |
|---------|--------|-----|
| `NOT IN (subquery)` | 4.18x slower | Use `NOT EXISTS` |
| `OR` in JOIN condition | 4.07x slower | Use `UNION ALL` |
| Deep nesting (3+ levels) | 3.06x slower | Use CTEs |
| `SELECT *` | 2.08x slower | Explicit column list |

Full list with benchmarks: `knowledge/domains/redshift/reference/anti-pattern-impact.yml`

## QA Standards

- **No row count comparisons** — use granular variance analysis (dimension-level breakdown, <0.1% threshold)
- **Never modify a test to make it pass** — investigate root cause first
- **Search past resolutions first** — check `knowledge/domains/dbt-pipelines/decision-traces/` before fresh investigation
- **Define grain before building** — document what makes each row unique before writing SQL

## Incremental Model Guidance

- Prefer `delete+insert` over `merge` on Redshift for composite keys
- `merge` with 10+ column unique keys causes per-row amount inflation at date boundaries
- Use `on_schema_change='sync_all_columns'` for CI compatibility
- Full details: `.claude/rules/dbt-incremental-merge-lessons.md`

## Pipeline Workflow

For pipeline lifecycle (new, resume, gate, close), the canonical workflow docs are:

- `.claude/commands/pipeline-new.md`
- `.claude/commands/pipeline-resume.md`
- `.claude/commands/pipeline-gate.md`
- `.claude/commands/pipeline-close.md`
- `.claude/commands/pipeline-status.md`
- `.claude/commands/pipeline-docs.md`

These are written as Claude slash commands but contain the full workflow logic — read them as process documentation.

## Agent Definitions

Agent specs under `.claude/agents/` describe specialized roles (builder, QA, analyst, etc.). Treat these as role descriptions with context about what each agent knows and how it operates. Index: `.claude/agents/AGENTS-INDEX.md`

## Manifests (Machine-Readable)

| File | Purpose |
|------|---------|
| `.claude/manifests/workspace-manifest.yaml` | Workspace topology and policy |
| `.claude/manifests/repo-adapters.yaml` | Per-repo routing contract |
| `.claude/manifests/workflow-contracts.yaml` | Workflow definitions |
| `.claude/manifests/global-dependencies.yaml` | Global dependency declarations |
