---
name: ai-analyst-ensemble
description: |
  Multi-analyst ensemble that fans out business questions to 4 parallel analyst personas
  (Forensic, Exploratory, Business, Statistical) and synthesizes their outputs into a
  consensus answer with disagreement highlighting. Use when asked to "analyze this data
  from multiple perspectives", "run the ensemble", "get different analyst viewpoints",
  or "deep analysis with consensus". Queries certified metrics via dbt MCP Semantic Layer API.
---

# AI Analyst Ensemble

4 analysts + 1 synthesizer. Each analyst sees the same question but applies a different
reasoning style. The synthesizer finds consensus, highlights disagreement, and produces
the final answer.

**When to use:** Business questions where multiple perspectives add value — especially
investigative, comparative, or strategic questions. For simple lookups, use `dbt-nl-queries`
or `ai-analyst-profile` directly.

---

## Execution Protocol

### Step 1: Validate, Detect Domain, and Frame the Decision

Check that the question is analytical (not a dbt development task). If it's about building
models, running tests, or pipeline work — route to the appropriate dbt skill instead.

**Domain detection priming (mandatory — 1 call, +28% novelty):** Before anything else,
name the business domain of this dataset/question. State it explicitly:
> "Domain: [e.g., BaaS card program analytics, gig economy disbursements, consumer lending]"

This single act primes all downstream reasoning with a domain-specific knowledge frame.
Data-to-Dashboard (2025) showed +28% novelty and +31% depth from this one intervention alone.

**SMART goal reframing (mandatory — prevents 34% quality degradation):** Rewrite the user's
question as a SMART analytical goal before dispatching:
- **S**pecific: What exactly are we measuring? (not "look at trends" but "measure month-over-month change in approval rate by partner")
- **M**easurable: What metric(s) will we query?
- **A**ttainable: Can the semantic layer answer this? (check available metrics)
- **R**elevant: How does this connect to a business decision?
- **T**ime-bound: What date range? (default: trailing 12 months if unspecified)

AgentPoirot ablation (ICLR 2025): removing SMART goal constraint drops quality scores by 34%.
Vague "find interesting trends" mandates degrade performance significantly.

**Decision framing (mandatory):** After domain + SMART reframing, identify and state:
- **What decision does this analysis serve?** (e.g., "whether to invest in gig economy partner growth")
- **Who is the decision-maker?** (e.g., "business managers evaluating partner portfolio")
- **What would change their action?** (e.g., "evidence that gig programs are growing faster than high-income")

Include domain, SMART goal, and decision framing in the prompt sent to all analysts.

### Prompt Scope Control (Learning: 2026-02-21)

Avoid overly specific domain terms in analyst agent instructions. Terms like "semantic layer" in
prompts restrict breadth and cause analysts to self-censor valid exploration paths. Use broader
framing: "data infrastructure" instead of "semantic layer", "business metrics" instead of
"MetricFlow metrics". Test prompt variations by running parallel agents with different scope.

**Anti-pattern:** "Analyze semantic layer adoption trends" → analyst ignores non-SL evidence
**Better:** "Analyze how certified metrics are consumed across the organization" → broader coverage

### Step 2: Fan Out to 4 Analysts

Launch 4 parallel agents using the Task tool:

```
For each analyst in [forensic, exploratory, business, statistical]:
  Task(
    subagent_type="general-purpose",
    prompt=[analyst system prompt] + [shared constraints] + [user question],
    description=f"{analyst} analyst",
    run_in_background=True
  )
```

Read each analyst's system prompt from `resources/{analyst}-analyst.md`.

### Step 3: Critic Verification

After all 4 analysts complete, pass their outputs to the Critic Agent:

```
Task(
  subagent_type="general-purpose",
  prompt=[critic prompt] + [all 4 analyst outputs] + [query results] + [decision framing],
  description="critic verification"
)
```

Read the critic prompt from `resources/critic-agent.md`.

The Critic checks every finding across 6 dimensions: citation accuracy, causal language
violations, scope extensions, insight categories, quantitative quality scoring (3-dimension
rubric: relevance/correctness/completeness ≥0.8), and banality. Plus cross-analyst
contradictions. It produces a verification report — NOT revised findings.

**Important:** The Critic has NO data tools. It only works with analyst outputs and
the query results you provide. This separation is the guarantee.

