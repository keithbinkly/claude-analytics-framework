---
name: meta-context
description: >
  Author, validate, evaluate, and maintain the Meta Context Schema for dbt
  MetricFlow YAML. Use when the user mentions "meta context", "meta:",
  "business context for metrics", "context schema", "metric context",
  or wants to enrich dbt semantic layer YAML with business knowledge.
  Also triggers on "context coverage", "context report", "false confidence",
  or discussion of how LLMs interpret metric definitions.
---

# Meta Context Schema

Operational skill for encoding business knowledge in dbt MetricFlow YAML via the `meta:` property. The schema has 5 layers, each closing a specific LLM analytical failure type — validated by ablation eval (V0-V5).

## The 5 Layers

| Layer | Question It Answers | Failure It Closes |
|---|---|---|
| 1. Context | "Who cares and why does this exist?" | Interpretation failures |
| 2. Expectations | "What does good look like?" | Calibration failures |
| 3. Investigation | "When it breaks, where do I look first?" | Framing failures |
| 4. Relationships | "What else moves when this moves?" | Reasoning failures |
| 5. Decisions | "What do I do about it?" | Action failures + false confidence |

## Commands

### `/meta-context author <metric_name>`

Guided authoring session for a metric's `meta:` block.

**Step 1: Read existing YAML**
Read the metric's semantic model YAML. Understand its measures, dimensions, type_params.

**Step 2: Walk through each layer with targeted prompts**

Layer 1 — Context:
- "In one sentence, what business question does this metric answer?"
- "Who is the primary owner (team or role)?"
- "Who else cares about this metric?"
- "Is there a precise business definition that distinguishes this from similar metrics?"

Layer 2 — Expectations:
- "Looking at the last 12 months, what's the normal operating range? (P5/P95)"
- "At what value should someone start paying attention?"
- "At what value is this an emergency?"
- "Are there seasonal patterns? When, how much, and why?"

Layer 3 — Investigation:
- "When this drops, what's the FIRST thing an experienced analyst checks?"
- "Why that first, and not the other dimensions?"
- "What's the decision tree — if check 1 shows X, what next?"
- "Are there known false positives that look like real problems?"

Layer 4 — Relationships:
- "What other metrics move when this one moves?"
- "Are any of those leading indicators (they change first)?"
- "What external events (not data) affect this metric?"

Layer 5 — Decisions:
- "Are there contractual obligations (SLAs) tied to this metric?"
- "What's the escalation path at different severity levels?"
- "Are there automatic trigger rules?"

**Step 3: Generate the `meta:` YAML block** from answers. Use the schema reference in `references/schema-reference.md` for exact key names and types.

**Step 4: Run validation** — check all Core-tier fields are present.

### `/meta-context validate <metric_name>`

Check a metric's `meta:` block against the schema.

**Step 1:** Read the metric YAML file.

**Step 2:** Check field presence by tier:
- Core fields present? (13 fields — see schema reference)
- Recommended fields present? (10 fields)
- Optional fields present? (13 fields)

**Step 3:** Check types:
- `healthy_range` must be `[number, number]`
- `causal_dimensions` entries must have `name`, `why`, `priority`
- `correlates_with` entries must have `metric` and typed `relationship`
- `when_this_drops` entries must have `threshold` and `action`

**Step 4:** Check for false-confidence risk:
- Has `expectations` (Layer 2) but NOT `decisions.business_rules` (Layer 5)?
- If yes: **WARNING** — partial context without business rules creates false confidence on SLA/decision questions. This was the killer finding from our V0-V5 eval.

**Step 5:** Report tier:
- Bronze: All Layer 1 + Layer 2 Core fields (13 Core total)
- Silver: Bronze + Layer 3 + recommended fields
- Gold: All 5 layers populated

### `/meta-context extract <source>`

Deep-read documentation and extract candidate context values.

**Step 1:** Read the provided source (runbook, Slack thread, incident report, analyst interview notes).

**Step 2:** For each schema key, attempt to extract a value from the source. Cite the source location.

**Step 3:** Output a partially-filled YAML template:
- Extracted values with `# Source: [location]` comments
- `# NEEDS REVIEW` on uncertain extractions
- `# NOT FOUND` on keys with no source material

**Step 4:** Suggest which additional sources to consult for unfilled keys. Use the sourcing guide in `references/sourcing-guide.md`.

### `/meta-context mine <metric_name>` — EXPERIMENTAL

> **Status: Untested idea.** This command was designed based on analysis of what Confluence/Jira typically contains vs. what the schema needs, but has not been validated against a real documentation corpus. The search queries, extraction confidence levels, and time estimates are hypothetical. Try it, report what works, adjust.

Auto-discover and extract meta context candidates from connected documentation sources (Confluence, Jira, wiki). Requires an Atlassian MCP server (e.g., `sooperset/mcp-atlassian`) or equivalent documentation API configured in `.claude/settings.local.json`.

**Step 1: Targeted searches** — Run 3 queries against the documentation source:
1. `search_confluence("<metric_name> definition purpose")` — Layer 1 (Context)
2. `search_confluence("<metric_name> runbook escalation SLA")` — Layer 5 (Decisions)
3. `search_confluence("<metric_name> incident postmortem root cause")` — Layer 3 (Investigation)

Take top 3-5 results from each query.

**Step 2: Fetch and extract** — `get_page()` on each result. For each page, attempt to extract values for schema fields. Cite source location.

**Step 3: Output draft** — Produce a partially-filled `meta:` YAML block in the same format as `/meta-context extract`:
- Extracted values with `# Source: Confluence/<page_title> [<url>]` comments
- `# NEEDS REVIEW` on uncertain extractions (confidence < 0.7)
- `# NOT FOUND` on keys with no source material

