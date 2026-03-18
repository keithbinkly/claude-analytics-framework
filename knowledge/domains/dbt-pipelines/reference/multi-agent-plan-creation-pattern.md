# Making Of: Merchant Spend Feature Expansion Plan

**Date:** December 17, 2025
**Output:** `handoffs/interchange_revenue_migration/merchant-spend-feature-expansion-plan.md`

---

## The Challenge

Consolidate 5 planned features into a single optimized implementation:
- Virtual card indicator
- eWallet value
- MCC description (4-digit)
- 90-day active cardholder boolean
- Interchange metrics

**Risk:** Row explosion in mart models, pipeline runtime degradation.

---

## Multi-Agent Workflow

### Phase 1: Orchestrator Agent (Claude Code)

**Skills Activated:**
| Skill | Purpose |
|-------|---------|
| `dbt-modeling` | CTE patterns, layer-specific templates |
| `dbt-redshift-optimization` | Conditional aggregation strategy, DISTKEY decisions |
| `dbt-semantic-layer-developer` | MetricFlow YAML patterns (measures → metrics) |

**Key Actions:**
1. Queried beads for planned features (fq7.1-fq7.4, 46, 45, 57, 58)
2. Retrieved model details via MCP (`get_model_details`, `get_model_parents`)
3. Discovered MCC description already exists → closed 2 beads immediately
4. Designed conditional aggregation strategy (same grain, more measures)
5. Drafted 3-phase implementation plan

**Critical Insight:** The semantic layer skill caught incorrect MetricFlow patterns in my initial draft. Corrected:
- Measures use `agg:` (sum, count_distinct)
- Simple metrics wrap measures with `type_params.measure:`
- Ratio metrics reference OTHER METRICS, not measures directly

### Phase 2: Learner Agent Evaluation

Human routed the draft plan to the Learner agent for tool utilization review.

---

#### What is the Learner Agent?

**Think of it as the team's "institutional memory" combined with a tool librarian.**

The Learner Agent is a specialized Claude Code session that:
1. **Knows what tools we have** - Tracks our evaluated tool stack (upstream-prod, qmd, mdflow, etc.)
2. **Remembers past solutions** - Indexes patterns from previous sessions in a searchable knowledge graph
3. **Evaluates new resources** - Analyzes external tools/articles and decides what's worth adopting
4. **Compounds learnings** - Extracts patterns from completed work and adds them to our knowledge base

It runs from a custom "slash command" (`/learner`) that loads specialized instructions for this role.

---

#### What Was I Asked To Do?

The human said:
> *"I want to ensure [the plan] is leveraging all the advanced tools we have in order to build this as quickly and reliably / accurately as possible."*

The Orchestrator had created a solid architectural plan, but it didn't include specific instructions on *which tools to use at each step*. Without these instructions, the implementation agent might:
- Rebuild upstream models unnecessarily (when `upstream-prod` auto-redirects to production data)
- Miss existing patterns in our knowledge base
- Skip data profiling queries that catch issues early
- Forget mandatory rules like "always compile before run"

---

#### What I Added

I enhanced the plan with a **Tool Utilization Guide** (~150 lines) containing:

**1. Pre-Implementation Checklist**
Before writing any code, check if the pattern already exists:
```
unified_retrieval("virtual card indicator BIN")  → Search our 21K-chunk knowledge graph
get_related_models("virtual card")               → MCP tool to find similar dbt models
get_model_health("int_transactions__auth_all")   → Verify upstream reliability
```

**2. Phase-Specific Tool Commands**
For each implementation phase, I added the exact commands to run:
```bash
# Profile source data BEFORE writing SQL
dbt show --inline "SELECT card_type, COUNT(*) FROM stg_edw__dim_bin GROUP BY 1"

# MANDATORY: Compile before run (catches 90% of errors in 5 seconds vs 5 minutes)
dbt compile --select model_name
dbt run --select model_name  # upstream-prod auto-enabled for fast iteration
```

**3. Skills to Load**
Each phase now specifies which specialized "skills" (curated instruction sets) to activate:
- Phase 1: `dbt-canonical-model-finder`, `dbt-data-discovery`
- Phase 2: `dbt-semantic-layer-developer`, `dbt-redshift-optimization`
- Phase 3: `dbt-qa-execution`, `dbt-dependency-mapper`

**4. QA Templates**
Referenced our proven validation queries from `troubleshooting.md`:
- Template 1: Variance analysis for new measures
- Template 4: Top N validation for interchange
- QUALIFY pattern for join fan-out prevention

**5. Quick Reference Table**
A cheat sheet at the end so the implementation agent can quickly look up any tool:

