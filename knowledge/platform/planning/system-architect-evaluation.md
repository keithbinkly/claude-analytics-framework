# System Architect Evaluation: CAF Monorepo Plan

**Author:** System Architect (domain agent)
**Date:** 2026-03-13 (pass 3 — with Builder and QA agent review)
**Status:** Approved for Phase 1 execution. All major risks resolved.

**Input documents reviewed:**
- `shared-agent-platform-monorepo-plan.md` (revised 2026-03-13)
- `global-to-caf-migration-inventory.md` (revised 2026-03-13)
- `dbt-agent-decomposition-inventory.md` (new 2026-03-13)
- `.claude/manifests/workspace-manifest.yaml` (revised 2026-03-13)
- `.claude/manifests/repo-adapters.yaml` (revised 2026-03-13)
- `README.md` (revised 2026-03-13)
- Actual CAF repo state (file tree, existing commands, CLAUDE.md)
- Builder agent memory (MEMORY.md, napkin.md) — operational impact review
- QA agent memory (MEMORY.md, napkin.md) — operational impact review

---

## Verdict Summary

| Dimension | Pass 1 (2026-03-12) | Pass 3 (2026-03-13) |
|-----------|---------------------|---------------------|
| Target architecture coherent? | Mostly — repo nesting contradiction | **Yes** — repos are external/linked, execution model proven |
| Migration phases realistic? | Phases 1-4 yes, Phase 5 risky, Phase 7 underscoped | **Yes** — Phase 5 eliminated, Phase 7 scoped correctly |
| Risks | Two-control-plane ambiguity, memory split, identity crisis | **All addressed** — including Builder/QA operational concerns |
| CAF as canonical root? | Right concept, not yet earned | **Confirmed** — earns authority by capability replacement |
| Pipeline safety | Not explicitly addressed | **Proven safe** — execution model already decoupled today |
| dbt CLI execution | Not assessed | **Non-issue** — already decoupled (see critical finding below) |

**Overall: Safe to proceed through Phase 3.** The execution model is already proven in production.

---

## CRITICAL FINDING: dbt Execution Decoupling Is Already Solved

**This section is essential context for Builder, QA, and any agent involved in pipeline work.**

### The concern that was raised

When evaluating whether agents could work from a CAF root directory, Builder and QA initially flagged that `dbt compile`, `dbt run`, `dbt test`, and `dbt show` all require `dbt_project.yml` in the working directory. If agents start sessions in CAF, how do they run dbt commands?

### Why this is a non-issue

**This pattern is already how every pipeline session works today.** The control plane (dbt-agent) and the execution target (dbt-enterprise) are already separate repos. Every Builder and QA session already:

1. Loads context from dbt-agent's `.claude/` (skills, commands, rules, knowledge bases)
2. Runs dbt CLI commands by `cd`-ing to dbt-enterprise
3. Uses `execute_sql` via MCP API (path-independent — works from any directory)

CAF does not change this relationship. It just moves the control plane up one level:

| Component | Today | CAF end state | Change? |
|-----------|-------|---------------|---------|
| **Control plane** (`.claude/`, skills, commands, rules) | dbt-agent | CAF | Yes — promotes up |
| **dbt execution target** (`dbt compile/run/test`) | dbt-enterprise (via `cd`) | dbt-enterprise (via `cd`) | **No change** |
| **MCP API** (`execute_sql`) | Path-independent | Path-independent | **No change** |
| **Knowledge base** (decision traces, QA templates) | dbt-agent/shared/ | CAF/repos/dbt-agent/shared/ (symlink) | Path changes, content doesn't |
| **Agent memory** | ~/.claude/agent-memory/ | ~/.claude/agent-memory/ | **No change** |

### What this means for agents

**Builder agent:** Your compile-before-run workflow, VPN gating, pre-flight checks, PLAN.md state machine, canonical registry lookups — none of these change mechanically. You already `cd` to dbt-enterprise for dbt commands. You will continue to do so. The only difference is that skills and commands load from CAF's `.claude/` instead of dbt-agent's `.claude/` once they're promoted.

**QA agent:** Your dual-mode execution (Claude QA via `execute_sql`, Copilot QA via Redshift) is already path-independent for the API path and `cd`-dependent for the CLI path. This doesn't change. Decision trace lookups will resolve through symlinks to the same files. The 4-template workflow, hypothesis-driven investigation, and trace logging all work identically.

**Both agents:** The hard architectural problem — separating "where I think" from "where I run dbt" — was already solved by necessity when dbt-agent and dbt-enterprise became separate repos. CAF inherits this proven pattern. There is no new decoupling to design.

### The only real migration work for agents

The remaining work is **path resolution in promoted skill and command files** — updating relative paths like `shared/knowledge-base/canonical-models-registry.md` to resolve correctly from CAF root (either via symlinks or absolute paths). This is Phase 3 mechanical work, not architectural risk.

---

## How Original Concerns Were Resolved

| Original concern | Resolution |
|---|---|
| Repo nesting mechanism undefined | Eliminated — repos are external, linked by absolute path in manifests |
| Two control planes during transition | Explicit 10-item capability cutover checklist in plan + manifests |
| Agent memory split | Global memory stays in `~/.claude/agent-memory/` — clean residency preserved |
| dbt-agent identity crisis | dbt-agent stays intact, adapter includes "continued native workflow execution" |
| Phase 5 high risk | Phase 5 removed — no physical nesting |
| Phase 7 underscoped | Phase 7 is now "decide what remains mirrored vs re-owned" — not absorb everything |
| Missing decomposition inventory | New file created with classification scheme + ownership labels |
| Ownership drift | Explicit labels: `source_of_truth`, `mirrored_from`, `deprecated_copy` |
| Open Q3: absolute vs relative paths | Resolved — manifests now use absolute paths |
| Builder: dbt CLI needs project dir | **Non-issue** — already decoupled today (see critical finding above) |
| Builder: PLAN.md and .dots/ paths | Resolved via symlinks — same files, accessible from CAF root |
| Builder: knowledge base relative paths | Phase 3 mechanical work — update paths in promoted skills |
| QA: decision trace paths | Resolved via symlinks — same files, accessible from CAF root |
| QA: dual-mode execution needs dbt-enterprise | **Non-issue** — already works via `cd` today |
| Both: .claude/settings.json hooks | Hooks promote to CAF's .claude/ as part of Phase 3 |

