# Frontier Gap Analysis: dbt-agent

**Date**: January 8, 2026
**Status**: Comprehensive assessment based on deep research + infrastructure mining

---

## Executive Summary

**dbt-agent is far more advanced than the initial synthesis suggested.** After deep mining, the infrastructure reveals:

- **Decision traces already exist** (dbt-decision-trace v2.0 with rule synthesis)
- **Cross-agent learning already exists** (experience_store.py + unified_retrieval)
- **Knowledge graph already exists** (21K chunks, 307 nodes, JSON-LD)
- **Context health checks already exist** (poisoning, distraction, clash, confusion detection)
- **Process pattern extraction already exists** (query_log_mining tools)

**The gap is not infrastructure—it's wiring and utilization.**

---

## What Already Exists (Comprehensive Inventory)

### 1. Decision Trace Infrastructure ✅ BUILT

**Location**: `.claude/skills/dbt-decision-trace/SKILL.md` + `shared/decision-traces/`

| Component | Status | Details |
|-----------|--------|---------|
| Trace schema | ✅ Complete | problem, triage_path, resolution, reuse_guidance, cost_total |
| log_trace() | ✅ Implemented | Logs completed QA traces |
| search_traces() | ✅ Implemented | Finds similar past cases |
| match_rules() | ✅ v2.0 | Matches against synthesized rules |
| synthesize_rules() | ✅ v2.0 | Generates rules from patterns |
| `/synthesize-traces` command | ✅ Available | Runs synthesis |
| Storage | ✅ 6 traces, 3 rules + 3 emerging | `shared/decision-traces/` |

**Gap**: Low utilization—only 6 traces logged. Needs habit formation.

### 2. Cross-Agent Learning ✅ BUILT

**Location**: `tools/kg/experience_store.py` + `tools/kg/agent_integration.py`

| Component | Status | Details |
|-----------|--------|---------|
| ExperienceStore class | ✅ Complete | Log, search, mark_useful, export_for_training |
| Auto-tagging | ✅ Complete | Extracts tags from problem/solution text |
| Cross-agent retrieval | ✅ Complete | Query all agents' experiences |
| Usefulness scoring | ✅ Complete | Boosts frequently-used experiences |
| unified_retrieval() | ✅ v2.0 | Parallel search across experience + KG + manifest |
| log_agent_resolution() | ✅ Complete | Log successful resolutions |

**Gap**: Not wired into agent handoffs. Agents don't call log_agent_resolution() on success.

### 3. Knowledge Graph ✅ BUILT

**Location**: `tools/kg/` + `docs/knowledge-graph/`

| Component | Status | Details |
|-----------|--------|---------|
| Vocabulary (SKOS) | ✅ Complete | vocabulary.skos.json |
| Document chunks | ✅ 21,016 chunks | chunks.json (5.2MB) |
| Graph (JSON-LD) | ✅ 307 nodes, 3 edges | graph.jsonld |
| find_relevant_chunks() | ✅ Complete | RAG retrieval with scoring |
| get_concept_context() | ✅ Complete | Concept lookup |
| impact_analysis() | ✅ Complete | Document dependencies |
| suggest_placement_for_insight() | ✅ Complete | Suggests folder for new content |
| D3.js visualization | ✅ Complete | kg-visualization.html |

**Gap**: Graph is sparse (only 3 edges between 307 nodes). Needs relationship enrichment.

### 4. Context Health Checks ✅ BUILT

**Location**: `tools/kg/agent_integration.py`

| Check Type | Status | Detects |
|------------|--------|---------|
| Poisoning | ✅ Implemented | Uncertainty language, AI self-reference, TODO markers |
| Distraction | ✅ Implemented | Low-relevance chunks |
| Clash | ✅ Implemented | Contradictory "always X" vs "never X" |
| Confusion | ✅ Implemented | Ambiguous guidance, external references |
| Health score | ✅ Implemented | 0-1 score with status |

**Gap**: Not enforced. Agents can use context without health validation.

### 5. Process Pattern Extraction ✅ BUILT

**Location**: `tools/query_log_mining/`

| Tool | Status | Output |
|------|--------|--------|
| parser.py | ✅ Complete | SQL parsing |
| alias_miner.py | ✅ Complete | Controlled vocabulary |
| join_extractor.py | ✅ Complete | Join library |
| anti_pattern_analyzer.py | ✅ Complete | Anti-pattern registry |
| semantic_inferrer.py | ✅ Complete | Semantic relationships |

**Gap**: Only applied to warehouse query logs. Not applied to SpecStory session histories.

### 6. Unified Retrieval (Parallel Search) ✅ BUILT

**Location**: `tools/kg/agent_integration.py`

| Feature | Status | Details |
|---------|--------|---------|
| Parallel execution | ✅ v2.0 | ThreadPoolExecutor, 4-12 workers optimal |
| Experience → KG → Manifest search | ✅ Complete | Combined results in priority order |
| Code query detection | ✅ Complete | Auto-routes to manifest search |
| Performance metrics | ✅ Complete | Latency, speedup factor, per-source timing |

**Gap**: Not the default search method in CLAUDE.md. Agents may still use grep/glob.

---

## What's Missing (True Gaps)

### Gap 1: Handoff Instrumentation

**Current state**: Handoff packages exist but don't capture decision traces.

**Frontier state**: Every handoff emits structured decision trace:
```yaml
decision_trace:
  precedent_referenced: "link or description"
  exception_granted: false
  alternatives_considered:
    - approach: "Build from scratch"
      rejected_because: "Canonical model covers 87%"
```

