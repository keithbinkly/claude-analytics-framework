# dbt-agent System Explainer

**Purpose:** Plain-language documentation for technical but non-expert readers.

---

## High-Level Overview

### 1. What is the dbt-agent system?

**Elevator Pitch:**
dbt-agent is an AI-powered development environment that turns Claude into a specialized dbt (data build tool) developer. Instead of a general-purpose AI assistant, you get an agent with deep knowledge of your specific codebase, established patterns, and proven workflows—one that remembers lessons from previous sessions and can coordinate multi-phase data pipeline work with human review gates.

**Expanded:**
At its core, dbt-agent is a structured knowledge system layered on top of Claude Code. It consists of 36 specialized "skills" (focused knowledge modules), a curated knowledge base of patterns and best practices, and a multi-agent workflow that breaks complex work into phases with mandatory human approval between each step.

The system connects to your data warehouse through MCP (Model Context Protocol), allowing the agent to actually run dbt commands, query live data, and validate its work against real results—not just generate code and hope it works. When you ask it to build a data model, it can compile, execute, profile the data, and run QA validation queries before handing off the work.

The secret sauce is "institutional memory": the system captures learnings from every session, identifies repeated patterns, and encodes solutions so they don't have to be rediscovered. If you solve a problem once, it becomes part of the knowledge base for all future work.

---

### 2. What problem does this system solve?

**The "Before" State (Manual dbt Development):**

| Challenge | Manual Reality |
|-----------|---------------|
| **Context loading** | Every session starts cold. You spend 10-15 minutes explaining the project structure, naming conventions, and business rules to the AI. |
| **Inconsistent patterns** | Different developers (or the same developer on different days) solve the same problem different ways. No single source of truth. |
| **Error repetition** | The same mistakes happen repeatedly. An AI might suggest putting a model in the wrong folder, and you have to correct it every time. |
| **No quality gates** | AI generates code, you run it, it fails, you debug, you run it again. This cycle repeats 3-4 times per model. |
| **Lost learnings** | You solve a tricky problem in January, but by June you've forgotten the solution. The AI never knew it in the first place. |
| **Handoff chaos** | Work passes between sessions with no structure. You spend time recreating context that existed in the previous session. |

**The "After" State (Agent-Assisted):**

| Improvement | dbt-agent Reality |
|-------------|-------------------|
| **Instant context** | Agent loads skills, patterns, and conventions automatically. It knows where models go, how to name them, and what tests to add. |
| **Consistent patterns** | Canonical models registry ensures reuse. Target: 75-90% of logic comes from existing patterns, not custom code. |
| **Error prevention** | "Zero tolerance" rules: always compile before run, always check dependencies, always validate architecture. Prevents 80%+ of common errors. |
| **Human approval gates** | Four-phase workflow with mandatory human review between phases. Problems caught early, not in production. |
| **Institutional memory** | Learner Agent extracts patterns weekly. Human corrections become permanent knowledge. The system gets smarter over time. |
| **Structured handoffs** | Handoff packages capture context, decisions, and next steps. Work survives session boundaries intact. |

**Measured Results:**
- Dev cycle time: **-97%** (upstream-prod tool)
- Context loading: **-95%** (mdflow templates)
- Convention violations caught: **817 warnings in baseline scan** (dbt-bouncer)
- Semantic search hit rate: **~65%** (qmd for "how do we handle X" queries)

---

### 3. What happens when a user starts a new pipeline migration?

**Step-by-step walkthrough (plain language):**

**Phase 1: Requirements Capture**
1. User says: "I need to migrate the merchant spend report to dbt"
2. Agent loads the **Business Context** skill
3. Agent asks: "Do you have a meeting transcript, requirements doc, or the legacy SQL script I should review?"
4. User provides the source material
5. Agent extracts: metric definitions, business rules, acceptance criteria, and builds a domain glossary
6. Agent writes: `handoffs/merchant-spend/business-context.md`
7. **GATE 1:** User reviews the requirements document. "Is this what you meant?" User approves or provides corrections.

