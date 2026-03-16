# Nested Repos Restructure Plan

**Date:** 2026-03-16
**Status:** Approved — execute when ready
**Supersedes:** Symlink approach (repos/ directory with symlinks)

---

## Decision

Move from symlinks to **gitignored nested repos**. Each team repo is cloned directly inside the workspace directory and gitignored by the workspace's git. Each repo keeps its own `.git/`, branches, remotes, and CI/CD.

**Why:** Symlinks are local-only, require a bootstrap script, and depend on hardcoded personal paths. Nested gitignored repos give every teammate identical relative paths with zero configuration.

---

## Target Structure

```
analytics-workspace/                    ← workspace git repo (tracked)
  .gitignore                            ← includes: dbt-enterprise/ dbt-agent/ data-centered/
  dbt-enterprise/                       ← full repo clone (gitignored, own .git/)
  dbt-agent/                            ← full repo clone (gitignored, own .git/)
  data-centered/                        ← full repo clone (gitignored, own .git/)
  .claude/                              ← shared control plane (tracked)
  knowledge/                            ← shared knowledge (tracked)
  CLAUDE.md                             ← workspace bootstrap (tracked)
  QUICKSTART.md                         ← teammate onboarding (tracked)
  TESTING.md                            ← integration tests (tracked)
  ...
```

Each nested repo is fully independent:
- Own `.git/` — own branches, commits, history
- Own remote — pushes/pulls to its own GitHub repo
- Own CI/CD — dbt Cloud, GitHub Pages, etc. all unchanged
- Gitignored by workspace — workspace git never sees the nested repos

---

## What Changes

### Paths in promoted command/skill/agent files

All `repos/dbt-agent/...` references become `dbt-agent/...`

```
Before: repos/dbt-agent/shared/knowledge-base/canonical-models-registry.md
After:  dbt-agent/shared/knowledge-base/canonical-models-registry.md
```

This is a find-replace across `.claude/commands/`, `.claude/agents/`, `.claude/rules/`.

### .gitignore

Add to workspace `.gitignore`:
```
dbt-enterprise/
dbt-agent/
data-centered/
```

### Remove symlink infrastructure

- Delete `repos/` directory (symlinks no longer needed)
- Delete or update `scripts/bootstrap-linked-repos.sh`
- Update `repos/README.md` content into QUICKSTART.md setup section

### QUICKSTART.md setup section

```bash
# Before (symlink approach):
bash scripts/bootstrap-linked-repos.sh

# After (nested repos approach):
cd analytics-workspace
git clone <dbt-enterprise-url> dbt-enterprise
git clone <dbt-agent-url> dbt-agent
git clone <data-centered-url> data-centered
```

### Manifests

Update `workspace-manifest.yaml` and `repo-adapters.yaml`:
- Linked repo paths change from absolute to relative
- `dbt-enterprise` path: `./dbt-enterprise` (not `/Users/kbinkly/...`)

### dbt execution routing

```
Before: cd /Users/kbinkly/git-repos/dbt_projects/dbt-enterprise && dbt compile
After:  cd dbt-enterprise && dbt compile
```

Simpler. No absolute paths. Works for any teammate.

---

## Execution Steps

### Step 1: Update .gitignore

Add `dbt-enterprise/`, `dbt-agent/`, `data-centered/` to workspace `.gitignore`.

### Step 2: Clone repos into workspace

```bash
cd /Users/kbinkly/git-repos/claude-analytics-framework
git clone git@github.com:<org>/dbt-enterprise.git dbt-enterprise
git clone git@github.com:<org>/dbt-agent.git dbt-agent  # or just copy local
git clone git@github.com:<org>/data-centered.git data-centered  # or copy local
```

Alternative for repos already on disk: move or copy them in.

### Step 3: Find-replace path references

```bash
# In all promoted commands, agents, rules:
# repos/dbt-agent/ → dbt-agent/
# repos/dbt-enterprise/ → dbt-enterprise/
# repos/data-centered/ → data-centered/
```

### Step 4: Update manifests

Change absolute paths to relative:
```yaml
# Before
path: "/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise"
# After
path: "./dbt-enterprise"
```

### Step 5: Update QUICKSTART.md

Replace bootstrap script instructions with clone instructions.

### Step 6: Remove symlink infrastructure

- Remove `repos/` symlinks
- Archive or delete `scripts/bootstrap-linked-repos.sh`
- Update `repos/README.md` → move useful content elsewhere

### Step 7: Verify

- `ls dbt-enterprise/dbt_project.yml` — exists
- `cd dbt-enterprise && git status` — own repo, own branch
- `grep -rl "canonical-models-registry" dbt-agent/shared/` — cross-repo search works
- `cd dbt-enterprise && dbt compile` — dbt CLI works
- Workspace `git status` — doesn't show nested repo files

---

## What Does NOT Change

- Each repo's internal structure (zero changes)
- Each repo's remote URL
- Each repo's CI/CD
- Each repo's branch protection
- dbt Cloud configuration
- GitHub Pages configuration
- Agent memory locations (`~/.claude/agent-memory/`)
- Any file path relative to its own repo root

---

## Teammate Setup (After Restructure)

```bash
# One-time setup
git clone <workspace-url> analytics-workspace
cd analytics-workspace
git clone <dbt-enterprise-url> dbt-enterprise
git clone <dbt-agent-url> dbt-agent
git clone <data-centered-url> data-centered

# Start working
claude
```

No bootstrap script. No symlinks. No personal path configuration.

---

## Blast Radius for Keith

When executing this on Keith's machine:

1. **VS Code workspace** — update workspace root to new path
2. **Terminal aliases/bookmarks** — update any hardcoded paths to dbt-enterprise
3. **Worktrees** — may need re-linking if main checkout moves
4. **dbt Cloud IDE** — unaffected (uses remote, not local path)
5. **MCP** — unaffected (path-independent API calls)

Recommend: do this on a quiet afternoon, not before a deadline.
