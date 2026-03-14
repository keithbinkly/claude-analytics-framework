# Canonical Model Scan

## Before Designing ANY New Model

Complete all three steps. All three are required — user memory is incomplete and the registry is not exhaustive.

1. **Ask user** for model suggestions in this domain
2. **Run `get_related_models()`** for domain terms
3. **Search codebase** independently (`tldr search "table_name"` or `get_context()`)

Target: 75-90% reuse from existing canonical models.

## Why Step 3 Is Mandatory

Step 3 (independent codebase scan) is the most commonly skipped and the most important. Users don't remember all overlapping models. The registry is a quick reference, not exhaustive. The only reliable path to 75-90% reuse is actually searching.

## EDW vs ODS

When choosing between EDW and ODS source tables, always prefer EDW where one exists (better performance, richer dimensions, pre-computed hierarchies). Only use ODS when no EDW equivalent exists.
