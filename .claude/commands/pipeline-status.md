<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/.claude/commands/pipeline-status.md
-->

# Pipeline Status

Show the current state of one pipeline or all active pipelines while starting from workspace root.

**Usage:**
- `/pipeline-status`
- `/pipeline-status [name]`

## Bootstrap

Before doing anything:

1. Read `AGENT_ENTRYPOINT.md`
2. Read `.claude/manifests/repo-adapters.yaml`
3. Read `.claude/manifests/pipeline-state-schema.yaml`
4. Resolve the `dbt-agent` repo location

Preferred resolution order:

- local convenience path: `repos/dbt-agent`
- fallback: path from `.claude/manifests/repo-adapters.yaml`

Treat the resolved location as `DBT_AGENT_ROOT`.

## Steps

### 1. Load Pipeline Registry

Read:

`DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`

If an argument is provided, filter to that pipeline. Otherwise show all active pipelines.

### 2. Load Per-Pipeline State

For each relevant pipeline, read:

- `DBT_AGENT_ROOT/handoffs/[name]/PLAN.md`

If present, also read:

- `DBT_AGENT_ROOT/.dots/pipeline-[name].md`

Extract:

- workflow type
- current phase
- gate status
- blockers
- last action
- next action

### 3. Present Summary

For all pipelines, show a compact table with:

- pipeline name
- type
- phase
- gate state
- last activity
- status

For a single pipeline, show:

- workflow type
- current phase
- gate status
- known artifacts
- blockers
- next action

### 4. Route Follow-Up

Offer the next likely command:

- `/pipeline-resume [name]` to continue
- `/pipeline-gate [...]` to approve a pending gate
- `/pipeline-close [name]` when the workflow is complete

## Notes

- Pipeline state still lives in `dbt-agent` during migration.
- analytics-workspace is the control-plane entrypoint, not the current storage location for pipeline state.
- Do not assume `dbt-enterprise` is where pipeline state is tracked; it is the dbt execution target.
