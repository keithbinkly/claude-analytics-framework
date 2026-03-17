# dbt-agent Decomposition Inventory

Purpose: classify `dbt-agent` assets before any serious copy-promote migration into analytics-workspace.

This is the prerequisite inventory called for by the System Architect evaluation. Without it,
"incremental promotion by copy" is too vague to execute safely.

## Classification Scheme
Use one of four classifications for each asset:

| Classification | Meaning |
|---|---|
| Promote to analytics-workspace | Reusable across analytics projects and should become part of the shared control plane |
| Keep in dbt-domain | Specific to dbt-enterprise operations or deep dbt domain work |
| Archive | Stale, superseded, or historical only |
| Already duplicated | Exists in both places and needs canonical resolution |

## Migration Guardrail
`dbt-agent` remains intact throughout migration. Promotion into analytics-workspace is by copy unless there is a later,
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
- shared bootstrap/control-plane portions -> Promote to analytics-workspace
- dbt-enterprise-specific operating constraints -> Keep in dbt-domain
- stale bootstrap variants -> Archive or resolve duplicates

### 2. Commands
Paths:
- `.claude/commands/`

Initial direction:
- generic/shared orchestration and workstream commands -> Promote to analytics-workspace
- dbt-specific pipeline commands -> Keep in dbt-domain unless generalized cleanly
- commands superseded by analytics-workspace equivalents -> Archive

#### Initial file-by-file command pass

| Source path | Classification | Rationale | analytics-workspace target | Ownership label | analytics-workspace copy mode | Cutover dependency |
|---|---|---|---|---|---|---|
| `.claude/commands/pipeline-new.md` | Promote to analytics-workspace | Core analytics-workspace-root pipeline entrypoint; already adapted to route state into `dbt-agent` and execution into `dbt-enterprise` | `.claude/commands/pipeline-new.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Live state still in `dbt-agent` handoffs/registry; optional dot state may also exist |
| `.claude/commands/pipeline-resume.md` | Promote to analytics-workspace | Core analytics-workspace-root continuity command; already adapted to the multi-repo model | `.claude/commands/pipeline-resume.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Live state and some learnings still in `dbt-agent`; dot files are auxiliary rather than guaranteed |
| `.claude/commands/pipeline-status.md` | Promote to analytics-workspace | Core analytics-workspace-root visibility command for active workflows | `.claude/commands/pipeline-status.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Registry and plan state still in `dbt-agent`; dot state is optional |
| `.claude/commands/pipeline-gate.md` | Promote to analytics-workspace | Needed to make the pipeline command slice closer to end-to-end from analytics-workspace root | `.claude/commands/pipeline-gate.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Gate rules are analytics-workspace-owned; live pipeline state still in `dbt-agent` handoffs/registry, with optional dot updates |
| `.claude/commands/pipeline-close.md` | Promote to analytics-workspace | Needed to complete lifecycle handling from analytics-workspace root without moving storage ownership yet | `.claude/commands/pipeline-close.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Pipeline state and some learning infrastructure still in `dbt-agent`; dot updates are conditional |
| `handoffs/_templates/PLAN-TEMPLATE.md` | Promote to analytics-workspace | Pipeline creation should rely on an explicit analytics-workspace-owned plan template instead of inferred state shape | `.claude/skills/dbt-orchestrator/resources/plan-template.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Live state still written in `dbt-agent` during migration |
| `shared/templates/business-context-template.md` | Promote to analytics-workspace | Early-phase artifact creation should have a analytics-workspace-root starter template for agents and users | `.claude/skills/dbt-business-context/resources/business-context-template.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Live artifact still stored in `dbt-agent` during migration |
| `shared/templates/data-discovery-template.md` | Promote to analytics-workspace | Early-phase artifact creation should have a analytics-workspace-root starter template for discovery handoffs | `.claude/skills/dbt-data-discovery/resources/data-discovery-template.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Live artifact still stored in `dbt-agent` during migration |
| `.claude/skills/dbt-qa/resources/report-template.md` | Promote to analytics-workspace | The gate contract already expects `qa-report.md`, so analytics-workspace should provide a starter template for it | `.claude/skills/dbt-qa/resources/qa-report-template.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Live artifact still stored in `dbt-agent` during migration |
| `shared/templates/handoff-package-template.md` | Promote to analytics-workspace | Builder-to-QA transfer works better with an explicit execution handoff package, especially for parallel QA | `.claude/skills/dbt-migration/resources/qa-execution-handoff-template.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Live artifacts still stored in `dbt-agent` during migration |
| `.claude/commands/pipeline-docs.md` | Keep in dbt-domain | Useful, but lower priority until analytics-workspace owns more of the pipeline lifecycle and artifact generation stack | TBD after first slice verification | TBD | Mirror later if promoted | Depends on pipeline artifact conventions still centered in `dbt-agent` |
| `.claude/commands/analyze.md` | Promote to analytics-workspace | Candidate high-leverage shared workflow command, but needs separate dependency mapping before promotion | `.claude/commands/analyze.md` | TBD | TBD | Must inventory linked skills, agents, and CCV3 dependencies first |
| `.claude/commands/load.md` | Promote to analytics-workspace | Likely shared cross-session workflow utility, but not yet mapped | `.claude/commands/load.md` | TBD | TBD | Needs dependency and ownership review |
| `.claude/commands/save.md` | Promote to analytics-workspace | Likely shared cross-session workflow utility, but not yet mapped | `.claude/commands/save.md` | TBD | TBD | Needs dependency and ownership review |
| `.claude/commands/builder.md` | Keep in dbt-domain | More tightly coupled to dbt-agent execution conventions and should follow skill/agent promotion, not precede it | TBD after agent slice planning | TBD | Mirror later if generalized | Depends on dbt-oriented agent stack and workflow internals |

