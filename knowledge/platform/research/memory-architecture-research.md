# Project Update: Memory Architecture Research & Capability Expansion

**Date:** December 3, 2025
**Session Type:** Deep Resource Analysis & Strategic Planning
**Duration:** ~45 minutes

---

## TL;DR

Deep-dived into 8 cutting-edge resources on AI agent memory, context engineering, and knowledge quality. Discovered three capability expansion vectors that could transform our agents from stateless tools to learning systems with shared memory. Created 4 high-priority Beads for implementation.

---

## What We Did

### 1. Deep Analyzed 8 External Resources

| Resource | Type | Impact Rating |
|----------|------|---------------|
| [Momo Research: Context Engineering](https://github.com/momo-personal-assistant/momo-research) | Memory Architecture | **HIGH** |
| [Spark: Shared Memory Paper](https://arxiv.org/html/2511.08301v1) | Academic Research | **HIGH** |
| [Semiosis: KB Unit Testing](https://github.com/AnswerLayer/semiosis) | Quality Framework | **HIGH** |
| [Memory in AI Agents](https://www.leoniemonigatti.com/blog/memory-in-ai-agents.html) | Taxonomy/Blog | Medium |
| [Holy Trinity for Enterprise Data](https://substack.com/inbox/post/179387219) | Meta Grid Pattern | Medium |
| [OSGym](https://github.com/agiopen-org/osgym) | Agent Infrastructure | Watch |
| [Simular.ai](https://www.simular.ai/) | Computer Use | Watch |
| Browser.cash | Browser Automation | Deferred |

### 2. Identified Three Capability Expansion Vectors

| Vector | What It Enables | Implementation Priority |
|--------|-----------------|------------------------|
| **Memory Architecture** | Agents learn across sessions, share knowledge | P0 - Start immediately |
| **Knowledge Quality** | Measure if KB actually works, find redundancy | P1 - Next quarter |
| **Agent Infrastructure** | Computer/browser use capabilities | P3 - Future state |

### 3. Designed Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORY ARCHITECTURE                        │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   WORKING    │   SEMANTIC   │   EPISODIC   │   PROCEDURAL   │
│ (Claude ctx) │ (KB + KG)    │ (session-logs)│ (Skills)       │
├──────────────┴──────────────┴──────────────┴────────────────┤
│                     MEMORY MANAGER (NEW)                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐ │
│  │ Extraction │  │ Consolidation│  │ Retrieval            │ │
│  │ (patterns) │  │ (dedupe)    │  │ (memory-as-tool)     │ │
│  └────────────┘  └────────────┘  └────────────────────────┘ │
├──────────────────────────────────────────────────────────────┤
│                     EXPERIENTIAL LOOP                        │
│  Session → Capture → Extract → Cluster → Curate → Share     │
└──────────────────────────────────────────────────────────────┘
```

---

## Why This Matters

### Current State (Stateless Agents)

| Problem | Impact |
|---------|--------|
| Migration agent solves auth issue | Solution lost when session ends |
| QA agent encounters same issue | Solves from scratch (duplicated effort) |
| Patterns discovered in sessions | Only saved if Learner runs manually |
| No way to know if KB is effective | 21K chunks, unknown usefulness |

### Target State (Learning System)

| Capability | Benefit |
|------------|---------|
| **Shared Memory** | One agent learns → all agents know |
| **Session Consolidation** | Patterns auto-extracted after each session |
| **Memory-as-Tool** | Agents query past solutions on demand |
| **KB Quality Metrics** | Know which docs work, which are redundant |

### Key Research Finding

From Spark paper: **Small models benefit most from shared memory**
- Qwen3-30B: +0.66 improvement (13.2%)
- GPT-5: +0.05 improvement (1%)

**Implication:** Our investment in KB/memory infrastructure provides maximum value. It's not about having the best model - it's about having the best memory system.

---

## What's Next (Tracked in Beads)

| Bead | Task | Priority | Effort |
|------|------|----------|--------|
| `dbt-agent-z5d` | Build Memory Manager module (`tools/memory/`) | P1 | 2 days |
| `dbt-agent-o47` | Implement Session Consolidation (Spark experiential loop) | P1 | 3 days |
| `dbt-agent-fdu` | Build KB Quality Testing (Semiosis-inspired) | P2 | 4 days |
| `dbt-agent-5y0` | Implement Memory-as-a-Tool for agent queries | P2 | 2 days |

### Implementation Phases

**Phase 1: Memory Architecture (Weeks 1-2)**
- Create `tools/memory/` module foundation
- Implement session consolidation pipeline
- Build memory-as-a-tool for agent access
- Connect to Beads for cross-session tracking

**Phase 2: KB Quality (Weeks 3-4)**
- Create `tools/semiosis/` module
- Build baseline measurement framework
- Implement redundancy detection
- Generate first KB quality report

**Phase 3: Meta Coordination (Weeks 5-6)**
- Design Meta Grid index across all repositories
- Build cross-repository search
- Integrate with Learner Agent

---

## How to Use This

### For Developers Building Memory System

**Key patterns from Momo/Manus:**
```python
# Restorable Compression
# Drop content but preserve references for later retrieval
chunk = {"content": None, "source": "migration-quick-reference.md", "lines": "45-67"}

# Memory-as-Tool
def remember(query: str) -> list[Memory]:
    """Agent calls this when it needs past solutions."""
    return memory_manager.retrieve(query, limit=5)

# Experiential Loop (after each session)
def consolidate(session_log: str) -> list[Pattern]:
    """Extract generalizable patterns from session."""
    raw_events = parse_session(session_log)
    patterns = extract_patterns(raw_events)
    clustered = cluster_by_similarity(patterns, existing_patterns)
    return curate_for_kb(clustered)
```

**Key patterns from Semiosis:**
```python
# KB Quality Testing
def test_kb_criticality(file: str) -> float:
    """How much does removing this file hurt agent performance?"""
    baseline = run_task(with_kb=True)
    intervention = run_task(without_file=file)
    return (baseline.success - intervention.success) / baseline.success

# If criticality > 0.3, file is critical
# If criticality < 0.1, file may be redundant
```

### For the Learner Agent

The Enhanced Evaluation Framework (v2.0) was added to `.claude/commands/learner.md`:
- Phase 1: Initial Triage (Knowledge Manager pattern)
- Phase 2: Multi-Source Synthesis (when evaluating 2+ resources)
- Phase 3: Integration (existing workflow)

---

## Metrics

| Metric | Value |
|--------|-------|
| Resources evaluated | 8 |
| High-impact discoveries | 3 (Momo, Spark, Semiosis) |
| Beads created | 4 |
| RESOURCES.md entries added | 8 |
| Capability vectors identified | 3 |
| Learner Agent enhancements | 1 (Enhanced Evaluation Framework v2.0) |

---

## Files Changed

```
Modified:
  docs/RESOURCES.md                           # Added 8 evaluated resources with integration notes
  .claude/commands/learner.md                 # Added Enhanced Evaluation Framework v2.0

Created:
  docs/updates/2025-12-03-memory-architecture-research.md  # This file
```

---

## Key Quotes to Remember

From Momo (Context Engineering):
> "Context engineering: the process of dynamically assembling and managing info within an LLM's context window to enable stateful agents."

From Spark (Shared Memory):
> "Smaller models benefited most, suggesting room for improvement in their base capabilities."

From Semiosis (KB Testing):
> "Like unit tests verify code correctness, Semiosis deploys standardized measurement probes that apply interventions and measure performance degradation."

From Holy Trinity (Meta Grid):
> "LLMs trained on fragmented glossaries and inconsistent lineage will hallucinate."

---

*Generated by Learner Agent session on 2025-12-03*
