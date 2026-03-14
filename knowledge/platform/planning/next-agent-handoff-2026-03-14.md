# Next Agent Handoff

Last updated: 2026-03-14
Primary workspace root: `/Users/kbinkly/git-repos/claude-analytics-framework`
Related repos:
- `/Users/kbinkly/git-repos/dbt-agent`
- `/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise`
- `/Users/kbinkly/git-repos/data-centered`

## Purpose

Use this handoff to resume the CAF-centered analytics workspace migration without replaying the full prior conversation. The target model is:

- CAF becomes the shared analytics control plane and team entrypoint.
- `dbt-enterprise` remains the intact production dbt project.
- `data-centered` remains the intact content and visualization project.
- `dbt-agent` remains intact and fully usable while high-leverage assets are copied into CAF over time.

This is a copy-promote migration, not a move-delete migration.

## Current Goal

Continue executing the plan in `dbt-agent/.dots/ai-team-workspace-migration.md` with emphasis on:

1. keeping CAF usable as the root entrypoint for agents
2. preserving active dbt workflow continuity
3. promoting high-leverage shared assets from `dbt-agent` into CAF
4. making workflows understandable to non-Claude agents such as Codex

## Mandatory Constraints

Do not violate these:

- `dbt-agent` must remain fully usable throughout migration.
- Prefer copy-promote over move-delete.
- Do not hardcode new machine-specific absolute paths into promoted assets.
- Do not archive or delete legacy CAF assets until replacements exist and are verified.
- Preserve active dbt pipeline delivery workflow at all times.
- Core workflow navigation must be expressible without Claude-only runtime features.
- Every promoted asset should include explicit ownership/provenance metadata.
- Every promoted asset should have explicit entries in `.claude/manifests/ccv3-dependencies.yaml`.
- For dbt work, CAF is the control plane, but dbt CLI execution belongs in `dbt-enterprise`.
- Do not edit `source` folder YAMLs or dbt models without user pre-approval.
- Do not use third-party MCP query tools for proprietary data; dbt MCP is allowed, Altimate MCP is not.

## Read Order For A Fresh Agent

Read these in this order before making new migration decisions:

1. `claude-analytics-framework/AGENT_ENTRYPOINT.md`
2. `claude-analytics-framework/README.md`
3. `claude-analytics-framework/CLAUDE.md`
4. `claude-analytics-framework/.claude/manifests/workspace-manifest.yaml`
5. `claude-analytics-framework/.claude/manifests/repo-adapters.yaml`
6. `claude-analytics-framework/.claude/manifests/workflow-contracts.yaml`
7. `claude-analytics-framework/.claude/manifests/ccv3-dependencies.yaml`
8. `claude-analytics-framework/knowledge/platform/planning/shared-agent-platform-monorepo-plan.md`
9. `claude-analytics-framework/knowledge/platform/planning/system-architect-evaluation.md`
10. `claude-analytics-framework/knowledge/platform/planning/global-to-caf-migration-inventory.md`
11. `claude-analytics-framework/knowledge/platform/planning/dbt-agent-decomposition-inventory.md`
12. `dbt-agent/.dots/ai-team-workspace-migration.md`

If deeper conversation context is needed, consult the prior session transcript referenced at the end of this handoff.

## What Has Already Been Done

The following foundational work is already in place in CAF:

- Agent-neutral bootstrap entrypoint:
  - `AGENT_ENTRYPOINT.md`
- Core workspace manifests:
  - `.claude/manifests/workspace-manifest.yaml`
  - `.claude/manifests/repo-adapters.yaml`
  - `.claude/manifests/workflow-contracts.yaml`
  - `.claude/manifests/ccv3-dependencies.yaml`
- Bootstrap and readiness scripts:
  - `scripts/bootstrap-linked-repos.sh`
  - `scripts/check-workspace-readiness.sh`
- CAF-root docs rewritten to match the shared control-plane model:
  - `README.md`
  - `CLAUDE.md`
  - `CONTRIBUTING.md`
- Shared domain knowledge skeletons created:
  - `knowledge/domains/README.md`
  - `knowledge/domains/dbt-pipelines/README.md`
  - `knowledge/domains/semantic-layer/README.md`
  - `knowledge/domains/redshift/README.md`
  - `knowledge/domains/data-storytelling/README.md`
  - `knowledge/domains/feature-store/README.md`
  - `knowledge/domains/tpg-pipelines/README.md`
