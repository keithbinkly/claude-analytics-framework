---
name: dbt-orchestrator
description: |
  Central workflow coordinator for the analytics-workspace-root dbt pipeline model. Manages pipeline state,
  enforces human review gates, routes workflow phases to the right skills, and keeps the
  control-plane / execution-target split explicit. Use when starting a new pipeline,
  resuming pipeline work, checking pipeline status, approving gates, or reasoning about
  pipeline phase transitions.
---

<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-orchestrator/SKILL.md
-->

# analytics-workspace dbt Orchestrator

Workflow state machine, gate rules, and phase-loading references for the analytics-workspace-root pipeline lifecycle.

## Purpose

This skill is the shared control-plane reference for pipeline orchestration in analytics-workspace.

It exists to make these rules explicit:

- analytics-workspace is the control-plane entrypoint.
- `dbt-enterprise` is the dbt execution target.
- `dbt-agent` remains fallback reference only where the capability has not yet been promoted.
- Human review gates are mandatory unless explicitly skipped and documented.

## Core References

Read these before using or extending the workflow:

- `knowledge/domains/dbt-pipelines/reference/migration-quick-reference.md`
- `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md`
- `knowledge/reference/standards/folder-structure-and-naming.md`
- `knowledge/domains/dbt-pipelines/reference/qa-validation-checklist.md`
- `knowledge/reference/tools/dbt-mcp-tools-reference.md`
- `.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md`
- `.claude/skills/dbt-orchestrator/resources/gate-enforcement-rules.md`
- `.claude/skills/dbt-orchestrator/resources/handoff-protocols.md`
- `.claude/skills/dbt-orchestrator/resources/workflow-state-machine.md`
- `.claude/manifests/pipeline-state-schema.yaml`

## Pipeline State Model

During migration, the active pipeline state still lives in `dbt-agent`.

Primary live state:

- `handoffs/[pipeline]/PLAN.md`
- `handoffs/PIPELINE_REGISTRY.yaml`

Optional auxiliary state:

- `.dots/pipeline-[name].md`

analytics-workspace owns the workflow contract and command entrypoints, but not yet the canonical storage.

## Phase Model

The orchestrator manages these major phases:

1. Requirements
2. Data discovery
3. Architecture
4. Implementation
5. Review / deploy

See `resources/workflow-state-machine.md` for valid transitions and blocked states.

## Gate Model

The orchestrator enforces four primary gates:

1. Requirements review
2. Data findings review
3. Architecture review
4. Deployment review

See `resources/gate-enforcement-rules.md` for required artifacts, validation checks, and blocked-state behavior.

## Skill Routing

Use analytics-workspace-promoted skills first when they exist.

Current expected routing:

- Phase 1: `dbt-business-context`
- Phase 2: `dbt-data-discovery`
- Phase 3: `dbt-standards` and `dbt-tech-spec-writer`
- Phase 4: `dbt-preflight`, `dbt-migration`, `dbt-qa`

If a required skill is not yet promoted into analytics-workspace, fall back explicitly to `dbt-agent`.

## Execution Routing

This skill does not change where dbt commands run:

- read context from analytics-workspace
- read or update pipeline state where it currently lives
- run dbt CLI from `dbt-enterprise`

Never treat analytics-workspace root as the dbt execution target.

## Definition Of Done For This Capability

This skill slice is only fully replaced in analytics-workspace when:

- gate rules are analytics-workspace-owned
- phase-loading specs are analytics-workspace-owned
- required companion skills are also promoted or explicitly wrapped
- pipeline commands no longer need hidden `dbt-agent` references for normal operation
