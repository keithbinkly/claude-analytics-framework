# No Background Agent Overwrites

## Rule

When making multi-file changes — especially with parallel or background agents — never overwrite a file without reading its current state first.

## Required Sequence

```
1. Read the file (get current state)
2. Make the edit (with awareness of current content)
3. Write/Edit the file
```

Never skip step 1. This applies even if you "just wrote" the file — a parallel agent may have modified it since.

## Background Agent Coordination

When multiple agents are running (Task tool, background agents):

- Each agent should read before writing
- If two agents need to edit the same file, make them sequential, not parallel
- Prefer Edit (surgical replacement) over Write (full overwrite) when possible
- If a background agent produces output, merge it — don't clobber existing content

## Verify Background Agent CSS/Structural Output

When a background agent converts or restyles a file (especially CSS transformations):

1. **Grep for all top-level HTML sections** — not just the main wrapper
2. **Check each section has the intended constraints** (max-width, margin, padding)
3. **Sections outside the primary container are the most likely to be missed**

Example: agent converts `.report-body` to single-column with `max-width: 720px`, but `.intro-spread` and `.sources` sit outside that container and go full-width. Always verify edge sections.

## The Bugs This Prevents

- A background agent overwrites a data file with an incompatible format, breaking the page that depends on it
- A CSS conversion agent applies constraints to the main wrapper but misses sibling sections that render full-width
- Source: showcase session 2026-03-17 (consumer finance PDF-to-scroll conversion)
