<!--
source_of_truth: caf
mirrored_from: dbt-agent/handoffs/_templates/PLAN-TEMPLATE.md
-->

# Pipeline Plan Template

analytics-workspace-owned template for `handoffs/[pipeline]/PLAN.md` during the migration period.

Use this when creating a new pipeline plan in the live state repo.

## Frontmatter Template

```yaml
---
# === RESUME BLOCK (new session reads this FIRST) ===
pipeline: PIPELINE_NAME
phase: requirements
last_action: "Pipeline plan created"
next_action: "Capture business context"
blockers: []
models_complete: []
models_remaining: []
branch: feat/PIPELINE_NAME
worktree: null

# === METADATA ===
created: YYYY-MM-DDTHH:MM:SS
last_updated: YYYY-MM-DDTHH:MM:SS
priority: P2
legacy_script: null
estimated_complexity: medium
canonical_reuse_target: 80
---
```

## Body Template

```markdown
# Pipeline Plan: PIPELINE_NAME

## Overview

[2-3 sentences: what this pipeline does, business value, current state]

---

## Phase History

### Requirements
- **Status**: not_started
- **Completed**: -
- **Artifacts**: []
- **Key findings**: -

### Discovery
- **Status**: not_started
- **Completed**: -
- **Artifacts**: []
- **Key findings**: -

### Architecture
- **Status**: not_started
- **Completed**: -
- **Artifacts**: []
- **Key findings**: -

### Implementation
- **Status**: not_started
- **Started**: -
- **Progress**: -
- **Models built**: 0/0

### QA
- **Status**: not_started
- **Variance**: -
- **Tests passing**: -

### Deploy
- **Status**: not_started
- **PR**: -
- **Merged**: -

---

## Model Inventory

| Model | Layer | Materialization | Status | Notes |
|-------|-------|-----------------|--------|-------|
| _to be filled during architecture phase_ | | | | |

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| _YYYY-MM-DD_ | _Pipeline created_ | _Initial planning_ |

---

## Gate Status

- [ ] **Gate 1** (Requirements -> Discovery): PENDING
- [ ] **Gate 2** (Discovery -> Architecture): PENDING
- [ ] **Gate 3** (Architecture -> Implementation): PENDING
- [ ] **Gate 4** (Implementation -> QA/Deploy): PENDING

---

## Blockers

_None currently._

---

## Artifacts

| Phase | Artifact | Path | Status |
|-------|----------|------|--------|
| Requirements | Business Context | `handoffs/PIPELINE_NAME/business-context.md` | - |
| Discovery | Data Discovery Report | `handoffs/PIPELINE_NAME/data-discovery-report.md` | - |
| Architecture | Tech Spec | `handoffs/PIPELINE_NAME/tech-spec.md` | - |
| QA | QA Report | `handoffs/PIPELINE_NAME/qa-report.md` | - |
```

## Notes

- Normalize the phase values using `.claude/manifests/pipeline-state-schema.yaml`.
- Prefer the four analytics-workspace primary gates even if older historical plans used an extra deploy checkpoint.
