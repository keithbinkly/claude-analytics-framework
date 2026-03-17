<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md
-->

# Agent Loading Specifications

Workspace-owned loading reference for pipeline phases.

Commands such as `/pipeline-new`, `/pipeline-resume`, and `/pipeline-gate` should use this file first when deciding which skills and references to load.

## Conventions

- `WS-KB:` -> `knowledge/domains/dbt-pipelines/reference/`
- `WS-REF:` -> `knowledge/reference/`
- `WS-SKILL:` -> `.claude/skills/[name]/SKILL.md`
- `DBT-AGENT-FALLBACK:` -> corresponding path in `dbt-agent` if analytics-workspace has not promoted the dependency yet

## Cross-Phase Resources

Load these at the start of a pipeline session:

```
READ: WS-KB:migration-quick-reference.md
READ: WS-KB:canonical-models-registry.md
READ: WS-REF:tools/dbt-mcp-tools-reference.md
READ: WS-REF:standards/folder-structure-and-naming.md
```

## Workflow A: Full Migration

### Phase 1: Requirements Capture

```
AGENT: Business Context Capture
  LOAD: WS-SKILL:dbt-business-context
  READ: WS-KB:canonical-models-registry.md
  READ: WS-KB:legacy-kpi-gold-standard-metrics.md
  OUTPUT: handoffs/[pipeline]/business-context.md
```

### Phase 2: Data Discovery

```
AGENT A: Source Profiler (PARALLEL)
  LOAD: WS-SKILL:dbt-data-discovery
  READ: WS-REF:standards/folder-structure-and-naming.md
  READ: WS-REF:tools/redshift-discovery-snippets.md
  READ: WS-KB:field-mappings.md
  TOOLS: execute_sql, get_source_details, get_column_lineage
  TOOLS: dbt show (if VPN available)

AGENT B: Lineage Analyst (PARALLEL)
  LOAD: WS-SKILL:dbt-lineage
  READ: WS-KB:canonical-models-registry.md
  READ: WS-REF:standards/folder-structure-and-naming.md

AGENT C: Legacy Script Analyst (PARALLEL)
  LOAD: WS-SKILL:dbt-migration
  LOAD: WS-SKILL:sql-hidden-gems
  READ: knowledge/domains/redshift/reference/anti-pattern-impact.yml
  READ: WS-KB:baas-join-registry.yml
```

### Phase 3: Architecture Design

```
AGENT A: Canonical Model Search (PARALLEL)
  LOAD: WS-SKILL:dbt-standards
  READ: WS-KB:canonical-models-registry.md
  READ: WS-KB:macros-registry.md
  TOOLS: get_related_models

AGENT B: Standards Validation (PARALLEL)
  LOAD: WS-SKILL:dbt-standards
  READ: WS-REF:standards/folder-structure-and-naming.md
  READ: WS-REF:standards/controlled-vocabulary.yml

AGENT C: Tech Spec Writer (SEQUENTIAL)
  LOAD: WS-SKILL:dbt-tech-spec-writer
  READ: WS-KB:migration-quick-reference.md
  READ: WS-KB:canonical-models-registry.md
  READ: WS-REF:standards/folder-structure-and-naming.md
  READ: WS-REF:standards/architecture-validation-checklist.md
```

### Phase 4: Implementation

```
STEP 4.1: Preflight
  LOAD: WS-SKILL:dbt-preflight
  READ: WS-REF:tools/dbt-mcp-tools-reference.md
  READ: WS-REF:standards/mandatory-compile-rule.md

STEP 4.2: Build
  LOAD: WS-SKILL:dbt-migration
  LOAD: WS-SKILL:dbt-fundamentals
  READ: WS-KB:migration-quick-reference.md
  READ: WS-KB:canonical-models-registry.md
  READ: WS-KB:baas-join-registry.yml
  READ: WS-REF:standards/folder-structure-and-naming.md
  READ: WS-REF:standards/controlled-vocabulary.yml
  READ: WS-REF:standards/mandatory-compile-rule.md

STEP 4.3: Testing
  LOAD: WS-SKILL:dbt-sql-unit-testing
  LOAD: WS-SKILL:dbt-qa

STEP 4.4: QA
  LOAD: WS-SKILL:dbt-qa
  READ: WS-KB:qa-validation-checklist.md
  READ: WS-KB:troubleshooting.md
  READ: knowledge/domains/dbt-pipelines/decision-traces/rules.json
  READ: knowledge/domains/dbt-pipelines/decision-traces/selected-traces.json
  READ: DBT-AGENT-FALLBACK:shared/decision-traces/traces.json
```

## Operational Rule

Whenever a `DBT-AGENT-FALLBACK` reference is used, note that dependency explicitly rather than pretending analytics-workspace owns it already.
