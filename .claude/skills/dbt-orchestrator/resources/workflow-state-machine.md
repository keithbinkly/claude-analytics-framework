<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-orchestrator/resources/workflow-state-machine.md
-->

# Workflow State Machine

CAF-owned state model for the dbt pipeline lifecycle.

Use `.claude/manifests/pipeline-state-schema.yaml` for the concrete storage contract and normalization rules.

## States

- `requirements_gathering`
- `data_discovery`
- `architecture_design`
- `implementation`
- `review_deploy`

## Valid Transitions

| From | To | Trigger |
|------|----|---------|
| `requirements_gathering` | `data_discovery` | Gate 1 passed |
| `data_discovery` | `architecture_design` | Gate 2 passed |
| `architecture_design` | `implementation` | Gate 3 passed |
| `implementation` | `review_deploy` | Gate 4 passed |

## Invalid Transitions

- skip-state transitions without explicit documented override
- backward transitions without explicit reset or correction
- advancing while current gate is blocked

## State Tracking

During migration, the state model is written into pipeline artifacts that still live in `dbt-agent`.

Primary live state:

- `handoffs/[pipeline]/PLAN.md`
- `handoffs/PIPELINE_REGISTRY.yaml`

Optional auxiliary state:

- `.dots/pipeline-[name].md`

CAF owns the meaning of the states. `dbt-agent` still owns much of the live state storage.

## Blocked State

If a gate cannot pass, the workflow remains in the current state and should be marked blocked with:

- blocked gate
- blocking reason
- required resolution

## Recovery Rule

When resuming:

1. read current saved state
2. verify artifacts exist
3. continue from the current state
4. do not replay completed phases unless explicitly requested
