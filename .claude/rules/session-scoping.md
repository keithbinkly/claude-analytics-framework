# Session Scoping

## The Problem

Sessions that try to accomplish too many goals hit context window limits, forcing lossy compactions that lose nuance and state.

## Guidance

When a session is getting large (many goals, many files touched, many agent spawns):

1. **Suggest scoping** — "We've accomplished X and Y. Want to save and start a fresh session for Z?"
2. **Don't try to do everything** — completing 2 things well beats partially completing 5
3. **Use workstream files as handoffs** — save state so the next session can pick up cleanly

## When to Suggest Splitting

- Session has completed 2+ distinct deliverables and there's more to do
- You've spawned 3+ sub-agents in a single session
- Multiple unrelated goals are queued ("fix the map AND write the blog post AND update the resume")
- Context is noticeably large (many tool calls, many files read)

## How to Suggest

```
"We've finished the dashboard and the blog post. The resume update is a different
context entirely — want me to save progress and we can tackle that in a fresh session
where I'll have full context budget for it?"
```

## Don't Over-Split

Single-goal sessions that are going well don't need splitting. This guidance is for multi-goal mega-sessions that are visibly running long.
