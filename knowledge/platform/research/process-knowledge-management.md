# Process Knowledge Management: Deep Research Report

**Date:** 2026-01-17
**Agent:** Librarian Mode (data-centered)
**Sources:** Jessica Talisman's Process Knowledge Management Series (Parts I-IV) + Context Graphs Article
**Cross-Reference:** dbt-agent repository knowledge assets analysis

---

## Executive Summary

This report synthesizes Jessica Talisman's Process Knowledge Management (PKM) series with an analysis of what we've already built in dbt-agent. The core insight: **we've independently arrived at many PKM patterns through practice, but lack the formal ontological foundation that would enable our knowledge assets to compound and interoperate at scale.**

Key finding: dbt-agent has sophisticated institutional memory infrastructure (decision traces, rule synthesis, skills as procedural capsules, experience replay). What's missing is the **Procedural Knowledge Ontology (PKO)** layer that would formalize procedure definitions, enable temporal reasoning, and support true knowledge graph federation.

---

## Part I: Core Concepts from Talisman's Series

### The Fundamental Distinction: Process vs. Procedural Knowledge

| Type | Definition | Where It Lives |
|------|------------|----------------|
| **Process Knowledge** | Raw material—tacit understanding, practiced expertise, the rhythms of how work actually happens | Slack channels, margin notes, institutional memory of workers, practiced hands |
| **Procedural Knowledge** | Process knowledge that has been formalized, encoded, and represented through structured semantic systems | Ontologies, knowledge graphs, structured documentation |

> "The transformation from process to procedural knowledge requires deliberate engineering work. It is one thing to elicit knowledge, but ultimately, that knowledge must be codified and represented formally."

**Critical Insight**: The act of formalizing and encoding decisions and decision reasoning is what transforms process knowledge into procedural knowledge. This transformation is non-trivial—it requires knowledge engineers who understand both the domain and semantic technologies.

### The Knowledge Levels Framework

Process knowledge operates across three abstraction levels, each requiring different capture strategies:

| Level | Focus | Stakeholders | Capture Method |
|-------|-------|--------------|----------------|
| **Operational** | Sequence and dependencies: order of tasks, conditions to move forward | Implementers, operators | Process mining, observation |
| **Tactical** | Optimization and adaptation: resource allocation, bottleneck identification | Managers, architects | Interviews, collaborative workshops |
| **Strategic** | Mission alignment: rationale behind processes, contribution to value creation | Executives, strategists | Document analysis, expert elicitation |

**Application to dbt-agent**: Our current skills capture operational knowledge well (step-by-step playbooks). We're weaker at tactical (why we chose certain patterns over others) and strategic (how pipelines contribute to business value).

---

## Part II: Collection, Organization, Encoding

### The Elicitation Challenge

> "We know more than we can tell." — Polanyi Paradox

Tacit knowledge resists extraction. Talisman identifies five complementary approaches:

1. **Structured Interviews**: Ask "why" not just "what"—Critical Incident Technique (CIT) to reveal judgment calls
2. **Observation/Ethnography**: Shadow workers through daily activities, pause to ask "why did you do that?"
3. **Process Mining**: Analyze event logs to reconstruct actual vs. documented processes
4. **Collaborative Workshops**: Cross-functional sessions with SMEs, knowledge consumers, and producers
5. **Document Analysis**: Extract from SOPs, training materials, decision matrices

**What we do well in dbt-agent:**
- Decision trace logging captures CIT-style incidents
- SpecStory archives contain rich "why" context
- Experience replay database holds problem-solution pairs

**What we're missing:**
- Systematic ethnographic capture (we rely on ad-hoc handoff documents)
- Process mining against our own execution logs
- Regular collaborative workshops with SMEs

### The Organization Framework

Process knowledge organization operates across three levels:

| Level | Purpose | Implementation |
|-------|---------|----------------|
| **Conceptual** | Define vocabularies and categories | Controlled vocabularies, SKOS |
| **Structural** | Arrange instances within framework | Taxonomies, thesauri |
| **Contextual** | Specify applicability boundaries | Named graphs, scoping annotations |

**Current dbt-agent state:**
- ✅ Conceptual: vocabulary.skos.json with 17 core concepts
- ✅ Structural: skills organized by domain (migration, QA, semantic layer)
- ⚠️ Contextual: Limited—we don't scope knowledge by business unit, regulation, or environment

### Encoding for AI Systems

Talisman emphasizes that encoding for RAG requires:

1. **Meaningful segmentation**: At activity/decision boundaries, not arbitrary character counts
2. **Rich metadata**: Position in larger process, applicability conditions, related segments
3. **Domain-tuned embeddings**: Recognize that "approve" ≈ "authorize" but "approve" ≠ "reject"

