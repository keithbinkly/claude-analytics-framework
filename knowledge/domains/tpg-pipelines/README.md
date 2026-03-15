# TPG Pipelines

**Maintainer:** TPG pipeline builders
**Status:** Open for contributions

## What This Covers

Everything specific to TPG (Third-Party Gateway) pipelines that the team needs to know — domain logic, source table quirks, business rules, naming conventions, and operational patterns.

## Why This Folder Matters

When you ask Claude to help with a TPG pipeline, it looks here first for team-specific context. Without content here, Claude falls back on generic dbt knowledge. With content here, it gives answers grounded in *how we actually do TPG work*.

**Example:** If you document that TPG transactions use a specific settlement date logic, Claude will apply that logic correctly instead of guessing.

## How Agents Use This Folder

Claude reads files here when:
- You mention "TPG" in your request
- You're working on models that touch TPG source tables
- You ask about TPG-specific business rules or patterns

The content here supplements the general dbt pipeline skills (migration, QA, preflight, etc.) with TPG-specific domain knowledge.

## What to Add

### `patterns/` — Proven approaches

Things that work and should be reused:
- TPG pipeline structure templates
- Common transformation patterns for TPG data
- Testing patterns specific to TPG sources
- Reconciliation approaches (e.g., how to tie out TPG vs internal records)

### `reference/` — Facts about TPG data

Things that are true about our TPG sources:
- Source table catalog (what tables exist, what they contain)
- Column dictionaries and data type quirks
- Business rule documentation (settlement logic, fee calculations, etc.)
- Filter and partition patterns (what date filters to use, known data gaps)

### `decisions/` — Why we do things this way

Decisions with rationale:
- "Why we model TPG data at this grain"
- "Why certain TPG fields are excluded or transformed"
- "Why we use this join strategy for TPG ↔ internal data"

## Getting Started

Don't try to document everything at once. Start with:

1. **One pain point** — What question do you keep answering about TPG data? Write it down.
2. **One source table** — Document the most important TPG source: columns, quirks, join keys.
3. **One pattern** — Your most common TPG transformation. Show the SQL.

```bash
mkdir -p patterns reference decisions

# Start with whatever you know best
cat > reference/tpg-source-overview.md << 'EOF'
# TPG Source Tables

## [table_name]
- **What it contains:** ...
- **Grain:** one row per ...
- **Key columns:** ...
- **Quirks:** ...
- **Join to internal data via:** ...
EOF

git add . && git commit -m "docs: initial TPG source documentation"
git push
```

## Creating a TPG Expert Agent (Optional)

See `QUICKSTART.md` for how to create a domain expert agent that reads from this folder. The short version:

1. Create `.claude/agents/tpg-expert.md` with a prompt that reads `knowledge/domains/tpg-pipelines/`
2. Optionally create `.claude/commands/tpg-expert.md` as a slash command
3. Or just add TPG keywords to the skill activation table in `CLAUDE.md`