### Step 4: Synthesize

Pass all 4 analyst outputs AND the critic's verification report to the synthesizer:

```
Task(
  subagent_type="general-purpose",
  prompt=[synthesizer prompt] + [all 4 analyst outputs] + [critic report] + [original question],
  description="synthesizer"
)
```

Read the synthesizer prompt from `resources/synthesizer.md`.

The synthesizer uses the critic report to:
- **Remove** findings flagged as `block` severity
- **Revise** findings flagged as `warn` severity
- **Highlight** contradictions rather than averaging them
- **Preserve** findings marked as `passed`

### Step 5: Present

Show the synthesizer's output to the user. Offer to show individual analyst outputs
or the critic report if the user wants transparency.

---

## Shared Constraints

23 analytical constraints injected into every analyst prompt. Extracted for progressive disclosure.

**Load:** Read `resources/shared-constraints.md` at Step 3 when assembling analyst prompts.

Topics: MCP-only metrics (#1-2), evidence labeling (#3-7), causal language (#11),
statistical rigor (#12-14, #21), progressive anchoring (#15-16), schema verification
(#17, #22), methodology (#18-20), drill-down access (#23).

## Resource Loading by Profile

| Resource | quick_scan | standard | escalated | deep | validate |
|----------|-----------|----------|-----------|------|----------|
| SKILL.md + execution-profiles.md | Step 0 | Step 0 | Step 0 | Step 0 | Step 0 |
| shared-constraints.md | Step 3 | Step 3 | Step 3 | Step 3 | -- |
| {best-fit}-analyst.md | Step 3 | Step 3 | Step 3 | -- | -- |
| all 4 analyst.md files | -- | -- | Step 4.5 | Step 3 | -- |
| anomaly + cache + sql-patterns | Step 3 | Step 3 | Step 3 | Step 3 | -- |
| critic-agent.md + failure-library | -- | Step 5.5 | Step 5.5 | Step 5.5 | -- |
| synthesizer.md | -- | Step 6 | Step 6 | Step 6 | -- |

---

## Data Access Architecture (Upgrade #8)

Analysts access warehouse data through the **Data-Puller teammate**, not directly.

| Role | MCP Access | Data Access |
|------|-----------|-------------|
| Data-Puller | YES — all dbt Semantic Layer tools | Queries warehouse, serves analysts |
| Forensic Analyst | NO direct access | Messages Data-Puller for drill-downs |
| Exploratory Analyst | NO direct access | Messages Data-Puller for drill-downs |
| Business Analyst | NO direct access | Messages Data-Puller for drill-downs |
| Statistical Analyst | NO direct access | Messages Data-Puller for drill-downs |
| Result-Checker | YES — independent verification | Queries warehouse to verify claims |

**Why this separation:**
- Prevents fabrication (analysts can't invent dimension values they never queried)
- Enables drill-down (analysts can request granular data mid-analysis)
- Deduplicates queries (4 analysts needing the same data get one query)
- Creates audit trail (Data-Puller logs every query for Result-Checker)

---

## Output Schema (All Analysts Produce This)

```yaml
analyst: <persona_name>
query: <original user question>
findings:
  - claim: <what you're asserting>
    claim_type: OBSERVED | INFERRED | SPECULATIVE
    evidence: <data/calculation/query result>
    evidence_status: VERIFIED | PARAPHRASED | NOT_FOUND
    confidence: high | medium | low
    confidence_rationale: <why this confidence level>
    actionability: <what would a decision-maker do with this?>
    gap: <what would strengthen this claim>
    queries_used:
      - tool: <tool name>
        input: <what you passed>
        result_summary: <key numbers>
methodology: <1-2 sentences on approach>
caveats: <data quality issues, limitations>
follow_up_questions:
  - <next question the data could answer>
```

---

## When NOT to Use the Ensemble

- **Simple lookups**: "What is our approval rate?" — use `ai-analyst-profile` or `dbt-nl-queries`
- **Development tasks**: Building models, running tests — use dbt skills
- **Single-perspective questions**: If only one type of analysis makes sense, call that analyst directly

The ensemble shines on: investigative questions, trend analysis, strategic decisions, and
anything where "it depends on how you look at it" is the honest first answer.
