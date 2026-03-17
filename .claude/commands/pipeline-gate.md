<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/.claude/commands/pipeline-gate.md
-->

# Approve Pipeline Gate

Formally approve a gate checkpoint from workspace root so the pipeline can advance to the next phase while state still lives in `dbt-agent`.

**Usage:** `/pipeline-gate [requirements|discovery|architecture|deploy]`

## Bootstrap

Before doing anything:

1. Read `AGENT_ENTRYPOINT.md`
2. Read `.claude/manifests/repo-adapters.yaml`
3. Read `.claude/manifests/workflow-contracts.yaml`
4. Read `.claude/manifests/pipeline-state-schema.yaml`
5. Resolve the `dbt-agent` repo location

Preferred resolution order:

- local convenience path: `repos/dbt-agent`
- fallback: path from `.claude/manifests/repo-adapters.yaml`

Treat the resolved location as `DBT_AGENT_ROOT`.

## Gate Keywords

| Keyword | Gate | Advances To |
|---------|------|-------------|
| `requirements` or `reqs` | Gate 1 | Phase 2: Data Discovery |
| `discovery` or `data` | Gate 2 | Phase 3: Architecture Design |
| `architecture` or `arch` | Gate 3 | Phase 4: Implementation |
| `deploy` or `qa` | Gate 4 | Completion / deployment handoff |

Numeric shortcuts `1` through `4` are acceptable for backwards compatibility.

## Steps

### 1. Identify Pipeline

If the pipeline name is not obvious from context:

- inspect `DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`
- if only one pipeline is active, use it
- if multiple pipelines are active, ask the user which one to gate

### 2. Resolve Gate

Gate keyword comes from `$ARGUMENTS`.

If no gate keyword is provided:

- read `DBT_AGENT_ROOT/handoffs/[name]/PLAN.md`
- read `DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`
- if present, read `DBT_AGENT_ROOT/.dots/pipeline-[name].md`
- determine which gate is currently `PENDING`

### 3. Validate Readiness

Read the relevant pipeline state:

- `DBT_AGENT_ROOT/handoffs/[name]/PLAN.md`
- `DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`

If present, also read:

- `DBT_AGENT_ROOT/.dots/pipeline-[name].md`

Then inspect the expected phase artifact:

- Gate 1: `DBT_AGENT_ROOT/handoffs/[name]/business-context.md`
- Gate 2: `DBT_AGENT_ROOT/handoffs/[name]/data-discovery-report.md`
- Gate 3: `DBT_AGENT_ROOT/handoffs/[name]/tech-spec.md`
- Gate 4: `DBT_AGENT_ROOT/handoffs/[name]/qa-report.md`

If analytics-workspace has already promoted the relevant workflow guidance, use it first.

Prefer analytics-workspace-promoted workflow references first:

- `.claude/skills/dbt-orchestrator/resources/gate-enforcement-rules.md`
- `.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md`

Otherwise, fall back to the `dbt-agent` references that still define the current workflow:

- `DBT_AGENT_ROOT/.claude/skills/dbt-orchestrator/resources/gate-enforcement-rules.md`
- `DBT_AGENT_ROOT/.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md`
- `DBT_AGENT_ROOT/shared/reference/qa-validation-checklist.md`

### 4. Present Gate Summary

If the gate is ready, show:

- pipeline name
- gate name
- key requirements satisfied
- artifact used for review
- next phase if approved

Then ask for explicit approval before mutating state.

If the gate is not ready, show:

- missing requirements
- what still needs to happen
- the command or workflow the user should run next

### 5. On Approval

Update the current source-of-truth state in `dbt-agent`:

- `DBT_AGENT_ROOT/handoffs/[name]/PLAN.md`
- `DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`

If a pipeline-specific dot file exists, update it too:

- `DBT_AGENT_ROOT/.dots/pipeline-[name].md`

Record:

- gate status as passed
- the next pending gate
- the next phase
- `last_action`
- `next_action`

### 6. Route Next Work Correctly

After approval:

- stay anchored in analytics-workspace as the control plane
- consult analytics-workspace-promoted skills or docs first
- use `dbt-agent` as fallback until the needed capability is promoted
- route dbt CLI execution into `dbt-enterprise` if the next phase requires it

Do not run dbt CLI from workspace root.

## Notes

- Pipeline state still lives in `dbt-agent` during migration.
- This analytics-workspace command is an entrypoint, not yet the canonical storage location for gate state.
- Missing promoted guidance is not a reason to guess; fall back to `dbt-agent` explicitly.
