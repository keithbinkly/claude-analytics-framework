# Log Work to Dots

Document completed or in-progress work to dots with full context linking for cross-session continuity.

---

## Trigger

Run this command when:
- Completing a significant task (>15 min of work)
- Hitting a blocker that needs to persist across sessions
- Making code changes that require follow-up (PRs, batch jobs, validation)
- User requests `/log_work_to_dots`

---

## Workflow

### Step 1: Check Existing Dots

First, scan for related dots that might already track this work:

```bash
ls dbt-agent/.dots/*.md
```

Look for dots matching:
- Same feature/pipeline name
- Same issue type (bug, feature, migration)
- Related models or files

If found, **UPDATE the existing dot** rather than creating a new one.

### Step 2: Gather Context to Link

**CRITICAL**: Any agent opening this dot should have complete context to continue the work.

Collect and link ALL relevant items:

#### Files Modified
```
- `path/to/file.sql` (line X) - Brief description of change
- `path/to/macro.sql` - What the macro does
```

#### Models Involved
```
| Model | Location | Role |
|-------|----------|------|
| `model_name` | `models/path/to/model.sql` | Description |
```

#### PRs and Commits
```
- PR #123: Title - Status (merged/open/draft)
- Commit: abc1234 - Brief message
```

#### dbt Cloud Jobs
```
| Job | ID | Status | Notes |
|-----|-----|--------|-------|
| Merge Job | 858935 | Success | Used --full-refresh |
```

#### Commands Used
```bash
# Include exact commands that worked
dbt run --full-refresh --select model_name --vars '{"key": "value"}'
```

#### Error Messages (if any)
```
Full error text for searchability
```

#### Related Dots
```
- `dbt-agent/.dots/related-dot.md` - How it relates
```

### Step 3: Write/Update Dot

**Location**: `dbt-agent/.dots/[project]-[short-descriptor].md`

**Naming Convention**:
- `dbt-agent-[feature-name].md` for dbt-agent work
- `dbt-enterprise-[pipeline-name].md` for dbt-enterprise work
- Use kebab-case, keep under 50 chars

**Required YAML Frontmatter**:
```yaml
---
title: "Clear, descriptive title"
status: open | in-progress | closed
priority: 0-4  # 0=P0/critical, 4=nice-to-have
issue-type: feature | bug | epic | research
created-at: "YYYY-MM-DDTHH:MM:SS-08:00"
updated-at: "YYYY-MM-DDTHH:MM:SS-08:00"  # Update on changes
tags: [relevant, tags, for, search]
---
```

**Required Sections**:

```markdown
## Summary
One paragraph: What is this work? Why does it matter?

## Root Cause (if bug)
- What caused the issue
- How it was discovered

## Solution Applied
- What was changed
- Code snippets if relevant

## Key Files
Link ALL files an agent would need to understand/continue this work:
- Macros, models, configs, runbooks, etc.

## Tasks
- [x] Completed task
- [ ] Pending task
- [ ] Blocked task (note why)

## Validation
How to verify the work succeeded:
- Queries to run
- Expected results
- dbt Cloud job to check

## Related
- Link to other dots, PRs, handoffs
```

### Step 4: Link Bidirectionally

If this dot references other dots, **update those dots** to reference back:

```markdown
## Related
- `dbt-agent/.dots/other-dot.md` - Linked from dbt-agent-new-dot.md
```

### Step 5: Report Summary

Output confirmation:

```
## Dot Updated: dbt-agent/.dots/dbt-agent-example.md

**Status**: in-progress
**Tasks**: 3 completed, 2 pending, 1 blocked

**Files Linked**:
- macros/utilities/time_filters.sql
- models/intermediate/.../model.sql
- docs/runbooks/backfill.md

**Next Action**: [What needs to happen next]
```

---

## Quality Checklist

Before finishing, verify the dot has:

- [ ] **Clear title** describing the work
- [ ] **Accurate status** (open/in-progress/closed)
- [ ] **All modified files** linked with paths
- [ ] **All related models** listed with locations
- [ ] **Commands that worked** (exact, copy-pasteable)
- [ ] **Error messages** if troubleshooting (full text)
- [ ] **Validation steps** to verify success
- [ ] **Next actions** if work is incomplete
- [ ] **Bidirectional links** to related dots

---

## Examples

### Good Dot (Complete Context)
```markdown
## Key Files

### Macros
- **`macros/utilities/transactions_time_filters.sql`** (lines 96-104)
  - `transactions_full_refresh_filter` - Environment-aware date filter
  - `batch_full_refresh_filter` - Adds batch vars support

### Models
| Model | Path | Uses Macro |
|-------|------|------------|
| `int_transactions__auth_all` | `models/intermediate/.../enriched_auth/` | batch_full_refresh_filter |
| `mrt_gbos_registration_cohort_progress` | `models/marts/.../customer_lifecycle/` | transactions_full_refresh_filter |

### Runbooks
- **`docs/runbooks/backfill_transactions_job.md`** - Batch loading commands
```

### Bad Dot (Missing Context)
```markdown
## Files
- Changed the macro
- Updated some models
- See PR for details
```

---

## Arguments

| Arg | Description | Default |
|-----|-------------|---------|
| `$ARGUMENTS` | Topic or dot name to create/update | (interactive) |

---

## Usage

```bash
# Create/update dot for current work
/log_work_to_dots

# Create/update specific dot
/log_work_to_dots prod-date-filter-fix

# Log work on specific topic
/log_work_to_dots "batch loading for transaction models"
```
