# Workstreams

Workstream files track the state of ongoing work across sessions. They're the durable record of what happened, what was decided, and what's next.

## Why workstreams?

Claude Code sessions are ephemeral — when a session ends or context compacts, the nuance is lost. Workstream files persist the state so the next session (or a different teammate) can pick up where you left off.

## How to use

### Save progress
```
/save
```
Or say "save progress" — Claude updates the active workstream YAML with what happened, what's next, and key artifacts.

### Resume work
```
/load [workstream-name]
```
Or say "load the overdraft workstream" — Claude reads the YAML, understands the current phase, and presents the next action.

### Create a new workstream
When starting work that will span multiple sessions, create a YAML file:

```yaml
---
name: Your Workstream Name
status: active
phase: "Phase 1: Discovery"
last_action: "Created workstream"
next_action: "Start data discovery for source tables"
priority: P2
created: 2026-03-19
updated: 2026-03-19
sessions: []
key_files: []
---

## Decision Log

(Decisions with rationale go here as work progresses)

## Phase History

### Phase 1: Discovery — IN PROGRESS
- Started: 2026-03-19
```

### When to use workstreams vs other state

| Situation | Use |
|-----------|-----|
| Multi-session pipeline work | Workstream |
| Recording decisions and progress | Workstream |
| Quick fix, single session | No workstream needed |
| Transferring work to a specific person | Handoff that points to the workstream |
| Personal notes | Your local `~/.claude/agent-memory/` |

## Shared vs personal

Workstreams in this directory are **team-shared** (git-tracked). Anyone can read them to understand where a project stands.

If you're doing work that only you need to track, you can keep workstream files locally — but most pipeline and analysis work benefits from being shared.
