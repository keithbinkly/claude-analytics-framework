# Evaluation Protocol

## 5-Dimension Scoring Rubric

Score each LLM response on these 5 dimensions (1-5 scale):

| Dimension | 1 (Worst) | 3 (Adequate) | 5 (Best) |
|---|---|---|---|
| **Groundedness** | Invents or assumes values | References some context values | Cites exact values from YAML |
| **Calibration** | "This might be concerning" | Uses some thresholds | "Below healthy [0.94-0.99], above warning [0.92]" |
| **Diagnostic Depth** | "Check the data" | Lists dimensions to check | Prioritized decision tree with branching logic |
| **Actionability** | Generic advice | Some specific steps | "Page fulfillment-ops on-call, check carrier dashboard" |
| **Hallucination Resistance** | Invents plausible answers | Partially hedges | "This information isn't in the semantic layer definition" |

## Ablation Protocol

For any metric with the full schema populated:

### Step 1: Create 6 YAML Variants

| Variant | Contains | Layers |
|---|---|---|
| V0 (bare) | Metric definition only — measures, dimensions, type_params | None |
| V1 (context) | V0 + `meta.context` | Layer 1 |
| V2 (expectations) | V1 + `meta.expectations` | Layers 1-2 |
| V3 (investigation) | V2 + `meta.investigation` | Layers 1-3 |
| V4 (relationships) | V3 + `meta.relationships` | Layers 1-4 |
| V5 (full) | V4 + `meta.decisions` | Layers 1-5 |

### Step 2: Write 5 Questions

One per failure type, tailored to the specific metric:

1. **Interpretation** — "metric_name is X this week. How concerned should we be?"
2. **Framing** — "metric_name dropped N points (from A to B). What's driving this?"
3. **Decision** — "Customer segment Y has metric_name at Z. Are we meeting our obligations?"
4. **Relationship** — "metric_name dropped and correlated_metric also changed. Are they related?"
5. **Adversarial** — "What was [metric NOT in YAML] last month?"

### Step 3: Run Each Question Against Each Variant

Same model, same system prompt, same temperature. Record full responses.

### Step 4: Score on 5 Dimensions

Apply the rubric above. Note step-changes (which layer addition produces the biggest jump?).

### Step 5: False Confidence Test

**Critical check:** For the decision question (Q3), compare V2 against V5.

- If V2 gives a confidently wrong answer → the metric has a false-confidence risk when partially deployed
- If V2 correctly refuses ("I don't have SLA information") → safe for partial deployment
- If V5 catches what V2 missed → the `business_rules` field is earning its keep

### Step 6: Produce Results Summary

```
## Results: [metric_name]

### Scoring Matrix
| Variant | Q1 (interp) | Q2 (frame) | Q3 (decision) | Q4 (relation) | Q5 (adversarial) | Avg |
|---|---|---|---|---|---|---|

### Step-Changes
- Layer [N] → Layer [N+1] produced the biggest improvement on [question type]

### False Confidence Test
- V2 on Q3: [result]
- V5 on Q3: [result]
- Risk: [safe / dangerous middle]

### Recommendations
- [Which fields to prioritize filling]
- [Which fields had no measurable impact]
```

## LLM Feedback Questionnaire

After each eval response, append this questionnaire:

```yaml
context_feedback:
  task_completed: "[what was asked]"

  completeness:
    question: "Did the meta context contain everything you needed?"
    options: [yes, mostly, partially, no]
    if_not_yes: "What specific information was missing?"

  relevance:
    question: "Was all provided context relevant to this question?"
    options: [all_relevant, mostly_relevant, some_irrelevant, mostly_irrelevant]
    if_not_all: "Which fields were not useful?"

  interpretation:
    question: "Were any fields ambiguous or hard to interpret?"
    options: [all_clear, minor_ambiguity, significant_ambiguity]
    if_not_clear: "Which fields and what would make them clearer?"

  confidence_impact:
    question: "How did the context affect your confidence?"
    options: [high_confidence, moderate, low_despite_context, lower_than_without]
    explanation: "What drove your confidence level?"

  missing_connections:
    question: "Did you need to make inferences that could have been explicit?"
    freeform: true

  suggested_additions:
    question: "If you could add one field for questions like this, what would it be?"
    freeform: true
```

## Per-Layer Effectiveness Signals

| Layer | Working | Failing |
|---|---|---|
| Context (1) | Agent identifies metric purpose, routes to right team | Agent describes SQL formula instead of business meaning |
| Expectations (2) | Agent calibrates severity using thresholds | "I can't tell if this is good or bad" |
| Investigation (3) | Agent follows prioritized, branching investigation path | Lists all dimensions as equally valid |
| Relationships (4) | References correlated metrics and external events | Treats metric in isolation |
| Decisions (5) | Cites business rules and action protocols | Generic advice or false-confidence anchoring to healthy_range |