**Phase 2: Data Discovery**
8. Agent loads the **Data Discovery** skill
9. Agent runs profiling queries against source tables (using MCP connection to warehouse)
10. Agent checks: row counts, date ranges, data quality issues, relationship cardinality
11. Agent detects: potential suppression risks (e.g., "table A has 1M rows but only 500K make it to the final report")
12. Agent writes: `handoffs/merchant-spend/data-discovery-report.md`
13. **GATE 2:** User reviews data findings. "These sources look healthy. That suppression makes sense because of X." User approves.

**Phase 3: Architecture Design**
14. Agent loads the **Tech Spec Writer** skill
15. Agent searches for canonical models: "What existing models can I reuse?"
16. Agent designs model inventory: which layer (staging/intermediate/marts), which folder, which materialization
17. Agent documents transformation rules and incremental strategy
18. Agent writes: `handoffs/merchant-spend/tech-spec.md`
19. **GATE 3:** User reviews architecture. "Change that model to use delete+insert instead of merge." User approves with modification.

**Phase 4: Implementation**
20. Agent loads the **Migration** skill
21. Agent writes SQL model files following the tech spec
22. Agent compiles (mandatory—never skip this step)
23. Agent runs the models
24. Agent executes QA validation queries (comparing to legacy output)
25. Agent writes: handoff package with results, variance analysis, and any known issues
26. **GATE 4:** User reviews deployment. "QA shows 0.03% variance, within tolerance. Approved for production."

**Total time:** 60-90 minutes across 1-2 sessions (vs. 4+ hours for manual approach)

**Key principle:** Humans stay in the loop at every phase transition. The agent does the heavy lifting, but humans approve architectural decisions before they become permanent.

---

## Architecture & Components

### 4. What are "skills" in this system?

**Plain language:**
Skills are specialized knowledge modules—like hiring an expert for a specific task. Instead of one general-purpose AI that knows a little about everything, you get focused expertise loaded on demand.

**How many:** 36 skills in `.claude/skills/` directory

**Examples (explained for a hiring manager):**

| Skill | What It Does | Like Hiring... |
|-------|--------------|----------------|
| **dbt-migration** | Guides the complete process of converting legacy SQL scripts into modern dbt models. Knows the 6-step playbook, checks for reuse opportunities, applies environment-specific date filters. | A senior data engineer who's done 50 migrations before. |
| **dbt-redshift-optimization** | Analyzes SQL for performance issues. Recommends distribution keys, sort keys, and incremental strategies. Estimates performance impact of changes. | A DBA who specializes in Redshift/Snowflake tuning. |
| **dbt-qa-execution** | Runs deep QA validation after models are built. Traces individual records through transformations, investigates variance, tests incremental behavior. | A QA engineer who doesn't just check "it runs"—they verify the numbers are right. |
| **dbt-canonical-model-finder** | Searches for existing reusable models before you build something new. Calculates overlap percentage. Prevents duplicate logic. | A librarian who knows every book in the library and says "we already have that." |

**Why this matters:**
Without skills, every conversation starts from scratch. With skills, the agent arrives with the right playbook already loaded. It knows what questions to ask, what patterns to follow, and what mistakes to avoid.

---

### 5. What is the knowledge base?

**Plain language:**
The knowledge base is the system's institutional memory—everything we've learned, codified into documents that agents can reference.

**What it contains:**

| Type | Example Files | Purpose |
|------|--------------|---------|
| **Patterns** | `migration-quick-reference.md`, `canonical-models-registry.md` | "Here's how we do things." Standard patterns that should be reused. |
| **Reference** | `folder-structure-and-naming.md`, `field-mappings.md` | "Here's where things go." Naming conventions, folder structures, column mappings. |
| **Troubleshooting** | `troubleshooting.md` | "Here's what to do when X breaks." Common errors and their fixes. |
| **Feedback** | `human-feedback-journal.md` | "Here's what the human corrected." Captures moments where the AI was wrong and the human fixed it. |
| **Templates** | QA queries, handoff packages, tech specs | "Here's the format to use." Standardized structures for common deliverables. |

