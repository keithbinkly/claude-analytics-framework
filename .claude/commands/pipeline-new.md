<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/commands/pipeline-new.md
-->

# Create New Pipeline

Start a new pipeline workflow from CAF root while keeping pipeline state in `dbt-agent` during migration.

**Usage:** `/pipeline-new [pipeline-name]`

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

### 1. Validate Pipeline Name

Use `$ARGUMENTS` as the initial name.

If missing, ask the user for a pipeline name and normalize it to kebab-case.

### 2. Check for Existing Pipeline

Check whether:

`DBT_AGENT_ROOT/handoffs/[name]/PLAN.md`

already exists.

If it does, tell the user to use `/pipeline-resume [name]` instead.

### 3. Determine Workflow Type

Ask the user which workflow type applies:

- Full Migration
- Enhancement
- Semantic Layer
- Net-New

### 4. Create Pipeline State In The Current Source Of Truth

Until CAF owns pipeline state directly, create the pipeline infrastructure in `dbt-agent`:

- `DBT_AGENT_ROOT/handoffs/[name]/`
- `DBT_AGENT_ROOT/handoffs/[name]/PLAN.md`
- update `DBT_AGENT_ROOT/handoffs/PIPELINE_REGISTRY.yaml`

Treat these as required minimum state:

- `PLAN.md`
- registry entry in `PIPELINE_REGISTRY.yaml`

Treat `.dots/pipeline-[name].md` as optional auxiliary state only.

Use CAF-promoted state guidance first:

- `.claude/manifests/pipeline-state-schema.yaml`
- `.claude/skills/dbt-orchestrator/resources/plan-template.md`
- `.claude/skills/dbt-business-context/resources/business-context-template.md`
- `.claude/skills/dbt-data-discovery/resources/data-discovery-template.md`

Prefer CAF-promoted orchestration references first:

- `.claude/skills/dbt-orchestrator/SKILL.md`
- `.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md`

### 5. Present Kickoff Summary

Show:

- pipeline name
- workflow type
- starting phase
- state location in `dbt-agent`
- next action

### 6. Continue From CAF Root

After creation:

- keep the user anchored in CAF as the control-plane entrypoint
- consult CAF-promoted assets first
- use `dbt-agent` as fallback reference until the relevant capability is promoted
- route dbt CLI execution into `dbt-enterprise` when implementation begins

## Notes

- This command intentionally keeps workflow state in `dbt-agent` for now.
- It exists in CAF so users can start from the shared team root without losing access to the existing pipeline system.