- CAF-native pipeline command slice promoted:
  - `.claude/commands/pipeline-new.md`
  - `.claude/commands/pipeline-resume.md`
  - `.claude/commands/pipeline-status.md`
  - `.claude/commands/pipeline-gate.md`
  - `.claude/commands/pipeline-close.md`
- First orchestrator skill slice promoted:
  - `.claude/skills/dbt-orchestrator/SKILL.md`
  - `.claude/skills/dbt-orchestrator/tools.yml`
  - `.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md`
  - `.claude/skills/dbt-orchestrator/resources/gate-enforcement-rules.md`
  - `.claude/skills/dbt-orchestrator/resources/handoff-protocols.md`
  - `.claude/skills/dbt-orchestrator/resources/workflow-state-machine.md`
- First phase-skill wrapper slice promoted:
  - `.claude/skills/dbt-business-context/SKILL.md`
  - `.claude/skills/dbt-data-discovery/SKILL.md`
  - `.claude/skills/dbt-standards/SKILL.md`
  - `.claude/skills/dbt-qa/SKILL.md`
- First promoted knowledge/reference slice in CAF:
  - `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md`
  - `knowledge/domains/dbt-pipelines/reference/migration-quick-reference.md`
  - `knowledge/domains/dbt-pipelines/reference/qa-validation-checklist.md`
  - `knowledge/reference/standards/folder-structure-and-naming.md`
  - `knowledge/reference/tools/dbt-mcp-tools-reference.md`
  - `knowledge/domains/redshift/reference/anti-pattern-impact.yml`
- Second curated dependency-reduction knowledge slice promoted:
  - `knowledge/reference/tools/redshift-discovery-snippets.md`
  - `knowledge/domains/dbt-pipelines/reference/field-mappings.md`
  - `knowledge/reference/standards/controlled-vocabulary.yml`
  - `knowledge/domains/dbt-pipelines/reference/baas-join-registry.yml`
  - `knowledge/domains/dbt-pipelines/reference/troubleshooting.md`
  - `knowledge/domains/dbt-pipelines/decision-traces/README.md`
  - `knowledge/domains/dbt-pipelines/decision-traces/rules.json`
- CAF wrapper skills now prefer CAF-owned discovery, standards, and troubleshooting references before falling back to `dbt-agent`
- Architecture and preflight slice promoted:
  - `.claude/skills/dbt-tech-spec-writer/SKILL.md`
  - `.claude/skills/dbt-tech-spec-writer/resources/tech-spec-template.md`
  - `.claude/skills/dbt-tech-spec-writer/resources/model-inventory-format.md`
  - `.claude/skills/dbt-tech-spec-writer/resources/transformation-rules-format.md`
  - `.claude/skills/dbt-tech-spec-writer/resources/review-checklist.md`
  - `.claude/skills/dbt-preflight/SKILL.md`
  - `knowledge/reference/standards/architecture-validation-checklist.md`
  - `knowledge/reference/standards/mandatory-compile-rule.md`
- Orchestrator loading specs now route Phase 3 tech spec work and Phase 4 preflight through CAF-promoted assets first
- Implementation wrapper slice promoted:
  - `.claude/skills/dbt-migration/SKILL.md`
  - `.claude/skills/dbt-fundamentals/SKILL.md`
- Orchestrator loading specs now route Phase 4 build work through CAF-promoted implementation wrappers first
- Lineage and SQL-unit-testing wrapper slice promoted:
  - `.claude/skills/dbt-lineage/SKILL.md`
  - `.claude/skills/dbt-sql-unit-testing/SKILL.md`
- Orchestrator loading specs now route lineage analysis and SQL unit-test guidance through CAF-promoted wrappers first
- Macro and advanced-SQL slice promoted:
  - `knowledge/domains/dbt-pipelines/reference/macros-registry.md`
  - `.claude/skills/sql-hidden-gems/SKILL.md`
- Orchestrator loading specs now route macro-registry and advanced SQL references through CAF-promoted assets first
- Curated trace slice promoted:
  - `knowledge/domains/dbt-pipelines/decision-traces/selected-traces.json`
- QA routing now reads CAF-promoted reusable rules plus a curated recent-trace subset before falling back to the full historical corpus in `dbt-agent`
- Certified KPI benchmark slice promoted:
  - `knowledge/domains/dbt-pipelines/reference/legacy-kpi-gold-standard-metrics.md`