For **tool use and agentic AI**, encoding must capture:
- **Pre-conditions**: What must be true before an activity begins
- **Post-conditions**: What becomes true after an activity completes
- **Invariants**: What must remain true throughout
- **Failure modes**: What can go wrong and how to respond
- **Decision points**: Where choices must be made and what factors inform them

**Critical gap in dbt-agent**: Our skills describe inputs/outputs but don't formalize pre/post-conditions, invariants, or failure modes. This limits automated verification and dynamic capability negotiation.

---

## Part III: Historical Context—Why This Matters Now

### The Outsourcing Paradox

Talisman traces a 40-year pattern: Western companies outsourced "execution" (manufacturing, knowledge work) without realizing they were outsourcing the capacity to capture procedural knowledge.

> "We outsourced what we dismissively called 'the boring stuff' without understanding that we were outsourcing the very capacity to understand how things get built."

The result: AI systems require rich procedural knowledge, but organizations find themselves impoverished in exactly that resource.

### The Engineering State vs. Lawyerly Society

| Engineering State | Lawyerly Society |
|-------------------|------------------|
| Cultural focus on building, optimizing, documenting | Focus on litigation, regulation, oversight |
| Values iterative improvement | Values risk mitigation |
| Treats documentation as integral to craft | Treats documentation as compliance burden |
| Knowledge accumulation | Knowledge gatekeeping |

**Implication for dbt-agent**: We've built an engineering culture that values documentation (320K+ lines). This is a competitive advantage—most enterprise data teams don't have this.

### The Death of Apprenticeship

Traditional knowledge transfer through mentorship broke when work moved to contractors and external providers. No one invests in building institutional memory for systems they don't own.

**dbt-agent parallel**: Our skills system is essentially codified apprenticeship—a senior engineer's accumulated wisdom encoded in machine-readable form. The question is whether this scales.

---

## Part IV: The Procedural Knowledge Ontology (PKO)

### PKO Architecture

The Procedural Knowledge Ontology from Cefriel provides a formal framework for representing procedures and their executions. Built from three industrial scenarios: safety procedures (Beko Europe), CNC machine commissioning (Fagor Automation), and microgrid management (Siemens).

**Core Distinction**: Procedures (abstract specifications) vs. Executions (concrete instances)

| PKO Concept Area | Purpose | dbt-agent Equivalent |
|------------------|---------|---------------------|
| **Procedure** | Specifications: types, targets, versions, status | Skills (SKILL.md files) |
| **Step** | Granular actions, functions, tools, expertise levels | Skill capabilities + resources |
| **Change of Status** | Provenance: creation, modification, validation, approval | Git commits + dot updates |
| **Procedure Execution** | Actual performance: sequences, feedback, errors, questions | Decision traces + SpecStory logs |
| **Agent** | People, orgs, software interacting with procedures | Agent registry (orchestrator, architect, etc.) |
| **Resource** | Supporting documentation, media, data sources | Knowledge base files, assets |

### PKO Semantic Relationships

| Relationship | Purpose | Current Support in dbt-agent |
|--------------|---------|------------------------------|
| `pko:nextStep` / `pko:previousStep` | Temporal logic of procedures | Implicit in skill playbooks |
| `pko:nextAlternativeStep` | Decision points, branching | Not formalized |
| `pko:isIncludedInProcedureExecution` | Links step execution to procedure | Not formalized |
| `pko:executesStep` | Links execution to abstract step | Not formalized |
| `prov:startedAtTime` / `prov:endedAtTime` | Temporal dimension | Timestamps in traces |
| `pko:hasUserQuestionOccurrence` | Questions raised during execution | Captured in handoff docs |
| `pko:hasEncounteredError` | Error tracking | Decision traces |
| `pko:FrequentlyAskedQuestions` | Patterns distilled from execution | Not formalized |

### PKO Standards Stack

PKO reuses established semantic web standards:

| Standard | Purpose |
|----------|---------|
| **PROV-O** | Provenance: who did what, when, how |
| **P-Plan** | Plans and plan executions |
| **DCAT** | Dataset metadata |
| **Time Ontology** | Temporal concepts |
| **SKOS** | Vocabulary control |

---

## Gap Analysis: dbt-agent vs. PKO

### What We Have (Strong Foundation)

| Asset | PKO Equivalent | Maturity |
|-------|---------------|----------|
| Skills (SKILL.md) | Procedure definitions | High—18 skills with triggers, capabilities, resources |
| Decision traces | Execution records | Medium—7 traces logged, synthesis engine operational |
| Rule synthesis | Pattern extraction | Medium—3 rules synthesized, confidence scoring |
| Experience replay | Case-based reasoning | High—50+ problem-solution pairs |
| vocabulary.skos.json | Controlled vocabulary | High—17 concepts, SKOS-compliant |
| Orchestrator workflow | State machine | High—4 phases, 4 gates, handoff protocols |
| Business concepts schema | Concept definitions | Medium—domain/SQL/conflict tracking |

