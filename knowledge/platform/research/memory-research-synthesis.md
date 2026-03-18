# Agent Memory Research Synthesis
**Date:** 2026-03-15
**Scope:** 7 user-provided resources + 6 deep-read papers from the paper list
**Purpose:** Extract patterns, validate our unified knowledge graph approach, identify gaps

---

## Executive Summary

The agent memory field has **exploded** since late 2024. The paper list alone tracks 200+ papers across three memory types (factual, experiential, working) and three representations (token-level, parametric, latent). The key finding for us: **our unified knowledge graph plan aligns with the cutting edge, but we're missing three patterns that the research strongly validates.**

### Three Patterns We Should Adopt

1. **Bidirectional memory updating** (A-MEM, NeurIPS 2025) — new knowledge retroactively enriches existing nodes
2. **Tiered memory hierarchy** (OpenViking, EverMemOS) — L0/L1/L2 loading, not all-or-nothing
3. **Evolving playbooks** (ACE) — contexts accumulate and self-refine through execution feedback

### What We're Already Doing Right

- Graph-based knowledge organization (validated by HippoRAG, Mem0, A-MEM)
- Session-to-learning pipeline (validated by EverMemOS, ACE, ExpeL)
- Curator gate / feedback loop (validated by Context Hub, ACE, AutoContext)
- Disconnected stores problem identified (validated by OpenViking's diagnosis)

---

## Resource Triage Matrix

| # | Resource | Type | Relevance | Verdict | Deep Read? |
|---|----------|------|-----------|---------|------------|
| 1 | Agent Memory Paper List | Index | HIGH | REFERENCE | Index scanned, 6 papers deep-read |
| 2 | DeepAgents (LangChain) | Framework | MEDIUM | DEFER | Batteries-included harness, useful patterns but framework-bound |
| 3 | OpenViking (ByteDance) | System | HIGH | ADOPT patterns | L0/L1/L2 hierarchy + filesystem paradigm highly relevant |
| 4 | Context Hub (Andrew Ng) | Tool | MEDIUM-HIGH | ADOPT pattern | Annotation persistence + feedback loop validates our curator gate |
| 5 | Skeleton of Thought | Technique | LOW | NOTE | Parallel expansion — useful for ensemble, not memory |
| 6 | Multi-Agent Memory (2603.10062) | Paper | HIGH | ADOPT framing | Computer architecture lens on multi-agent memory |
| 7 | ACE: Agentic Context Engineering | Paper | VERY HIGH | ADOPT | Evolving playbooks = exactly what our learnings should become |
| 8 | A-MEM (Zettelkasten) | Paper | VERY HIGH | ADOPT | Bidirectional memory updating directly applicable |
| 9 | HippoRAG / HippoRAG 2 | Paper | HIGH | INFORM design | KG + PageRank validates our graph search approach |
| 10 | Mem0 | Paper | MEDIUM | DEFER | Production system, graph-based, but heavier than we need |
| 11 | EverMemOS | Paper | HIGH | ADOPT patterns | MemCell → MemScene lifecycle maps to our extraction → distillation |
| 12 | GAM (General Agentic Memory) | Paper | MEDIUM | NOTE | JIT compilation of context at query time — interesting but complex |

---

## Deep Analysis: High-Priority Resources

### 1. A-MEM: Zettelkasten Memory (NeurIPS 2025)

**Paper:** arXiv:2502.12110 | **Verdict:** ADOPT

**Core insight:** When a new memory is added, the system doesn't just store it — it:
1. Generates structured notes with keywords, tags, contextual descriptions
2. Searches for related existing memories
3. **Creates links** between new and existing memories
4. **Retroactively updates** existing memories with new context

**Why this matters for us:** Our current pipeline is *write-only*. When we distill a new learning about "incremental merge," it gets stored with its own tags, but existing learnings about related topics (Redshift performance, CI failures, delete+insert) **don't get updated to reference the new one.** A-MEM says: every new memory should trigger a backward pass that enriches the existing graph.

**Concrete adoption:** In Phase 1 of our unified knowledge graph, after building nodes, add a step that:
- For each new node, searches for related existing nodes by topic overlap
- Creates `related` edges automatically
- Updates existing nodes' `topics` lists if the new node reveals a connection they didn't have

This is precisely the "cross-store edge inference" step in our plan, but A-MEM validates it should also **modify existing nodes**, not just add edges.

---

### 2. ACE: Agentic Context Engineering

**Paper:** arXiv:2510.04618 | **Verdict:** ADOPT

**Core insight:** Contexts should be treated as **evolving playbooks** that accumulate, refine, and organize strategies through:
- **Generation** — create initial context from task experience
- **Reflection** — analyze what worked and didn't
- **Curation** — prune, merge, and reorganize

**Two failure modes they identify (we have both):**
- **Brevity bias** — distillation strips domain insights for conciseness. Our learnings like "Be careful with incremental models" are brevity-biased.
- **Context collapse** — iterative rewriting erodes details over time. We've seen this when learnings get reworded across distillation cycles.

**Their fix: structured, incremental updates.** Instead of rewriting a learning, append new evidence. Instead of replacing a playbook, extend it with new sections.

**Concrete adoption:** Change our distillation pipeline from "rewrite learning" to "append evidence to learning." Each learning entry gets an `evidence_log`:
```yaml
- id: efx-007
  trigger: "Merge with composite keys causes inflation"
  action: "Use delete+insert with unique_key='calendar_date'"
  evidence_log:
    - date: 2026-03-04
      session: "session-84"
      outcome: "Fixed 10-27x per-row inflation"
    - date: 2026-03-15
      session: "session-112"
      outcome: "Loaded, user didn't need to correct agent"
```

This directly connects to our curator gate — the evidence_log IS the feedback data.

**Bonus:** ACE matches the top AppWorld leaderboard agent using a smaller model, specifically because accumulated context compensates for model size. Validates our approach of loading learnings at session start.

---

### 3. OpenViking: Context Database (ByteDance)

**Repo:** github.com/volcengine/OpenViking | **Verdict:** ADOPT patterns

**Core insight:** Abandon the "dump everything into context" approach. Use **L0/L1/L2 three-tier structure, loaded on demand:**

| Tier | What | When Loaded | Our Equivalent |
|------|------|-------------|----------------|
| L0 | System identity, core rules | Always | `.claude/rules/`, CLAUDE.md |
| L1 | Domain knowledge, skill summaries | On keyword match | Skills, learning retrieval |
| L2 | Full details, raw data, examples | On explicit request | Skill resources, decision traces |

**Why this matters:** We currently load L0 (rules, CLAUDE.md) always, but L1 and L2 are haphazard. Sometimes a skill's full SKILL.md gets loaded (expensive) when just its 1-line trigger/action summary would suffice. Sometimes a decision trace is needed but never loaded because there's no retrieval path.

**Concrete adoption:** Our unified graph should have a `detail_level` field on each node:
- `L0`: Always injected (title + 1-line summary, ~50 tokens)
- `L1`: Loaded on topic match (summary + relationships, ~200 tokens)
- `L2`: Loaded on explicit traversal (full content from underlying store)

The graph search function returns L1 by default, L2 only when depth > 1.

**Their other key insight:** "Visualization of directory retrieval trajectories" — let users see WHY a piece of context was retrieved. Our graph search should include `retrieval_path` showing which topic match → which edge → which related node.

---

### 4. EverMemOS: Memory Operating System

**Paper:** arXiv:2601.02163 | **Verdict:** ADOPT lifecycle pattern

**Core insight:** Memory has a **lifecycle** inspired by neuroscience engrams:

```
Dialogue → Episodic Traces (MemCells) → Semantic Consolidation (MemScenes) → Reconstructive Recollection
```

**Mapped to our system:**

| EverMemOS | Our System | Status |
|-----------|-----------|--------|
| Episodic Traces (MemCells) | Experience extraction (chatops-session-extract.py) | Working |
| Semantic Consolidation (MemScenes) | Distillation pipeline (importance_scorer → distillation_staging) | Working |
| User Profile Updates | Learning KB updates (shared/learnings/*.yaml) | Working |
| Reconstructive Recollection | learning_retrieval.py → session-start hook | Working but primitive |

**What we're missing:** "Foresight signals" — EverMemOS extracts time-bounded predictions from conversations. When a user says "we're freezing merges after Thursday," that becomes a MemCell with an expiry date. Our system doesn't capture temporal context.

**Concrete adoption:** Add optional `valid_until` and `valid_from` fields to learning nodes. Learnings about temporary states (merge freezes, CI environment issues, in-progress migrations) should expire.

---

### 5. HippoRAG: Hippocampus-Inspired Retrieval

**Paper:** arXiv:2405.14831 | **Verdict:** INFORM design

**Core insight:** Use **Personalized PageRank** on a knowledge graph for retrieval instead of flat vector similarity. When a query arrives:
1. Find seed nodes that match the query
2. Run PageRank from those seeds — nodes connected to seeds by many paths rank higher
3. Retrieve the top-ranked nodes

**Why it matters:** Single-step HippoRAG matches or beats iterative RAG (IRCoT) while being 10-30x cheaper. The graph structure makes multi-hop reasoning automatic — you don't need to retrieve → reason → retrieve again.

**For our unified graph:** Our plan's `_match_nodes()` → `_traverse()` approach is a simplified version of this. If we ever need more sophisticated ranking, Personalized PageRank is the proven algorithm. For now, our topic overlap + edge traversal is sufficient at our scale (150-300 nodes), but this validates the graph approach.

---

### 6. Multi-Agent Memory: Computer Architecture Perspective

**Paper:** arXiv:2603.10062 | **Verdict:** ADOPT framing

**Core insight:** Multi-agent memory should be modeled like computer memory architecture:

| CPU Concept | Agent Concept | Our System |
|-------------|--------------|-----------|
| Registers | Working context (current message) | Claude's context window |
| L1 Cache | Recently-used knowledge | Auto-loaded rules + learnings |
| L2 Cache | Domain knowledge pool | Skills, reference docs |
| Main Memory | Full knowledge base | All 9 stores |
| Disk | Historical archive | SpecStory transcripts, raw sessions |

**Two critical missing protocols they identify:**
1. **Cache sharing** across agents — when one agent learns something, how do others get it?
2. **Memory consistency** — how do you prevent stale reads when knowledge is updated?

**For us:** We already have the cache sharing problem. When a background agent discovers something during an ensemble run, it writes to `session-logs/` but the main agent may never read it. And memory consistency — when a learning gets updated, sessions that loaded the old version don't know.

**Concrete adoption:** The unified graph index becomes our "shared L2 cache." The `built_at` timestamp + staleness detection (Phase 5 of our plan) addresses consistency. For cache sharing: background agents should write findings back to the graph index, not just to session logs.

---

## Medium-Priority Resources

### DeepAgents (LangChain)

**What it is:** An opinionated agent harness with auto-summarization, file-based context management, and sub-agent spawning.

**Relevant pattern:** Their `write_todos` planning tool and automatic context summarization when conversations get long. We already have dots/tasks for planning, but their auto-summarization is interesting — it triggers at a threshold rather than waiting for compaction.

**Verdict:** DEFER. Framework-specific patterns, not easily extractable.

### Context Hub (Andrew Ng)

**What it is:** CLI for agents to search, fetch, and annotate documentation with persistent notes.

**Key insight:** **Annotations that persist across sessions.** When an agent reads a doc and notes "this section was misleading about X," that note appears for every future agent that reads the same doc.

**For us:** Our skills don't have persistent annotations. When we discover that a skill's instructions are wrong or incomplete during a session, we either fix the skill (heavy) or forget (common). A lightweight annotation layer — "this skill's Step 3 is outdated as of 2026-03" — would be cheaper than rewriting.

**Verdict:** ADOPT pattern. Could be implemented as a JSON sidecar per skill.

### Skeleton of Thought

**What it is:** Prompt technique — outline first, then fill sections in parallel. 2.39x speedup on structured tasks.

**For us:** Already relevant to how our ensemble works (4 analysts run in parallel). Could inform how `/analyze` structures its synthesis step — outline the answer structure first, then fill each section from analyst outputs.

**Verdict:** NOTE. Low priority but conceptually interesting.

### GAM: General Agentic Memory

**What it is:** JIT compilation of memory — lightweight offline storage, full context assembled at query time.

**For us:** Validates our L0/L1/L2 approach from OpenViking. GAM's "Memorizer" = our index builder. GAM's "Researcher" = our graph search with content fetching.

**Verdict:** NOTE. Confirms direction.

### Mem0

**What it is:** Production memory system (26% improvement, 91% lower latency, 90% token savings vs full-context).

**Key architecture:** Dynamic extraction + consolidation + graph-based retrieval. Two variants — base (flat) and enhanced (graph).

**For us:** Their "90% token savings" validates that selective retrieval (our L0/L1/L2 approach) dramatically outperforms loading everything. Their graph variant outperforms their flat variant, confirming our move from flat file search to graph index.

**Verdict:** DEFER. Validates our approach but no new patterns to extract.

---

## Landscape Map: Where We Sit

The field has converged on a clear architecture pattern. Here's how every system relates:

```
                    STORE                 ORGANIZE               RETRIEVE              LEARN
                    ─────                 ────────               ────────              ─────
HippoRAG           KG triples            PageRank               Graph walk            ✗
A-MEM              Zettelkasten notes     Bidirectional links    Tag + link match      Backward update
EverMemOS          MemCells → MemScenes  Thematic clustering    Scene-guided search   Consolidation
ACE                Playbook sections      Gen/Reflect/Curate     Topic match           Execution feedback
Mem0               Dynamic extracts       Graph edges            Hybrid vector+graph   Feedback weights
OpenViking         Filesystem dirs        L0/L1/L2 hierarchy     Directory + semantic  Self-evolution
Context Hub        Markdown + annotations Version control        CLI search            User feedback
AutoContext         Playbooks + lessons    Coach/Curator agents   Role-based            Tournament ELO
Cognee             Graph + vectors        Entity extraction      Hybrid search         Feedback weights

OUR SYSTEM          9 stores (flat files)  ✗ (disconnected)      Per-store search      Curator gate
OUR PLAN            Unified graph index    Topic + edge links     Graph traversal       Weight adjustment
```

**The gap is clear:** We have the STORE and RETRIEVE layers. We're building ORGANIZE (the graph index). Our LEARN layer (curator gate) is primitive. Every cutting-edge system has a more sophisticated learning mechanism.

---

## Recommended Enhancements to Unified Knowledge Graph Plan

Based on this research, I recommend these additions to `thoughts/shared/plans/unified-knowledge-graph-plan.md`:

### Enhancement 1: Bidirectional Memory Updating (from A-MEM)

Add to Phase 1, Step 1.2.8 (Cross-Store Edge Inference):
```
When building a new node, not only CREATE edges to existing nodes,
but also UPDATE existing nodes' topics lists to reflect the new connection.
If efx-030 is about "semantic layer CI" and links to existing node
"skill-semantic-layer", add "ci-cd" to the skill node's topics.
```

### Enhancement 2: L0/L1/L2 Detail Levels (from OpenViking)

Add `detail_level` field to Node schema:
```json
{
  "efx-007": {
    "detail_level": "L1",
    "l0_summary": "delete+insert beats merge on Redshift composite keys",
    "l1_summary": "Merge with 10-16 col unique keys causes per-row inflation at month boundaries. Fix: delete+insert with unique_key='calendar_date'.",
    "l2_content_path": "shared/learnings/cross-cutting/dbt-qa.yaml#efx-007"
  }
}
```

Graph search returns L0 for related nodes, L1 for direct matches, L2 only on explicit request.

### Enhancement 3: Evidence Accumulation (from ACE)

Add optional `evidence_log` to learning nodes. Instead of rewriting learnings during distillation, append evidence:
```json
{
  "evidence_log": [
    {"date": "2026-03-04", "session": "84", "outcome": "fixed", "note": "10-27x inflation resolved"},
    {"date": "2026-03-15", "session": "112", "outcome": "prevented", "note": "loaded, no correction needed"}
  ]
}
```

### Enhancement 4: Temporal Validity (from EverMemOS)

Add optional `valid_from` / `valid_until` fields:
```json
{
  "valid_from": "2026-03-04",
  "valid_until": null,
  "temporal_note": "Permanent — Redshift behavior, not a temporary workaround"
}
```

Nodes past `valid_until` get weight reduced to 0.3 (not deleted — may still be informative).

### Enhancement 5: Retrieval Path Transparency (from OpenViking)

Graph search results should include the traversal path:
```
efx-007 (direct topic match: "merge")
  → related to: rule-incremental-merge (edge: reinforces, topic overlap: 0.6)
    → related to: skill-redshift-opt (edge: elaborated_in, topic overlap: 0.4)
```

This helps debug retrieval quality and builds user trust in the system.

---

## Papers Worth Tracking (for future deep reads)

From the paper list, these are the most relevant to our work but I didn't have time to deep-read:

| Paper | Why Track |
|-------|-----------|
| **ExpeL** (2023, experiential learning) | Foundational paper on learning from agent execution — our pipeline is an ExpeL variant |
| **SkillWeaver** (2504.07079) | Auto-generating reusable skills from agent experience — relevant to compound-learnings |
| **Agent Workflow Memory** (2024) | Workflow-specific memory — relevant to our pipeline-specific learnings |
| **Dynamic Cheatsheet** (2504.07952) | Precursor to ACE — lighter weight evolving context |
| **LEGOMem** (2510.04851) | Modular memory composition — relevant to our multi-store architecture |
| **Reflexion** (2303.11366) | Self-reflection for agent improvement — foundational for our learning loop |
| **Generative Agents** (2304.03442) | The original — memory retrieval with recency/importance/relevance scoring |

---

## CAF Super-Repo Integration

The unified knowledge graph must account for the move to `claude-analytics-framework` (CAF) as the canonical root:

- **Graph index lives in CAF** (`knowledge/platform/graph/unified-index.json`) — it's a control-plane function
- **3 domains** (agent, business, platform) across 4 repos (CAF, dbt-agent, dbt-enterprise, data-centered)
- **Migration-aware**: `promoted_to_caf` flag tracks which dbt-agent assets have been promoted
- **Repo-adapters.yaml** for path resolution — no hardcoded absolute paths
- **Scoped retrieval**: session hooks load agent domain, ensemble loads business domain

See `thoughts/shared/plans/unified-knowledge-graph-plan.md` for the full 5-phase implementation plan with CAF integration addendum.

## Bottom Line

The research validates our direction but reveals we're building a **first-generation system** when the field is at **third generation:**

- **Gen 1** (us, current): Store → Retrieve. Flat files, keyword search, manual curation.
- **Gen 2** (our plan): Store → Organize → Retrieve. Graph index, cross-store edges, topic matching.
- **Gen 3** (A-MEM, ACE, EverMemOS): Store → Organize → Retrieve → Learn → Reorganize. Bidirectional updating, evidence accumulation, temporal validity, execution feedback that modifies the graph structure itself.

The 5 enhancements above bridge us from Gen 2 to Gen 3 without adding infrastructure complexity. They're all additions to the existing plan — JSON fields, Python logic, no new databases.