- Requirements capture now reads the CAF-promoted KPI benchmark reference first, and testing now routes through CAF `dbt-qa` rather than the legacy fallback
- Pipeline state contract slice promoted:
  - `.claude/manifests/pipeline-state-schema.yaml`
- CAF pipeline commands now treat `dbt-agent/handoffs/PIPELINE_REGISTRY.yaml` and `handoffs/[pipeline]/PLAN.md` as primary live state, with `.dots` treated as optional auxiliary state
- Pipeline starter template slice promoted:
  - `.claude/skills/dbt-orchestrator/resources/plan-template.md`
  - `.claude/skills/dbt-business-context/resources/business-context-template.md`
  - `.claude/skills/dbt-data-discovery/resources/data-discovery-template.md`
- Pipeline creation guidance now points agents to CAF-owned starter templates instead of relying on inferred artifact shapes
- QA report template promoted:
  - `.claude/skills/dbt-qa/resources/qa-report-template.md`
- QA and handoff guidance now have a CAF-owned starter artifact for `qa-report.md`
- Builder-to-QA handoff template promoted:
  - `.claude/skills/dbt-migration/resources/qa-execution-handoff-template.md`
- Build and QA guidance now support a richer execution-handoff pattern when a builder agent hands work to a QA agent

## Current CAF Git Status

At the time of this handoff, CAF has these uncommitted changes:

- Modified:
  - `.claude/manifests/ccv3-dependencies.yaml`
  - `.claude/manifests/workflow-contracts.yaml`
  - `knowledge/platform/planning/dbt-agent-decomposition-inventory.md`
  - `knowledge/domains/README.md`
  - `knowledge/domains/dbt-pipelines/README.md`
  - `knowledge/domains/redshift/README.md`
- Untracked:
  - `.claude/commands/pipeline-new.md`
  - `.claude/commands/pipeline-resume.md`
  - `.claude/commands/pipeline-status.md`
  - `.claude/commands/pipeline-gate.md`
  - `.claude/commands/pipeline-close.md`
  - `knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md`
  - `knowledge/domains/dbt-pipelines/reference/migration-quick-reference.md`
  - `knowledge/domains/dbt-pipelines/reference/qa-validation-checklist.md`
  - `knowledge/domains/redshift/reference/anti-pattern-impact.yml`
  - `knowledge/reference/README.md`
  - `knowledge/reference/standards/folder-structure-and-naming.md`
  - `knowledge/reference/tools/dbt-mcp-tools-reference.md`
  - `.claude/skills/dbt-orchestrator/`
  - `.claude/skills/dbt-business-context/`
  - `.claude/skills/dbt-data-discovery/`
  - `.claude/skills/dbt-standards/`
  - `.claude/skills/dbt-qa/`
  - `knowledge/platform/planning/next-agent-handoff-2026-03-14.md`

Treat these as in-progress migration work. Do not delete or overwrite them casually.

## Current dbt-agent Git Status

`dbt-agent` also has unrelated user/work-in-progress changes. Do not revert them.

Observed status:

- Modified:
  - `docs/visualizations/disbursements-platform-data-story.html`
  - `docs/visualizations/ewallet-data-story.html`
  - `docs/visualizations/geo-intelligence-v7.html`
  - `handoffs/disbursements/PLAN.md`
- Untracked:
  - `thoughts/shared/handoffs/chatops-analytics/auto-handoff-2026-03-14T05-52-47.yaml`
  - `thoughts/shared/handoffs/chatops-analytics/auto-handoff-2026-03-14T10-39-57.yaml`

Those changes are not the CAF migration slice and should be left alone unless the user explicitly asks otherwise.

## Source Of Truth And Routing

Use this routing model:

- CAF:
  - shared manifests
  - cross-repo coordination
  - promoted shared commands, skills, agents, and knowledge
  - agent-neutral bootstrap docs
- `dbt-enterprise`:
  - production dbt project
  - dbt CLI execution
  - model code, tests, analyses, project-local rules
- `dbt-agent`:
  - current operational reference
  - migration source for reusable shared assets
  - legacy depth for dbt-agent-native workflows
- `data-centered`:
  - publishing, content, visualization, and storytelling work

## Immediate Next Work

The next reasonable migration slice is to keep mapping `dbt-agent` assets file-by-file into CAF targets, building on the now-expanded pipeline command slice.

Recommended sequence:

