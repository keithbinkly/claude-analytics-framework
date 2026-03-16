# Load Workstream

Resume an existing workstream or pipeline. The pair to `/save` — loads context so any session can pick up where another left off.

**Usage:**
- `/load` — show all workstreams/pipelines and pick one
- `/load [name]` — load a specific workstream or pipeline by name

---

## Steps

### 0. Parse Arguments

Arguments: `$ARGUMENTS`

- If `[name]` provided: skip to Step 2 with that name
- If empty: continue to Step 1 (picker)

### 1. Discover All Loadable Work

Scan both workstream files and pipeline PLANs:

```bash
ls thoughts/shared/workstreams/*.yaml 2>/dev/null
ls repos/dbt-agent/handoffs/*/PLAN.md 2>/dev/null
```

For each file found, read the YAML frontmatter to extract:
- **Workstreams**: `workstream`, `status`, `phase`, `priority`, `last_updated`, `next_action`
- **Pipelines**: pipeline name (from folder), `phase`, `priority`, `last_updated`, `next_action`

### 1b. Present Picker

Use `AskUserQuestion` to show the options. Format each option as:

```
label: "[name]"
description: "[status] — [phase] (last: [relative time])"
```

Group workstreams first, then pipelines. Include status emoji:
- active → (active)
- paused → (paused)
- blocked → (blocked)

If only one loadable item exists, skip the picker and load it directly.

### 2. Load the Selected Work

Based on the selection:

**If workstream** (`thoughts/shared/workstreams/[name].yaml`):
- Read the full file
- Display the **resume block** (YAML frontmatter) formatted for quick scanning:

```
## Resuming: [workstream name]

**Status:** [status] | **Priority:** [priority]
**Phase:** [phase]
**Last action:** [last_action]
**Next action:** [next_action]
**Blockers:** [blockers or "None"]

**Key files:**
[list key_files with roles]

**Active dots:**
[list active dots]

**Sessions:** [count] sessions linked
**Last saved:** [last_updated] by session [last_saved_by prefix]
```

**If pipeline** (`repos/dbt-agent/handoffs/[name]/PLAN.md`):
- Read the PLAN.md
- Display similar resume summary from its frontmatter

### 3. Link This Session

Read the current session GUID:
```bash
cat /tmp/claude-session-id 2>/dev/null
```

Print it so it gets indexed in the transcript:
```
Session [GUID] now working on: [workstream name]
```

This creates the bidirectional link — the workstream file lists session GUIDs (from `/save`), and this session's transcript contains the workstream name.

### 4. Load Agent Context

Check if the workstream YAML has an `agent:` field.

**If `agent:` is present:**

1. Look up the agent name (e.g., `agent: builder`)
2. Read the agent's core interior files from `~/.claude/agent-memory/<agent>/`:
   - `MEMORY.md` — identity, voice, commitments (always load)
   - `napkin.md` — corrections, anti-patterns (always load)
   - `decisions.md` — architectural choices with rationale (always load)
3. Note the agent identity in the resume block:
   ```
   **Agent:** [agent name] (identity loaded from ~/.claude/agent-memory/[agent]/)
   ```
4. If the agent has a command file (`.claude/commands/<agent>.md`), read it for startup instructions — it may reference additional topic files to load.

**If no `agent:` field:** Skip agent loading (backward compatible).

### 5. Load Workstream Context

After displaying the summary, proactively read the most important context files:

a) Read any **active dots** listed in the workstream (`repos/dbt-agent/.dots/*.md`)
b) If the workstream has a `key_files` list, mention them (don't read all — ask first if there are >3)
c) Check for recent handoff YAMLs that reference this workstream

### 6. Ready Prompt

End with:
```
Ready to continue. What would you like to work on?

When done, run `/save` to update the workstream state.
```

---

## Design Principles

1. **Fast resume** — Show the resume block immediately. Don't make the user wait for deep reads.
2. **Session linking** — Always print the GUID so transcripts are searchable.
3. **Progressive detail** — Summary first, offer to load more context on demand.
4. **Paired with /save** — Every `/load` should end with a `/save`. Bookend pattern.
