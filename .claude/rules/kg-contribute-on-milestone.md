# Contribute Knowledge on Milestones

## Rule

After completing pipeline work, data investigations, or stakeholder analysis — prompt for `/contribute` before ending the session.

## When to Prompt

- Pipeline phase completed (any gate passed)
- QA issue resolved with non-obvious root cause
- Business question answered with ensemble or drill-down analysis
- Performance optimization applied with measured improvement
- Data quirk discovered that would trip up the next person

## How to Prompt

```
"We discovered [finding]. Want to /contribute this to the team knowledge graph?
It would help future sessions working on [related domain]."
```

## Why

Knowledge that stays in session context dies at session end. The `/contribute` skill writes it to `knowledge/` where the KG indexes it. Without prompting, contributors forget — and the same issues get reinvestigated.

## Source

System Architect session 2026-03-19: Built the /contribute skill and KG eval suite. The skill exists but needs agents to invoke it proactively.
