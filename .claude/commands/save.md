# Save Progress

Save your current work to the workstream state file. Like saving a game — captures where you are so any session can resume.

**Usage:**
- `/save` — update current workstream (auto-detects from context or asks)
- `/save [name]` — update a specific workstream
- `/save --new [name]` — create a new workstream state file
- `/save --list` — show all workstreams

---

## Session GUID Tracking

Every Claude Code session has a UUID (e.g., `d69143e8-02ad-4741-ab20-423a61486ac3`). The `session-start.py` hook writes it to `/tmp/claude-session-id` on first prompt. `/save` reads this and appends it to the workstream's `sessions:` list, creating a bidirectional link:

- **Workstream → Sessions**: The YAML lists all session GUIDs that contributed
- **Session → Workstream**: The GUID printed in chat gets indexed in the JSONL transcript

To find all chats for a workstream:
```bash
grep "sessions:" thoughts/shared/workstreams/[name].yaml
```

To find the workstream for a chat:
```bash
grep -rl "[session-guid-prefix]" thoughts/shared/workstreams/
```

---

## Steps

### 0. Parse Arguments

Arguments: `$ARGUMENTS`

- If `--list`: skip to Step 6
- If `--new [name]`: skip to Step 5
- If `[name]` provided: use that workstream
- If empty: detect current workstream (Step 1)

### 1. Detect Current Workstream

Check which workstream this session is working on:

a) Check if any workstream file was recently read this session (likely from `/save` or manual load)

b) List existing workstreams AND pipeline PLANs:
```bash
ls thoughts/shared/workstreams/*.yaml 2>/dev/null
ls dbt-agent/handoffs/*/PLAN.md 2>/dev/null
```

c) If only one workstream exists, use it. If multiple, check which has dots that overlap with files modified this session.

d) **Pipeline fallback:** If the name matches a pipeline in `dbt-agent/handoffs/` but has no workstream file, inform the user:
```
Found pipeline PLAN at dbt-agent/handoffs/[name]/PLAN.md — no workstream file yet.
Options:
1. Update the pipeline PLAN.md directly (pipeline work)
2. Create a workstream file that links to the pipeline (recommended for long-running work)
```
If user picks option 1, read the PLAN.md frontmatter and update its `last_action`, `next_action`, and `last_updated` fields — same save semantics, different file.
If user picks option 2, create a workstream YAML that references the pipeline PLAN in `key_files`.

e) If can't determine, ask user: "Which workstream? [list options] or create new with `/save --new name`"

### 2. Read Current State

Read the workstream file: `thoughts/shared/workstreams/$NAME.yaml`

Parse the YAML frontmatter to understand what was last saved.

### 2b. Read Session GUID

```bash
cat /tmp/claude-session-id 2>/dev/null
```

This file is written by `session-start.py` on the first prompt of every session. Store the value — it will be appended to the workstream's `sessions:` list in Step 4.

If the file doesn't exist, derive the GUID from the most recent JSONL:
```bash
ls -t ~/.claude/projects/-Users-kbinkly-git-repos-dbt-agent/*.jsonl | head -1 | xargs basename | sed 's/.jsonl//'
```

### 3. Gather Session Updates

Collect what happened since last save. Use your current context to determine:

**a) Status updates:**
- What phase is the workstream in now?
- What was the last action completed?
- What's the logical next action?
- Any new blockers?

**b) Dots changes:**
- Were any dots created, updated, or completed this session?
- Check: `ls dbt-agent/.dots/*$NAME*.md 2>/dev/null` and any dots mentioned in conversation

**c) Decisions made:**
- Any architectural, design, or approach decisions made this session?
- Capture: what was decided, why, what alternatives were rejected

**d) Key files:**
- Any new files created that are important to this workstream?
- Any existing files significantly modified?

### 4. Write Updated State

Update the workstream YAML file with gathered information:

