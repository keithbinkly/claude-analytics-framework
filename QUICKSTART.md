# Quick Start — Analytics & Insights Team Workspace

**Time to useful:** 5 minutes.

---

## What This Is

This is the Analytics & Insights team's shared AI workspace. It has skills, knowledge, and workflows that make Claude (or any AI coding agent) better at our analytics work — dbt pipelines, data science, QA, visualization, and more.

**It is NOT where dbt code lives.** dbt code stays in `dbt-enterprise`. This workspace is the brain that helps you work on it.

---

## Setup (2 minutes)

### 1. Clone and link repos

```bash
git clone <this-repo-url>
cd analytics-workspace
bash scripts/bootstrap-linked-repos.sh
```

This creates symlinks to the sibling repos (dbt-enterprise, dbt-agent) so you can search across them.

### 2. Verify MCP

```bash
cp .env.example .env
# Edit .env with your dbt Cloud API token and account ID
# Get token: https://cloud.getdbt.com/settings/tokens
bash scripts/validate-mcp.sh
```

### 3. Start Claude Code

```bash
cd analytics-workspace
claude
```

That's it. Claude now has access to 27 skills, 24 commands, 21 operating rules, and the team's shared knowledge base.

---

## Your First Session

Try any of these:

```
"What skills are available for dbt pipeline work?"
"I need to QA a model — what's the methodology?"
"Help me design an intermediate model for customer transactions"
"/pipeline-status"
"/analyze What's driving the decline in approval rates?"
```

Claude will auto-load the right skill based on keywords. See the full keyword→skill table in `CLAUDE.md`.

---

## How It Works

### Three repos, one workspace

| Repo | What | You do here |
|------|------|------------|
| **AI Team Workspace** (this) | Shared brain — skills, knowledge, commands | Read skills, add domain knowledge, use commands |
| **dbt-enterprise** | Production dbt code | Write models, run dbt compile/run/test |
| **dbt-agent** | Reference (migration source) | Read reference material if not yet in workspace |

### When Claude needs to run dbt

Claude knows to `cd` to dbt-enterprise for dbt CLI commands. You don't need to do anything — the routing rules in `.claude/manifests/repo-adapters.yaml` handle it.

### What the skills do

Skills are loaded automatically by keyword. When you say "optimize this query," Claude loads the Redshift Optimization skill. When you say "QA this model," it loads the QA skill with the 4-template methodology.

You don't invoke skills manually — just describe what you need.

---

## Adding Your Domain Knowledge

This is the most valuable thing you can do for the team.

### Example: Kyuhyun setting up Feature Store knowledge

```bash
cd analytics-workspace/knowledge/domains/feature-store
```

The folder already exists with a README. Add your files:

```
knowledge/domains/feature-store/
  README.md                          ← already exists
  patterns/
    feature-freshness-checks.md      ← "Here's how we validate feature freshness"
    naming-conventions.md            ← "Feature names follow this pattern"
    feature-pipeline-template.md     ← "Standard pipeline structure"
  reference/
    feature-store-architecture.md    ← "How our feature store is set up"
    common-transforms.md             ← "Reusable transformation patterns"
  decisions/
    why-we-use-X.md                  ← "We chose X over Y because..."
```

**What happens:** Next time anyone asks Claude about feature store patterns, it can read these files and give answers grounded in *our team's* actual practices — not generic LLM knowledge.

### The pattern works for any domain

```
knowledge/domains/tpg-pipelines/     ← TPG team adds their patterns here
knowledge/domains/semantic-layer/    ← Semantic layer patterns
knowledge/domains/redshift/          ← Redshift optimization learnings
knowledge/domains/data-storytelling/ ← Visualization patterns
```

### Commit and push

```bash
git add knowledge/domains/feature-store/
git commit -m "docs: add feature store engineering patterns"
git push
```

Everyone on the team benefits on next pull.

---

## Creating a Domain Expert Agent (Optional)

Want Claude to have a dedicated "Feature Store Expert" persona? Create an agent definition with persistent memory that the whole team benefits from.

### Team vs Personal Agents

| Type | Memory location | Git-tracked? | Who benefits? |
|------|----------------|-------------|---------------|
| **Team agent** | `.claude/agent-memory/<name>/` (in this repo) | Yes | Everyone on `git pull` |
| **Personal agent** | `~/.claude/agent-memory/<name>/` (on your machine) | No | Only you |

**Rule of thumb:** If your agent's accumulated knowledge would help teammates, make it a team agent. If it's personal preferences or scheduling, make it personal.

Existing team agents: Builder, QA, Context Builder, Analytics Manager. Their memory lives in `.claude/agent-memory/` and is shared with the team via git.