### What We're Missing (PKO Gaps)

| Missing Element | PKO Feature | Impact |
|-----------------|-------------|--------|
| **Formal procedure steps** | pko:Step with preconditions/postconditions | Can't verify procedure correctness |
| **Conditional logic** | pko:nextAlternativeStep with conditions | Can't handle branching automatically |
| **Constraint representation** | Formal invariants | Business rules buried in prose |
| **Temporal reasoning** | Time ontology integration | Can't query "what was true when X happened" |
| **Failure mode catalog** | Explicit anti-patterns | Only capture successes, not blockers |
| **Procedure versioning** | pko:ProcedureVersion with status | Skills version, procedures within don't |
| **OWL formalization** | Full semantic web stack | Limited to SKOS + custom JSON |
| **Execution trace linking** | pko:executesStep | Traces don't link to abstract procedures |

---

## Actionable Recommendations

### Priority 1: Formalize Procedure Steps

Transform implicit playbooks into explicit step definitions with:
- Pre-conditions (what must be true)
- Post-conditions (what becomes true)
- Failure modes (what can go wrong)
- Decision points (where to branch)

**Example transformation for kb-dbt-migration's 6-step playbook:**

```yaml
procedure:
  id: pipeline-build-playbook
  version: "3.0"
  steps:
    - id: analyze_tech_spec
      preconditions:
        - tech-spec.md exists
        - business-context.md exists
        - data-discovery-report.md exists
      postconditions:
        - canonical_models identified
        - transformation_approach selected
      failure_modes:
        - missing_requirements: escalate_to_business_context_agent
        - conflicting_specs: request_clarification
      decision_points:
        - incremental_or_full_refresh: based on data_volume + change_frequency
```

### Priority 2: Implement Execution Trace Linking

Modify decision trace schema to link executions to abstract procedure steps:

```json
{
  "trace_id": "trace-007",
  "executes_procedure": "pipeline-build-playbook",
  "executes_step": "configure_incremental",
  "step_execution": {
    "started_at": "2026-01-17T14:00:00Z",
    "ended_at": "2026-01-17T14:45:00Z",
    "questions_raised": ["Should we use delete+insert or merge?"],
    "errors_encountered": ["tuple_collision_on_merge"],
    "deviation_from_spec": "Used delete+insert instead of merge per rule-002"
  }
}
```

### Priority 3: Add Conditional Logic Representation

Create a decision tree format for branching logic:

```yaml
decision_point:
  id: incremental_strategy_selection
  condition_type: AND
  conditions:
    - attribute: table_row_count
      operator: ">"
      value: 10000000
    - attribute: change_rate_daily
      operator: "<"
      value: 0.05
  if_true: incremental_merge
  if_false: full_refresh
  justification: "High volume + low change rate favors incremental"
```

### Priority 4: Build Failure Mode Catalog

Create explicit anti-pattern registry:

```yaml
failure_modes:
  - id: blind_full_refresh
    description: "Running dbt run --full-refresh without cost estimation"
    detection_signals:
      - no_preflight_check
      - table_size > 100M_rows
    prevention: kb-dbt-preflight skill
    recovery: abort_and_run_incremental

  - id: orphaned_incremental
    description: "Incremental model with no upstream CDC detection"
    detection_signals:
      - materialization = incremental
      - no_is_deleted_column
      - no_updated_at_column
    prevention: data_discovery_checklist
    recovery: add_delete_detection_logic
```

### Priority 5: Integrate PKO Standards

Create a `procedural-knowledge.owl` file that imports:
- PROV-O for provenance
- P-Plan for plan execution
- SKOS for vocabulary (already have)
- Time Ontology for temporal reasoning

### Priority 6: Close the Loop—Execution → Pattern → Skill

Formalize the learning cycle:

```
Execution → Trace → Pattern Recognition → Rule Synthesis → Skill Update
     ↑                                                           |
     └───────────────────────────────────────────────────────────┘
```

Implement automated detection of:
- Traces matching no existing rules (novel situation)
- Rules with high match rate but low confidence (needs validation)
- Patterns emerging from multiple executions (candidate for skill promotion)

---