**YAML frontmatter updates:**
- `phase`: current phase description
- `last_action`: what was just completed
- `next_action`: what should happen next
- `blockers`: current blockers ([] if none)
- `last_updated`: current ISO timestamp
- `last_saved_by`: the session GUID from Step 2b
- `status`: active/paused/blocked/complete
- `dots.active`: list of open/in-progress dots
- `dots.completed`: append newly completed dots
- `key_files`: add any new important files
- `sessions`: append current session GUID (from Step 2b) with date and summary. **Do not duplicate** — check if GUID is already listed.

**Markdown body updates:**
- Update "Current State" section with fresh summary
- Append new decisions to "Decision Log" (with today's date header)
- Update "Phase History" if a phase was completed

**IMPORTANT:** Preserve all existing content. Only update/append — never delete history.

Present the diff to the user before writing:
```
## Saving workstream: [name]

### Changes:
- phase: [old] → [new]
- last_action: "[new action]"
- next_action: "[new next]"
- [N] dots updated
- [N] decisions logged

Write these updates?
```

After user confirms, write the file.

### 5. Create New Workstream (--new)

Create a new workstream file from template:

```yaml
---
workstream: $NAME
type: <ask user: pipeline | skills | presentation | research | tooling | other>
status: active
phase: "Getting started"
last_action: "Workstream created"
next_action: "<ask user or infer from context>"
blockers: []
priority: <ask user: P0 | P1 | P2 | P3>

created: <current ISO timestamp>
last_updated: <current ISO timestamp>
last_saved_by: <session GUID from Step 2b>

dots:
  active: []
  completed: []

key_files: []

sessions:
  - id: <session GUID from Step 2b>
    date: <today's date>
    summary: "Workstream created"
---

# Workstream: <Name>

## Overview
<Ask user for 2-3 sentence description, or infer from conversation context>

## Current State
Workstream just created. See next_action for first step.

## Decision Log
<!-- Append-only. Each /save adds decisions made since last save. -->

## Phase History
<!-- Completed phases with dates and key artifacts -->
```

Write to `thoughts/shared/workstreams/$NAME.yaml`.

Also check if a dot should be created: "Create a tracking dot at `dbt-agent/.dots/$NAME.md`?"

### 6. List All Workstreams (--list)

```bash
ls thoughts/shared/workstreams/*.yaml 2>/dev/null
ls dbt-agent/handoffs/*/PLAN.md 2>/dev/null
```

For each file, read YAML frontmatter and display unified view:

```
## All Active Work

### Workstreams (thoughts/shared/workstreams/)
| Workstream | Type | Phase | Priority | Last Updated | Status |
|------------|------|-------|----------|--------------|--------|
| [name] | skills | Phase 2 | P1 | 2h ago | Active |
| [name] | presentation | Draft | P2 | 3d ago | Paused |

### Pipelines (dbt-agent/handoffs/*/PLAN.md)
| Pipeline | Phase | Priority | Last Updated | Status |
|----------|-------|----------|--------------|--------|
| merchant-spend | deploy | P1 | 1d ago | Active |
| disbursements | deploy | P1 | 3h ago | Active |

Use `/save [name]` to update, or `/save --new [name]` to create.
```

Flag stale entries (>7 days since last update).

---

## Post-Save Confirmation

After successful save, display:

```
Saved [workstream] at [timestamp]
  Session: [full GUID]
  Phase: [phase]
  Next: [next_action]
  Dots: [N active, M completed]
  Sessions linked: [total count]

Any session can resume with:
  Read thoughts/shared/workstreams/[name].yaml
```

**IMPORTANT:** Always print the full session GUID. This text appears in the JSONL transcript, making the session discoverable when searching for the workstream later.

---

## Design Principles

1. **Single source of truth** — The workstream file IS the canonical state. Not dots, not handoffs, not ledgers.
2. **Append-only history** — Decisions and phases are never deleted, only appended.
3. **Human-readable** — A person reading the file should understand the full project state.
4. **Session-portable** — Any Claude session can load this file and pick up where another left off.
5. **Quick to update** — `/save` should take <30 seconds. Don't over-gather.
