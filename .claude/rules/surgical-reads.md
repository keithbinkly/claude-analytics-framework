# Surgical File Reads

## Rule

Before any `Read` call, determine the minimum lines needed. Full-file reads waste context tokens — 358k tokens (36%) were consumed by reads in one session.

## Pattern

1. **Grep first** to find the line number of what you need
2. **Read with offset+limit** — only the section around those lines (typically 20-50 lines)
3. **Full reads only** for files under ~200 lines that haven't been read this session

## Examples

```
WRONG: Read(file_path, limit=2000)  → reads entire 2800-line file
RIGHT: Grep("function renderMap") → line 1322
       Read(file_path, offset=1320, limit=30)

WRONG: Re-read a file you read 5 minutes ago to find one value
RIGHT: Grep for the value, read just that section
```

## When Full Reads Are OK

- First read of a small file (<200 lines)
- Files you need to understand holistically (CLAUDE.md, MEMORY.md, workstream YAML)
- Writing/rewriting an entire file (need to see current state)

## Why

Context variety degrades output quality independent of token count. Every unnecessary full-file read adds noise that competes with the details that matter. Surgical reads keep the context focused on the task.