| Tool | When to Use | Command |
|------|-------------|---------|
| upstream-prod | Every `dbt run` in dev | Auto-enabled |
| dbt compile | BEFORE every `dbt run` | `dbt compile --select model` |
| dbt show | Data profiling, QA queries | `dbt show --inline "SQL"` |
| unified_retrieval() | Find existing patterns | Python KG query |

---

### Phase 3: Execution Agent (GitHub Copilot)

**Skills Activated:**
| Skill | Purpose |
|-------|---------|
| `sql-analysis` | Ad-hoc querying via `dbt show` to profile data |
| `dbt-execution` | Running models and operations in the IDE terminal |
| `data-validation` | Comparing datasets side-by-side to verify logic |

---

#### What is the Copilot?

**I am the "hands-on developer" living directly inside VS Code.**

While the Orchestrator plans the architecture and the Learner optimizes the tooling, I am the one who actually:
1.  **Touches the code** - I edit files, run terminal commands, and fix syntax errors.
2.  **Validates assumptions** - I run the queries to prove if the plan's data assumptions are true.
3.  **Iterates rapidly** - I work in a tight loop with the human to debug issues in real-time.

I have access to the full workspace context, the terminal, and the dbt CLI, allowing me to execute the "last mile" of the work.

---

#### What Was I Asked To Do?

The Orchestrator's plan included a critical dependency: **"Investigate if EDW tables can replace GBOS for wallet type attribution."**

The goal was to simplify our pipeline. If the Enterprise Data Warehouse (EDW) already had clean wallet data (Apple Pay, Google Pay, etc.), we wouldn't need to build complex logic on top of the raw GBOS transaction tables.

My task was to:
1.  Find the relevant EDW tables.
2.  Prove they link to our transactions.
3.  Verify the data matches what we see in GBOS.

---

#### The Investigation Story (A Plot Twist)

**1. The False Start**
I started by searching the EDW schema for "wallet" columns. Initial results looked bleak—I found `dim_payment_instrument_hist`, but it only tracked physical form factors (Plastic vs. Virtual), not the specific wallet provider (Apple vs. Google). I was ready to report back: *"EDW doesn't have this data."*

**2. The Human Intervention**
The human developer intervened, pointing out specific tables I had missed: `dim_wallet_type` and `dim_payment_identifier_device`. This is a key part of the workflow—I can search broadly, but human domain knowledge often provides the necessary shortcut.

**3. The "Apple Pay" Problem**
Armed with the right table names, I ran a side-by-side comparison query.
- **Left side:** GBOS data (Source of Truth)
- **Right side:** EDW data (The Challenger)

The results were shocking.
- GBOS showed a transaction was **"Google Pay"**.
- EDW showed the *same* transaction was **"Apple Pay"**.

I dug deeper. It turned out that for this specific data source (`sor_uid=3`), the EDW was defaulting almost *everything* to "Apple Pay". It had **zero** records for Google Pay, despite GBOS having millions.

**4. The Pivot**
Because I could run these queries in real-time and show the results to the human, we made a data-driven decision immediately.
- **Plan A (EDW):** Rejected due to data quality failure.
- **Plan B (GBOS):** Accepted. I validated a "Point-in-Time" logic to handle the complex history of device updates in GBOS.

I updated the handoff file with these findings, allowing the Orchestrator to proceed with the correct architectural decision without wasting days building on bad data.

---

#### Why This Matters

**Without tool instructions:** Implementation agent might take 3-4 iterations to get it right, missing optimizations and repeating past mistakes.

**With tool instructions:** Implementation agent has a checklist to follow, leveraging months of accumulated learnings in a single session.

**The broader pattern:** The Learner Agent acts as a "force multiplier" - it doesn't write the implementation code, but ensures the agent that does has access to everything we've learned.

---

#### Bonus: What Else Happened in This Learner Session

Before reviewing the merchant spend plan, the Learner Agent was doing its regular job:

**1. Tool Evaluation Completed**
Marked `qmd` (semantic search tool) as ✅ KEEP after 1-week evaluation. Updated the tool evaluation dashboard.

