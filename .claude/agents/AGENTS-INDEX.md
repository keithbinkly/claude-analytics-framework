# Agents Directory

## Domain Agents (Realized)

Domain agents own workstreams, accumulate memory via interior files, and deploy task agents as sub-agents.

| Agent | Definition | Command | Memory | Domain |
|-------|------------|---------|--------|--------|
| **Builder** | `builder.md` | `/builder` | `.claude/agent-memory/builder/` | Design & Build |
| **QA** | `qa.md` | `/qa` | `.claude/agent-memory/qa/` | Validation & Integrity |
| **Context Builder** | `context-builder.md` | `/context-builder` | `.claude/agent-memory/context-builder/` | Semantic Layer & Ontology |
| **Analytics Manager** | `analytics-manager.md` | `/analyst` | `.claude/agent-memory/analytics-manager/` | Business Intelligence |
| **System Architect** | `system-architect.md` | `/system-architect` | `.claude/agent-memory/system-architect/` | Agent Systems & Meta-Infra |

Each domain agent has 3 core interior files:
- `MEMORY.md` — Identity, voice, core commitments (auto-loaded, ≤200 lines)
- `napkin.md` — Corrections, anti-patterns, what didn't work
- `decisions.md` — Choices made with rationale, alternatives rejected

## Task Agents (Specialist Execution)

Task agents are deployed BY domain agents as sub-agents within a session.

| Agent | File | Role | Deployed By |
|-------|------|------|-------------|
| **Pipeline Orchestrator** | `orchestrator.md` | Per-pipeline coordinator, phase management | Builder |
| **QA Analyst** | `qa-agent.md` | Data quality validation, variance analysis | QA |
| **SQL Builder** | `sql-builder-agent.md` | dbt model implementation | Builder |
| **Architect** | `architect.md` | Tech spec design, model inventory | Builder |
| **Data Discoverer** | `discovery-agent.md` | Source profiling, schema validation | Builder, QA |
| **Analyst** | `analyst-agent.md` | Conversational BI via Semantic Layer | Analytics Manager |
| **Learner** | `learner.md` | Knowledge curation, gap detection | Context Builder |

## XML Tag Structure (Task Agents)

Each task agent uses structured XML tags:

| Tag | Purpose |
|-----|---------|
| `<role>` | WHO — identity, personality, approach |
| `<mission>` | WHY — success criteria |
| `<rules>` | MUST/MUST NOT — hard constraints |
| `<method>` | HOW — step-by-step workflow |
| `<anti_patterns>` | Common mistakes to avoid |
| `<evaluation>` | Self-check before delivering |
| `<chain>` | Handoff protocol — who to pass to next |
| `<fallback>` | What to do when stuck |

## Cleanup History

- **2026-02-16**: Created 4 domain agents (Builder, QA, Context Builder, Analytics Manager) with definitions, commands, and seeded interior files (12 files total).
- **2026-02-16**: Deleted 7 v1 backup files (~89KB). Deleted `_agent-registry.md` (superseded by `agent-map.yaml`). Moved `_metrics-capture.md` and `LEARNING-CODIFICATION-QUICK-REFERENCE.md` to `dbt-agent/shared/reference/`.
- **2026-02-17**: Moved System Architect from data-centered to dbt-agent (agent + memory + command). Rationale: most system evolution work targets dbt-agent's tools/skills/hooks.

## Related

- **Repo-local agent manifest**: `.claude/agent-manifest.yaml` (current bootstrap map for this repo)
- **Skills**: `.claude/skills/` — knowledge layer
- **Reference docs**: `dbt-agent/shared/reference/metrics-capture-protocol.md`, `dbt-agent/shared/reference/learning-codification-quick-reference.md`
