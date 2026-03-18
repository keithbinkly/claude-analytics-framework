# Audit Before Bulk Edit

## Rule

Before making bulk changes (renaming, removing references, migrating files), run an audit agent first.

## The Pattern

1. **Audit** (scout/research agent): Produce a classified inventory
   - Every instance found, with file path and line
   - Classification: REMOVE / KEEP / MOVE TO CONFIG / MIXED
   - Rationale for each classification
2. **Review** (human): Approve or adjust classifications
3. **Execute** (spark/implementation agent): Apply approved changes

## Why

Bulk edits without classification cause collateral damage:
- Renaming catches unrelated matches
- Removing references breaks legitimate routing
- Moving files orphans downstream references

## Anti-Pattern

"Just search-replace all instances of X." This skips classification and treats all matches identically.

## Source

Session 2026-03-17: data-centered cleanup (13 REMOVE, 6 KEEP, 1 MOVE TO CONFIG — classifications were critical). CAF→analytics-workspace rename (106 files, required distinguishing display names from internal IDs).