**How agents use it:**
When an agent encounters a problem—say, "where should this model go?"—it doesn't guess. It loads `folder-structure-and-naming.md`, checks the rules, and applies them. When it's unsure if a pattern exists, it checks `canonical-models-registry.md` before building something new.

**How agents search it:**
The `unified_retrieval()` function searches across all knowledge sources in a single call:
- **Experience Store** — Cross-agent learnings from previous sessions
- **Manifest Parser** — Compiled SQL, model lineage, column definitions
- **Knowledge Graph** — 21,000+ documentation chunks indexed for instant search

One function call, all sources searched in parallel, results returned in ~125ms.

**Size:** ~6,000 lines of curated documentation across 18 files in `shared/knowledge-base/`

---

### 6. Explain the "handoff package" concept.

**The problem:**
AI conversations have memory limits. When a session ends or context fills up, knowledge is lost. If you're doing multi-step work (like a 4-phase pipeline migration), how do you preserve context between phases?

**The solution:**
Handoff packages are structured documents that capture everything the next phase (or the next session) needs to know. They're like a comprehensive meeting notes document that lets someone join mid-project without losing context.

**What's in a handoff package:**

```markdown
## Context Summary
- What we're building, why, who owns it

## Models Created
- List of files, their purpose, row count estimates

## Canonical Models Reused
- What existing patterns we leveraged (target: 75-90%)

## Initial Validation Results
- Did it compile? Did QA pass? What's the variance?

## Known Issues
- Any concerns, edge cases, or decisions that need review

## Next Steps
- Exactly what needs to happen next
```

**Why not just "continue the conversation"?**
1. **Context limits:** Claude has a token limit. Complex work exceeds it.
2. **Different specialists:** Phase 2 (data discovery) uses different skills than Phase 4 (implementation). Clean handoffs let each phase load the right expertise.
3. **Human review:** Handoffs create natural pause points for human approval.
4. **Durability:** Handoff files persist in git. Conversation context doesn't.

**Location:** `handoffs/` directory, organized by pipeline name and date.

---

### 7. What are the different agents?

**Agent roster (2-3 sentences each):**

| Agent | Specialty |
|-------|-----------|
| **Orchestrator** | The coordinator. Routes work to specialist agents, manages workflow state, enforces gates between phases. Knows which agent should handle which task and ensures handoffs happen properly. |
| **Discovery Agent** | The data profiler. Runs queries against source tables to validate assumptions before architecture is designed. Catches data quality issues and suppression risks early—before any code is written. |
| **Architect Agent** | The designer. Takes business requirements and data findings, then designs the model inventory: what models, which layers, what materializations, what incremental strategies. Produces the tech spec that implementation follows. |
| **Migration Agent** | The builder. Takes a tech spec and writes actual SQL model files. Applies patterns from the knowledge base, ensures reuse of canonical models, handles the 6-step migration playbook end-to-end. |
| **QA Agent** | The validator. Receives handoff packages from Migration Agent, runs deep variance analysis, tests incremental behavior, validates edge cases. Provides the "pass/fail" recommendation before production deployment. |
| **Learner Agent** | The librarian. Scans session logs for patterns, identifies when existing knowledge wasn't used, updates the knowledge base with new learnings. Makes the system smarter over time. |
| **Analyst Agent** | The data explorer. Runs ad-hoc queries against semantic layer metrics, validates business questions, produces data-driven answers. Used for "what were our top 10 merchants last month?" type questions. |

**How they coordinate:**
Agents communicate through handoff packages (structured markdown files) and Beads (a task tracking system). When one agent completes its phase, it creates a handoff and marks the work ready for the next agent.

---

### 7a. What are Beads?

**Plain language:**
Beads are external memory for tracking improvements across sessions. When an agent identifies work that can't be completed immediately, it creates a Bead—a tracked task that survives context resets and can be picked up in future sessions.

**Why they exist:**
AI sessions have context limits. If an agent discovers "we should add a test for X" but is in the middle of something else, that insight would be lost when the session ends. Beads capture it permanently.

