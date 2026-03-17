# Session Protocol

## Start of Session

1. Call `get_context("current task")` before any action
2. For pipeline work, use slash commands (`/pipeline-resume`, `/pipeline-status`, etc.) — they load the right agents, skills, and knowledge bases automatically
3. Never advance a pipeline phase without explicit user approval at the gate

## During Session

- Be extremely concise. Reference files by path instead of pasting contents.
- Reserve verbose output for: decision rationale, error debugging, QA variance results, architecture trade-offs.
- **Auto-save**: After completing any milestone (ensemble run, experiment, artifact creation, decision), save state to the active workstream file. See `.claude/rules/auto-save-state.md`.

## End of Session

1. Call `complete_task()` to log learnings to the experience store
2. If a QA issue was resolved, log a decision trace to `dbt-agent/shared/decision-traces/traces.json`
3. Scan modified SQL for anti-patterns (see `dbt-qa-standards` rule)

Logging is required, not optional. Without traces, future agents re-investigate already-solved problems.
