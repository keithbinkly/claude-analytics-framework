# Domain Knowledge

This directory is for shared, team-contributed domain knowledge that should live in CAF rather than in an execution repo.

Use domain folders for:

- reusable patterns
- operational reference material
- decision logs
- team-shared heuristics and conventions

Do not use this folder for:

- production dbt project code
- project-local troubleshooting that only belongs in `dbt-enterprise`
- historical reference content that has not yet been promoted from `dbt-agent`

## Current Priority Domains

- `dbt-pipelines`
- `semantic-layer`
- `redshift`
- `data-storytelling`
- `feature-store`
- `tpg-pipelines`

## Suggested Structure

Each domain can grow into:

- `patterns/`
- `reference/`
- `decisions/`

During early migration, the top-level README in each domain is enough to establish ownership and contribution intent.

Use `knowledge/reference/` for shared tool and standards material that is broader than a single domain.
