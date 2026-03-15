# dbt Pipelines

**Maintainer:** Keith
**Status:** Accepting contributions

## What This Covers

Everything the team needs to build, test, and maintain dbt pipelines in dbt-enterprise — migration methodology, QA workflow, canonical model reuse, folder structure, join patterns, and troubleshooting.

## Why This Folder Matters

This is the most content-rich domain folder because pipeline building is our most common daily task. When Claude helps with a pipeline, it reads these files to know our canonical models, our QA methodology (4-template system, not row counts), our folder structure rules, and the join patterns for our specific data sources.

**Without these files:** Claude writes generic dbt models.
**With these files:** Claude writes models that follow our conventions, reuse canonical models (75-90% target), and pass QA on first attempt.

## How Agents Use This Folder

Claude reads files here when:
- You invoke `/pipeline-new`, `/pipeline-resume`, or `/builder`
- You mention "migrate", "QA", "canonical models", or "dbt pipeline"
- The orchestrator skill loads phase-specific context

This folder works alongside many skills:
- `dbt-migration` — 4-phase migration workflow
- `dbt-orchestrator` — pipeline lifecycle management
- `dbt-qa` — 4-template QA methodology
- `dbt-preflight` — pre-execution cost estimation
- `dbt-standards` — folder placement and naming
- `dbt-lineage` — dependency mapping and impact analysis

## What's Here Already

### Reference (8 files)
| File | What it tells Claude |
|------|---------------------|
| `canonical-models-registry.md` | Which models already exist — reuse these instead of building from scratch (75-90% target) |
| `migration-quick-reference.md` | Step-by-step migration patterns |
| `qa-validation-checklist.md` | The 4-template QA methodology (never use row count comparisons) |
| `troubleshooting.md` | Common Redshift and dbt errors with fixes |
| `field-mappings.md` | Column name mappings between source systems |
| `legacy-kpi-gold-standard-metrics.md` | Certified KPI benchmarks for QA tie-outs |
| `macros-registry.md` | Available macros and when to use them |
| `baas-join-registry.yml` | Join patterns for BaaS data sources |

### Decision Traces (3 files)
| File | What it tells Claude |
|------|---------------------|
| `rules.json` | Reusable QA rules from past investigations |
| `selected-traces.json` | Curated high-value QA cases with root causes |
| `README.md` | How decision traces work and migration status |

## What to Add

### `patterns/` — Proven approaches

- Model templates for common pipeline shapes (staging → intermediate → mart)
- CTE structure patterns for complex transformations
- Incremental model patterns for our specific use cases
- Cross-pipeline join patterns

### `reference/` — More facts about our data

- Source table profiles (row counts, update frequency, key columns)
- Business logic documentation ("how authorization attempts become settlements")
- Environment-specific notes (VPN requirements, date filter macros)

### `decisions/` — Past QA resolutions and architectural choices

- "Why we chose this grain for the merchant spend mart"
- "Why the disbursements pipeline uses `delete+insert` not `merge`"
- "How we resolved the 99% row suppression issue in ewallet filtering"

## Getting Started

This folder is already well-seeded. The highest-value additions are:
1. **New decision traces** — when you solve a hard QA issue, document the root cause
2. **Source table profiles** — the discovery data for tables not yet documented
3. **Business logic** — the domain knowledge that lives in people's heads

## The QA Rule

**Never use row count comparisons for QA.** Always use granular variance analysis (Template 1: dimension-level breakdown with variance percentage). Acceptance threshold: <0.1% variance for critical metrics.

This is enforced by `.claude/rules/dbt-qa-standards.md` and the QA skill.