---

## Pipeline Preservation Assessment

The primary concern — maintaining the ability to build dbt pipelines during migration — is now structurally guaranteed through four reinforcing mechanisms:

1. **Adapter-level**: `repo-adapters.yaml` lists "continued dbt-agent-native workflow execution" as a safe work type for dbt-agent
2. **Policy-level**: `workspace-manifest.yaml` says `phase_out_from_dbt_agent: "nothing by default during incremental migration"`
3. **Plan-level**: "promotion into CAF is by copy unless there is a later, explicit decision to re-home"
4. **Architectural**: The control-plane / execution-target split is already proven in production — CAF inherits an existing working pattern, not inventing a new one

---

## Three Remaining Refinements

### 1. Decomposition inventory is scaffolding, not yet content

The `dbt-agent-decomposition-inventory.md` correctly identifies 8 areas and the classification scheme, but the "Required Next Pass" section says it needs file-by-file classification across 6 path groups. Until that pass happens, Phase 3 (copy highest-leverage content) doesn't have a concrete input list.

**This is the right prerequisite to call out.** The document is scaffolding for the inventory work, not the work itself. Phase 3 needs the completed inventory as input.

**Severity:** Expected — the document acknowledges this explicitly.

### 2. Routing rules have a gap for pipeline-building workflows

The four routing rules in `repo-adapters.yaml` cover:
- Platform work → `caf`
- Production dbt code → `dbt-enterprise`
- Content work → `data-centered`
- Migration extraction → `dbt-agent`

But the most common daily task — "build a new dbt pipeline using dbt-agent's skills, commands, and knowledge base against dbt-enterprise" — matches both `dbt-enterprise` (production dbt code) and `dbt-agent` (operational reference). The routing rules need either:

- A compound condition: "pipeline building uses dbt-enterprise adapter with dbt-agent as reference source"
- Or a note that multi-adapter tasks are expected and the agent should consult both

**Severity:** Low — agents will figure this out, but making it explicit prevents future confusion.

**Suggested addition to `repo-adapters.yaml` routing_rules:**
```yaml
- condition: "task concerns building dbt pipelines (requires both production project and operational reference)"
  use_adapter: "dbt-enterprise"
  also_consult: "dbt-agent"
  note: "Pipeline building uses dbt-enterprise as the execution target and dbt-agent as the skill/knowledge reference. This is the existing proven pattern."
```

### 3. The `promoted/dbt-agent/` directory creates a shadow structure

The topology shows `promoted/dbt-agent/` as the landing zone for copied assets. This creates a parallel shadow of dbt-agent inside CAF. Over time, agents will need to decide: "do I look in `promoted/dbt-agent/` or in the real dbt-agent?"

**Better approach:** Promote assets into their natural CAF-native locations (`knowledge/domains/dbt/`, `.claude/skills/`, `.claude/commands/`) and use the ownership labels to track provenance. The `promoted/` directory makes the migration visible but makes the end state messier.

**Severity:** Low-medium — worth changing before Phase 3 execution, but not before Phase 1 rollout.

**Suggested change to topology:**
```text
# Instead of:
promoted/
  dbt-agent/               # shadow copy

# Use:
knowledge/domains/dbt/     # for dbt domain knowledge
.claude/skills/            # for promoted skills
.claude/commands/          # for promoted commands
# Each file carries ownership metadata (source_of_truth, mirrored_from)
```

---

## Remaining Open Questions

| Question | Status |
|---|---|
| ~~Should CAF's existing generic commands be archived or evolved?~~ | Still open — the README.md references ADLC-style `/idea`, `/roadmap` commands that don't match the analytics platform target |
| ~~What's the minimum set of dbt-agent capabilities CAF needs?~~ | Resolved — the 10-item cutover checklist in the plan |
| ~~Should workspace manifest use absolute paths?~~ | Resolved — now uses absolute paths |
| ~~Builder: can dbt CLI work from CAF root?~~ | Resolved — already decoupled, `cd` to dbt-enterprise is the proven pattern |
| ~~QA: will decision traces be accessible?~~ | Resolved — symlinks make them accessible from CAF root |
| Is the learning loop infrastructure (`tools/chatops/`) a CAF asset or a dbt-agent asset? | Still open — this is the single largest infrastructure component and needs a classification decision |
| How do `dbt-enterprise` worktrees (4 active) interact with the CAF model? | Still open — worktrees use separate paths that aren't in the manifest |

---

## Recommended Next Steps

1. **Phase 1 rollout doc** — plan is approved, proceed
2. **Add symlinks** to CAF `repos/` as Phase 1 infrastructure (cross-repo search + path resolution)
3. **Add the compound routing rule** for pipeline-building workflows
4. **Decide on `promoted/` vs native placement** before Phase 3 execution
5. **Complete the decomposition inventory** (file-by-file pass) as input to Phase 3 asset selection
6. **Classify `tools/chatops/`** — this is the hardest classification call and should be made early
7. **Test one full pipeline cycle from CAF root** before declaring CAF ready as default working directory
