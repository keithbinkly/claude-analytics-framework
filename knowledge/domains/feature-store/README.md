# Feature Store

**Maintainer:** Data science team
**Status:** Open for contributions

## What This Covers

Feature engineering pipelines, ML feature store patterns, feature freshness and versioning, and reusable practices for model-serving and experimentation work.

## How Agents Use This Folder

When someone asks Claude about feature engineering, feature freshness, feature pipelines, or related topics, Claude reads files in this folder to ground its answers in **our team's actual practices** rather than generic LLM knowledge.

The more specific and practical the content here, the better the agent's answers.

## What to Add

### `patterns/` — Proven approaches

Things that work and should be reused:
- Feature pipeline templates (standard structure, naming)
- Feature freshness validation patterns
- Common transformation patterns (windowed aggregations, lag features, etc.)
- Testing patterns for feature correctness

### `reference/` — Facts and configurations

Things that are true about our setup:
- Feature store architecture overview
- Tool configuration and access patterns
- Data source catalog (what tables feed features)
- Schema documentation

### `decisions/` — Why we do things this way

Decisions with rationale so future engineers don't re-debate them:
- "Why we chose X feature store over Y"
- "Why features are versioned this way"
- "Why certain features are computed daily vs real-time"

## How to Contribute

1. Create a markdown file in the appropriate subfolder
2. Be specific and practical — "here's the SQL pattern" beats "features should be well-tested"
3. Include context: when to use it, when NOT to use it, what breaks if you do it wrong
4. Commit and push — the whole team benefits on next pull

```bash
mkdir -p patterns reference decisions
# Write your file
git add .
git commit -m "docs: add feature freshness validation pattern"
git push
```

## Creating a Feature Store Expert Agent (Optional)

If you want a dedicated agent persona, see `QUICKSTART.md` for the step-by-step guide to creating a domain expert agent that reads from this folder.