**What a Bead contains:**
- **Title:** What needs to be done
- **Description:** Context, investigation steps, related files
- **Priority:** P0 (critical) through P4 (nice-to-have)
- **Status:** open, in-progress, closed
- **Assignee:** `claude` or `human`
- **Dependencies:** Links to blocking/blocked-by tasks

**How agents use them:**
```bash
# Create a Bead when you discover work
bd create --title "Add unique test for transaction_id" --priority 2

# Check what's open at session start
bd list --assignee claude --json

# Mark complete when done
bd update dbt-agent-xyz --status closed
```

**Current count:** 117 tracked issues

**Location:** `bd` CLI tool, stored in `.beads/` directory

---

## The Secret Sauce

### 8. Explain the "human approval gates" concept.

**What it is:**
Mandatory pause points where work stops and waits for human review before proceeding. The agent can do analysis and propose solutions, but major architectural decisions require explicit human approval.

**Where humans stay in the loop:**

| Gate | When | What Human Reviews |
|------|------|-------------------|
| **Gate 1** | After requirements capture | "Is this what you actually meant? Did I capture the business rules correctly?" |
| **Gate 2** | After data discovery | "These sources have these characteristics. Any concerns before I design the architecture?" |
| **Gate 3** | After architecture design | "Here's the model inventory and transformation rules. Approve this design?" |
| **Gate 4** | After implementation & QA | "Models built, QA passed with 0.03% variance. Ready for production?" |

**Why it matters:**
1. **Early error detection:** It's cheap to fix a requirements misunderstanding in Gate 1. It's expensive to discover it after models are in production.
2. **Architectural control:** Humans decide structure. Agents execute within that structure.
3. **Trust calibration:** Over time, you learn when to trust the agent's recommendations and when to dig deeper.
4. **Accountability:** There's always a human who approved the decision. The agent proposes; the human disposes.

**Anti-pattern this prevents:**
Without gates, agents can "declare victory early"—claim something is done when it's actually incomplete. Gates force verification before moving on.

---

### 9. What is "cross-agent learning"?

**The problem:**
When Agent A solves a problem on Monday, Agent B doesn't know about it on Tuesday. Each session starts fresh, re-learning things the system "should" already know.

**The solution:**
The Learner Agent extracts patterns from session logs, encodes them into the knowledge base, and makes them available to all future sessions.

**How it works:**

```
Monday: Migration Agent struggles with incremental strategy for late-arriving data
        → Eventually solves it with delete+insert pattern
        → Solution captured in session-logs/

Wednesday: Learner Agent scans session-logs/
           → Extracts pattern: "late-arriving data → delete+insert strategy"
           → Adds to knowledge-base/troubleshooting.md
           → Updates dbt-redshift-optimization skill references

Next Monday: Different user, different pipeline
             → Migration Agent loads skill
             → Pattern already available
             → No re-learning required
```

**What gets captured:**
- **Repeated solutions:** Same pattern used 3+ times → add to knowledge base
- **Human corrections:** User says "no, do it THIS way" → add to feedback journal
- **Error fixes:** Agent made mistake, here's how to avoid it → add to troubleshooting

**The compounding effect:**
Each session makes the system slightly smarter. After 50 sessions, you have 50 sessions worth of encoded learnings. The agent that works today is meaningfully better than the agent that worked three months ago.

---

### 10. Explain the QA methodology and "Row-Level Sample Trace."

**Why aggregate comparisons fail:**

Traditional QA: "Legacy report has 1,000,000 rows. New model has 1,000,000 rows. ✓ Match!"

**Problem:** The numbers can match while the data is completely wrong. If you're over-counting in one dimension and under-counting in another, they can cancel out.

**The Row-Level Sample Trace approach:**

Instead of comparing totals, trace **individual records** through every step of the transformation:

1. **Pick a sample:** Select 3-5 specific transactions
   - 1 "happy path" (typical case)
   - 1 edge case (NULL in optional field, boundary date)
   - 1 from a problematic population (if investigating variance)
   - 1-2 random samples

