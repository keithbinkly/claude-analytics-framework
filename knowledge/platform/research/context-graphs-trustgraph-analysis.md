# Context Graphs & TrustGraph Analysis

**Date:** 2026-01-11
**Type:** Research & Adoption Recommendation
**Scope:** Thought leadership synthesis + TrustGraph evaluation

---

## TL;DR

**Context Graphs Thought Leadership:** The paradigm shift from "systems of record" to "systems of context" is real and directly relevant to dbt-agent. The key insight from the new articles: **reification, not decision traces**—computer systems don't "decide," they produce auditable records of behavior that can be annotated with provenance.

**TrustGraph Adoption:** **PARTIAL ADOPT** — Don't deploy TrustGraph infrastructure (overkill for our use case), but adopt its **conceptual patterns** for our existing KG infrastructure: Context Cores, reification for provenance, and layered knowledge architecture.

---

## Part 1: Thought Leadership Synthesis

### What's New Since Original Synthesis (Jan 8)

Two new articles from Jack Colquitt (TrustGraph creator):

#### 1. "Reification, Not Decision Traces"

**Core argument:** "Decision trace" is a misnomer. Computer systems don't make decisions—decisions are human constructs shaped by goals, incentives, and starting conditions. What we actually capture is **reification**: statements about statements.

**Key examples:**
```
# Simple fact:
Fred -> hasLegs -> 4

# Reified with provenance:
<<Fred -> hasLegs -> 4>>
  assertedBy -> Mark
  assertedDate -> "2026-01-08"
  dataQualityScore -> 0.94
  approvedBy -> data-governance-team
```

**Why this matters for us:**
- Our "decision traces" in `shared/decision-traces/traces.json` are really reified observations
- We capture *what happened* and *who validated*, not a cognitive "decision"
- This framing clarifies what we should actually capture: provenance, approvals, alternatives considered

**New concept: Layered context systems**
1. **Grounding layers** — curated knowledge (our KB, canonical models)
2. **System-of-record layer** — captured behavior (session logs, QA results)
3. **Synthetic grounding** — derived from model outputs (learnings from SpecStory mining)

This enables measuring **context drift** — how far synthetic diverges from ground truth.

#### 2. "Context Graph Manifesto"

**Key insight:** There's no "right way" to store graphs. RDF vs property graphs vs Cassandra all work. The choice is operational preference, not capability.

**Progression roadmap:**
1. LLMs answer from training data
2. RAG: chunk text + vector similarity
3. GraphRAG: relationship-aware retrieval
4. OntologyRAG: controlled vocabulary for precision
5. **Next:** Domain-specific retrieval analytics (temporal, accuracy-sensitive, anomaly)
6. **Future:** Self-describing information stores + autonomous learning

**Where we are:** Between 3-4. We have graphs (KG with 21K chunks) and controlled vocabulary (SKOS from query-log mining), but retrieval isn't graph-traversal yet.

### Updated Philosophy Position

| View | Description | Our Position |
|------|-------------|--------------|
| Decision Traces (Foundation Capital) | Capture at commit time | ⚠️ Reframe as "reification" |
| Systems of Memory (Jaeg Park) | Ingest all raw audio | ❌ Too expensive/privacy concerns |
| Process Knowledge (Glean) | Capture *how*, approximate *why* | ✅ Aligns with dbt-agent |
| **Reification (TrustGraph)** | Statements about statements with provenance | ✅ **Adopt this framing** |

---

## Part 2: TrustGraph Technical Analysis

### What TrustGraph Does

**Core proposition:** Transform fragmented data into interconnected Context Graphs optimized for AI, reducing hallucinations through grounded retrieval.

**Architecture:**
- **Streaming backbone:** Apache Pulsar (persistent queues, replay)
- **Graph storage:** Cassandra (default), Neo4j, Memgraph, FalkorDB
- **Vector storage:** Qdrant (default), Pinecone, Milvus
- **LLM integration:** 40+ providers including Anthropic
- **Deployment:** Fully containerized, Docker Compose, multi-cloud

**Key innovations:**
1. **Context Cores** — modular, reusable knowledge packages that can be loaded/removed at runtime
2. **Fact extraction** — LLM identifies entities/relationships instead of naive chunking
3. **Hybrid retrieval** — combines vector similarity + graph traversal
4. **Reification** — provenance metadata travels with facts

### Comparison: TrustGraph vs dbt-agent Current State

| Capability | TrustGraph | dbt-agent Today | Gap |
|------------|-----------|-----------------|-----|
| Graph storage | Cassandra/Neo4j | JSON files (chunks.json) | Low priority |
| Vector search | Qdrant + hybrid | BM25 keyword only | Medium priority |
| Fact extraction | LLM-driven entity extraction | Markdown chunking | Low priority |
| Context Cores | Modular, runtime loadable | Skills + KB files (static) | **High relevance** |
| Provenance | Built-in reification | Decision traces (incomplete) | **High relevance** |
| Agent integration | Full agentic framework | MCP + skills | We have this |
| Deployment | Docker Compose full stack | Claude Code native | We have simpler |

