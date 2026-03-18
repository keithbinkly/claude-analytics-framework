# Workstream Over Handoff

## Rule

When recording progress, update the **workstream file** — not a handoff document.

- Workstream (`thoughts/shared/workstreams/*.yaml`): Durable record of what happened, decisions made, what's next. Survives across sessions.
- Handoff (`handoffs/*.md`): Ephemeral transfer document for passing work to a specific session. Consumed once.

## When to use each

| Situation | Use |
|-----------|-----|
| Recording progress, decisions, artifacts | Workstream |
| Transferring work to another agent/session | Handoff (points to workstream) |
| Saving state before context compaction | Workstream |
| "What did we do?" | Workstream |

## Anti-Pattern

Writing progress to a handoff file when a workstream exists. The handoff becomes stale; the workstream stays current.

## Source

Session 2026-03-17: Keith corrected "write a handoff" → "update the workstream."
