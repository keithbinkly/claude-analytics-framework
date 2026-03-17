<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/.claude/commands/pipeline-resume.md
-->

# Resume Pipeline

Load a pipeline's current context from workspace root and continue where the workflow left off.

**Usage:** `/pipeline-resume [name]`

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

## Steps

### 1. Identify Pipeline

Pipeline name comes from `$ARGUMENTS`.

If no name is provided, read:

`DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`

List active pipelines and ask which one to resume.

### 2. Load Pipeline State

Read these files:

- `DBT_AGENT_ROOT/handoffs/[name]/PLAN.md`
- `DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`

If present, also read:

- `DBT_AGENT_ROOT/.dots/pipeline-[name].md`

If available, also skim the latest phase artifact:

- `business-context.md`
- `data-discovery-report.md`
- `tech-spec.md`
- `qa-report.md`

### 3. Present Resume Context

Summarize:

- workflow type
- current phase
- last action
- next action
- blockers
- gate status

### 4. Route Capability Loading

If analytics-workspace already has the needed promoted workflow asset, use it.

Prefer these analytics-workspace-promoted orchestration references first:

- `.claude/skills/dbt-orchestrator/SKILL.md`
- `.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md`

Otherwise, consult the corresponding `dbt-agent` reference material under:

- `DBT_AGENT_ROOT/.claude/commands/`
- `DBT_AGENT_ROOT/.claude/skills/`
- `DBT_AGENT_ROOT/shared/`

### 5. Respect Execution Routing

If the next action requires dbt CLI execution:

- keep control-plane context in analytics-workspace
- route execution into `dbt-enterprise`

Do not run dbt CLI from workspace root.

## Notes

- This command is a workspace-root entrypoint into a workflow whose state still lives in `dbt-agent`.
- During migration, analytics-workspace may provide only part of the full capability stack. When in doubt, use `dbt-agent` as fallback reference.