### Adoption Recommendation: PARTIAL ADOPT

**Don't adopt:**
- ❌ Full TrustGraph deployment (Apache Pulsar, Cassandra, Docker Compose)
- ❌ Replacing our KG infrastructure with TrustGraph's
- ❌ The heavyweight containerized approach

**Reasons:**
1. **Infrastructure overkill** — We're a single-agent system in Claude Code, not a production AI platform
2. **Deployment complexity** — Apache Pulsar + Cassandra + Docker vs our Python-native KG
3. **Integration friction** — TrustGraph designed for standalone deployment, not embedded in existing systems

**Do adopt (patterns, not infrastructure):**

#### Pattern 1: Context Cores Architecture
Apply to our skills system:

```yaml
# Current: Skills are static files
.claude/skills/dbt-migration/SKILL.md

# Future: Skills as Context Cores
context_cores/
├── core_migration_patterns.yaml    # Learned migration workflows
├── core_qa_validation.yaml         # QA resolution patterns
├── core_canonical_usage.yaml       # When/how to reuse canonicals
└── core_exception_handling.yaml    # Historical exceptions as precedent
```

Each core is:
- Dynamically loadable based on task
- Versioned and testable
- Derived from session analysis

#### Pattern 2: Reification for Decision Traces
Update our trace format:

```yaml
# Current format (traces.json):
{
  "id": "qa_2026-01-07_001",
  "pattern": "CI fails with 'materialization not found'",
  "resolution": "Restore macro"
}

# Reified format:
{
  "id": "qa_2026-01-07_001",
  "statement": {
    "subject": "int_dates model",
    "predicate": "requires_materialization",
    "object": "view_create_or_replace"
  },
  "reification": {
    "discovered_by": "qa-agent",
    "discovered_at": "2026-01-07T20:45:00-08:00",
    "verified_by": "ci_run_458a13f",
    "confidence": 0.95,
    "alternatives_rejected": ["standard_view"],
    "precedent_referenced": null
  }
}
```

#### Pattern 3: Layered Knowledge Architecture
```
grounding/           # Curated, canonical (KB files)
├── canonical-models-registry.md
├── migration-quick-reference.md
└── folder-structure-and-naming.md

records/             # System behavior capture (reified)
├── session-logs/
├── decision-traces/
└── qa-results/

synthetic/           # Model-derived learnings
├── specstory-extracted-patterns/
├── session-consolidation/
└── drift-measurements/
```

Enable drift measurement: compare synthetic against grounding.

---

## Part 3: Recommended Actions

### Immediate (This Session)

1. **Update RESOURCES.md** — Add TrustGraph with PARTIAL ADOPT status
2. **Create skill framework** — Design `context-graph-expert` skill

### Short-term (Next Week)

3. **Create Bead:** Implement reified trace format in `shared/decision-traces/`
4. **Create Bead:** Design Context Cores architecture proposal

### Medium-term (Next Month)

5. **Evaluate:** Add vector search to KG (qmd + embeddings)
6. **Implement:** Context drift measurement (synthetic vs grounding)

---

## Part 4: Context Graph Expert Skill Scope

The skill should enable Claude to:

1. **Synthesize thought leadership** — Understand competing philosophies (Foundation Capital, Jaeg Park, Glean, TrustGraph)
2. **Apply concepts** — Map context graph patterns to dbt-agent infrastructure
3. **Stay current** — Use Exa/web search to find new developments
4. **Create artifacts** — Generate perspective pieces when warranted
5. **Advise on tooling** — Evaluate new tools against our architecture

**Knowledge corpus:**
- Original synthesis (23 articles)
- New articles (reification, manifesto)
- TrustGraph documentation
- Our existing context infrastructure analysis

---

## Sources

- [TrustGraph - Context Graph Factory](https://trustgraph.ai/)
- [TrustGraph GitHub](https://github.com/trustgraph-ai/trustgraph)
- [Reification not Decision Traces](https://trustgraph.ai/news/decision-traces-reification/)
- [Context Graph Manifesto](https://blog.trustgraph.ai/)
- [TrustGraph + Qdrant Case Study](https://qdrant.tech/blog/case-study-trustgraph/)
- [Knowledge Cores: Memento Nightmare](https://blog.trustgraph.ai/p/how-trustgraph-s-knowledge-cores-end-the-memento-nightmare)
- [TrustGraph Documentation](https://docs.trustgraph.ai/overview/)

---

*Generated by Learner Agent session on 2026-01-11*
