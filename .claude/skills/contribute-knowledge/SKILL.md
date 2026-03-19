---
name: contribute-knowledge
description: Commit a finding, pattern, or lesson to the shared Knowledge Graph so the whole team benefits. Low-friction — one command, agent handles placement and indexing.
triggers:
  - contribute
  - share this finding
  - add to knowledge base
  - commit to KG
  - save this for the team
  - everyone should know
  - log this pattern
  - share what we learned
---

# /contribute — Share Knowledge with the Team

Commit a finding, pattern, or discovery to the shared knowledge base so every future session and teammate benefits.

## When to Use

After you've:
- Built or enhanced a pipeline and learned something reusable
- Investigated data and found a pattern, quirk, or gotcha
- Resolved a stakeholder question with non-obvious analysis
- Discovered a performance fix, anti-pattern, or best practice
- Found something that would save someone else time

## How It Works

**Step 1: Identify the contribution** from the current session. If the user said "contribute" or "share this", use the context they referenced. If invoked at session end, review what was accomplished and ask:

> "What from this session should the team know? I see we [summary of work]. Want me to contribute any of these findings?"

**Step 2: Classify** into one of these types:

| Type | Goes to | Example |
|------|---------|---------|
| `pipeline-pattern` | `knowledge/domains/dbt-pipelines/reference/` | "delete+insert beats merge for composite keys" |
| `redshift-pattern` | `knowledge/domains/redshift/reference/` | "ANALYZE post-hook prevents nested-loop regression" |
| `semantic-layer` | `knowledge/domains/semantic-layer/` | "entity-qualify all MetricFlow dimensions" |
| `business-finding` | `knowledge/findings/` | "Samsung declines driven by code-59 from two neobanks" |
| `data-quirk` | `knowledge/findings/` | "ODS product_channel has duplicates — always dedup" |
| `tool-pattern` | `knowledge/domains/dbt-pipelines/reference/` | "DuckDB CTE injection catches 70% of logic errors" |
| `analysis-insight` | `knowledge/findings/` | "CP approval rates 92-97%, CNP 75-85% across all partners" |

**Step 3: Connect** — search the KG for related existing knowledge, then ask the user two quick questions:

```bash
python3 knowledge/platform/graph/graph_search.py "[key terms]" --max 5
```

Show the top 3-5 results and ask:

> "Related context I found in the KG:
>   1. [title] — [one-line summary]
>   2. [title] — [one-line summary]
>   3. [title] — [one-line summary]
>
> Any of these related? (numbers, or 'none')
> Which pipeline/partner does this relate to?
> Who benefits most — builder, qa, analyst, or everyone?"

This takes ~10 seconds and creates edges that keyword matching alone would miss. If the user skips, that's fine — proceed without.

**Step 4: Write** a concise markdown file with frontmatter for KG enrichment:

```markdown
---
contributed: YYYY-MM-DD
source: [pipeline name / analysis / investigation]
partner: [partner name, if applicable]
benefits: [builder, qa, analyst, or everyone]
related:
  - node-id-from-step-3
  - another-node-id
tags: [2-4 domain keywords the user mentioned]
---

# [Clear, specific title]

## What We Found

[1-3 paragraphs. Lead with the finding, then the evidence, then the implication.]

## When This Applies

[Bullet list: what situation triggers this knowledge being relevant]

## Evidence

[The query, metric, or observation that supports this. Include specific numbers.]
```

The `related:` field creates explicit KG edges at index time. The `benefits:` field weights retrieval toward the right agent context. Both are optional — the file works without them.

**Step 5: Place** the file:
- Filename: lowercase-kebab-case, descriptive. e.g., `samsung-decline-code-59-neobank-concentration.md`
- Directory: per the type table above

**Step 6: Index** — rebuild the KG to include the new file:

```bash
python3 knowledge/platform/graph/index_builder.py
```

**Step 7: Confirm** to the user:

> "Contributed: [title] to knowledge/[path].
> Connected to: [list of related nodes from step 3].
> Available to team on next `git pull`. KG rebuilt — [N] nodes."

## What NOT to Contribute

- Raw session logs or debugging transcripts (too noisy)
- Findings that are only true for one specific date range with no pattern
- Things already in a skill or rule (check first: `python3 knowledge/platform/graph/graph_search.py "keywords"`)
- Personal workflow preferences (those go in `~/.claude/agent-memory/`)

## Dedup Check

Before writing, search the KG to make sure this isn't already captured:

```bash
python3 knowledge/platform/graph/graph_search.py "[key terms from the finding]" --max 3
```

If a similar node exists, either skip or update the existing file instead of creating a duplicate.

## Low-Friction Mode

If the user says "contribute" with no further context, scan the session for:
1. Any resolved QA issue → extract the pattern
2. Any business question answered → extract the finding
3. Any performance fix applied → extract the technique
4. Any data quirk discovered → extract the gotcha

Present the top 1-2 candidates and ask which to contribute. Don't make them write it — you write it, they approve.
