# Deep Dive: Resource Analysis & Workflow Gap Mapping

**Date:** 2026-01-11
**Type:** Comprehensive Research & Integration Strategy
**Resources Analyzed:** 20+ tools, frameworks, and patterns
**Focus:** SQL QA processes, Semantic Layer, Knowledge Graph, Agent Infrastructure

---

## Executive Summary

After analyzing all resources in the intake queue, I've mapped them against our critical workflow gaps. The findings reveal **three urgent priorities** that would dramatically improve our system:

1. **Dots → Replace Beads** — 107× smaller, Claude Code hooks built-in, markdown-native
2. **Flow-Next Re-anchoring Pattern** — Prevents drift during long migrations (our #1 failure mode)
3. **Knowledge Engineering (Heimsbakk)** — Encode semantic layer as triples for relationship-aware retrieval

**Key insight:** Many gaps we're trying to solve with complex infrastructure (TrustGraph, semantic search MCPs) have simpler solutions in the patterns discovered here.

---

## Part 1: Our Current Workflow Gaps

### Gap Analysis by Workflow

| Workflow | Current State | Pain Point | Impact |
|----------|---------------|------------|--------|
| **SQL QA** | Templates 1-4, manual variance | No automated drift detection during QA | 3+ iterations per model |
| **Semantic Layer** | MetricFlow skill, DEV/PROD awareness | Relationships not queryable by graph | Hard to find related metrics |
| **Knowledge Graph** | 21K chunks, BM25 search | No semantic similarity, no relationship traversal | "We have this" detection misses |
| **4-Agent Workflow** | Gates 1-4, handoff packages | Context drift mid-workflow | Architecture decisions forgotten |
| **Decision Traces** | traces.json, rules.json | No provenance, not reified | Can't audit "who verified" |
| **Session Persistence** | Beads (25MB), session-logs | Beads too heavy, loses TodoWrite sync | Context lost between sessions |
| **Skills Architecture** | 18 skills, triggers in CLAUDE.md | Not portable, no validation | Skills can't be shared |
| **CLAUDE.md** | 1000+ lines | Too long, degrades performance | Agents ignore parts of it |

### Critical Gap: Context Drift in Long Operations

From session logs and QA validation issues, our **#1 failure mode** is:

> Agent makes correct decision in iteration 1 → By iteration 50, has forgotten constraints → Makes invalid decision that violates earlier choices

**Evidence:**
- Interchange QA: Forgot dependency analysis, built on stale schema
- Merchant Spend: Placed models in wrong folder despite prior discussion
- Phase 3a: Forgot environment-aware date limits mid-session

This is **exactly what Agent Harness and Flow-Next address**.

---

## Part 2: Tool-by-Tool Analysis

### Tier 1: Immediate Adoption (This Week)

#### 1. **Dots** → Replace Beads

| Metric | Beads | Dots | Winner |
|--------|-------|------|--------|
| Binary size | 25 MB | 233 KB | Dots (107×) |
| Lines of code | 115,000 | 2,800 | Dots (41×) |
| Dependencies | Go, SQLite/Wasm | None | Dots |
| Claude Code hooks | Custom scripts | Built-in | Dots |
| TodoWrite sync | Manual | Automatic | Dots |
| Format | JSON database | Markdown + YAML | Dots |

**Key feature we need:** Dots has built-in `PostToolUse` hook that syncs TodoWrite to dots automatically. No more manual bead creation.

**Migration path:**
1. Export Beads to markdown (bd export)
2. Move to `.dots/` format
3. Update CLAUDE.md references
4. Delete Beads binary

**Recommendation:** **ADOPT IMMEDIATELY**

---

#### 2. **Flow-Next Re-anchoring Pattern** → Prevent Drift

The core pattern:

```
Before EVERY task:
1. Re-read the epic spec from .flow/
2. Re-read the task spec from .flow/
3. Re-read git state
4. THEN execute with fresh context
```

**Why this matters:** Instead of relying on accumulated conversation history (which drifts), re-anchor to source-of-truth files every iteration.

**Adaptation for dbt-agent:**
```
Before EVERY model in migration:
1. Re-read handoffs/[pipeline]/tech-spec.md
2. Re-read canonical-models-registry.md
3. Check compiled SQL state (dbt compile)
4. THEN write model
```

**Implementation:**
- Add to `dbt-migration` skill as mandatory protocol
- Create `.flow/` equivalent: `handoffs/[pipeline]/` already exists
- Add re-anchoring reminder to TodoWrite active task

**Recommendation:** **ADOPT THIS WEEK** (pattern only, not full Flow-Next)

---

#### 3. **CLAUDE.md Optimization** → Progressive Disclosure

Current state: 1000+ lines in root CLAUDE.md
Best practice: <300 lines, with references to `agent_docs/` folder

**The pattern from HumanLayer:**

```markdown
# CLAUDE.md (60 lines max)

## What This Project Is
[3-5 sentences]

## How to Run/Test
[commands]

## Key Conventions
[critical 5-10 rules]

## Deep Documentation
See agent_docs/ for:
- `building_the_project.md` - Full build process
- `code_conventions.md` - Style guide
- `database_schema.md` - Data model
```

**Anti-patterns we're hitting:**
- Style guidelines in CLAUDE.md → Should be in linter (dbt-bouncer handles this)
- Verbose workflow descriptions → Move to skills
- Full checklist → Reference by path

**Adaptation:**
1. Trim CLAUDE.md to essentials (<300 lines)
2. Move detailed workflows to skills
3. Keep only: role, quick-start, critical principles, references
4. Use file:line pointers instead of pasted content

**Recommendation:** **ADOPT THIS WEEK** (incremental, not rewrite)

---

### Tier 2: Near-Term Integration (Next 2 Weeks)

#### 4. **Knowledge Engineering (Heimsbakk)** → Semantic Layer as Triples

This is the **highest-impact knowledge gap**. The tutorials show:

```python
# Transform semantic model to triples
semantic_model -> hasMetric -> "revenue_total"
semantic_model -> hasDimension -> "calendar_date"
"revenue_total" -> hasMeasure -> "sum_revenue"
"revenue_total" -> reliesOn -> "calendar_date"  # Time spine dependency
```

**Why this matters for us:**
- Currently: Search KB with keywords "revenue metric"
- With triples: Traverse "revenue_total → reliesOn → ?" to find all dependencies
- Enables: "What metrics share this dimension?" (impossible with BM25)

**Implementation path:**
1. Read both Heimsbakk tutorials thoroughly
2. Create `tools/kg/semantic_layer_to_triples.py`
3. Generate triples from `semantic_manifest.json`
4. Add SPARQL-style queries to `unified_retrieval()`

**Recommended ontologies:**
- **SKOS** — For metric/dimension concept hierarchies
- **PROV** — For lineage provenance (who created, when)
- **DCAT** — For dataset/model cataloging

**Recommendation:** **ADOPT** (requires 8-12 hours implementation)

---

#### 5. **session-transcripts.ts Pattern** → SpecStory Mining

We have **358K lines** of SpecStory archives. The pi-mono script shows how to:

1. Chunk sessions into 100K char files (~20K tokens)
2. Run pattern analysis with structured output
3. Aggregate patterns across sessions
4. Compare against existing AGENTS.md

**Output format:**
```
PATTERN: <name>
STATUS: NEW | EXISTING
TYPE: agents-md | skill | prompt-template
FREQUENCY: <count>
EVIDENCE: ["quote 1", "quote 2"]
DRAFT: <proposed content>
```

**Adaptation:**
```python
# tools/extract_specstory_patterns.py
1. Read session-logs/*.md and .specstory/
2. Chunk by token limit
3. For each chunk: identify patterns with 2+ occurrences
4. Map to: skill | kb-entry | troubleshooting | decision-trace
5. Generate draft additions with evidence
```

**Recommendation:** **ADOPT** (4-6 hours to adapt script)

---

#### 6. **Agent Harness Patterns** → Drift Monitoring

Key insight from the research:

> "A 1% difference on a leaderboard cannot detect reliability if a model drifts off-track after fifty steps."

**The monitoring pattern:**
- Capture trajectories where agents fail to follow instructions late in workflows
- Feed back into training/prompts
- "Harness as Dataset" — competitive advantage comes from failure data

**Adaptation for dbt-agent:**
```yaml
# session-logs/[date]/drift_markers.yaml
iteration_50:
  expected: "Use canonical model int_transactions__posted"
  actual: "Built new model from scratch"
  deviation: true
  root_cause: "Forgot to check registry"

iteration_75:
  expected: "Apply environment-aware date limit"
  actual: "Hardcoded date filter"
  deviation: true
```

**Recommendation:** **ADOPT** (add to handoff package template)

---

#### 7. **Adversarial Spec** → Cross-Model Tech Spec Review

Before stakeholder review of tech specs, run multi-model debate:

```
1. Claude drafts tech spec
2. GPT-4, Gemini critique independently
3. Claude synthesizes + defends
4. Iterate until consensus
5. THEN present to user
```

**Why this matters:**
- Single-model specs have blind spots
- Multi-model catches: missing edge cases, ambiguous requirements, unstated assumptions
- Reduces user correction cycles

**Integration point:** Gate 3 (Architecture Review) in 4-agent workflow

**Recommendation:** **EVALUATE** (need to assess token cost vs. value)

---

### Tier 3: Queued for Later (Month+)

#### 8. **AgentFS** → Production Session Persistence

More sophisticated than Dots, provides:
- SQLite-based audit trail
- Snapshot/restore for reproducibility
- Key-value store for agent state
- Tool-call history

**Why defer:**
- Dots solves immediate pain (TodoWrite sync)
- AgentFS is infrastructure investment
- Better fit if we need multi-agent coordination

**Recommendation:** **DEFER** (revisit if Dots proves insufficient)

---

#### 9. **Workflow DevKit** → Durable Agent Patterns

Provides:
- Automatic retry (3× by default)
- Step isolation (failures don't crash workflow)
- Persistent streams across reconnects

**Why defer:**
- Our workflows are synchronous within Claude Code
- Would require architectural change
- Better fit for production deployment

**Recommendation:** **DEFER** (pattern reference only)

---

#### 10. **Agent Skills Spec** → Cross-Agent Portability

The spec defines:
- Standard `SKILL.md` format with YAML frontmatter
- `scripts/`, `references/`, `assets/` directories
- Progressive disclosure tiers (metadata → instructions → resources)
- Validation tooling

**Why defer:**
- Our skills already follow similar pattern
- Portability not urgent (we're Claude Code only)
- Would require skill format changes

**Recommendation:** **ADOPT FORMAT SPEC** (align our skills, don't rewrite)

---

#### 11. **Claude Delegator** → Multi-Model Experts

Interesting pattern: route domain questions to specialized GPT experts via MCP.

**Why defer:**
- We have specialized skills already
- Adding GPT dependency increases complexity
- Better fit for cross-model validation (see Adversarial Spec)

**Recommendation:** **DEFER**

---

#### 12. **Every Code / Claude Canvas** → Multi-Agent Orchestration

Advanced patterns:
- Multi-model consensus (/plan, /solve)
- Auto-healing with parallel worktrees
- TUI toolkit for interactive displays

**Why defer:**
- We're single-agent, single-session
- Infrastructure overhead not justified
- Ralph already provides autonomous mode

**Recommendation:** **DEFER** (reference only)

---

## Part 3: Integration with Existing Queue

### Updated Tool Priority Matrix

| Priority | Tool | Category | Gap Addressed | Status |
|----------|------|----------|---------------|--------|
| **P0** | **Dots** | Infrastructure | Session persistence, TodoWrite sync | **ADOPT NOW** |
| **P0** | **Flow-Next re-anchor** | Pattern | Drift prevention | **ADOPT NOW** |
| **P0** | **CLAUDE.md optimization** | Architecture | Performance degradation | **ADOPT NOW** |
| P1 | Heimsbakk KG patterns | Knowledge | Semantic layer as triples | Implement |
| P1 | session-transcripts adaptation | Learning | SpecStory mining | Implement |
| P1 | Agent Harness monitoring | Quality | Drift detection | Implement |
| P2 | mem-agent-mcp | Memory | Session continuity | Queued (existing) |
| P2 | DeepEval | Testing | Agent output validation | Queued (existing) |
| P2 | Adversarial Spec | Quality | Cross-model tech spec review | Evaluate |
| P3 | Agent Skills spec | Architecture | Skills portability | Align format |
| P3 | AgentFS | Infrastructure | Production persistence | Defer |
| P3 | RAGAS | Quality | KG quality metrics | Queued (existing) |

### Synergies Identified

**Dots + Flow-Next:**
- Dots tracks tasks in `.dots/`
- Flow-Next re-anchors from `.flow/`
- **Synergy:** Use `.dots/` AS the re-anchoring source
- Each task file contains spec + constraints
- Agent re-reads task file before each iteration

**Heimsbakk + Semantic Layer Skill:**
- Heimsbakk provides triple patterns
- Semantic layer has `semantic_manifest.json`
- **Synergy:** Generate triples from manifest → enable "What metrics use this dimension?" queries

**session-transcripts + Decision Traces:**
- session-transcripts extracts patterns
- Decision traces need evidence
- **Synergy:** Auto-populate trace evidence from session mining

---

## Part 4: Implementation Roadmap

### Week 1: Foundation

**Day 1-2: Dots Migration**
- [ ] Install Dots: `brew install dots` or build from source
- [ ] Export Beads: `bd export --format markdown`
- [ ] Convert to Dots format (YAML frontmatter + markdown)
- [ ] Configure Claude Code hooks (SessionStart, PostToolUse)
- [ ] Update CLAUDE.md references

**Day 3-4: Re-anchoring Pattern**
- [ ] Add re-anchoring protocol to `dbt-migration` skill
- [ ] Create template: `handoffs/[pipeline]/checkpoint.md`
- [ ] Add TodoWrite instruction: "Re-read checkpoint before task"
- [ ] Test on simple migration

**Day 5: CLAUDE.md Trim**
- [ ] Identify content to move (workflows → skills, checklists → references)
- [ ] Create `docs/agent-docs/` progressive disclosure structure
- [ ] Reduce CLAUDE.md to <300 lines
- [ ] Test agent behavior

### Week 2: Knowledge Enhancement

**Day 1-3: Heimsbakk Implementation**
- [ ] Read both tutorials in detail
- [ ] Create `tools/kg/semantic_triples.py`
- [ ] Parse `semantic_manifest.json` → triples
- [ ] Add to `unified_retrieval()` as triple queries
- [ ] Test: "What metrics share calendar_date dimension?"

**Day 4-5: SpecStory Mining**
- [ ] Adapt `session-transcripts.ts` to Python
- [ ] Run on `.specstory/` archive
- [ ] Generate pattern report
- [ ] Create decision traces with evidence

### Week 3: Quality & Monitoring

- [ ] Add drift markers to handoff template
- [ ] Evaluate Adversarial Spec for Gate 3
- [ ] Review DeepEval for agent testing

---

## Part 5: Metrics to Track

### Before/After Targets

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| QA iterations per model | 3-4 | 1-2 | Handoff package logs |
| Context drift incidents | ~1/session | 0 | Deviation markers |
| "We have this" detection | ~60% | >90% | Learner agent accuracy |
| CLAUDE.md load time | N/A | <500ms | Token efficiency |
| Session continuity | Manual | Automatic | Dots sync |
| Semantic layer query accuracy | Keyword only | Relationship-aware | Triple query success |

### Leading Indicators

- **Re-anchoring compliance:** Did agent re-read spec before task? (binary)
- **Dots sync rate:** TodoWrite → Dots without manual intervention (%)
- **Triple query coverage:** Semantic layer entities with triples (%)
- **Pattern extraction yield:** Patterns from SpecStory per 10K tokens

---

## Part 6: Reference Summary

### Key Patterns to Remember

1. **Re-anchoring:** Re-read source-of-truth before every task iteration
2. **Progressive disclosure:** <300 lines in CLAUDE.md, details in references
3. **Triples for relationships:** Subject → Predicate → Object enables graph traversal
4. **Harness as dataset:** Failure trajectories are competitive advantage
5. **Atomic tools + agent judgment:** Don't embed logic in tools
6. **Consensus validation:** Multi-model debate catches single-model blind spots

### Anti-Patterns to Avoid

1. **Context accumulation:** Long conversations drift; re-anchor instead
2. **Over-instruction:** >50 rules degrades uniform performance
3. **Style in prompts:** Use linters (dbt-bouncer), not instructions
4. **Feature tools:** Keep tools atomic; compose in prompts
5. **Single-model review:** Misses systematic blind spots

---

## Sources

### High Priority (Implemented)
- [Heimsbakk Part 1](https://veronahe.substack.com/p/from-data-engineering-to-knowledge)
- [Heimsbakk Part 2](https://veronahe.substack.com/p/data-engineering-ontologies)
- [Dots](https://github.com/joelreymont/dots)
- [Flow-Next](https://github.com/gmickel/gmickel-claude-marketplace)
- [Agent Harness](https://www.philschmid.de/agent-harness-2026)
- [CLAUDE.md Best Practices](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

### Medium Priority (Queued)
- [AgentFS](https://github.com/tursodatabase/agentfs)
- [session-transcripts.ts](https://github.com/badlogic/pi-mono/blob/main/scripts/session-transcripts.ts)
- [Adversarial Spec](https://github.com/zscole/adversarial-spec)
- [Agent Skills Spec](https://agentskills.io/specification)

### Reference Only
- [Workflow DevKit](https://useworkflow.dev/docs/ai)
- [bash-tool](https://vercel.com/changelog/introducing-bash-tool-for-filesystem-based-context-retrieval)
- [Context Field](https://github.com/NeoVertex1/context-field/blob/main/code_field.md)
- [Every Code](https://github.com/just-every/code)
- [nanocode](https://github.com/1rgs/nanocode)
- [Pi](https://shittycodingagent.ai/)

---

*Generated by Learner Agent deep dive session on 2026-01-11*
