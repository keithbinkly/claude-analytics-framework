# System Architect Evaluation: CAF Monorepo Plan

**Author:** System Architect (domain agent)
**Date:** 2026-03-12
**Input documents reviewed:**
- `shared-agent-platform-monorepo-plan.md`
- `global-to-caf-migration-inventory.md`
- `.claude/manifests/workspace-manifest.yaml`
- `.claude/manifests/repo-adapters.yaml`
- Actual CAF repo state (file tree, existing commands, CLAUDE.md)

---

## Verdict Summary

| Dimension | Assessment |
|-----------|-----------|
| Target architecture coherent? | Mostly yes — one structural contradiction around repo nesting |
| Migration phases realistic? | Phases 1-4 yes, Phase 5 high risk / low value, Phase 7 underscoped |
| Risks | Two-control-plane ambiguity, agent memory split, dbt-agent identity crisis |
| CAF as canonical root? | Right concept, not yet earned — needs content before authority |

---

## 1. Architecture Coherence

The three-layer model is sound: CAF as control plane, `dbt-enterprise` and `data-centered` as intact nested projects, `dbt-agent` as absorption source. The repo-adapters pattern is well-designed — explicit routing rules prevent the ambiguity that caused the original pain.

### Structural contradiction: repo nesting mechanism undefined

The plan says `dbt-enterprise` and `data-centered` should live under `repos/` inside CAF (Phase 5), but both are separate git repos with their own histories. The plan hand-waves this: "preserve git history/boundaries" without specifying the mechanism.

| Mechanism | Preserves history | Agent sees unified tree | Operational friction |
|-----------|------------------|------------------------|---------------------|
| Submodules | Yes | Yes (after init) | High (checkout, push, sync) |
| Symlinks | Yes (separate repos) | Yes | Low, but fragile |
| Actual copy | No | Yes | None after copy |
| Worktree mounts | No | Partial | Medium |

The existing CAF repo has `scripts/convert-to-submodules.sh` and `scripts/setup-submodules.sh` — so submodules were the original intent. But submodules are the #1 source of git friction for solo/small teams. This needs a definitive decision before Phase 5.

---

## 2. Migration Phase Realism

### Phases 1-4: Realistic and well-ordered

Phase 1 (control plane) is already partially done — manifests exist, planning docs exist. Phases 2-4 are content moves with low blast radius.

### Phase 5 (relocate repos): High risk, questionable value

Moving `dbt-enterprise` under CAF's tree is the riskiest phase and delivers the least value. Right now, agents work across repos by reading CLAUDE.md at each root. Moving the folders doesn't change agent behavior — only the manifests and adapters change behavior. The plan could achieve 90% of its goals without ever physically nesting the repos.

### Phase 7 (dbt-agent absorption): Unrealistically scoped

`dbt-agent` has ~45 skills, 8 domain agent memory directories, 23 slash commands, extensive knowledge bases, 40+ dots, workstream files, decision traces, and the entire learning loop infrastructure (`tools/chatops/`). "Progressively absorbed" is aspirational without a per-asset inventory with keep/move/archive decisions. The migration inventory covers `~/.claude` thoroughly but barely touches `dbt-agent` internals.

---

## 3. Risks and Contradictions

### Risk 1: Two control planes during transition (HIGH)

The plan creates CAF as the new control plane but doesn't specify when `dbt-agent`'s CLAUDE.md stops being authoritative. During the transition, agents loading from `dbt-agent` will still see 10 rules, 45 skills, and a full CLAUDE.md. Adding a second authoritative CLAUDE.md in CAF creates the exact ambiguity the plan is trying to solve — but now with two sources instead of one.

**Mitigation needed:** Define the cutover trigger — "dbt-agent's CLAUDE.md is authoritative until CAF has equivalent coverage for: [list of N capabilities]." Without this, you get a slow drift where both are half-authoritative.

### Risk 2: Agent memory split (MEDIUM)

The plan moves `system-architect` and `designer` memory from `~/.claude/agent-memory/` to CAF. But the existing architecture (decisions.md, 2026-02-20) placed global agents in `~/.claude/agent-memory/` specifically because they're invoked from multiple repos. Moving them to CAF means they're only visible when CAF is the working directory — unless path resolution logic is added. This reverses an architectural decision that was working.

**Recommendation:** Keep `~/.claude/agent-memory/` as the agent memory location. CAF can reference it via manifests without owning the files. The current residency rule (global = `~/.claude`, project = repo-local) is clean. Moving memory into CAF creates a coupling between agent identity and working directory.

### Risk 3: dbt-agent identity crisis (MEDIUM)

Today, `dbt-agent` is where all the work happens. It's where sessions start, where Claude loads context, where dots and workstreams live. The plan says it becomes a "migration source" with `safe_work_types: content extraction, migration planning, reference lookup`. But the existing CLAUDE.md in dbt-agent is a 300-line operating manual with MCP tool routing, VPN split architecture, preflight rules, QA standards — none of which CAF replaces. If you change dbt-agent's role to "migration source" before CAF has equivalent depth, you lose operational capability.