## Architectural Vision: PKO-Enhanced dbt-agent

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PKO-Enhanced Knowledge Layer                     │
├─────────────────────────────────────────────────────────────────────┤
│  procedural-knowledge.owl    │  vocabulary.skos.json (existing)     │
│  - Procedure definitions     │  - 17 core concepts                  │
│  - Step specifications       │  - Hierarchical relationships        │
│  - Execution traces          │  - Alternative labels                │
│  - Temporal reasoning        │                                      │
├─────────────────────────────────────────────────────────────────────┤
│                        Decision Trace Layer                          │
├─────────────────────────────────────────────────────────────────────┤
│  traces.json (enhanced)      │  rules.json (existing)               │
│  - Links to procedure steps  │  - Synthesized patterns              │
│  - Temporal metadata         │  - Confidence scoring                │
│  - Question/error tracking   │  - Promotion threshold               │
├─────────────────────────────────────────────────────────────────────┤
│                         Skills Layer (existing)                      │
├─────────────────────────────────────────────────────────────────────┤
│  kb-dbt-migration           │  kb-dbt-qa                            │
│  kb-dbt-preflight           │  kb-dbt-decision-trace                │
│  kb-dbt-orchestrator        │  kb-dbt-semantic-layer                │
│  (+ formal procedure specs) │  (+ pre/post conditions)              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Key Lessons from Talisman's Series

### 1. "Context Graph" is Marketing—This is Knowledge Management

> "This is a knowledge management problem. Repeat. This is a knowledge management problem."

The hype around "context graphs" obscures that the underlying challenge is capturing, organizing, and encoding procedural knowledge. Foundation Capital's vision requires the same knowledge engineering work that information architects have done for decades.

### 2. Data Does Not Self-Organize

> "At the end of the day, data does not self organize and describe itself, no matter how much pixie dust is distributed throughout."

AI cannot magically extract procedural knowledge. Someone must:
- Observe work practices
- Interview experts
- Extract tacit understanding
- Encode in formal representations

### 3. The Socio-Technical Ethos Matters

Documentation-as-culture, not documentation-as-compliance. Organizations that treat knowledge capture as integral to craft (not administrative burden) build compounding advantages.

**dbt-agent strength**: 320K+ lines of documentation represents engineering culture, not checkbox compliance. This ethos is rare and valuable.

### 4. Process Knowledge Requires Specialized Management

Not all knowledge is the same. Process knowledge requires:
- Unique elicitation methods (observation, CIT, think-aloud)
- Unique organization (temporal, conditional, hierarchical)
- Unique encoding (procedures, steps, executions, constraints)

Generic knowledge management tools don't capture this richness.

### 5. The Paradox of AI and Knowledge

> "Just as AI technology has created an urgent need for high-quality procedural knowledge, organizations find themselves impoverished in exactly that resource."

The organizations that outsourced execution lost the feedback loops that generate procedural knowledge. Now they need it for AI but don't have it.

**dbt-agent advantage**: We kept execution in-house. Every pipeline build generates traces that feed back into knowledge assets.

---

## Next Steps

### Immediate (This Week)
1. Create `procedural-knowledge.owl` skeleton with PKO core classes
2. Enhance decision trace schema to link executions to procedure steps
3. Draft failure mode catalog for top 5 common issues

### Short-Term (This Month)
1. Formalize procedure steps for kb-dbt-migration playbook
2. Add pre/post conditions to all skill definitions
3. Implement temporal queries on decision traces

### Medium-Term (This Quarter)
1. Build PKO-compliant procedure editor (web form for domain experts)
2. Integrate rule synthesis with procedure step definitions
3. Deploy GraphRAG with PKO-structured knowledge

### Long-Term (2026)
1. Full OWL formalization with reasoning capabilities
2. Cross-agent procedure composition
3. Automated procedure verification (formal methods)

---

## Sources

1. Talisman, Jessica. "Context Graphs and Process Knowledge." *Intentional Arrangement*, January 12, 2026.
2. Talisman, Jessica. "Process Knowledge Management, Part I: Accounting for How We Work." *Intentional Arrangement*, December 3, 2025.
3. Talisman, Jessica. "Process Knowledge Management, Part II: Collection Development and Organizing Principles." *Intentional Arrangement*, December 8, 2025.
4. Talisman, Jessica. "Process Knowledge Management, Part III: How We Lost Our Way." *Intentional Arrangement*, December 13, 2025.
5. Talisman, Jessica. "Process Knowledge Management, Part IV: From Theory to Practice, The Procedural Knowledge Ontology." *Intentional Arrangement*, December 18, 2025.
6. Carriero, Valentina Anita, Mario Scrocca, Ilaria Baroni, Antonia Azzini, Irene Celino. "Procedural Knowledge Ontology (PKO)." *ESWC 2025*.
7. dbt-agent repository analysis, January 17, 2026.

---

## Appendix: PKO Namespace Prefixes

```turtle
@prefix pko: <https://w3id.org/pko#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix pplan: <http://purl.org/net/p-plan#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix time: <http://www.w3.org/2006/time#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
```

---

*Report generated by Librarian agent. Process knowledge is the "boring stuff" that turns out to be foundational infrastructure for intelligent systems. Perhaps it was never boring at all.*
