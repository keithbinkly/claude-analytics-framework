# Context Graphs & Knowledge Engineering: Synthesis for dbt-agent

**Research Date**: January 8, 2026
**Sources**: 23 X articles + web research on TrustGraph, Anthropic, Cognizant, dbt Labs

---

## Executive Summary

A paradigm shift is emerging from **systems of record** (what happened) to **systems of context** (why it happened). The dbt-agent environment is exceptionally well-positioned to capture this shift—the semantic layer already encodes metric definitions as knowledge, and the infrastructure for decision traces exists but isn't fully instrumented.

**Key insight**: Context graphs aren't about graph databases. They're about capturing the **decision traces**—the exceptions, overrides, approvals, and precedents that currently evaporate into Slack threads and Zoom calls.

---

## The Core Thesis

### What Context Graphs Capture

| Traditional Systems | Context Graphs |
|---------------------|----------------|
| **State**: Deal stage changed to "Closed Won" | **Trace**: VP approved 20% discount based on 3 SEV-1 incidents, referencing Q3 precedent with similar customer |
| **Fact**: Pipeline ran successfully | **Trace**: Used staging model A instead of B because analyst verified schema via `dbt show` first—avoided hallucinated column error |
| **Record**: Model created in `marts/` folder | **Trace**: Placed in `marts/finance/` after checking canonical model registry; reused 87% from existing patterns |

### Why This Matters for Enterprise AI

> "Rules tell an agent what should happen in general. Decision traces capture what happened in this specific case."
> — Jaya Gupta, Foundation Capital

Without decision traces, AI agents:
- Re-discover the same edge cases repeatedly
- Can't reference precedent for similar situations
- Lose institutional knowledge when employees leave
- Make decisions that "sound right" but violate unwritten rules

---

## Three Competing Philosophies

### 1. Decision Traces at Orchestration Layer (Foundation Capital)

**Core idea**: Capture at commit time when agent makes decisions. Emit structured traces: inputs gathered, policy evaluated, exception route invoked, who approved, what state written.

**Advantage**: In the write path, not read path. Context captured at moment of decision.

**Limitation**: Only captures what flows through instrumented systems.

### 2. Systems of Memory (Jaeg Park critique)

**Core idea**: Decision traces are just "receipts"—capture raw audio of the business instead. Ingest Slack threads, Zoom calls, email chains. Structure emerges from the mess.

**Advantage**: Captures reasoning that happens in the gaps between systems.

**Limitation**: Expensive to process; privacy concerns; not all important context is recorded.

### 3. Process Knowledge (Glean refinement)

**Core idea**: "You can't reliably capture the *why*; you can capture the *how*." The *how* leaves digital trails. Over many cycles, process traces approximate the *why*.

**Advantage**: Pragmatic—captures observable patterns without requiring intent modeling.

**Our position**: This aligns best with dbt-agent. We capture the *how* in transformation logic, test definitions, and QA sessions.

---

## Context Engineering for AI Agents

### Anthropic's Principles (January 2026)

| Principle | Description | dbt-agent Application |
|-----------|-------------|----------------------|
| **Just-in-time retrieval** | Don't load all data upfront; maintain identifiers and fetch dynamically | MCP tools fetch manifest data on demand |
| **Hybrid approaches** | Balance pre-loaded context with autonomous exploration | CLAUDE.md + grep/glob exploration |
| **Compaction** | Summarize history while preserving architectural decisions | Session summaries preserving QA findings |
| **Structured note-taking** | Persistent external memory (NOTES.md) | Decision trace files in handoffs |
| **Sub-agent architectures** | Specialized agents return distilled summaries | Learner, Analyst, Architect, QA agents |

### The Formula

```
Effective Agent = Constraints + Context Packet + Oracle + Loop
```

- **Constraints**: Laws of physics (p99 targets, invariants, forbidden actions)
- **Context Packet**: Curated collision points (canonical models, prior art, not full repo dump)
- **Oracle**: Definition of done (QA templates, variance thresholds, tests)
- **Loop**: Small diffs, run checks, iterate

---

## dbt-agent: Current State Analysis

### What We Already Have (Context Infrastructure)

| Asset | Function | Context Graph Analog |
|-------|----------|---------------------|
| **Semantic Layer** (68 metrics) | Governed metric definitions | Knowledge graph of business logic |
| **Canonical Models Registry** | Reusable patterns (87% reuse rate) | Platform/primitives layer |
| **QA Templates 1-4** | Validation methodology | Oracle definitions |
| **SpecStory Archives** | Historical sessions (31 sessions, 358K lines) | Raw decision trace material |
| **Query Log Mining Output** | Controlled vocabulary, join library | Process pattern extraction |

### What's Missing (Decision Trace Gaps)

| Gap | Impact | Potential Solution |
|-----|--------|-------------------|
| **Why this canonical model?** | Re-discovery of same decisions | Handoff field: "Precedent referenced" |
| **Who approved exception?** | No audit trail for deviations | Handoff field: "Exception approved by" |
| **What alternatives considered?** | Lost exploration context | Decision trace: "Approaches rejected" |
| **Process patterns** | Tribal knowledge | SpecStory corpus mining |

---

## Recommended Implementation Path

### Phase 1: Instrument Handoff Packages (Low effort, high value)

Add decision trace fields to existing handoff templates:

