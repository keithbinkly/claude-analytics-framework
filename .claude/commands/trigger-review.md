# Trigger Review

Interactive review of suggested trigger phrases. Approving an item adds the phrase to the target skill's trigger list in SKILL.md.

---

## Steps

### 1. Load Queue

Read the trigger review queue:

```bash
cat repos/dbt-agent/.dots/dbt-agent-trigger-review-queue.md
```

Parse all unchecked items (`- [ ]`). Each has format:
```
- [ ] `phrase` → skill-name (conf: X, freq: Y)
```

If no unchecked items, report "Queue empty" and stop.

### 2. Present Items for Review

Group by skill. For each item, show:
- The phrase
- Confidence and frequency
- Whether the phrase overlaps with existing triggers in CLAUDE.md skill activation table

Ask user to approve/reject each batch (by skill).

### 3. Apply Approved Items

For each approved phrase:

1. Read the target skill's SKILL.md file at `.claude/skills/{skill-name}/SKILL.md`
2. Find the YAML frontmatter `triggers:` list (or the trigger keywords section)
3. Add the new phrase to the triggers list
4. Also update the `CURRENT_TRIGGERS` dict in `repos/dbt-agent/tools/chatops/trigger_suggester.py` to keep it in sync

### 4. Mark Applied in Queue

In `repos/dbt-agent/.dots/dbt-agent-trigger-review-queue.md`, change applied items from:
```
- [ ] `phrase` → skill-name ...
```
to:
```
- [x] `phrase` → skill-name ... applied YYYY-MM-DD
```

For rejected items, mark:
```
- [~] `phrase` → skill-name ... rejected YYYY-MM-DD
```

### 5. Summary

Report:
```
## Trigger Review Complete

- Approved: X phrases across Y skills
- Rejected: Z phrases
- Remaining: N unchecked

Skills updated:
- skill-name: +X triggers
```

---

## Arguments

| Arg | Description | Default |
|-----|-------------|---------|
| `--skill` | Review only one skill | all |
| `--auto-reject-below` | Auto-reject items below confidence | none |

---

## Example

```
/trigger-review

> ## Trigger Review Queue
>
> ### dbt-qa (3 items)
> 1. `verify results` (conf: 0.8, freq: 4) — Approve? [y/n]
> 2. `check output` (conf: 0.7, freq: 3) — Approve? [y/n]
> 3. `run checks` (conf: 0.7, freq: 2) — Approve? [y/n]
>
> Approved 2, rejected 1. Updated dbt-qa/SKILL.md.
```