### 3. Agent definitions
Paths:
- `.claude/agents/`

Initial direction:
- shared operating patterns, templates, and generic role behavior -> Promote to analytics-workspace
- deep dbt/domain execution agents -> Keep in dbt-domain
- duplicate or stale agent files -> Archive or resolve

### 4. Agent memory
Paths:
- `.claude/agent-memory/`

Initial direction:
- memory standards and interior contract -> Promote to analytics-workspace
- dbt-domain judgment -> Keep in dbt-domain
- project-specific historical context -> Archive or leave local

### 5. Skills
Paths:
- `.claude/skills/`

Initial direction:
- reusable analytics/team skills -> Promote to analytics-workspace
- deep dbt-enterprise/Redshift specific skills -> Keep in dbt-domain
- archived or superseded skills -> Archive

#### Initial file-by-file skill pass

| Source path | Classification | Rationale | analytics-workspace target | Ownership label | analytics-workspace copy mode | Cutover dependency |
|---|---|---|---|---|---|---|
| `.claude/skills/dbt-orchestrator/SKILL.md` | Promote to analytics-workspace | Central pipeline workflow coordinator and the cleanest first skill slice after the command layer | `.claude/skills/dbt-orchestrator/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Still depends on non-promoted companion skills for full execution |
| `.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md` | Promote to analytics-workspace | Commands depend on it; needed to reduce hidden `dbt-agent` references | `.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Full phase loading still falls back to `dbt-agent` for non-promoted skills |
| `.claude/skills/dbt-orchestrator/resources/gate-enforcement-rules.md` | Promote to analytics-workspace | Commands depend on it for gate validation and blocked-state behavior | `.claude/skills/dbt-orchestrator/resources/gate-enforcement-rules.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Live pipeline state still in `dbt-agent` |
| `.claude/skills/dbt-orchestrator/resources/handoff-protocols.md` | Promote to analytics-workspace | Defines cross-phase artifact contract and belongs in analytics-workspace control-plane docs | `.claude/skills/dbt-orchestrator/resources/handoff-protocols.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Active artifact storage still in `dbt-agent` |
| `.claude/skills/dbt-orchestrator/resources/workflow-state-machine.md` | Promote to analytics-workspace | Core workflow contract should be analytics-workspace-owned | `.claude/skills/dbt-orchestrator/resources/workflow-state-machine.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | State persistence still stored outside analytics-workspace |
| `.claude/skills/dbt-business-context/SKILL.md` | Promote to analytics-workspace | High-leverage phase-1 skill and now promoted as a analytics-workspace-owned wrapper | `.claude/skills/dbt-business-context/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Still depends on legacy KPI standards in `dbt-agent` |
| `.claude/skills/dbt-data-discovery/SKILL.md` | Promote to analytics-workspace | High-leverage phase-2 skill and now promoted as a analytics-workspace-owned wrapper | `.claude/skills/dbt-data-discovery/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Still depends on discovery snippets, field mappings, and join registry in `dbt-agent` |
| `.claude/skills/dbt-qa/SKILL.md` | Promote to analytics-workspace | High-leverage QA skill and now promoted as a analytics-workspace-owned wrapper | `.claude/skills/dbt-qa/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Still depends on troubleshooting and decision traces in `dbt-agent` |
| `.claude/skills/dbt-standards/SKILL.md` | Promote to analytics-workspace | High-leverage placement/reuse skill and now promoted as a analytics-workspace-owned wrapper | `.claude/skills/dbt-standards/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Still depends on controlled vocabulary and join registry in `dbt-agent` |
| `.claude/skills/dbt-tech-spec-writer/SKILL.md` | Promote to analytics-workspace | High-leverage phase-3 architecture/spec skill and now promoted as a analytics-workspace-owned wrapper | `.claude/skills/dbt-tech-spec-writer/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Still depends on some unpromoted helper resources in `dbt-agent` |
| `.claude/skills/dbt-preflight/SKILL.md` | Promote to analytics-workspace | High-leverage phase-4 execution-safety skill and now promoted as a analytics-workspace-owned wrapper | `.claude/skills/dbt-preflight/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Full historical preflight patterns still remain in `dbt-agent` |
| `.claude/skills/dbt-migration/SKILL.md` | Promote to analytics-workspace | High-leverage phase-4 implementation skill and now promoted as a analytics-workspace-owned wrapper | `.claude/skills/dbt-migration/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Still depends on deeper macro registry and full long-tail implementation guidance in `dbt-agent` |
| `.claude/skills/dbt-fundamentals/SKILL.md` | Promote to analytics-workspace | General dbt foundation guidance is useful for analytics-workspace-root implementation workflows | `.claude/skills/dbt-fundamentals/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Full long-form resource set still remains in `dbt-agent` |
| `.claude/skills/dbt-lineage/SKILL.md` | Promote to analytics-workspace | Phase-2 and impact-analysis workflows need a analytics-workspace-root lineage entrypoint | `.claude/skills/dbt-lineage/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Full manifest-parser depth still remains in `dbt-agent` |
| `.claude/skills/dbt-sql-unit-testing/SKILL.md` | Promote to analytics-workspace | Phase-4 testing benefits from a analytics-workspace-root local SQL unit-test entrypoint | `.claude/skills/dbt-sql-unit-testing/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Full local test harness details still remain in `dbt-agent` |
| `.claude/skills/sql-hidden-gems/SKILL.md` | Promote to analytics-workspace | Advanced SQL tactics are a reusable shared capability for migration and debugging workflows | `.claude/skills/sql-hidden-gems/SKILL.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Full long-form pattern catalog still remains in `dbt-agent` |