```yaml
decision_trace:
  precedent_referenced: "LINK_OR_DESCRIPTION"
  exception_granted: false
  exception_approver: null
  exception_rationale: null
  alternatives_considered:
    - approach: "Build from scratch"
      rejected_because: "Canonical model covers 87% of requirements"
    - approach: "Extend existing pipeline X"
      rejected_because: "Different grain, would require breaking changes"
  canonical_models_reused:
    - model: "fct_daily_account_balance"
      reuse_pct: 90
```

### Phase 2: SpecStory Mining (Medium effort)

Create session summary extraction using the 4-category framework:

1. **Plans**: What was the stated objective? How was it decomposed?
2. **Knowledge**: What facts were discovered or confirmed?
3. **Decisions**: What choices were made and why?
4. **Lessons Learned**: What worked? What failed? What should be different next time?

Delegate to Learner agent (already ticketed as Bead `dbt-agent-4c3` for dbt-enterprise QA sessions).

### Phase 3: Process Pattern Mining (Higher effort)

Analyze SpecStory corpus to extract:
- Recurring workflow patterns
- Common failure modes and resolutions
- Schema validation sequences
- Exception handling approaches

This becomes the "process knowledge" layer—the *how* that approximates the *why*.

### Phase 4: Context Cores (Future)

Inspired by TrustGraph architecture—modular, reusable context bases:

```
context_cores/
├── core_migration_patterns.yaml    # Learned migration workflows
├── core_qa_validation.yaml         # QA resolution patterns
├── core_canonical_usage.yaml       # When/how to reuse canonicals
└── core_exception_handling.yaml    # Historical exceptions as precedent
```

Dynamically load relevant cores based on task type.

---

## TrustGraph Architecture Insights

From web research, TrustGraph implements:

- **Automated Context Graph Construction**: Transforms raw data → interconnected structures with ontology-driven engineering
- **Context Cores**: Reusable, modular context bases—dynamically loaded/removed at runtime
- **GraphRAG**: Combines context graphs with vector search for retrieval
- **Agent-powered extraction**: ReAct framework enables agents to autonomously populate knowledge graph

**Relevance to dbt-agent**: The Context Cores pattern maps well to our skills/knowledge-base architecture. Each skill could have an associated "context core" that loads relevant decision traces and patterns.

---

## Key Takeaways

### 1. dbt Semantic Layer IS a Context Graph

The semantic layer already captures:
- Metric definitions (the "what")
- Dimension relationships (the "how it connects")
- Business logic as code (the "why it's calculated this way")

This is a significant competitive advantage. Most organizations don't have their business logic version-controlled and semantically structured.

### 2. The Missing Layer is Decision Traces

We capture *what* gets built but not:
- *Why* specific approaches were chosen
- *Who* approved exceptions
- *Which* precedents governed choices
- *What* alternatives were considered

Instrumenting handoff packages is the lowest-effort way to start capturing this.

### 3. SpecStory is Untapped Gold

358K lines of historical sessions contain:
- Actual decision rationale (in conversation)
- Error patterns and resolutions
- Schema validation sequences
- Alternative approaches discussed

Mining this corpus (via Learner agent) could surface patterns we don't even know we have.

### 4. Process Knowledge > Static Docs

The query-log-mining white paper already demonstrated this: mining 474K queries produced controlled vocabulary, join library, anti-pattern registry. Same approach applies to session histories—extract the *how* patterns.

### 5. Be Where Decisions Happen

> "If you're the place where decisions happen, you don't need to reconstruct the decision trace. You emit it as exhaust."

dbt-agent handoffs and QA sessions ARE where decisions happen. The infrastructure to emit traces is close—just needs instrumentation.

---

## Action Items

| Priority | Action | Owner | Status |
|----------|--------|-------|--------|
| P1 | Instrument handoff packages with decision trace fields | Architect | Proposed |
| P1 | Delegate SpecStory mining to Learner (dbt-enterprise) | PM | Bead `dbt-agent-4c3` created |
| P2 | Create session summary template (4-category extraction) | Learner | Pending |
| P2 | Add SpecStory to Learner agent search locations | Migration Agent | Pending |
| P3 | Research TrustGraph for Context Cores implementation patterns | Research | This document |
| P3 | Evaluate process pattern mining on dbt-agent SpecStory | Learner | Future |

---

## Sources

### Primary Articles (X corpus)
- Jaya Gupta / Ashu Garg - "AI's trillion-dollar opportunity: Context graphs"
- "Context Graphs Can't Organize Knowledge That Was Never Captured"
- "From CRM to CRCG: A Practical Example of Context Graphs"
- Aaron Levie - "The Era of Context"
- Glean - "Context is the next data platform"
- "Decision Traces Are Just Receipts" (Jaeg Park critique)
- "Footprints in the Sand" (emergent AI behaviors)
- Practical Guide to Context Engineering
- Where Good Ideas Come From (for coding agents)

### Web Research
- [Anthropic - Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [TrustGraph - Context Graph Factory](https://trustgraph.ai/)
- [Cognizant ContextFabric announcement](https://news.cognizant.com/2025-08-29-Cognizant-to-Deploy-1,000-Context-Engineers)
- [dbt Semantic Layer as Data Interface for LLMs](https://www.getdbt.com/blog/semantic-layer-as-the-data-interface-for-llms)
- [Context Engineering 2026 Guide](https://codeconductor.ai/blog/context-engineering/)

---

*Generated by deep research synthesis, January 8, 2026*
