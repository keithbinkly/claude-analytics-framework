<!--
source_of_truth: caf
mirrored_from: dbt-agent/shared/templates/business-context-template.md
-->

# Business Context Template

CAF-owned template for `handoffs/[pipeline]/business-context.md`.

```markdown
# Business Context: [Pipeline Name]

> **Status**: DRAFT | REVIEWED | APPROVED
> **Created**: [date]
> **Stakeholder**: [name/team]
> **Priority**: [P1/P2/P3/P4]

---

## Overview

### Problem Statement
[What problem does this pipeline solve?]

### Business Value
[Why does this matter?]

### Current State
[How is this handled today?]

### Target State
[What should the new pipeline provide?]

---

## Source Information

| Field | Value |
|-------|-------|
| **Legacy Script** | [path or N/A] |
| **Stakeholder** | [name/team] |
| **Meeting Date** | [date or N/A] |
| **Transcript** | [path or N/A] |

---

## Key Metrics

| Metric Name | Business Definition | Acceptance Threshold |
|-------------|---------------------|---------------------|
| [Metric 1] | [definition] | < [X]% variance |

---

## Business Rules

| Rule ID | Description | Applies To |
|---------|-------------|------------|
| BR-001 | [description] | [metrics/models] |

---

## Acceptance Criteria

### Functional
- [ ] [Criterion 1]

### Data Quality
- [ ] Variance < [X]% vs legacy
- [ ] No NULL in [critical columns]

### Performance
- [ ] Refresh completes in < [X] minutes

---

## Domain Glossary

| Term | Definition | Technical Mapping |
|------|------------|-------------------|
| [Term 1] | [definition] | [column/table] |

---

## Out of Scope

| Item | Reason |
|------|--------|
| [Item 1] | [reason] |

---

## Questions for Discovery

- [ ] [Question 1]
- [ ] [Question 2]
```
