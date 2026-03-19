# Team Findings

Business findings, data quirks, analysis insights, and other discoveries contributed via `/contribute`.

These are automatically indexed into the Knowledge Graph and searchable via:

```bash
python3 knowledge/platform/graph/graph_search.py "your search terms"
```

## How to Add

Use `/contribute` at the end of any session — the agent handles placement, formatting, and indexing.

## File Format

Each finding is a standalone markdown file:
- Lowercase-kebab-case filename
- Leads with what was found, then when it applies, then evidence
- No frontmatter needed — the index builder extracts metadata from content
