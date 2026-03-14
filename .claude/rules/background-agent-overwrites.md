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

## The Bug This Prevents

A background agent overwrites a data file with an incompatible format, breaking the page that depends on it. The main agent doesn't notice because it wrote the page first and assumed the data file was stable.
