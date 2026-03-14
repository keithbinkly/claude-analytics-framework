<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-orchestrator/resources/agent-loading-specs.md
-->

# Agent Loading Specifications

CAF-owned loading reference for pipeline phases.

Commands such as `/pipeline-new`, `/pipeline-resume`, and `/pipeline-gate` should use this file first when deciding which skills and references to load.

## Conventions

- `CAF-KB:` -> `knowledge/domains/dbt-pipelines/reference/`
- `CAF-REF:` -> `knowledge/reference/`
- `CAF-SKILL:` -> `.claude/skills/[name]/SKILL.md`
- `DBT-AGENT-FALLBACK:` -> corresponding path in `dbt-agent` if CAF has not promoted the dependency yet

## Cross-Phase Resources

Load these at the start of a pipeline session:

```
READ: CAF-KB:migration-quick-reference.md
READ: CAF-KB:canonical-models-registry.md
READ: CAF-REF:tools/dbt-mcp-tools-reference.md
READ: CAF-REF:standards/folder-structure-and-naming.md
```

## Workflow A: Full Migration

### Phase 1: Requirements Capture

```
AGENT: Business Context Capture
  LOAD: CAF-SKILL:dbt-business-context
  READ: CAF-KB:canonical-models-registry.md
  READ: CAF-KB:legacy-kpi-gold-standard-metrics.md
  OUTPUT: handoffs/[pipeline]/business-context.md
```

### Phase 2: Data Discovery

```
AGENT A: Source Profiler (PARALLEL)
  LOAD: CAF-SKILL:dbt-data-discovery
  READ: CAF-REF:standards/folder-structure-and-naming.md
  READ: CAF-REF:tools/redshift-discovery-snippets.md
  READ: CAF-KB:field-mappings.md
  TOOLS: execute_sql, get_source_details, get_column_lineage
  TOOLS: dbt show (if VPN available)

AGENT B: Lineage Analyst (PARALLEL)
  LOAD: CAF-SKILL:dbt-lineage
  READ: CAF-KB:canonical-models-registry.md
  READ: CAF-REF:standards/folder-structure-and-naming.md

AGENT C: Legacy Script Analyst (PARALLEL)
  LOAD: CAF-SKILL:dbt-migration
  LOAD: CAF-SKILL:sql-hidden-gems
  READ: knowledge/domains/redshift/reference/anti-pattern-impact.yml
  READ: CAF-KB:baas-join-registry.yml
```

### Phase 3: Architecture Design

```
AGENT A: Canonical Model Search (PARALLEL)
  LOAD: CAF-SKILL:dbt-standards
  READ: CAF-KB:canonical-models-registry.md
  READ: CAF-KB:macros-registry.md
  TOOLS: get_related_models

AGENT B: Standards Validation (PARALLEL)
  LOAD: CAF-SKILL:dbt-standards
  READ: CAF-REF:standards/folder-structure-and-naming.md
  READ: CAF-REF:standards/controlled-vocabulary.yml

AGENT C: Tech Spec Writer (SEQUENTIAL)
  LOAD: CAF-SKILL:dbt-tech-spec-writer
  READ: CAF-KB:migration-quick-reference.md
  READ: CAF-KB:canonical-models-registry.md
  READ: CAF-REF:standards/folder-structure-and-naming.md
  READ: CAF-REF:standards/architecture-validation-checklist.md
```

### Phase 4: Implementation

```
STEP 4.1: Preflight
  LOAD: CAF-SKILL:dbt-preflight
  READ: CAF-REF:tools/dbt-mcp-tools-reference.md
  READ: CAF-REF:standards/mandatory-compile-rule.md

STEP 4.2: Build
  LOAD: CAF-SKILL:dbt-migration
  LOAD: CAF-SKILL:dbt-fundamentals
  READ: CAF-KB:migration-quick-reference.md
  READ: CAF-KB:canonical-models-registry.md
  READ: CAF-KB:baas-join-registry.yml
  READ: CAF-REF:standards/folder-structure-and-naming.md
  READ: CAF-REF:standards/controlled-vocabulary.yml
  READ: CAF-REF:standards/mandatory-compile-rule.md

STEP 4.3: Testing
  LOAD: CAF-SKILL:dbt-sql-unit-testing
  LOAD: CAF-SKILL:dbt-qa

STEP 4.4: QA
  LOAD: CAF-SKILL:dbt-qa
  READ: CAF-KB:qa-validation-checklist.md
  READ: CAF-KB:troubleshooting.md
  READ: knowledge/domains/dbt-pipelines/decision-traces/rules.json
  READ: knowledge/domains/dbt-pipelines/decision-traces/selected-traces.json
  READ: DBT-AGENT-FALLBACK:shared/decision-traces/traces.json
```

## Operational Rule

Whenever a `DBT-AGENT-FALLBACK` reference is used, note that dependency explicitly rather than pretending CAF owns it already.
