# Team vs Personal Agent Memory

## Rule

When creating or modifying domain agents, place their memory files based on whether the team benefits from their accumulated knowledge.

| Agent type | Memory location | Git-tracked? |
|-----------|----------------|-------------|
| **Team agent** | `.claude/agent-memory/<name>/` (in analytics-workspace) | Yes |
| **Personal agent** | `~/.claude/agent-memory/<name>/` (machine-local) | No |

## Decision test

> "Would a teammate benefit from this agent's accumulated anti-patterns, decisions, and session history?"

- **Yes** → Team agent. Memory in repo.
- **No** → Personal agent. Memory stays global.

## Current classification

| Team (repo) | Personal (global) |
|------------|-------------------|
| Builder, QA, Context Builder, Analytics Manager | Life Admin, Designer, System Architect |

## When creating a new agent

1. Decide team vs personal using the test above
2. Create 4 memory files: MEMORY.md, napkin.md, decisions.md, session-log.md
3. Add memory loading to the agent definition
4. If team: commit the memory files to git

## Source

Session 2026-03-17: Discovered Builder/QA accumulated knowledge was trapped on one machine. Residency rule revised from "invoked from 2+ repos = global" to "team benefit = repo."
