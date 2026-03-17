<!--
source_of_truth: analytics-workspace
mirrored_from: dbt-agent/shared/templates/data-discovery-template.md
-->

# Data Discovery Template

Workspace-owned template for `handoffs/[pipeline]/data-discovery-report.md`.

```markdown
# Data Discovery Report: [Pipeline Name]

> **Status**: DRAFT | IN_REVIEW | APPROVED
> **Created**: [date]
> **Business Context**: `handoffs/[pipeline]/business-context.md`

## Executive Summary

| Field | Value |
|-------|-------|
| **Pipeline Name** | [name] |
| **Sources Profiled** | [count] |
| **Critical Findings** | [count] |
| **Suppression Risk** | [Low/Medium/High] |
| **Schema Validated** | [YES/NO] |

### Key Findings
- [Finding 1]
- [Finding 2]

---

## Source Inventory

| Source | Schema.Table | Row Count | Date Range | Freshness |
|--------|--------------|-----------|------------|-----------|
| [src1] | [schema.table] | [count] | [range] | [hours/days] |

---

## Schema Validation

| Source | Column | Type | Nullable | Sample Values |
|--------|--------|------|----------|---------------|
| [src] | [col] | [type] | [Y/N] | [samples] |

---

## Volume Analysis

| Stage | Filter | Row Count | % of Previous |
|-------|--------|-----------|---------------|
| Raw source | None | [count] | 100% |
| Final | All filters | [count] | [%] |

### Suppression Risks

| Filter | Rows Removed | % Suppression | Risk Level |
|--------|--------------|---------------|------------|
| [filter] | [count] | [%] | [Low/Med/High] |

---

## Relationship Analysis

| Left | Right | Join Key | Cardinality | Match Rate |
|------|-------|----------|-------------|------------|
| [tbl] | [tbl] | [key] | [1:1/1:N/N:N] | [%] |

---

## Data Quality Issues

| Source | Column | Issue | Severity | Mitigation |
|--------|--------|-------|----------|------------|
| [src] | [col] | [issue] | [High/Med/Low] | [fix] |

---

## Recommendations

| Finding | Recommendation | Priority |
|---------|----------------|----------|
| [finding] | [recommendation] | [P1/P2/P3] |

---

## Questions for Stakeholder

- [ ] [Question 1]
- [ ] [Question 2]
```
