# Proactive Save on Context Pressure

## Rule

When context is building up during a long session, proactively suggest saving progress. Don't wait for the user to ask.

## Triggers

Save or suggest saving when:

- **After completing a milestone** — ensemble run, artifact creation, major finding, experiment
- **After 15-20 tool uses** without a save — context is getting heavy
- **Before spawning parallel agents** — multi-agent runs consume context fast
- **When the session has been running for a while** and multiple deliverables are done
- **Before ANY expected compaction** — if you sense context is large, save first

## How to Save

1. Update the active workstream YAML (`thoughts/shared/workstreams/*.yaml`)
2. Update the dot if one exists (`.dots/*.md`)
3. Include: what was done, what's next, key file paths, decisions made

## What to Say

```
"We've completed X and Y. Let me save workstream progress before we continue —
context is getting heavy and I don't want to lose state."
```

Or at a natural break point:

```
"Good stopping point. Saving progress to the workstream file."
```

## Anti-Pattern

"I'll save at the end of the session." — Context compaction is unpredictable. Save after each completed milestone, not at the end.