**Mitigation:** dbt-agent keeps its current role until CAF demonstrably replaces each capability. The adapter should reflect current reality, not aspirational end state.

### Risk 4: Plan-reality gap in existing CAF scaffolding (LOW but notable)

The existing CAF repo has generic scaffolding (setup wizard, devcontainer, sample project, generic commands like `/start`, `/switch`, `/pause`). The planning docs describe a specialized analytics control plane. These are different products. The existing commands don't map to the target architecture at all — they'll need to be replaced, not extended.

---

## 4. What Should Change Before Implementation

### A. Don't physically nest repos — defer Phase 5 indefinitely

Use manifests + path resolution instead. CAF can be the canonical root without containing the other repos as subdirectories. This eliminates the git complexity risk entirely. Agents already navigate across repos — the manifests just need to tell them where to look.

Replace `repos/dbt-enterprise/` and `repos/data-centered/` in the topology with path references to their actual locations on disk. The workspace manifest already has the infrastructure for this.

### B. Define cutover triggers, not just direction

Specify concrete conditions: "dbt-agent's CLAUDE.md is authoritative until CAF has equivalent coverage for these capabilities:

1. MCP tool routing (VPN split)
2. Preflight rules
3. QA standards and templates
4. Skill activation table
5. Pipeline orchestration commands
6. Agent loading specs
7. Anti-pattern enforcement
8. Decision trace lookup
9. Learning loop infrastructure
10. Workstream state management"

Each capability migrates independently. dbt-agent's authority shrinks as CAF's grows.

### C. Reconsider moving global agent memory

Keep `~/.claude/agent-memory/` as the canonical location for global agent memory. CAF manifests can reference these paths. The current residency rule is sound:

- Global (invoked from 2+ repos): `~/.claude/agent-memory/`
- Project (single repo): `<repo>/.claude/agent-memory/`

Moving memory into CAF couples agent identity to working directory. An agent invoked from `data-centered` shouldn't need CAF checked out to find its own memory.

### D. Create the dbt-agent decomposition inventory (prerequisite to Phase 2)

The migration inventory covers `~/.claude` well but `dbt-agent` barely. Before Phase 2, create a file-by-file inventory of `dbt-agent/.claude/` classifying each asset:

| Classification | Meaning |
|---------------|---------|
| Promote to CAF | Reusable across analytics projects |
| Keep in dbt-domain | Specific to dbt-enterprise operations |
| Archive | Superseded or stale |
| Already duplicated | Exists in both places — resolve |

This is the actual hard work of the migration.

### E. Reconcile existing CAF scaffolding with target architecture

The current commands (`/start`, `/switch`, `/build`, `/pause`, `/complete`, `/pr`) are generic project management. The target is an analytics operating system. Either:

- Evolve these commands to serve the analytics platform, or
- Replace them with the analytics-specific commands from the plan

Don't leave two command philosophies coexisting.

---

## 5. Is CAF the Right Canonical Root?

**Yes, but not yet.**

The concept is right: a shared control plane above the delivery repos. The current state of `dbt-agent` as both "knowledge base" and "control plane" is unsustainable — it was the right choice when there was one repo, but with three repos and growing, it creates the navigation ambiguity the plan correctly identifies.

However, CAF earns canonical status by **having the content**, not by **declaring itself canonical**. Current state:

| What CAF has | What dbt-agent has |
|---|---|
| Manifests, planning docs, generic scaffolding | 45 skills, 8 agent memories, 23 commands |
| — | Decision traces, learning loop infra |
| — | QA standards, preflight rules |
| — | All operational depth |

The honest current state is: CAF is a *planned* canonical root. It becomes the *actual* canonical root when an agent starting a fresh session in CAF can orient itself as well as one starting in dbt-agent. That's the real milestone.

---

## 6. Recommended Execution Order

| Step | Phase | Notes |
|------|-------|-------|
| 1 | Phase 1 (done) | Manifests exist, keep iterating |
| 2 | New: dbt-agent decomposition | Full inventory — prerequisite to Phase 2 |
| 3 | Phase 2 | Extract reusable patterns, but leave dbt-agent authoritative until CAF has equivalent |
| 4 | Phase 3 | Adapters — already drafted, looks solid |
| 5 | Phase 4 (modified) | Selective global migration: manifests + commands yes, agent memory no |
| 6 | **Skip Phase 5** | Don't physically nest repos — use path references |
| 7 | Phase 6 | Unified workstream state — high value, doesn't depend on repo nesting |
| 8 | Phase 7 | Only after CAF demonstrably works as primary root |

---

## 7. Open Questions for the Next Session

1. Should CAF's existing generic commands be archived or evolved?
2. What's the minimum set of dbt-agent capabilities CAF needs before it can claim canonical status?
3. Should the workspace manifest use absolute paths to sibling repos instead of relative `repos/` paths?
4. Is the learning loop infrastructure (`tools/chatops/`) a CAF asset or a dbt-agent asset?
5. How do `dbt-enterprise` worktrees (4 active) interact with the CAF model?