2. **Trace each record:**
```sql
-- Stage 1: Is the record in the source?
SELECT * FROM source_table WHERE transaction_id = 'ABC123'
-- Expected: 1 row

-- Stage 2: Does it survive the first join?
SELECT * FROM stage_2_cte WHERE transaction_id = 'ABC123'
-- Expected: 1 row. If 0 → record was suppressed. If 2+ → fan-out from join.

-- Stage 3: After aggregation...
-- Continue for each CTE in the model
```

3. **Document what you find:**
   - Row count at each stage (1 → 1 is good; 1 → 0 is suppression; 1 → 2+ is fan-out)
   - Which join caused the issue
   - Key field values that explain the behavior

**Why this is better:**
- You understand the **actual data flow**, not just the end result
- You catch fan-out (accidental row duplication from joins) that aggregate QA misses
- You catch suppression (records dropped unexpectedly) that "row counts match" hides
- You build concrete understanding of the transformation logic

**Authoritative source:** `shared/reference/qa-validation-checklist.md`, Phase 4.4

---

### 11. What is the Learner Agent?

**Role:** The repository knowledge expert—responsible for continuous learning, knowledge curation, and identifying when existing resources can solve current challenges.

**Core mission:** "You know what we have."

When any agent struggles with a problem, the Learner can identify:
- Existing patterns in the knowledge base that apply
- Skills that should have been loaded but weren't
- Documentation that answers the question
- Prior session learnings that solved the same issue

**Key responsibilities:**

| Responsibility | What It Does |
|----------------|--------------|
| **Gap detection** | When a problem has no existing solution, document it. Create a Bead (task) to add the solution after it's resolved. |
| **Underutilization detection** | "Agent solved problem the hard way when a skill existed." Identifies when knowledge wasn't used and updates triggers. |
| **Pattern extraction** | Scans session logs weekly. Extracts repeated solutions, common errors, user corrections. |
| **Resource evaluation** | When new external resources (articles, tools, frameworks) are submitted, evaluates: Is it relevant? Is it novel? How should it be integrated? |

**Tools available:**
- Knowledge Graph with 21,000+ indexed chunks (instant search)
- qmd semantic search for conceptual queries
- Session logs directory for pattern mining

**Deliverables:**
- Weekly learning reports
- Updates to `troubleshooting.md`, `canonical-models-registry.md`, `human-feedback-journal.md`
- Project update documents in `docs/updates/`

---

## By The Numbers

### 12. Stats summary

| Metric | Count |
|--------|-------|
| **Skills** | 36 directories in `.claude/skills/` |
| **Knowledge base files** | 18 files, ~6,000 lines in `shared/knowledge-base/` |
| **Documentation (markdown files)** | 471 files across repo |
| **Python tooling** | ~5,300 lines in `tools/` |
| **Tracked tasks (Beads)** | 117 issues |
| **QA validation checklist** | 580 lines, 6 phases |
| **Skills registry** | 912 lines documenting all skills |
| **CLAUDE.md (main agent instructions)** | ~900 lines |
| **Handoff template** | 490 lines with 5 phases |
| **Tool evaluations completed** | 4 tools adopted, 6+ queued |

---

### 13. Measured improvements

| Metric | Before | After | Improvement | Source |
|--------|--------|-------|-------------|--------|
| **Dev cycle time** | 15-30 min (upstream rebuilds) | 55 seconds | **-97%** | upstream-prod evaluation |
| **Context loading time** | ~2 min (10+ Read calls) | ~5 sec (1 mdflow command) | **-95%** | mdflow evaluation |
| **Convention violations caught** | Manual review | 817 warnings automated | **Automated** | dbt-bouncer baseline |
| **Semantic search hit rate** | ~30% (grep) | ~65% (qmd) | **+116%** | qmd evaluation |
| **QA iterations per model** | 3-4 cycles | 1-2 cycles | **-50%** | qa-validation-checklist |
| **Target: Canonical reuse** | Variable | 75-90% | **Standard** | migration-quick-reference |
| **Target: QA variance** | Variable | < 0.1% | **Standard** | qa-validation-checklist |
| **Target: First-compile rate** | Variable | 100% | **Standard** | compile-first rule |