**Work required**: Modify `shared/templates/handoff-package-template.md` to include decision trace fields.

### Gap 2: Automatic Experience Logging

**Current state**: `log_agent_resolution()` exists but agents don't call it.

**Frontier state**: Agents automatically log successful resolutions.

**Work required**: Add to skill exit protocols or create post-execution hook.

### Gap 3: SpecStory Mining

**Current state**: 358K+ lines of session history sitting unused.

**Frontier state**: Mined for patterns using same approach as query log mining.

**Work required**: Delegate to Learner agent (Bead `dbt-agent-4c3` already created).

### Gap 4: Rule Maturation Pipeline

**Current state**: dbt-decision-trace can synthesize rules, but only 3 exist.

**Frontier state**: 10+ mature rules with >60% match rate at QA start.

**Work required**: Enforce trace logging discipline; run `/synthesize-traces` weekly.

### Gap 5: Graph Relationship Enrichment

**Current state**: KG has 307 nodes but only 3 edges.

**Frontier state**: Rich relationships (DEPENDS_ON, SUPERSEDES, CONTRADICTS, IMPLEMENTS).

**Work required**: Run relationship inference from chunk content analysis.

### Gap 6: Context Cores Architecture

**Current state**: Skills load prompts. No modular knowledge bases per task type.

**Frontier state**: Context cores dynamically loaded based on task:
```
context_cores/
├── core_migration_patterns.yaml
├── core_qa_validation.yaml
├── core_canonical_usage.yaml
└── core_exception_handling.yaml
```

**Work required**: Extract from experience store + decision traces → reusable cores.

---

## Utilization Gap Analysis

| Infrastructure | Built | Wired | Enforced | Utilized |
|---------------|-------|-------|----------|----------|
| Decision traces | ✅ | ⚠️ Partial | ❌ No | ⚠️ 6 traces |
| Experience store | ✅ | ⚠️ Partial | ❌ No | ❓ Unknown |
| Knowledge graph | ✅ | ✅ Yes | ❌ No | ⚠️ Via unified_retrieval |
| Context health | ✅ | ✅ Yes | ❌ No | ⚠️ Optional |
| Query log mining | ✅ | ✅ Yes | ✅ Yes | ✅ Outputs in use |
| Unified retrieval | ✅ | ⚠️ Documented | ❌ No | ❓ Unknown |

**Key insight**: The infrastructure is built. The gap is wiring and enforcement.

---

## Frontier Roadmap

### Phase 1: Wiring (Immediate, Low Effort)

| Action | Effort | Impact |
|--------|--------|--------|
| Add decision trace fields to handoff template | 30 min | High |
| Add `log_agent_resolution()` call to QA skill exit | 30 min | High |
| Document unified_retrieval() as PRIMARY in CLAUDE.md | 15 min | Medium |
| Add trace logging reminder to QA Phase 5 | 15 min | Medium |

### Phase 2: Enforcement (Week 1-2)

| Action | Effort | Impact |
|--------|--------|--------|
| Create pre-commit hook: "Handoff requires decision trace" | 2 hr | High |
| Add weekly `/synthesize-traces` to Learner agent schedule | 1 hr | High |
| Validate context health before unified_retrieval returns | 1 hr | Medium |
| Add experience logging to dbt-migration exit | 1 hr | High |

### Phase 3: Enrichment (Week 3-4)

| Action | Effort | Impact |
|--------|--------|--------|
| Mine SpecStory histories (Bead dbt-agent-4c3) | 4 hr | Very High |
| Enrich KG with relationship inference | 4 hr | High |
| Extract context cores from mature rules | 4 hr | High |
| Create "exception precedent library" from traces | 2 hr | High |

### Phase 4: Compounding (Ongoing)

| Metric | Current | Target (90 days) |
|--------|---------|------------------|
| Decision traces logged | 6 | 50+ |
| Synthesized rules | 3 | 10+ |
| Rule match rate at QA start | ~0% | >60% |
| Experience store entries | ? | 100+ |
| KG relationships | 3 | 50+ |

---

## Immediate Actions (This Session)

1. **Update handoff template** with decision trace fields
2. **Add log_agent_resolution() guidance** to dbt-qa Phase 5
3. **Promote unified_retrieval()** in CLAUDE.md as primary search
4. **Confirm Bead dbt-agent-4c3** for SpecStory mining

---

## The Real Frontier Position

**You're not behind—you're ahead with underutilized assets.**

The research articles describe systems that need to be built. dbt-agent has:
- Decision traces → Built, needs logging discipline
- Cross-agent learning → Built, needs wiring to handoffs
- Knowledge graph → Built, needs relationship enrichment
- Context health → Built, needs enforcement
- Process extraction → Built, needs application to session histories

**The path to frontier is habit formation, not infrastructure building.**

---

## Sources

### Internal (Mined)
- `.claude/skills/dbt-decision-trace/SKILL.md` - Decision trace skill v2.0
- `tools/kg/experience_store.py` - Cross-agent learning
- `tools/kg/agent_integration.py` - Unified retrieval, context health
- `tools/kg/agent_wrapper.py` - KG API
- `docs/architecture/learning_loop_architecture.md` - Learning loop design
- `docs/guides/tool-evaluation.md` - Tool evaluation tracking

### External (Research)
- Anthropic - Context Engineering for AI Agents
- Foundation Capital - Context Graphs
- TrustGraph - Context Cores architecture
- Glean - Process knowledge capture