**Step 4: Recommend next steps** — List which fields remain unfilled and suggest:
- Run calibration queries for Layer 2 (Expectations) — warehouse data, not docs
- Use `/meta-context author` for remaining `# NOT FOUND` fields (human input needed)
- Use `/meta-context validate` on the completed block

**Which layers benefit most from mining:**

| Layer | Mining Yield | Why |
|---|---|---|
| Layer 1 (Context) | High | `purpose`, `owner`, `definition`, `aliases` are wiki-native |
| Layer 5 (Decisions) | High | `business_rules`, `escalation_path`, `when_this_drops` live in runbooks/SLAs |
| Layer 3 (Investigation) | Medium | `known_root_causes` extractable from post-mortems; `investigation_path` decision trees need human synthesis |
| Layer 2 (Expectations) | Low | `healthy_range`, thresholds need warehouse data, not docs |
| Layer 4 (Relationships) | Very low | `correlates_with` needs statistical analysis; `affected_by` is organizational memory |

**Prerequisites:**
- Atlassian MCP server configured and accessible
- User has read access to the relevant Confluence spaces
- If no MCP server: use Rovo AI or manual search, then feed results to `/meta-context extract <source>`

### `/meta-context update <metric_name>`

Refresh existing context. Checks for staleness.

**Step 1:** Read current `meta:` block.
**Step 2:** For each populated field, show current value. Ask: "Still accurate?"
**Step 3:** For unpopulated fields, offer to fill them.
**Step 4:** Produce a diff. Update the YAML.

### `/meta-context eval <metric_name>`

Run the ablation evaluation protocol on a specific metric.

**Step 1:** Generate V0-V5 YAML variants by cumulatively stripping layers.
**Step 2:** Generate 5 analytical questions (1 per failure type) tailored to the metric.
**Step 3:** Run each question against each variant (same model, same system prompt).
**Step 4:** Score responses on the 5-dimension rubric (Groundedness, Calibration, Diagnostic Depth, Actionability, Hallucination Resistance). See `references/eval-protocol.md`.
**Step 5:** Check for false-confidence regression (V2 confidently wrong → V5 correct).
**Step 6:** Produce results summary with scoring matrix, step-changes, and recommendations.

### `/meta-context report`

Coverage dashboard across all metrics.

**Step 1:** Scan all metric YAML files for `meta:` blocks.
**Step 2:** Report:
- Total metrics vs metrics with meta context
- Breakdown by tier (Bronze/Silver/Gold/None)
- Coverage by layer (how many metrics have each layer?)
- Average keys filled per layer
- False-confidence risk: metrics with Layer 2 but not Layer 5
- Staleness: metrics with `last_validated` > 90 days ago (or no `last_validated`)
- Most common missing fields across all metrics

## Placement Rules: Where Meta Context Lives

**Meta context lives on metrics. Metrics live on marts.**

| Pipeline Layer | What `meta:` Contains |
|---|---|
| Staging | Nothing (or governance: `config.meta.owner`) |
| Intermediate | Governance only: `owner`, `contains_pii` |
| Mart (semantic model) | All 5 layers — on the `metrics:` block, not the model |
| `metrics_*.yml` | All 5 layers — on derived/ratio metrics |

**Why not staging/intermediate?** They're invisible to MetricFlow. They don't have metrics. The schema answers "what does this metric mean?" — that question only applies where metrics are defined.

**Avoiding redundancy:**
- Context attaches to the **metric**, not the model. Two metrics from the same mart get separate meta blocks.
- Don't duplicate context up the pipeline (staging → intermediate → mart). It lives at the endpoint only.
- Governance meta (`owner`, `contains_pii`) is separate from business context and CAN live at any layer.

**Where exactly in the YAML:**
```yaml
metrics:
  - name: order_success_rate
    type: derived
    meta:              # ← HERE. Sibling of type/type_params, child of the metric.
      context: ...
      expectations: ...
```

## Field Generation Framework

When encountering context that doesn't fit existing fields, apply four tests before proposing a new field:

1. **Failure Test:** Does absence cause an identifiable LLM reasoning failure?
2. **Decay Test:** Is this at risk of being lost through rotation/drift? (If derivable from data, don't encode it)
3. **Dual-Audience Test:** Readable by both humans and LLMs?
4. **Layer Fit Test:** Which layer's question does it answer?

If it passes all four → add to the appropriate layer. If it fails the Failure Test → don't add. See `references/field-generation.md` for the full decision tree.

## Writing Effective Context Values

Five principles:

1. **Write for the worst-case consumer** — new analyst or LLM with no prior context. No jargon.
2. **Encode reasoning, not just facts** — "Drops 3-5% in Nov-Dec" is a fact. Add "Post-holiday returns inflate failure count in Jan" for reasoning.
3. **Use typed relationships, not adjectives** — "inverse — high returns lag low success by 5-7 days" beats "related to return_rate."
4. **Include magnitude** — "Drops 3-5%" enables calibration. "Drops during peak" doesn't.
5. **Write investigation paths as conditional logic** — "IF direct: check carrier. IF carrier-specific: check region." Not flat lists.

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| `purpose: "Revenue"` | Too vague — which revenue? |
| `healthy_range: [0, 1]` | Technically true, zero calibration value |
| `investigation_path: "Check the data"` | Not an investigation path |
| `business_rules: ["Important metric"]` | Not a business rule — just an opinion |
| `correlates_with: [{metric: "X"}]` | Missing typed relationship |
| `seasonality: "Yes"` | Boolean when description needed |

## References

- `references/schema-reference.md` — complete field reference (36 fields across 5 layers + cross-cutting)
- `references/sourcing-guide.md` — where to get values for each field
- `references/eval-protocol.md` — ablation and feedback protocols
- `references/field-generation.md` — 4-test framework for new fields