**2. External Resource Analysis**
Human shared [Chip Huyen's llama-police](https://huyenchip.com/llama-police.html) - a list of 40+ open source LLM tools. Learner analyzed which ones would benefit our workflow:
- **dbt-bouncer** → Added to queue (convention linter, prevents folder misplacement)
- **mem-agent-mcp** → Added to queue (MCP-native memory, potential claude-mem replacement)
- **DeepEval** → Added to queue (pytest for LLM outputs, could test our agents)
- **SQLCoder** → Extracted knowledge, didn't adopt tool (see below)

**3. Knowledge Extraction (Not Just Tool Adoption)**
For SQLCoder (text-to-SQL model), instead of just deferring it, the Learner researched the underlying techniques and created a new knowledge base document:

`shared/knowledge-base/text-to-sql-prompt-patterns.md`

Key patterns extracted:
- Schema representation tiers (basic → relationships → CREATE TABLE)
- Foreign keys add +2% accuracy on JOINs
- In-domain examples add +48% accuracy vs zero-shot
- Context window rule: ~70% useful for examples, then degrades

**This is the Learner's value proposition:** Don't just say "yes/no" to tools - extract the underlying knowledge and make it available to all agents.

### Phase 3: Orchestrator Final Pass

Fixed markdown formatting issues (nested code fences) to ensure document renders correctly for human review.

---

## Outcome

| Metric | Result |
|--------|--------|
| Features consolidated | 5 → 1 cohesive plan |
| Beads closed (already done) | 2 |
| Row explosion prevented | Conditional agg strategy |
| Skills activated | 3 |
| Agents collaborated | 2 (Orchestrator + Learner) |
| Human review gates | 1 (awaiting approval) |

---

## Agent Delegation Plan

### Division of Labor

| Agent | Platform | Responsibilities |
|-------|----------|------------------|
| **Claude Code (Orchestrator)** | Claude CLI | Planning, architecture, skill loading, documentation |
| **Claude Code (Developer)** | Claude CLI | Writing SQL models, YAML configs, schema definitions |
| **Gemini 2.5 Pro (Copilot)** | VS Code Extension | Warehouse execution: `dbt run`, `dbt show`, `dbt test` |

### Why Split Execution?

Claude Code excels at reasoning and code generation but lacks direct warehouse connectivity. Gemini Copilot has MCP access to execute SQL against Redshift. This mirrors our successful QA workflow (see `docs/updates/2025-12-12-multi-agent-qa-workflow-deep-dive.md`).

### Handoff Points by Phase

#### Phase 1: Virtual Card + eWallet Enrichment
| Step | Agent | Output |
|------|-------|--------|
| 1a. Write `is_virtual_card` logic | Claude Developer | SQL in `int_transactions__auth_all.sql` |
| 1b. Write `ewallet_type` pattern | Claude Developer | SQL in same model |
| **→ HANDOFF** | | |
| 1c. Profile BIN data | Gemini Copilot | `dbt show` results |
| 1d. Profile merchant patterns | Gemini Copilot | `dbt show` results |
| 1e. Compile + run model | Gemini Copilot | `dbt compile && dbt run` |
| 1f. Verify output | Gemini Copilot | `dbt show` validation |

#### Phase 2: Conditional Aggregations + Semantic Layer
| Step | Agent | Output |
|------|-------|--------|
| 2a. Add conditional aggs to `int_transaction_pairs__purchase` | Claude Developer | SQL edits |
| 2b. Update semantic base model | Claude Developer | SQL edits |
| 2c. Write MetricFlow YAML | Claude Developer | `_semantic.yml` |
| **→ HANDOFF** | | |
| 2d. Verify grain unchanged | Gemini Copilot | `dbt show` row counts |
| 2e. Run models | Gemini Copilot | `dbt run --select +int_transaction_pairs__purchase` |
| 2f. Validate MetricFlow | Gemini Copilot | `mf validate-configs && mf query` |

#### Phase 3: Active Cardholder + Interchange
| Step | Agent | Output |
|------|-------|--------|
| 3a. Write `is_active_90d` join | Claude Developer | SQL in enrichment model |
| 3b. Create interchange integration model | Claude Developer | New SQL file |
| **→ HANDOFF** | | |
| 3c. Profile account actives source | Gemini Copilot | `dbt show` |
| 3d. Check interchange join fan-out | Gemini Copilot | `dbt show` duplicates query |
| 3e. Run full pipeline | Gemini Copilot | `dbt run` |
| 3f. Execute QA Templates 1 & 4 | Gemini Copilot | Variance + Top N validation |

### Handoff Package Format

Each handoff to Gemini Copilot includes:
```markdown
## Execution Package: [Phase X Step]

### Files Modified
- path/to/model.sql (lines X-Y)

### Commands to Run
1. `dbt compile --select model_name`
2. `dbt run --select model_name`
3. `dbt show --inline "validation query"`

### Success Criteria
- [ ] Compile succeeds
- [ ] Row count within 10% of baseline
- [ ] QA variance < 0.1%

### Report Back
- Row counts before/after
- Any errors encountered
- QA query results
```

---

## Why This Matters

Traditional approach: 5 separate implementations, each risking grain changes, runtime hits, and QA gaps.

Multi-agent approach:
1. **Orchestrator** designs holistic architecture with skill-informed patterns
2. **Learner** ensures implementation will leverage full tool stack
3. **Human** reviews consolidated plan before any code is written

Result: Faster execution, fewer iterations, knowledge captured for future pipelines.

---

*Generated by Orchestrator Agent (Claude Code)*
