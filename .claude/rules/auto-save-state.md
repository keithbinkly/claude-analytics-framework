# Auto-Save State to Workstream

Context windows are finite. Work that isn't saved to the workstream file before compaction is lost.

## When to Save

Save workstream state (`/save` or manual update to `thoughts/shared/workstreams/<workstream>.yaml`) at these checkpoints:

| Checkpoint | Trigger |
|---|---|
| **After ensemble completion** | Any `/analyze` run finishes Steps 1-8 |
| **After experiment completion** | Controlled comparisons, A/B tests, validation runs |
| **After major finding** | Discovery that changes decisions or architecture |
| **After artifact creation** | New HTML pages, agent definitions, skill files |
| **Before expected compaction** | Context usage above ~70%, long background agent runs |
| **After decision made** | Architecture, design, or process choices with rationale |

## What to Save

The workstream YAML frontmatter must include:

- `phase`: Current phase name and number
- `last_action`: What just happened (1-2 sentences)
- `next_action`: What should happen next
- `sessions`: Entry for this session with summary
- `key_files`: Any new artifacts created
- `dots`: Reference to active dot files

The markdown body should capture:

- **Decision Log entries**: Rationale for choices made this session
- **Phase History updates**: Progress within the current phase

## How to Save

**Option 1: `/save` skill** (preferred — handles all the above automatically)

**Option 2: Manual update** (when `/save` isn't available)
```
Read thoughts/shared/workstreams/<workstream>.yaml
Edit: update frontmatter fields + append decision log entries
```

## Anti-Pattern: "I'll Save Later"

Never defer saving because "I still have context." Context compaction is unpredictable during:
- Long background agent runs (monitoring loops consume context)
- Multi-step ensemble dispatches (4+ agents)
- Research sessions with many file reads

**Save after each completed milestone, not at the end of the session.**

## For Ensemble Runs Specifically

After `/analyze` Step 8 (writeback) or Step 8.5 (failure library update), save:
1. Number of findings written and to which partner files
2. Any new failure library entries
3. Key metrics or conclusions
4. Artifacts produced (HTML pages, data files)

This is Step 8.7 in the `/analyze` workflow.
