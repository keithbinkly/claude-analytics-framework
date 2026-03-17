<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/.claude/commands/pipeline-close.md
-->

# Close Pipeline

Complete a pipeline workflow from workspace root, capture learnings, and close or archive the state that still lives in `dbt-agent`.

**Usage:** `/pipeline-close [name]`

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

### 1. Identify Pipeline

Pipeline name comes from `$ARGUMENTS`.

If no name is provided:

- inspect `DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`
- list active pipelines
- ask which one should be closed

### 2. Verify Completion State

Read:

- `DBT_AGENT_ROOT/handoffs/[name]/PLAN.md`
- `DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`

If present, also read:

- `DBT_AGENT_ROOT/.dots/pipeline-[name].md`

Check whether the workflow appears complete for its type:

- Full Migration: final gate passed, QA report exists, deployment handoff or equivalent exists
- Enhancement: final QA/handoff step completed
- Semantic Layer: final validation and documentation completed

If the pipeline is not complete, warn clearly and ask whether to:

- close anyway as partial completion
- continue work instead
- cancel closure

### 3. Gather Artifacts And Learnings

Inspect the pipeline directory under:

- `DBT_AGENT_ROOT/handoffs/[name]/`

Collect:

- produced artifacts
- major design decisions
- error/fix patterns
- reusable workflow patterns
- anti-patterns or time wasters

If relevant analytics-workspace-promoted learning infrastructure exists, use it.

Otherwise, use `dbt-agent` reference material such as:

- `DBT_AGENT_ROOT/shared/decision-traces/`
- `DBT_AGENT_ROOT/.claude/commands/synthesize-traces.md` if applicable
- `DBT_AGENT_ROOT/.claude/skills/dbt-decision-trace/SKILL.md`

### 4. Present Completion Summary

Summarize:

- workflow type
- phases and gates completed
- artifacts produced
- key metrics or quality outcomes if available
- learnings extracted
- whether anything remains incomplete

### 5. Update Source-Of-Truth State

If the user confirms closure, update the current source-of-truth state in `dbt-agent`:

- `DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`
- optionally `DBT_AGENT_ROOT/handoffs/[name]/PLAN.md` if needed for closure notes

If a pipeline-specific dot file exists, update it too:

- `DBT_AGENT_ROOT/.dots/pipeline-[name].md`

Record:

- completed or closed status
- completion date
- partial-completion notes if applicable

### 6. Ask About Archival

Because active state still lives in `dbt-agent`, ask whether to:

- keep the handoff directory in place
- archive it under the repo's archival convention

Do not archive automatically without confirmation.

## Notes

- This command closes workflow state that still lives in `dbt-agent`.
- analytics-workspace is the control-plane entrypoint for the user, but not yet the storage owner for pipeline lifecycle state.
- If learning capture depends on non-promoted assets, call that out explicitly instead of assuming the analytics-workspace copy exists.
