# Analyze (Multi-Analyst Ensemble)

Fan out a business question to 4 parallel analyst personas and synthesize their perspectives into a single answer with disagreement highlighting.

**Usage:**
- `/analyze What is driving the increase in decline rates?`
- `/analyze How does this quarter compare to last quarter for transaction volume?`
- `/analyze Should we be concerned about approval rate trends?`

---

## Steps

### 0. Parse the Question + Route to Best-Fit Analyst

Arguments: `$ARGUMENTS`

If no question provided, ask the user: "What business question would you like the analyst ensemble to investigate?"

**Best-fit analyst routing (mandatory — determines initial analyst):**

| Question Pattern | Best-Fit Analyst | Why |
|---|---|---|
| "What is X?" / "How much?" / "Show me" / reporting | **Business Analyst** | Counting, grouping, reporting |
| "Why did X change?" / "What caused?" / anomaly | **Forensic Analyst** | Root cause decomposition |
| "What patterns?" / "What's interesting?" / discovery | **Exploratory Analyst** | Discovery, segmentation |
| "Is X significant?" / "Should we change threshold?" | **Statistical Analyst** | Formal tests warranted from start |

Default: Business Analyst (most questions are business questions).

**User-facing depth controls:**
- `--quick` → 1 analyst, no escalation, cap at ~150K tokens
- `--deep` → start with full 4-analyst ensemble immediately
- `--present` → full ensemble + auto-chain to /data-story + /present all
- No flag → adaptive depth (default) — start with 1 analyst, escalate on signal

**Routing output:**
```
Best-fit analyst: [name] — [1-sentence rationale]
Depth mode: [adaptive | quick | deep | present]
```

**Set ACTIVE_PROFILE based on flags:**
| Flag | ACTIVE_PROFILE | BEST_FIT_ANALYST |
|------|---------------|------------------|
| `--quick` | quick_scan | routing table result |
| (none) | standard | routing table result |
| `--deep` | deep_analysis | n/a (all 4) |
| `--present` | presentation_ready | n/a (all 4) |
| `--validate` | validate_only | n/a |
| `--forensic` etc. | quick_scan | forced to named analyst |

If `--deep` or `--present`: skip adaptive routing, proceed with full ensemble (Steps 1-8 as today).
If `--quick`: dispatch single analyst, skip to Step 4.5 Depth Check (which will return `none`).
If adaptive (default): dispatch single best-fit analyst, proceed to Step 4.5 after their analysis.

### 1. Load Shared Constraints + Detect Domain + Frame the Decision

Read the skill file for protocol and output schema, plus shared constraints (separate file for progressive disclosure):
```
Read .claude/skills/ai-analyst-ensemble/SKILL.md                              # protocol + output schema
Read .claude/skills/ai-analyst-ensemble/resources/shared-constraints.md       # 23 constraints (skip if validate_only)
```