---

## For The Skeptic

### 14. What's the difference between this and "just using Claude/Copilot"?

**Fair question.** Here's the honest answer:

| Capability | Vanilla Claude/Copilot | dbt-agent |
|------------|----------------------|-----------|
| **Context retention** | Starts fresh every session | Skills + knowledge base + handoffs persist learnings |
| **Domain expertise** | General-purpose | 36 specialized skills for dbt/data engineering |
| **Warehouse connectivity** | None (generates code only) | MCP connection: compile, run, query, validate |
| **Quality gates** | None (generates, you validate) | 4-phase workflow with mandatory human approval |
| **Pattern reuse** | No awareness of your patterns | Canonical models registry, 75-90% reuse target |
| **Error prevention** | Reactive (fails, then debug) | Proactive: compile-first rule, dependency checks, architecture validation |
| **Learning loop** | None | Learner Agent extracts patterns weekly |
| **Structured handoffs** | Context lost at session end | Handoff packages preserve full context |
| **Convention enforcement** | Manual review | dbt-bouncer automates 2,800+ checks |

**The infrastructure adds:**
1. **Consistency** — Same patterns applied every time, not dependent on the prompt you wrote
2. **Memory** — Learnings compound over time; mistakes become prevention rules
3. **Integration** — Actually runs code against your warehouse, not just generates text
4. **Gates** — Forces verification before moving forward
5. **Specialization** — Right expertise loaded for the right task

**When vanilla Claude is enough:**
- One-off questions ("what does this SQL do?")
- Simple tasks with clear specs
- Exploratory work where you want flexibility

**When dbt-agent shines:**
- Complex multi-step work (pipeline migrations)
- Work that needs to follow established patterns
- Work where mistakes are expensive to fix later
- Work that spans multiple sessions

---

### 15. What are the current limitations?

**Honest assessment of what doesn't work well yet:**

| Limitation | Description | Impact | Mitigation |
|------------|-------------|--------|------------|
| **Setup complexity** | The system has 36 skills, 18 KB files, MCP configuration, multiple tools. Onboarding a new user takes time. | High (barrier to adoption) | This explainer document; gradual exposure |
| **Memory still imperfect** | Despite handoffs, context can still be lost between sessions. unified_retrieval() helps but isn't automatic. | Medium | claude-mem evaluation queued (auto-injection) |
| **Skill loading is manual** | You have to know which skill to load, or rely on keyword triggers that may miss. | Medium | Better triggers; Learner detects underutilization |
| **Learning loop not fully automated** | Learner Agent runs weekly, manually triggered. Not real-time pattern extraction. | Medium | Potential automation with hooks |
| **dbt Fusion compatibility** | Some tools (dbt-bouncer) require dbt Core manifests. Dual-environment management adds friction. | Low-Medium | Document workarounds clearly |
| **Limited to dbt domain** | This system is hyper-specialized. It won't help with non-dbt work. | Low (intentional) | Use vanilla Claude for other work |
| **Token cost at scale** | Complex sessions with many MCP calls still consume significant tokens. | Medium | Advanced Tool Use evaluation queued (-85% potential) |
| **No CI/CD integration yet** | dbt-bouncer runs manually. Not yet wired into GitHub Actions. | Medium | On roadmap (week 3 of bouncer eval) |

**What we're actively working on:**
- `dbt-agent-z5d`: Memory Manager module (better session persistence)
- `dbt-agent-aku`: mem-agent-mcp evaluation (MCP-native memory)
- `dbt-agent-rp3`: DeepEval evaluation (automated agent testing)

**What we've explicitly deferred:**
- Multi-model orchestration (Airflow, Dagster) — we use dbt Cloud
- Real-time streaming patterns — focus is batch analytics
- Non-dbt data tools — intentionally specialized

---

*Generated by Orchestrator Agent, 2025-12-23*
*Reviewed and corrected by Learner Agent, 2025-12-23*
