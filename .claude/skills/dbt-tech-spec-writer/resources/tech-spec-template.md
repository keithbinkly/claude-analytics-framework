<!--
source_of_truth: caf
mirrored_from: dbt-agent/.claude/skills/dbt-tech-spec-writer/resources/tech-spec-template.md
-->

# Technical Specification: [Pipeline Name]

> **Status**: DRAFT | IN_REVIEW | APPROVED
> **Created**: [date]
> **Author**: [agent or reviewer]
> **Approver**: [name]

---

## 1. Overview

| Field | Value |
|-------|-------|
| **Pipeline Name** | [name] |
| **Purpose** | [business value] |
| **Legacy Source** | [path or N/A] |
| **Priority** | [P1/P2/P3/P4] |
| **Complexity** | [Low/Medium/High] |
| **Canonical Reuse** | [target]% |
| **Estimated Models** | [count] |

## 2. Business Requirements Summary

**Source Document**: `handoffs/[pipeline]/business-context.md`

### Key Metrics

| Metric | Definition | Acceptance Criteria |
|--------|------------|---------------------|
| [metric] | [definition] | [threshold] |

### Critical Business Rules

1. **[Rule]**: [description]
2. **[Rule]**: [description]

## 2.5 Semantic Layer Decision

| Decision | Answer |
|----------|--------|
| Feeds semantic layer? | YES / NO |
| Mart design approach | NORMALIZED / DENORMALIZED |
| Rationale | [why] |

## 3. Data Discovery Summary

**Source Document**: `handoffs/[pipeline]/data-discovery-report.md`

| Source | Status | Key Finding |
|--------|--------|-------------|
| [table] | [PASS/WARN] | [finding] |

## 4. Model Inventory

| Model Name | Layer | Materialization | Grain | Unique Key | Est. Rows | Reuse |
|------------|-------|-----------------|-------|------------|-----------|-------|
| [model] | [layer] | [type] | [grain] | [key] | [rows] | [NEW/CANONICAL/EXTEND] |

### Folder Placement

| Model | Target Folder | Validation |
|-------|---------------|------------|
| [model] | [path] | [structure guide used] |

## 5. Transformation Rules

| Target Column | Source Column(s) | Transformation | Business Rule |
|---------------|------------------|----------------|---------------|
| [target] | [source] | [logic] | [reference] |

## 6. Incremental Strategy

| Model | Strategy | Unique Key | Lookback | Rationale |
|-------|----------|------------|----------|-----------|
| [model] | [strategy] | [key] | [window] | [why] |

## 7. Test Requirements

| Model | Column | Test Type | Severity | Config |
|-------|--------|-----------|----------|--------|
| [model] | [column] | [test] | [severity] | [config] |

## 8. Dependencies

| Dependency | Type | Critical | Notes |
|------------|------|----------|-------|
| [model/source] | [type] | YES / NO | [notes] |

## 9. Risks And Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [risk] | [level] | [level] | [plan] |

## 10. Architecture Decisions

| Decision | Options Considered | Selected | Rationale |
|----------|--------------------|----------|-----------|
| [decision] | [options] | [selected] | [why] |

## 11. Human Review Checklist

- [ ] model inventory matches requirements
- [ ] folder placement validated against structure guides
- [ ] canonical reuse documented
- [ ] transformation rules reviewed
- [ ] tests cover critical paths
- [ ] risks have mitigations