### 6. Knowledge base and reference material
Paths:
- `shared/knowledge-base/`
- `shared/reference/`
- `shared/decision-traces/`

Initial direction:
- analytics-team reusable patterns -> Promote to analytics-workspace
- production-environment-specific dbt operating knowledge -> Keep in dbt-domain
- stale reference material -> Archive

#### Initial file-by-file knowledge/reference pass

| Source path | Classification | Rationale | analytics-workspace target | Ownership label | analytics-workspace copy mode | Cutover dependency |
|---|---|---|---|---|---|---|
| `shared/knowledge-base/canonical-models-registry.md` | Promote to analytics-workspace | High-value canonical reuse reference needed for pipeline design from analytics-workspace root | `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Some companion docs remain in `dbt-agent` until promoted |
| `shared/knowledge-base/legacy-kpi-gold-standard-metrics.md` | Promote to analytics-workspace | Certified KPI benchmark guidance is useful for requirements capture and QA framing from analytics-workspace root | `knowledge/domains/dbt-pipelines/reference/legacy-kpi-gold-standard-metrics.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Full long-form certified metric catalog still remains in `dbt-agent` |
| `shared/knowledge-base/migration-quick-reference.md` | Promote to analytics-workspace | High-leverage migration playbook referenced across dbt workflow phases | `knowledge/domains/dbt-pipelines/reference/migration-quick-reference.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Some linked standards and QA references remain split across analytics-workspace and `dbt-agent` for now |
| `shared/knowledge-base/folder-structure-and-naming.md` | Promote to analytics-workspace | Cross-domain standards reference that belongs in shared analytics-workspace guidance | `knowledge/reference/standards/folder-structure-and-naming.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Migration quick-reference still contains some legacy path references |
| `shared/reference/dbt-mcp-tools-reference.md` | Promote to analytics-workspace | Shared tool reference needed by agents starting in analytics-workspace root | `knowledge/reference/tools/dbt-mcp-tools-reference.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Depends on external dbt MCP setup, but not on undocumented CCV3 behavior |
| `shared/reference/anti-pattern-impact.yml` | Promote to analytics-workspace | High-value Redshift optimization evidence base that belongs in shared analytics-workspace reference material | `knowledge/domains/redshift/reference/anti-pattern-impact.yml` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | None beyond downstream docs choosing the analytics-workspace path |
| `shared/reference/qa-validation-checklist.md` | Promote to analytics-workspace | High-value QA workflow reference needed for analytics-workspace-root validation guidance | `knowledge/domains/dbt-pipelines/reference/qa-validation-checklist.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Editable analytics-workspace-owned copy | Some embedded references still point to legacy companion docs until those are promoted |
| `shared/knowledge-base/redshift-discovery-snippets.md` | Promote to analytics-workspace | High-value discovery snippets unblock analytics-workspace-root profiling and schema validation work | `knowledge/reference/tools/redshift-discovery-snippets.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Full long-tail snippet set still remains in `dbt-agent` |
| `shared/knowledge-base/field-mappings.md` | Promote to analytics-workspace | Reusable field-name semantics reduce migration and QA errors across pipelines | `knowledge/domains/dbt-pipelines/reference/field-mappings.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Some niche mappings still remain only in `dbt-agent` |
| `shared/knowledge-base/macros-registry.md` | Promote to analytics-workspace | Macro reuse guidance is a core migration and architecture dependency that should be visible from analytics-workspace root | `knowledge/domains/dbt-pipelines/reference/macros-registry.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Full macro source still lives in the execution repo |
| `shared/reference/controlled-vocabulary.yml` | Promote to analytics-workspace | Naming-consistency guidance belongs in shared analytics-workspace standards material | `knowledge/reference/standards/controlled-vocabulary.yml` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Full mined alias corpus still remains in `dbt-agent` |
| `shared/reference/architecture-validation-checklist.md` | Promote to analytics-workspace | Placement-validation guidance belongs in portable analytics-workspace standards used by architecture and review workflows | `knowledge/reference/standards/architecture-validation-checklist.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Project-local structure guides still remain in `dbt-enterprise` |
| `shared/reference/MANDATORY_COMPILE_RULE.md` | Promote to analytics-workspace | Compile-first rule is a cross-workflow execution standard and should be visible from analytics-workspace root | `knowledge/reference/standards/mandatory-compile-rule.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Execution still routes to `dbt-enterprise` |
| `shared/reference/baas-join-registry.yml` | Promote to analytics-workspace | Common join guidance is repeatedly useful for discovery, standards, and implementation planning | `knowledge/domains/dbt-pipelines/reference/baas-join-registry.yml` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Full join corpus still remains in `dbt-agent` |
| `shared/knowledge-base/troubleshooting.md` | Promote to analytics-workspace | Core dbt/Redshift troubleshooting belongs in analytics-workspace so QA and implementation wrappers are useful at root | `knowledge/domains/dbt-pipelines/reference/troubleshooting.md` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Curated analytics-workspace-owned copy | Long-tail troubleshooting cases still remain in `dbt-agent` |
| `shared/decision-traces/` | Prepare staged promotion | High-value learning loop asset, but the corpus is large enough to migrate incrementally | `knowledge/domains/dbt-pipelines/decision-traces/` | `source_of_truth: caf`, `mirrored_from: dbt-agent` | Staged analytics-workspace landing area | Curated `rules.json` and `selected-traces.json` promoted; full historical trace corpus still pending |

### 7. Learning loop and telemetry
Paths:
- `tools/chatops/`
- `tools/chatops_analysis/`
- `data/chatops/`
- docs describing learning loop infrastructure

Initial direction:
- shared learning-loop infrastructure -> Promote to analytics-workspace
- project-local telemetry artifacts -> Archive or reference from analytics-workspace rather than copy blindly

### 8. Live state and active artifacts
Paths:
- `handoffs/`
- `.dots/`
- workstream files

Initial direction:
- shared state model -> Promote to analytics-workspace
- active or historical project artifacts -> Keep local or archive

## Prioritization Rule
Promote highest first:
1. Assets that improve analytics-workspace-root startup and routing
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
- whether the analytics-workspace copy should be read-only mirror or editable team-owned copy

## Cutover Guardrail
Do not downgrade `dbt-agent` from active control plane status until analytics-workspace has equivalent replacement coverage for:

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