Extract the shared constraints (#1-23) — this gets injected into every analyst prompt.
**If ACTIVE_PROFILE is validate_only:** skip shared-constraints.md (no analysts will be spawned).

**Domain detection priming (mandatory — 1 call, +28% novelty):** Before anything else,
name the business domain of this dataset/question. State it explicitly:
> "Domain: [e.g., BaaS card program analytics, gig economy disbursements, consumer lending]"

This single act primes all downstream reasoning with a domain-specific knowledge frame.

**SMART goal reframing (mandatory — prevents 34% quality degradation):** Rewrite the user's
question as a SMART analytical goal:
- **S**pecific: What exactly are we measuring?
- **M**easurable: What metric(s) will we query?
- **A**ttainable: Can the semantic layer answer this?
- **R**elevant: How does this connect to a business decision?
- **T**ime-bound: What date range? (default: trailing 12 months if unspecified)

**Decision framing (mandatory):** After domain + SMART reframing, identify and state:
- **What decision does this analysis serve?** (e.g., "whether to invest in gig economy partner growth")
- **Who is the decision-maker?** (e.g., "business managers evaluating partner portfolio")
- **What would change their action?** (e.g., "evidence that gig programs are growing faster than high-income")

Include domain, SMART goal, and decision framing in the prompt sent to all analysts AND the critic.

### 1.5. Load Partner Context (Memory-First Pattern)

**Before querying any data, load business context.** This is the NVIDIA memory-first pattern — analysts who read context first ask better questions and produce grounded interpretations.

Detect which partner(s) the question relates to by scanning for keywords:
- Dayforce / Ceridian / wallet / EWA / wage access → `repos/dbt-agent/shared/knowledge-base/partners/dayforce.md`
- Amazon / Flex / driver / gig → `repos/dbt-agent/shared/knowledge-base/partners/amazon-flex.md`
- QuickBooks / Intuit / SMB / Money by → `repos/dbt-agent/shared/knowledge-base/partners/quickbooks.md`
- Wealthfront / cash account / robo / wealth → `repos/dbt-agent/shared/knowledge-base/partners/wealthfront.md`
- Credibly / lending / loan / MCA → `repos/dbt-agent/shared/knowledge-base/partners/credibly.md`

If the question is about **all partners** or **portfolio-level**, read ALL 5 partner files in parallel.
If no partner is detectable, read the INDEX to understand what's available:
```
Read repos/dbt-agent/shared/knowledge-base/partners/INDEX.md
```

Extract from each partner file:
- **Business Context** section (for interpretation)
- **Recent Developments** section (for explaining metric changes)
- **Data Quality Notes** section (for caveats)
- **Analyst Findings** section (for prior findings — avoid re-discovering known facts)

This context gets injected into every analyst's prompt as `PARTNER CONTEXT`.

### 2. Load MCP Tool Availability

Before dispatching analysts, verify which MCP tools are available:

```
ToolSearch query: "+dbt query_metrics"
```

If `mcp__dbt__query_metrics` is not available, warn the user:
"Semantic layer tools not connected. Analysts won't be able to query metrics. Connect MCP first or proceed with limited analysis."

### 2.5. Query Plan Validator (Pre-Dispatch Schema Scout)

Before dispatching analysts, run the Query Plan Validator to produce a VERIFIED SCHEMA artifact.
This prevents analysts from guessing metric/dimension names and wasting queries on invalid references.

```
Read .claude/agents/query-plan-validator.md
```

Launch the validator agent:

```
Task(
  subagent_type="general-purpose",
  description="schema validator",
  prompt="""
  {query-plan-validator system prompt from .claude/agents/query-plan-validator.md}

  DOMAIN: {business domain detected in Step 1}
  USER QUESTION: {the user's question}

  Query the dbt Semantic Layer and produce the VERIFIED SCHEMA artifact.
  """
)
```

The validator's VERIFIED SCHEMA output gets injected into every analyst's prompt (Step 4) as:
```
VERIFIED SCHEMA (use ONLY these metric/dimension names in your QUERY PLANs):
{validator output}
```

If the validator returns `status: UNAVAILABLE`, warn the user and proceed without the schema —
analysts will need to run their own discovery queries.

DAAF (2025): Plan-checker agent validates query plans against available data BEFORE execution.
SiriusBI (VLDB 2025): Data Preparation Agent fires pre-analysis to validate data availability.

### 3. Load Analyst Prompts (Profile-Gated)

**If ACTIVE_PROFILE is quick_scan or standard:** Read 1 analyst + support files:
```
Read .claude/skills/ai-analyst-ensemble/resources/{BEST_FIT_ANALYST}-analyst.md
Read .claude/skills/ai-analyst-ensemble/resources/sqlite-cache-protocol.md
Read .claude/skills/ai-analyst-ensemble/resources/anomaly-detection-primitives.md
```

**If ACTIVE_PROFILE is deep_analysis or presentation_ready:** Read all 4 + support files:
```
Read .claude/skills/ai-analyst-ensemble/resources/forensic-analyst.md
Read .claude/skills/ai-analyst-ensemble/resources/exploratory-analyst.md
Read .claude/skills/ai-analyst-ensemble/resources/business-analyst.md
Read .claude/skills/ai-analyst-ensemble/resources/statistical-analyst.md
Read .claude/skills/ai-analyst-ensemble/resources/sqlite-cache-protocol.md
Read .claude/skills/ai-analyst-ensemble/resources/anomaly-detection-primitives.md
```

**If ACTIVE_PROFILE is validate_only:** Skip — no analyst prompts needed.

### 3.5. Create Analysis Team (Agent Teams — Upgrade #8)

**Architecture shift:** Instead of dispatching isolated sub-agents with static data, create
an agent team where teammates can communicate mid-analysis. This enables the core analytical
workflow: see aggregate pattern → drill down → unpack root cause.

**Team composition (profile-dependent):**

**If ACTIVE_PROFILE is quick_scan or standard** (3 members):

| Teammate | Role | MCP Access | Messages |
|----------|------|------------|----------|
| Data-Puller | Warehouse query specialist | YES (exclusive) | Receives drill-down requests from analyst |
| {BEST_FIT_ANALYST} | Best-fit analyst from Step 0 | No direct queries | Messages Data-Puller for data |
| Result-Checker | Independent claim verification | YES (for verification) | Receives analyst output, challenges claims |

**If ACTIVE_PROFILE is deep_analysis or presentation_ready** (6 members):

| Teammate | Role | MCP Access | Messages |
|----------|------|------------|----------|
| Data-Puller | Warehouse query specialist | YES (exclusive) | Receives drill-down requests from analysts |
| Forensic | Hypothesis testing | No direct queries | Messages Data-Puller for data |
| Exploratory | Pattern discovery | No direct queries | Messages Data-Puller for data |
| Business | Decision framing | No direct queries | Messages Data-Puller for data |
| Statistical | Quantitative rigor | No direct queries | Messages Data-Puller for data |
| Result-Checker | Independent claim verification | YES (for verification) | Receives analyst outputs, challenges claims |

**If ACTIVE_PROFILE is validate_only** (1 member):

| Teammate | Role | MCP Access | Messages |
|----------|------|------------|----------|
| Result-Checker | Re-derivation of prior conclusions | YES (for verification) | Reports to lead |

**Anti-hallucination architecture:** Analysts do NOT query the warehouse directly. They message
the Data-Puller, who validates schema, checks dimension existence, executes the query, and
returns verified data. This preserves the anti-fabrication property while enabling drill-down.

**Team creation:**

The orchestrator (you, the lead) creates the team with a shared task list:

```yaml
team_tasks:
  - id: canvas
    assignee: data-puller
    description: "Pre-query ALL low-cardinality dimensions for {time_range}"
    status: pending
    depends_on: []

  - id: forensic-analysis
    assignee: forensic
    description: "Forensic analysis: {user_question}"
    status: pending
    depends_on: [canvas]

  - id: exploratory-analysis
    assignee: exploratory
    description: "Exploratory analysis: {user_question}"
    status: pending
    depends_on: [canvas]

  - id: business-analysis
    assignee: business
    description: "Business analysis: {user_question}"
    status: pending
    depends_on: [canvas]

  - id: statistical-analysis
    assignee: statistical
    description: "Statistical analysis: {user_question}"
    status: pending
    depends_on: [canvas]

  - id: result-checking
    assignee: result-checker
    description: "Verify all analyst claims against warehouse"
    status: pending
    depends_on: [forensic-analysis, exploratory-analysis, business-analysis, statistical-analysis]
```

**Spawn teammates with role-specific prompts:**

Each teammate receives:
1. Their agent spec (from `.claude/agents/` or `.claude/skills/ai-analyst-ensemble/resources/`)
2. The VERIFIED SCHEMA from Step 2.5
3. Shared constraints #1-23 from SKILL.md
4. The SMART GOAL, DECISION FRAME, and PARTNER CONTEXT from Steps 1-1.5
5. The user's question
6. Instructions on how to message the Data-Puller for data

**Data-Puller prompt includes:**
```
Read .claude/agents/data-puller.md

VERIFIED SCHEMA:
{verified schema artifact from Step 2.5}

TIME RANGE: {analysis time range}
METRICS: {all metric names from schema}
DIMENSIONS: {all dimension names from schema}

Execute the canvas protocol first. Then respond to drill-down requests from teammates.
```

**Analyst prompt template (each of the 4 analysts):**
```
{analyst_system_prompt from resources/{name}-analyst.md}

SHARED CONSTRAINTS:
{shared constraints #1-23 from SKILL.md}

DOMAIN: {business domain detected in Step 1}

SMART GOAL: {SMART-reframed question from Step 1}

DECISION FRAME:
- Decision: {what decision this analysis serves}
- Decision-maker: {who will act on this}
- Action threshold: {what evidence would change their action}

PARTNER CONTEXT:
{from Step 1.5}

VERIFIED SCHEMA:
{verified schema artifact from Step 2.5}

ANOMALY DETECTION PRIMITIVES:
{from anomaly-detection-primitives.md}

DATA ACCESS:
You do NOT query the warehouse directly. The Data-Puller teammate handles all queries.

1. You will receive CANVAS DATA (all dimensions × months) when the Data-Puller completes
   its initial queries. Start your analysis with this data.

2. When you need MORE GRANULAR DATA mid-analysis (cross-dimension breakdowns, filtered
   slices, different time grains), message the Data-Puller with a structured request:

   data_request:
     need: "program × processor breakdown for Jul 2025"
     dimensions: ["program_code", "processor"]
     filters: {metric_time: "2025-07-01"}
     metrics: ["disbursement_success_rate", "disbursement_transaction_count"]
     reason: "Testing hypothesis that UberOneTime routes through VisaDirect"
     priority: high

3. The Data-Puller will respond with a verified data table. Incorporate it into your analysis.

THIS IS THE KEY ANALYTICAL WORKFLOW: See pattern in aggregate → request drill-down → unpack
root cause → request further detail if needed. Do not stop at "coverage gap" when drill-down
data could answer your question.

USER QUESTION:
{the user's question}

Produce your analysis following the output schema in the system prompt.
Remember:
- Methodology rigor checklist (constraint #20) — QUERY PLAN before every metric query
- Observations BEFORE interpretation (constraint #15) — bullet-point facts first, then claims
- Evidence table BEFORE narrative (constraint #13)
- Progressive anchoring (constraint #16) — baseline → deviation → co-occurrence → mechanism
```

**Result-Checker prompt:**
```
Read .claude/agents/result-checker.md

VERIFIED SCHEMA:
{verified schema artifact from Step 2.5}

You are a teammate on the analysis team. When analysts complete their findings, you receive
their outputs. For each analyst output:

1. Extract every factual claim with a specific number, dimension value, or trend assertion
2. Independently query the warehouse to verify each claim
3. Produce a verification report with VERIFIED / REFUTED / UNVERIFIABLE verdicts
4. Message the lead with your report

You have direct MCP access for verification queries. You do NOT use the Data-Puller —
your queries are independent to ensure true verification.
```

Tell the user: "Creating analysis team (Data-Puller + 4 Analysts + Result-Checker). Analysts can request drill-down data mid-analysis..."

### 4. Team Execution (Self-Coordinating)

The team self-coordinates through the shared task list and direct messaging:

1. **Data-Puller starts** → queries all low-cardinality dimensions → messages team "canvas ready"
2. **4 Analysts start** (after canvas) → analyze canvas data in parallel
3. **Analysts request drill-downs** → message Data-Puller → receive verified data → continue analysis
4. **As each analyst completes** → Result-Checker picks up their output immediately
5. **Result-Checker verifies** → produces verification report for each analyst

The lead monitors progress via the shared task list. No manual "collect results" step —
teammates report completion directly.

**Expected drill-down patterns:**
- Forensic may request: cross-dimension breakdowns to test causal hypotheses
- Exploratory may request: alternative time grains to find inflection points
- Business may request: dimension filters to scope recommendations
- Statistical may request: additional dimensions for regression/correlation analysis

**Time budget:** 10 minutes for the full team execution (canvas + analysis + drill-downs + verification).
If any teammate exceeds their task, the lead can check status and intervene.

### 4.1. Source Tie-Out Gate

Before analysts release their findings, run the source tie-out:

```
Task(
  subagent_type="general-purpose",
  prompt="You are the Source Tie-Out agent. Read .claude/agents/source-tie-out.md.
         Canvas output is at: [canvas path].
         Run the tie-out protocol and report results.",
  description="Source tie-out verification",
  model="sonnet"
)
```

**Gate logic:**
| Tie-Out Result | Action |
|---|---|
| PASS | Proceed to Step 5 (Collect Team Results) |
| WARN | Proceed, but inject this caveat into the Critic's input: "Source tie-out flagged [metric] with [delta]% discrepancy. Treat findings involving this metric with extra scrutiny." |
| FAIL | HALT. Re-run the Data-Puller canvas. If tie-out fails again after re-run, escalate to user: "Data integrity check failed twice for [metric]. Recommend manual verification before proceeding." |

### 4.5. Depth Check — Should We Go Deeper?

**Skip this step if `--deep` or `--present` was specified** (already running full ensemble).

Read the initial analyst's output. Check for these escalation signals:

```yaml
depth_check:
  signals:
    surprise: false    # Finding contradicts partner brief or prior analyses
    ambiguity: false   # Finding is near a threshold, noisy, CI overlaps zero
    stakes: false      # Finding would change a business decision if true
    conflict: false    # Finding contradicts another data source or analyst
    user_depth: false  # User specified --deep or --stats
  signal_count: 0
  escalation: none
  rationale: ""
```

**Escalation rules:**
| Signals | Escalation | What Happens Next |
|---|---|---|
| 0 signals | `none` | Synthesize current findings → present → done (~150K total) |
| 1-2 signals | `verify` | Dispatch Result-Checker on flagged findings only → synthesize → done (~250-300K) |
| 3+ signals OR `stakes: true` | `ensemble` | Dispatch remaining analysts for triangulation → full Step 5+ pipeline (~500-600K) |
| `user_depth: true` | `full` | Dispatch full ensemble + Statistical Analyst with formal tests (~600-800K) |

**If escalation is `none`:**
Skip Steps 5-6.5. Write a brief synthesis of the single analyst's findings:

```markdown
## Answer
[Direct answer — 2-3 sentences]

## Evidence
[Key metrics and dimensions queried]

## Confidence
[HIGH/MEDIUM/LOW based on data clarity]

## Caveats
[Any source tie-out warnings or data limitations]
```

Present to user and proceed to Step 7 (Present Results) and Step 8 (Writeback).

**If escalation is `ensemble` (3+ signals or stakes):**
Load the 3 remaining analyst prompts not loaded in Step 3:
```
Read .claude/skills/ai-analyst-ensemble/resources/{each remaining}-analyst.md
```
Spawn 3 new teammates with same prompt template. They join the existing team
and receive the Data-Puller's canvas data. Create tasks in shared task list.

**If escalation is `verify` or higher:**
State: "Depth check detected [signal names]. Escalating to [level]."
Dispatch additional agents as specified and continue with Step 5.

### 5. Collect Team Results

When all analysts and the Result-Checker have completed:

1. Read each analyst's final output (includes any drill-down data they incorporated)
2. Read the Result-Checker's verification report for each analyst
3. Apply gate logic from the Result-Checker:

| Result-Checker Status | Lead Action |
|---|---|
| **PASS** | Proceed to Critic (Step 5.5) with all analyst outputs unchanged |
| **WARN** | Proceed, but inject UNVERIFIABLE caveats into Critic input |
| **FAIL** | For each REFUTED claim: annotate with `[CLAIM REFUTED — actual: {value}]`, strip from findings |

4. Read the Data-Puller's query log for auditability

5. Check the Result-Checker's re-derivation results:

| Re-Derivation Verdict | Action |
|---|---|
| All CONVERGENT | High confidence — proceed |
| Any PARTIAL | Note in synthesis: "Independent verification partially confirmed [conclusion]" |
| Any DIVERGENT + claim PASS | WARN in synthesis: "Numbers verified but framing may be misleading for [conclusion]" |
| Any DIVERGENT + claim FAIL | BLOCK — do not include this conclusion. Note: "Conclusion [X] failed both verification and independent re-derivation" |

6. Check for Simpson's Paradox flags:
- If any flagged: inject into Critic input: "Result-Checker flagged potential Simpson's Paradox in [finding]. Verify that aggregate claims hold at segment level."

### 5.5. Critic Verification

**Skip if:** ACTIVE_PROFILE is quick_scan AND escalation is none.
**Skip if:** ACTIVE_PROFILE is validate_only.

Read the critic prompt and failure library:
```
Read .claude/skills/ai-analyst-ensemble/resources/critic-agent.md
Read .claude/skills/ai-analyst-ensemble/resources/failure-library.yaml
```

If the failure library has entries, include them in the critic prompt as `KNOWN ERROR PATTERNS`
(the critic should watch for these with extra vigilance — they are empirically observed patterns).

Launch the Critic Agent with all 4 analyst outputs:

```
Task(
  subagent_type="general-purpose",
  description="critic verification",
  prompt="""
  {critic_system_prompt from resources/critic-agent.md}

  ORIGINAL QUESTION:
  {the user's question}

  DECISION FRAME:
  {decision framing from Step 1 — what decision, who decides, what changes action}

  --- FORENSIC ANALYST OUTPUT ---
  {forensic analyst output}

  --- EXPLORATORY ANALYST OUTPUT ---
  {exploratory analyst output}

  --- BUSINESS ANALYST OUTPUT ---
  {business analyst output}

  --- STATISTICAL ANALYST OUTPUT ---
  {statistical analyst output}

  Produce your verification report following the output format in your system prompt.
  Check all 6 dimensions: citations, causal language, scope, insight categories, quality scoring (3-dimension rubric), banality.
  Then check cross-analyst consistency.
  """
)
```

Tell the user: "Critic verification complete. [N] findings passed, [M] flagged."

### 6. Synthesize

**Skip if:** Step 5.5 was skipped.

Read the synthesizer prompt:
```
Read .claude/skills/ai-analyst-ensemble/resources/synthesizer.md
```

Launch the synthesizer agent with analyst outputs AND the critic report:

```
Task(
  subagent_type="general-purpose",
  description="synthesizer",
  prompt="""
  {synthesizer_system_prompt from resources/synthesizer.md}

  ORIGINAL QUESTION:
  {the user's question}

  --- CRITIC VERIFICATION REPORT ---
  {critic agent output from Step 5.5}

  --- FORENSIC ANALYST OUTPUT ---
  {forensic analyst output}

  --- EXPLORATORY ANALYST OUTPUT ---
  {exploratory analyst output}

  --- BUSINESS ANALYST OUTPUT ---
  {business analyst output}

  --- STATISTICAL ANALYST OUTPUT ---
  {statistical analyst output}

  IMPORTANT: Read the Critic report FIRST. Apply block/warn/info flags before synthesizing.
  Produce the final synthesized answer following your output format.
  """
)
```

### 6.5. Integration Validation (Post-Synthesis Quality Gate)

Read the integration validator:
```
Read .claude/agents/integration-validator.md
```

Launch the Integration Validator with all outputs:

```
Task(
  subagent_type="general-purpose",
  description="integration validator",
  prompt="""
  {integration-validator system prompt from .claude/agents/integration-validator.md}

  ORIGINAL QUESTION:
  {the user's question}

  --- SYNTHESIZED OUTPUT ---
  {synthesizer output from Step 6}

  --- FORENSIC ANALYST OUTPUT ---
  {forensic analyst output}

  --- EXPLORATORY ANALYST OUTPUT ---
  {exploratory analyst output}

  --- BUSINESS ANALYST OUTPUT ---
  {business analyst output}

  --- STATISTICAL ANALYST OUTPUT ---
  {statistical analyst output}

  --- CRITIC REPORT ---
  {critic agent output from Step 5.5}

  Produce your integration validation report.
  """
)
```

**If status = FAIL:**
Show the user the critical issue(s) and the synthesis, noting what needs revision.
Consider re-running the synthesizer with the validator's fixes injected.

**If status = WARN:**
Include a brief "Quality Notes" section when presenting results (Step 7).

**If status = PASS:**
Proceed to presentation. Optionally mention "Integration validation: PASS" for confidence.

DAAF (2025): Integration-checker catches cross-agent contradictions that individual agents miss.
Table-Critic (ACL 2025): Curator agent ensures table-text consistency post-generation.

### 7. Present Results

Show the synthesizer's output to the user.

Then offer: "Want to see individual analyst outputs for any perspective? (forensic / exploratory / business / statistical)"

### 8. Writeback Findings to Partner Files

After presenting results, extract key findings from the synthesis and append them to the relevant partner file(s).

**Which partner file(s)?** Use the same detection from Step 1.5. If analysis covered multiple partners, write to each.

**What to write?** For each distinct finding in the synthesis, append an entry to the `## Analyst Findings` section:

```markdown
### [today's date] [Brief title from the finding]
- **Claim**: [The specific finding — one sentence]
- **Evidence**: [Metrics queried, values observed, dimensions used]
- **Confidence**: [HIGH | MEDIUM | LOW — from the synthesizer's confidence assessment]
- **Gap**: [What additional data would strengthen this — from the synthesizer or analysts]
- **Source**: [Which analyst(s) surfaced this — e.g., "Consensus (4/4)" or "Forensic + Statistical"]
- **Session**: [Current session GUID from /tmp/claude-session-id]
- **Status**: ACTIVE
- **Action**: [Recommended action from synthesis — or "No action required"]
- **Owner**: [Decision owner from action items table — or "TBD"]
- **Follow-up**: [Follow-up date — or "N/A"]
```

**Rules**:
- Only write findings with actual evidence (not speculation or recommendations)
- If a finding contradicts a prior ACTIVE finding, mark the prior one as `SUPERSEDED` with a note
- If a finding disproves a prior finding, mark the prior one as `DISPROVEN` — do NOT delete it
- Keep the entry concise — 3-5 lines max per finding
- Append at the bottom of the Analyst Findings section (before Known Gaps)
- Replace the "_No findings yet._" placeholder if this is the first writeback

**Skip writeback if**:
- The analysis produced no data-grounded findings (e.g., MCP tools weren't connected)
- The user explicitly asks not to write back
- The question was purely hypothetical / didn't query actual metrics

Tell the user: "Logged [N] findings to [partner file(s)]."

### 8.5. Update Failure Library (Automatic)

After the critic report is consumed, extract any `block` or `warn` severity issues and
append them to the failure library:

```
Read .claude/skills/ai-analyst-ensemble/resources/failure-library.yaml
```

For each critic-flagged issue with `block` or `warn` severity:
1. Check if a matching entry already exists (same `type` + similar `example`)
2. If exists: increment `frequency`, update `last_seen`
3. If new: append entry with `frequency: 1`

**Entry format:**
```yaml
- type: <issue_type from critic — e.g., causal_language, scope_extension, citation_not_found>
  category: <Access | Data | Method | Perf | Process>
  analyst: <which analyst produced this — forensic/exploratory/business/statistical>
  example: "<the specific claim that was flagged — 1 sentence>"
  fix: "<the critic's suggested correction — 1 sentence>"
  severity: <block | warn>
  frequency: 1
  first_seen: <today's date>
  last_seen: <today's date>
```

**Category assignment guide:**
- **Access**: MCP tool unavailable, permission denied, connection timeout
- **Data**: Wrong denominator, missing data, wrong grain, data quality issue
- **Method**: Causal language, ecological fallacy, scope extension, confirmation bias
- **Perf**: Slow query, token budget exceeded, timeout
- **Process**: Missed step, wrong agent routing, writeback failure

**Rules:**
- Max 50 entries. If at 50, drop the entry with lowest frequency before adding.
- Only `block` and `warn` — skip `info` (those are not errors, just notes).
- Don't duplicate: same type + same analyst + similar example = increment, not new entry.

Table-Critic (ACL 2025): The Curator agent distills critique patterns into a reusable template
tree. Our failure library is the lightweight version — empirical error patterns that prime
future critic runs.

### 8.7. Save Workstream State

After writeback and failure library update, persist session state to prevent loss on compaction:

1. **Identify the active workstream** from `thoughts/shared/workstreams/` (typically `ai-analysis-r-and-d.yaml`)
2. **Update the workstream YAML**:
   - `last_action`: Brief summary of this `/analyze` run (topic, finding count, partner files written)
   - `next_action`: What follow-up analysis or action is warranted
   - Append a `sessions` entry if this is a new session
   - Add any new artifacts to `key_files`
3. **Update the decision log** if this run produced conclusions that affect future analysis

This step is especially critical during multi-round analysis (Step 9) — save after EACH round, not just at the end.

See: `.claude/rules/auto-save-state.md` for full auto-save protocol.

### 9. Offer Follow-Up Round (Optional)

After presenting results, offer the user a follow-up analysis round:

"Want to go deeper on any finding? I can run a focused follow-up round where analysts
build on these results rather than starting fresh."

**If user accepts:**
1. Take the synthesis output as `PRIOR FINDINGS` context
2. Take the user's follow-up question
3. Inject both into the analyst dispatch (Step 4) as additional context:
   ```
   PRIOR FINDINGS (from previous round — do NOT rediscover these):
   {synthesis output from Step 6}

   FOLLOW-UP QUESTION:
   {user's new question}

   Build on the prior findings. Do not repeat what is already established.
   Focus on what the prior round could not answer or left as gaps.
   ```
4. Run Steps 4-8 again with the enriched context

**Rules:**
- Maximum 2 follow-up rounds (3 total including initial). After that, recommend a
  new `/analyze` session — context accumulation degrades quality past 3 rounds.
- Each round's analysts receive ALL prior synthesis outputs (cumulative history).
- Track round number: "Round [N] of 3"

DataSage: 6 questions with history achieved "significantly higher diversity and coverage"
than 12 without. QUIS: iterative bootstrapping builds cumulative analytical depth.

---

## Quick Mode

For simpler questions where the full ensemble is overkill, the user can call a single analyst directly:

- `/analyze --forensic Why did approval rates drop?` — hypothesis testing only
- `/analyze --exploratory Show me transaction patterns` — broad scan only
- `/analyze --business Should we adjust our thresholds?` — decision framing only
- `/analyze --statistical Is this trend significant?` — rigor check only

When a `--{analyst}` flag is detected, skip steps 4-6 and dispatch only that single analyst.
Present its output directly (no synthesizer needed).