### 1. Create the agent file

```bash
# .claude/agents/feature-store-expert.md
```

```markdown
---
name: feature-store-expert
description: Feature engineering and feature store specialist
model: sonnet
---

# Feature Store Expert

You are a feature store specialist for our analytics team.

## Your knowledge base

Before answering any question about feature engineering, read these files:
- knowledge/domains/feature-store/README.md
- knowledge/domains/feature-store/patterns/*.md
- knowledge/domains/feature-store/reference/*.md

## What you do

- Help design features for ML models
- Review feature freshness and quality
- Suggest naming conventions per our team standards
- Help with feature pipeline architecture

## What you don't do

- You don't run dbt commands (route to dbt-enterprise for that)
- You don't modify production code without explicit approval
- You don't guess when you could read the knowledge base
```

### 2. Create the agent's memory files

```bash
mkdir -p .claude/agent-memory/feature-store-expert
```

Create the standard 4-file set:

| File | Purpose | Update when |
|------|---------|-------------|
| `MEMORY.md` | Identity, commitments (keep under 200 lines) | Rare — identity changes |
| `napkin.md` | Anti-patterns, things that went wrong | After mistakes |
| `decisions.md` | Choices with rationale | After non-trivial decisions |
| `session-log.md` | What happened recently | End of each session |

Then add memory loading to your agent file — add this section to the agent markdown:

```markdown
## Your memory (team-shared)

Read these files to load your accumulated knowledge:
- .claude/agent-memory/feature-store-expert/MEMORY.md
- .claude/agent-memory/feature-store-expert/napkin.md
- .claude/agent-memory/feature-store-expert/decisions.md
```

### 4. Create a slash command (optional)

```bash
# .claude/commands/feature-store-expert.md
```

```markdown
Read and load the feature store expert agent from `.claude/agents/feature-store-expert.md`.
Then read all files in `knowledge/domains/feature-store/` to build context.
Greet the user and ask what feature engineering task they need help with.
```

### 5. Use it

```
/feature-store-expert
"Help me design features for the churn prediction model"
```

Or just ask about feature store topics — if you add it to the skill activation table in `CLAUDE.md`, it'll load automatically.

### 6. Commit the memory

```bash
git add .claude/agent-memory/feature-store-expert/
git commit -m "docs: add feature store expert agent memory"
git push
```

Now everyone on the team gets this agent's accumulated knowledge on their next pull.

---

## Key Commands

| Command | What it does |
|---------|-------------|
| `/pipeline-new [name]` | Start a new dbt pipeline |
| `/pipeline-resume [name]` | Resume pipeline work |
| `/pipeline-status` | Check all pipeline status |
| `/analyze [question]` | Multi-analyst ensemble (3 AI analysts answer your question) |
| `/explore-data` | Systematic data exploration |
| `/save` | Save workstream progress |
| `/load [name]` | Resume from saved state |
| `/qa` | Load QA agent |
| `/builder` | Load Builder agent |
| `/morning-review` | Daily standup: check workstreams, dots, pipeline status |
| `/development-kickoff` | Load all dbt skills for an implementation session |
| `/pipeline-gate` | Advance a pipeline through phase gates |

For the full list of 23 commands, see `.claude/commands/README.md`.

---

## What NOT to Put Here

- **dbt model code** → goes in dbt-enterprise
- **Personal notes** → your local `~/.claude/agent-memory/` (auto-managed by Claude)
- **Sensitive data** → never committed to git. Use gitignored `session-logs/`
- **One-off analysis scripts** → keep in dbt-enterprise `analyses/` or local

---

## Troubleshooting

**"Claude doesn't seem to know about my domain knowledge"**
→ Make sure your files are committed and pushed. Claude reads from the filesystem, not from memory.

**"dbt commands fail from workspace root"**
→ Expected. dbt commands run from dbt-enterprise, not here. Claude handles the `cd` automatically.

**"MCP not working"**
→ Run `bash scripts/validate-mcp.sh`. If it fails, check `.env` credentials and restart Claude Code.

**"I don't see the symlinks in repos/"**
→ Run `bash scripts/bootstrap-linked-repos.sh`. Symlinks are local-only (gitignored).

---

## Learn More

| Doc | What it covers |
|-----|---------------|
| `CLAUDE.md` | Full skill activation table, routing rules, anti-patterns |
| `AGENT_ENTRYPOINT.md` | Agent-neutral bootstrap (for non-Claude AI tools) |
| `CONTRIBUTING.md` | How to contribute shared assets |
| `knowledge/platform/planning/ai-team-workspace-spec.md` | Full architecture specification |
