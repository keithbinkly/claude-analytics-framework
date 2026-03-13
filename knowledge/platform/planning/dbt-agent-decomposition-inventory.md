# dbt-agent Decomposition Inventory

Purpose: classify `dbt-agent` assets before any serious copy-promote migration into CAF.

This is the prerequisite inventory called for by the System Architect evaluation. Without it,
"incremental promotion by copy" is too vague to execute safely.

## Classification Scheme
Use one of four classifications for each asset:

| Classification | Meaning |
|---|---|
| Promote to CAF | Reusable across analytics projects and should become part of the shared control plane |
| Keep in dbt-domain | Specific to dbt-enterprise operations or deep dbt domain work |
| Archive | Stale, superseded, or historical only |
| Already duplicated | Exists in both places and needs canonical resolution |

## Migration Guardrail
`dbt-agent` remains intact throughout migration. Promotion into CAF is by copy unless there is a later,
explicit decision to re-home or retire a specific asset.

## Ownership Metadata
Every copied or mirrored asset should record one of:
- `source_of_truth: dbt-agent`
- `source_of_truth: caf`
- `mirrored_from: dbt-agent`
- `deprecated_copy: true`

This prevents drift while both repos remain active.

## High-Level Inventory Areas

### 1. Core control-plane docs
Paths:
- `CLAUDE.md`
- `AGENTS.md`
- `START_HERE.md`
- `ENVIRONMENT.md`
- `.claude/agent-manifest.yaml`

Initial direction:
- shared bootstrap/control-plane portions -> Promote to CAF
- dbt-enterprise-specific operating constraints -> Keep in dbt-domain
- stale bootstrap variants -> Archive or resolve duplicates

### 2. Commands
Paths:
- `.claude/commands/`

Initial direction:
- generic/shared orchestration and workstream commands -> Promote to CAF
- dbt-specific pipeline commands -> Keep in dbt-domain unless generalized cleanly
- commands superseded by CAF equivalents -> Archive

### 3. Agent definitions
Paths:
- `.claude/agents/`

Initial direction:
- shared operating patterns, templates, and generic role behavior -> Promote to CAF
- deep dbt/domain execution agents -> Keep in dbt-domain
- duplicate or stale agent files -> Archive or resolve

### 4. Agent memory
Paths:
- `.claude/agent-memory/`

Initial direction:
- memory standards and interior contract -> Promote to CAF
- dbt-domain judgment -> Keep in dbt-domain
- project-specific historical context -> Archive or leave local

### 5. Skills
Paths:
- `.claude/skills/`

Initial direction:
- reusable analytics/team skills -> Promote to CAF
- deep dbt-enterprise/Redshift specific skills -> Keep in dbt-domain
- archived or superseded skills -> Archive

### 6. Knowledge base and reference material
Paths:
- `shared/knowledge-base/`
- `shared/reference/`
- `shared/decision-traces/`

Initial direction:
- analytics-team reusable patterns -> Promote to CAF
- production-environment-specific dbt operating knowledge -> Keep in dbt-domain
- stale reference material -> Archive

### 7. Learning loop and telemetry
Paths:
- `tools/chatops/`
- `tools/chatops_analysis/`
- `data/chatops/`
- docs describing learning loop infrastructure

Initial direction:
- shared learning-loop infrastructure -> Promote to CAF
- project-local telemetry artifacts -> Archive or reference from CAF rather than copy blindly

### 8. Live state and active artifacts
Paths:
- `handoffs/`
- `.dots/`
- workstream files

Initial direction:
- shared state model -> Promote to CAF
- active or historical project artifacts -> Keep local or archive

## Prioritization Rule
Promote highest first:
1. Assets that improve CAF-root startup and routing
2. Assets teammates can immediately use and contribute to
3. Assets that do not disrupt active dbt pipeline delivery
4. Assets with clear shared ownership

## Required Next Pass
This document needs a file-by-file pass across:
- `dbt-agent/.claude/commands/`
- `dbt-agent/.claude/agents/`
- `dbt-agent/.claude/agent-memory/`
- `dbt-agent/.claude/skills/`
- `dbt-agent/shared/`
- `dbt-agent/tools/chatops*`

For each asset, record:
- path
- classification
- rationale
- target location if promoted
- owner after migration
- cutover dependency if any
- ownership label
- whether the CAF copy should be read-only mirror or editable team-owned copy

## Cutover Guardrail
Do not downgrade `dbt-agent` from active control plane status until CAF has equivalent replacement coverage for:

1. MCP tool routing
2. Preflight rules
3. QA standards and templates
4. Skill activation table
5. Pipeline orchestration commands
6. Agent loading specs
7. Anti-pattern enforcement
8. Decision trace lookup
9. Learning loop infrastructure
10. Workstream state management
