# Morning Review

Daily orientation for the analytics workspace. Surfaces what needs attention.

---

## Steps

### 0. Active Sessions (NEW)

Read session state files:

```bash
cat thoughts/shared/WORKING.md
```

Summarize active sessions by status:
- Active: currently being worked
- Paused: blocked by VPN, teammate, etc.
- Blocked: needs external resolution

Also check recent session history:

```bash
head -50 thoughts/shared/session-log.md
```

### 1. Check Latest Audit

Read the most recent system audit:

```bash
ls -t repos/dbt-agent/data/telemetry/audits/system-audit-*.md | head -1
```

Summarize key findings: skill underutilization, trigger suggestions, wiring issues.

### 2. Check Inbox

```bash
cat repos/dbt-agent/data/inbox/system-evolution.md
```

Report any new notifications since last review.

### 3. Dots by Priority

```bash
ls repos/dbt-agent/.dots/*.md
```

Read each dot's YAML frontmatter. Group by status and priority:
- **P0-P1 open**: needs action today
- **In-progress**: check for staleness (>3 days)
- **Completed**: can be closed/archived

### 4. Trigger Review Queue

```bash
cat repos/dbt-agent/.dots/dbt-agent-trigger-review-queue.md
```

Count unchecked items (`- [ ]`). If >5 pending, recommend running `/trigger-review`.

### 5. Handoff Action Items

Scan active handoffs for unresolved action items:

```bash
cd /Users/kbinkly/git-repos/dbt-agent && .venv/bin/python3 -m tools.chatops.handoff_action_scanner --dry-run
```

Surface any "Next Steps", "Proposed Improvements", or "Recommendations" that haven't been triaged. These are improvement suggestions from past sessions that need routing to the right dot or skill.

### 6. Active Handoffs

```bash
ls repos/dbt-agent/handoffs/*/PLAN.md 2>/dev/null
```

List any active pipeline work that needs continuation.

### 7. Recommend Focus

Based on the above, recommend today's focus area:
- If handoff action items are unresolved → triage into dots
- If inbox has items → address notifications first
- If trigger queue is full → run `/trigger-review`
- If pipeline handoffs exist → resume pipeline work
- Otherwise → check P1 dots

---

## Output Format

```
## Morning Review — YYYY-MM-DD

### Active Sessions
[count] active | [count] paused | [count] blocked
- [session-name]: [1-line status]
- ...

### Audit Summary
[1-2 line summary of latest audit]

### Inbox
[X new notifications / empty]

### Dots
- P0: X open
- P1: X open
- In-progress: X (Y stale)

### Trigger Queue
X items pending review

### Handoff Action Items
X unresolved items across Y handoffs [or "all triaged"]

### Active Handoffs
[list or "none"]

### Recommended Focus
-> [action]
```

---

## Related Commands

- `/load` — Show all workstreams/pipelines and pick one to continue
- `/development-kickoff` — Start new dbt development work
