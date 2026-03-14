<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/reference/architecture-validation-checklist.md
-->

> CAF migration note: this is a portable CAF copy of the architecture validation checklist. Prefer this from CAF root, then validate against the actual structure guides in `dbt-enterprise`.

# Architecture Validation Checklist

Use this before recommending model placement, writing a tech spec, or approving architecture decisions.

## When To Use

- before creating new intermediate or mart models
- before approving folder placement
- before finalizing a tech spec
- during code review of model structure

## Step 1: Load Project Reality

Read the actual structure guides from `dbt-enterprise` before deciding placement.

Typical targets:

- `models/intermediate/.../*_structure_guide.md`
- `models/marts/.../*_structure_guide.md`

Do not rely on memory or generic dbt guidance alone.

## Step 2: Identify Model Purpose

Answer these first:

1. What does the model do?
2. What are the inputs?
3. Who consumes it?
4. What is the grain?

## Step 3: Match Purpose To Placement

| Model purpose | Typical location | Anti-pattern |
|---|---|---|
| transaction processing | `transactions/...` | putting transaction logic in `foundations/...` |
| account or product enrichment | `foundations/...` | mixing it into transaction folders |
| metric calculations | `metrics/...` | mixing it into foundations or transactions |
| balance processing | `balances/...` | hiding it inside unrelated metric folders |
| marts for direct consumers | `marts/...` | placing final outputs in intermediate |

## Step 4: Check Anti-Patterns

Reject these:

- transaction models in foundations folders
- path depth so deep that discovery becomes hard
- duplicate folder concepts for the same content type
- mixed-purpose folder names
- marts organized contrary to documented consuming-team patterns

## Step 5: Validate Path Depth

Guidelines:

- 3-4 levels from `models/` is ideal
- 5 levels may be acceptable if project structure requires it
- 6+ levels should usually be rethought

## Step 6: Document The Validation

Every recommendation should state:

- model purpose
- recommended path
- structure guide used
- compliance result
- rejected alternatives
- path depth
- anti-pattern checks performed

## Quick Template

```markdown
## Model Placement Validation

- **Name:** [model_name]
- **Purpose:** [purpose]
- **Recommended Path:** `[path]`
- **Validated Against:** `[structure guide]`
- **Compliance:** ✅ / ⚠️ / ❌
- **Path Depth:** [n]

### Alternatives Rejected
- `[path]` - [reason]
- `[path]` - [reason]
```