1. Verify the first command slice and dependency metadata are internally consistent.
2. Continue the `dbt-agent` decomposition inventory for the next highest-leverage shared assets.
3. Pick the next promotion slice deliberately, likely one of:
   - the remaining decision-trace corpus beyond the currently curated `selected-traces.json`
   - deeper execution/reference assets such as selected `traces.json` entries, fuller lineage/unit-testing helper resources, or additional dbt-agent knowledge docs with repeated workflow value
   - additional later-phase templates or execution conventions if we want even more of the lifecycle scaffolded from CAF
4. For each candidate asset, record:
   - source path
   - target CAF path
   - classification
   - ownership label
   - CCV3/global dependency set
   - whether the CAF copy is mirror-only or CAF-owned
5. Promote the next slice by copy, not by deletion from `dbt-agent`.

Do not skip back into broad restructuring before the inventory and metadata stay ahead of the changes.

## Suggested Verification Checklist

Before ending the next work session, verify:

1. CAF still works as a cold-start entrypoint.
2. A non-Claude agent can read CAF docs/manifests and route to the right repo.
3. No promoted asset relies on undocumented global behavior.
4. `dbt-agent` remains operationally intact.
5. No dbt execution guidance was accidentally moved to CAF root instead of routed to `dbt-enterprise`.
6. New promoted assets have explicit provenance and dependency metadata.

## Files Most Likely To Matter Next

- `claude-analytics-framework/.claude/manifests/ccv3-dependencies.yaml`
- `claude-analytics-framework/.claude/commands/pipeline-new.md`
- `claude-analytics-framework/.claude/commands/pipeline-resume.md`
- `claude-analytics-framework/.claude/commands/pipeline-status.md`
- `claude-analytics-framework/.claude/commands/pipeline-gate.md`
- `claude-analytics-framework/.claude/commands/pipeline-close.md`
- `claude-analytics-framework/.claude/skills/dbt-orchestrator/SKILL.md`
- `claude-analytics-framework/.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md`
- `claude-analytics-framework/.claude/skills/dbt-orchestrator/resources/gate-enforcement-rules.md`
- `claude-analytics-framework/.claude/skills/dbt-business-context/SKILL.md`
- `claude-analytics-framework/.claude/skills/dbt-data-discovery/SKILL.md`
- `claude-analytics-framework/.claude/skills/dbt-standards/SKILL.md`
- `claude-analytics-framework/.claude/skills/dbt-qa/SKILL.md`
- `claude-analytics-framework/knowledge/domains/dbt-pipelines/reference/canonical-models-registry.md`
- `claude-analytics-framework/knowledge/domains/dbt-pipelines/reference/migration-quick-reference.md`
- `claude-analytics-framework/knowledge/domains/dbt-pipelines/reference/qa-validation-checklist.md`
- `claude-analytics-framework/knowledge/reference/standards/folder-structure-and-naming.md`
- `claude-analytics-framework/knowledge/reference/tools/dbt-mcp-tools-reference.md`
- `claude-analytics-framework/knowledge/domains/redshift/reference/anti-pattern-impact.yml`
- `claude-analytics-framework/knowledge/platform/planning/dbt-agent-decomposition-inventory.md`
- `claude-analytics-framework/knowledge/platform/planning/global-to-caf-migration-inventory.md`
- `dbt-agent/.dots/ai-team-workspace-migration.md`
- `dbt-agent/CLAUDE.md`

## Things To Avoid

- Do not assume CAF is already the authoritative home for all analytics capabilities.
- Do not flatten the multi-repo model into a single physical repo structure.
- Do not replace portable manifest-driven routing with ad hoc local path assumptions.
- Do not depend on Claude slash commands as the only explanation of how workflows operate.
- Do not clean up or “simplify” `dbt-agent` by removing source material during migration.

## If You Need More Context

There is a prior agent transcript for this migration session:

- Transcript UUID: `df35407d-2221-43d1-861e-9051653bf6c6`
- Transcript file:
  - `/Users/kbinkly/.cursor/projects/Users-kbinkly-git-repos-dbt-agent/agent-transcripts/df35407d-2221-43d1-861e-9051653bf6c6/df35407d-2221-43d1-861e-9051653bf6c6.jsonl`

Search the transcript by filenames such as:

- `shared-agent-platform-monorepo-plan.md`
- `ai-team-workspace-migration.md`
- `ccv3-dependencies.yaml`
- `pipeline-new.md`
- `pipeline-resume.md`
- `pipeline-status.md`

Do not read the transcript linearly unless necessary. Search first, then read only the relevant windows.
