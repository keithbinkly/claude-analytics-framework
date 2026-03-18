# Claude Code Tips from the Team — Expanded Edition

**Boris Cherny** (@bcherny) — Jan 31, 2026
**Our Annotations** — Feb 2, 2026

I'm Boris and I created Claude Code. I wanted to quickly share a few tips for using Claude Code, sourced directly from the Claude Code team. The way the team uses Claude is different than how I use it. Remember: there is no one right way to use Claude Code -- everyones' setup is different.

Source: [X thread](https://x.com/bcherny/status/2017742741636321619?s=20)

---

> **How to read this document**
>
> Regular text = Boris's original tips (verbatim)
>
> Blocks marked with **`>>> OUR SETUP`** = How we implement this tip
>
> Blocks marked with **`>>> DEEPER DIVES`** = Resources from our library that expand on this tip
>
> Blocks marked with **`>>> GAP`** = What we're missing vs the recommendation

---

## 1. [Do more in parallel](https://x.com/bcherny/status/2017742743125299476?s=20)

Spin up 3–5 git worktrees at once, each running its own Claude session  in parallel. It's the single biggest productivity unlock, and the top tip from the team. Personally, I use multiple git checkouts, but most of the Claude Code team prefers worktrees.

---

> **`>>> OUR SETUP`** | Rating: **Partial**
>
> - **Cross-terminal coordination DB**: PostgreSQL (`continuous_claude`) with `sessions` and `file_claims` tables for conflict detection across terminals (`.claude/rules/cross-terminal-db.md`)
> - **Proactive delegation rule**: `.claude/rules/proactive-delegation.md` detects independent tasks and spawns parallel agents automatically
> - **VPN constraint** forces serial batching: VPN ON = Copilot (warehouse), VPN OFF = Claude Code. Can't run both simultaneously.
> - No git worktrees usage found.

> **`>>> GAP`**
>
> True 3-5 session parallelism blocked by VPN. Once that constraint resolves, git worktrees are the next unlock.

> **`>>> DEEPER DIVES`**
>
> - **Agent Swarms Are Here** (`sources/x_articles_text/agent_swarms_are_here.md`) — Deep dive on parallel spawning, dependency graphs, free parallelism up to 7-10 agents
> - **Mission Squad** (`sources/x_articles_text/mission_squad.md`) — Real implementation: 10 parallel agents with staggered heartbeats, session isolation
> - **Multi-Agent Orchestration Pattern** (`dbt-agent/docs/RESOURCES.MD`) — 9 agents across 3 platforms (Claude Code, Codex, Gemini CLI), Beads as central tracker

---

## 2. [Start every complex task in plan mode](https://x.com/bcherny/status/2017742745365057733?s=20)

Pour your energy into the plan so Claude can 1-shot the implementation.

One person has one Claude write the plan, then they spin up a second Claude to review it as a staff engineer.

Another says the moment something goes sideways, they stop and re-plan rather than letting Claude iterate.

---

> **`>>> OUR SETUP`** | Rating: **Strong**
>
> - **Architect agent** (`.claude/agents/architect.md`): Opus-powered, uses "Erotetic Check" — frames the full question space E(X,Q) before producing a plan
> - **4-phase workflow**: `dbt-agent/shared/knowledge-base/pko/procedures/four-phase-workflow.yaml`
> - **Development kickoff command**: `dbt-agent/.claude/commands/development-kickoff.md` — loads 12+ skills at session start, checks active handoffs, forces planning before execution
> - **48 specialized agents** across planning, execution, review, and validation roles
> - Two-Claude pattern: architect plans, then phoenix/kraken implements

> **`>>> DEEPER DIVES`**
>
> - **Practical Guide to Context Engineering** (`sources/x_articles_text/practical_guide_context_eng.md`) — "Plan for longer, refine even longer" workflow with plan mode emphasis
> - **Give Agents A Computer** (`sources/x_articles_text/give_agents_a_computer.md`) — Offloading context to filesystem plan files; agents read plan back to reinforce objectives
> - **Agent Failure Modes & Solutions** (`dbt-agent/docs/RESOURCES.MD`) — "Declares victory too early" → feature list JSON with end-to-end descriptions fixes it
> - **Agent Swarms Are Here** (`sources/x_articles_text/agent_swarms_are_here.md`) — Task dependency graphs enforce correctness, planning externalized into structure

---

## 3. [Invest in your CLAUDE.md](https://x.com/bcherny/status/2017742747067945390?s=20)

After every correction, end with: "Update your CLAUDE.md so you don't make that mistake again." Claude is eerily good at writing rules for itself.

Ruthlessly edit your CLAUDE.md over time. Keep iterating.

---

> **`>>> OUR SETUP`** | Rating: **Strong**
>
> - **3 project-level CLAUDE.md files**: PM agent (`CLAUDE.md`, multi-repo orchestrator), data-centered (`.claude/CLAUDE.md`, content pipeline), dbt-agent (`CLAUDE.md`, 269 lines)
> - **13 rule files** in `.claude/rules/`: claim-verification, destructive-commands, proactive-delegation, agent-model-selection, dynamic-recall, cross-terminal-db, etc.
> - **Dots system**: 101 tracking files across repos (85 in dbt-agent, 16 in data-centered) — YAML frontmatter with status/priority, mandatory for >15min tasks
> - **Claim verification rule** born from an actual 80% false claim rate — exactly Boris's "update after corrections" pattern
> - **320K+ lines of documentation** across the system

> **`>>> DEEPER DIVES`**
>
> - **Obsidian + Claude Code 101** (`sources/x_articles_text/obsidian_claude_code101.md`) — Building 2000-line CLAUDE.md files, teaching agents your philosophy and conventions
> - **You Could've Invented Claude Code** (`sources/x_articles_text/you_couldve_invented_claude.md`) — Section "Goal: Project-Specific Context (CLAUDE.md)" explains how CLAUDE.md becomes project knowledge
> - **Clawd Bot How It Works** (`sources/x_articles_text/clawd_bot_how_it_works.md`) — SOUL.md and AGENTS.md patterns for agent configuration and behavior rules
> - **Mission Squad** (`sources/x_articles_text/mission_squad.md`) — Full taxonomy: SOUL files, AGENTS.md, HEARTBEAT.md
> - **Learning Machines** (`sources/x_articles_text/learning_machines.md`) — Agents evolving their own context/instructions over time through reflection

---

## 4. [Create your own skills and commit them to git](https://x.com/bcherny/status/2017742748984742078?s=20)

Reuse across every project.

Tips from the team:
- If you do something more than once a day, turn it into a skill or command
- Build a `/techdebt` slash command and run it at the end of every session to find and kill duplicated code
- Set up a slash command that syncs 7 days of Slack, GDrive, Asana, and GitHub into one context dump
- Build analytics-engineer-style agents that write dbt models, review code, and test changes in dev

Learn more: [code.claude.com](https://code.claude.com)

---

> **`>>> OUR SETUP`** | Rating: **Strong**
>
> - **47 skills in dbt-agent** (`dbt-agent/.claude/skills/`): Skills-first architecture v2.0 with `SKILL.md` + `tools.yml` + `workflows/` + `guardrails/` per skill
> - **4 skills in data-centered**: librarian, editor, visual-testing, frontend-design
> - **10 slash commands** (`dbt-agent/.claude/commands/`): `/development-kickoff`, `/morning-review`, `/trigger-review`, `/log_work_to_dots`, etc.
> - **Skills Registry**: `dbt-agent/.claude/skills/SKILLS_REGISTRY.md`
> - Boris's "analytics-engineer-style agents" tip? That's literally dbt-agent: 36 dbt-specific skills for migration, QA, lineage, semantic layer, optimization
> - All git-committed, shared across sessions, progressive disclosure via YAML frontmatter

> **`>>> DEEPER DIVES`**
>
> - **Skills/Agents Merged** (`sources/x_articles_text/skills_agents_merged.md`) — Official announcement merging slash commands into skills, progressive disclosure pattern
> - **Fintool Build Process** (`sources/x_articles_text/fintool_build_process.md`) — "Skills Are Everything" section: markdown-based skills as the product, industry-specific guidelines, copy-on-write shadowing
> - **Obsidian + Claude Code 101** (`sources/x_articles_text/obsidian_claude_code101.md`) — "Every note is basically a skill... highly curated knowledge that gets injected when relevant"
> - **AgentSkills.io** (`dbt-agent/docs/RESOURCES.MD`) — Open standard by Anthropic; our `.claude/skills/` structure matches it

---

## 5. [Claude fixes most bugs by itself](https://x.com/bcherny/status/2017742750473720121?s=20)

Here's how the team does it:

- Enable the Slack MCP, then paste a Slack bug thread into Claude and just say "fix." Zero context switching required.
- Or, just say "Go fix the failing CI tests." Don't micromanage how.
- Point Claude at docker logs to troubleshoot distributed systems -- it's surprisingly capable at this.

---

> **`>>> OUR SETUP`** | Rating: **Good**
>
> - **64 active hooks** (`.claude/hooks/dist/*.mjs`): failure-detection, import-error-detector, compiler-in-the-loop, auto-error-resolver (triggered at 5+ errors)
> - **MCP warehouse access**: `datamate` server for direct database debugging
> - **Debug agents**: debug-agent, sleuth — specialized investigation and root cause analysis

> **`>>> GAP`**
>
> No Slack MCP for CI failure threads. No dedicated `/fix-ci` command. These would be straightforward to add.

> **`>>> DEEPER DIVES`**
>
> - **Clawd Bot Exec Assistant** (`sources/x_articles_text/clawd_bot_exec_assistant.md`) — Sandboxed VM setup, prompt injection inoculation, permission systems for autonomous bug fixing
> - **Clawdbot Tips** (`sources/x_articles_text/clawdbot_tips.md`) — Multi-model agent setup (senior/junior/intern), approval rules, automated monitoring (AWS bill checks)
> - **Fintool Build Process** (`sources/x_articles_text/fintool_build_process.md`) — Production monitoring, auto-filing GitHub issues for errors, sandboxed execution

---

## 6. [Level up your prompting](https://x.com/bcherny/status/2017742752566632544?s=20)

a. **Challenge Claude.** Say "Grill me on these changes and don't make a PR until I pass your test." Make Claude be your reviewer. Or, say "Prove to me this works" and have Claude diff behavior between main and your feature branch.

b. **Push for elegance.** After a mediocre fix, say: "Knowing everything you know now, scrap this and implement the elegant solution."

c. **Write detailed specs** and reduce ambiguity before handing work off. The more specific you are, the better the output.

---

> **`>>> OUR SETUP`** | Rating: **Strong**
>
> - **Erotetic logic** across agents: frames the question space E(X,Q) before acting (scout, architect agents)
> - **Voice engineering**: Librarian skill analyzes McPhee, DFW, Feynman, Jacob Collier for voice patterns — "precision that expands rather than narrows"
> - **5,681 lines** across 48 agent definitions — each with specific tools, model selection, execution patterns
> - **Epistemic markers**: claim-verification rule requires VERIFIED / INFERRED / UNCERTAIN markers on factual claims
> - **Detailed spec templates**: dbt tech-spec-writer skill, design-document-writer skill

> **`>>> DEEPER DIVES`**
>
> - **Practical Guide to Context Engineering** (`sources/x_articles_text/practical_guide_context_eng.md`) — "Optimal set of high-signal tokens", plan refinement, asking Claude to ask clarifying questions
> - **Obsidian + Claude Code 101** (`sources/x_articles_text/obsidian_claude_code101.md`) — "Depth over breadth. Quality over speed. Tokens are free. This is about excellence."
> - **Fintool Build Process** (`sources/x_articles_text/fintool_build_process.md`) — Domain-specific eval datasets, adversarial grounding, precision requirements
> - **How I'd Build a One-Person Business** (`sources/x_articles_text/how_id_build_a_one_person_business.md`) — System prompts, teaching AI personality and boundaries through detailed specs

---

## 7. [Terminal and environment setup](https://x.com/bcherny/status/2017742753971769626?s=20)

The team loves Ghostty! Multiple people like its synchronized rendering, 24-bit color, and proper unicode support.

For easier Claude-juggling, use `/statusline` to customize your status bar to always show context usage and current git branch. Many of us also color-code and name our terminal tabs, sometimes using tmux — one tab per task/worktree.

Use voice dictation. You speak 3x faster than you type, and your prompts get way more detailed as a result. (Hit fn x2 on macOS)

More tips: [Terminal config docs](https://code.claude.com/docs/en/terminal-config)

---

> **`>>> OUR SETUP`** | Rating: **Partial**
>
> - **Ghostty**: Installed and active
> - **Shell config**: `.zshrc` with Claude-specific env vars (`CLAUDE_OPC_DIR`, `CLAUDE_CODE_TASK_LIST_ID`, `CLAUDE_CODE_ENABLE_TELEMETRY`)
> - **Cross-terminal DB**: PostgreSQL coordination for multi-terminal session awareness

> **`>>> GAP`**
>
> - No `/statusline` customization (context usage, git branch display)
> - No color-coded terminal tabs per project/worktree
> - No voice dictation setup (fn x2 on macOS — free, immediate win)
> - No tmux configuration for tab management

> **`>>> DEEPER DIVES`**
>
> - **You Could've Invented Claude Code** (`sources/x_articles_text/you_couldve_invented_claude.md`) — Building agent from scratch with bash/filesystem primitives, terminal-based agent loop
> - **Give Agents A Computer** (`sources/x_articles_text/give_agents_a_computer.md`) — "The fundamental coding agent abstraction is the CLI... agents need access to the OS layer"

---

## 8. [Use subagents](https://x.com/bcherny/status/2017742755737555434?s=20)

a. **Append "use subagents"** to any request where you want Claude to throw more compute at the problem.

b. **Offload individual tasks** to subagents to keep your main agent's context window clean and focused.

c. **Route permission requests to Opus 4.5** via a hook — let it scan for attacks and auto-approve the safe ones (see [hooks#permissionrequest](https://code.claude.com/docs/en/hooks#permissionrequest)).

---

> **`>>> OUR SETUP`** | Rating: **Strong**
>
> - **48 specialized agents** (5,681 lines in `.claude/agents/`): scout, oracle, kraken, spark, arbiter, architect, phoenix, debug-agent, sleuth, herald, profiler, and 37 more
> - **Proactive delegation rule** (`.claude/rules/proactive-delegation.md`): Pattern detection (multiple tasks → parallel agents), workflow suggestions (/fix, /build, /explore), "Main Context = Coordination Only"
> - **Permission hooks**: Hook system blocks/redirects tool calls (e.g., `explore-to-scout.mjs` redirects Haiku to Sonnet for accuracy)
> - **Model selection rules** (`.claude/rules/agent-model-selection.md`): Default inherit Opus, Haiku only for mechanical tasks, never for research/exploration
> - **Context isolation**: Each agent gets its own context window, main agent stays clean

> **`>>> DEEPER DIVES`**
>
> - **Agent Swarms Are Here** (`sources/x_articles_text/agent_swarms_are_here.md`) — Context isolation, 7-10 parallel subagents, free parallelism, layer-by-layer delegation
> - **Mission Squad** (`sources/x_articles_text/mission_squad.md`) — Complete 10-agent system with session isolation, heartbeat scheduling, cross-agent communication
> - **Practical Guide to Context Engineering** (`sources/x_articles_text/practical_guide_context_eng.md`) — "Librarian" subagent pattern: separate context window, cheaper model, summarized results
> - **Clawd Bot How It Works** (`sources/x_articles_text/clawd_bot_how_it_works.md`) — Lane-based command queues, session isolation, "Default to Serial, go for Parallel explicitly"
> - **Fast Agentic Search** (`dbt-agent/docs/RESOURCES.MD`) — 4x latency reduction via parallel tool execution, no penalty for 4-12 simultaneous calls

---

## 9. [Use Claude for data & analytics](https://x.com/bcherny/status/2017742757666902374?s=20)

Ask Claude Code to use the "bq" CLI to pull and analyze metrics on the fly. We have a BigQuery skill checked into the codebase, and everyone on the team uses it for analytics queries directly in Claude Code. Personally, I haven't written a line of SQL in 6+ months.

This works for any database that has a CLI, MCP, or API.

---

> **`>>> OUR SETUP`** | Rating: **Strong**
>
> - **36 dbt-specific skills**: Semantic layer, migration, QA, lineage, optimization, fundamentals, Redshift tuning
> - **MCP warehouse access**: `datamate` server in `.cursor/mcp.json` — direct database queries, no manual SQL copying
> - **InstaChart visualization** (`dataviz-studio/bin/instachart`): `--file data.json --auto-plot`, headless ASCII mode, documented in both CLAUDE.md files
> - **Query log mining**: Analyzed 474K Redshift queries, discovered 666 CPU hours/month in one pattern (`.dots/drafts/query-log-mining-blog-draft.md`)
> - **68 semantic layer metrics**, 331 production models, 340 data quality tests
> - **tldr-cli** (`.claude/rules/tldr-cli.md`): Structure analysis, CFG/DFG, import analysis, diagnostics — 22+ commands
> - Boris says "I haven't written SQL in 6+ months." We have 36 skills that *generate* SQL.

> **`>>> DEEPER DIVES`**
>
> - **Fintool Build Process** (`sources/x_articles_text/fintool_build_process.md`) — Financial agent with SQL + bash, S3-first architecture, structured data normalization
> - **Who Needs a Semantic Layer Anyway?** (`dbt-agent/docs/RESOURCES.MD`) — Query log mining methodology, discovering the "de facto semantic layer" from what people actually query
> - **ADE-Bench** (`dbt-agent/docs/RESOURCES.MD`) — dbt Labs' official benchmark for AI data engineering agents: 8 challenge categories, 60+ tasks
> - **dbt MCP Server Conversational Analytics** (`dbt-agent/docs/RESOURCES.MD`) — Norlys case study: metrics-first approach, AI + dbt in production

---

## 10. [Learning with Claude](https://x.com/bcherny/status/2017742759218794768?s=20)

A few tips from the team to use Claude Code for learning:

a. **Enable the "Explanatory" or "Learning" output style** in `/config` to have Claude explain the *why* behind its changes.

b. **Have Claude generate a visual HTML presentation** explaining unfamiliar code. It makes surprisingly good slides!

c. **Ask Claude to draw ASCII diagrams** of new protocols and codebases to help you understand them.

d. **Build a spaced-repetition learning skill:** you explain your understanding, Claude asks follow-ups to fill gaps, stores the result.

---

> **`>>> OUR SETUP`** | Rating: **Good**
>
> - **Semantic memory system**: PostgreSQL with BGE embeddings (1024-dim, bge-large-en-v1.5), 100+ real learnings
> - **Recall/store scripts**: `opc/scripts/core/recall_learnings.py` and `store_learning.py` — hybrid RRF search (text + vector combined)
> - **Learning types**: ARCHITECTURAL_DECISION, WORKING_SOLUTION, FAILED_APPROACH, ERROR_FIX, USER_PREFERENCE, OPEN_THREAD, CODEBASE_PATTERN
> - **Memory-awareness hook** (`memory-awareness.mjs`): Proactively injects relevant memories into context with "MEMORY MATCH" tag
> - **Proactive disclosure rule** (`.claude/rules/proactive-memory-disclosure.md`): Acknowledges relevant memories, applies past solutions, offers deep recall
> - **ASCII diagrams**: tldr-cli generates CFG/DFG graphs; architecture diagrams in `dbt-agent/docs/architecture/`

> **`>>> GAP`**
>
> - No spaced-repetition review system (monthly `/recall-review` of FAILED_APPROACH entries would close this)
> - No HTML presentation generation for code explanations
> - No "Explanatory" output style configured in `/config`

> **`>>> DEEPER DIVES`**
>
> - **Learning Machines** (`sources/x_articles_text/learning_machines.md`) — GPU Poor Learning: agents learning from interactions, memory stores, knowledge transfer across sessions
> - **Obsidian + Claude Code 101** (`sources/x_articles_text/obsidian_claude_code101.md`) — Vault as thinking partner, progressive disclosure, agents leaving breadcrumbs for future sessions
> - **Momo Research** (`dbt-agent/docs/RESOURCES.MD`) — 5-layer memory stack, compaction strategies, memory-as-a-tool
> - **Coding Tutor Plugin** (`dbt-agent/docs/RESOURCES.MD`) — Spaced repetition quizzes, progress tracking, curriculum planning (directly addresses our gap)

---

Hope these tips are helpful! What do you want to hear about next?

---

## Summary Scorecard

| # | Tip | Rating | Notes |
|---|-----|--------|-------|
| 1 | Parallel work | **Partial** | Infra exists (DB, delegation), VPN blocks true parallelism |
| 2 | Plan mode | **Strong** | Erotetic logic + architect agent + 4-phase workflows |
| 3 | CLAUDE.md | **Strong** | 3 CLAUDE.md + 13 rules + 101 dots + claim verification |
| 4 | Skills | **Strong** | 47 skills, 10 commands, skills-first architecture v2.0 |
| 5 | Bug fixing | **Good** | 64 hooks + debug agents. Gap: no Slack MCP |
| 6 | Prompting | **Strong** | Erotetic logic, voice engineering, epistemic markers |
| 7 | Terminal | **Partial** | Ghostty + env vars. Gap: statusline, color tabs, voice |
| 8 | Subagents | **Strong** | 48 agents, proactive delegation, model selection rules |
| 9 | Data & analytics | **Strong** | 36 dbt skills + MCP + InstaChart + 474K query analysis |
| 10 | Learning | **Good** | Semantic memory + proactive recall. Gap: spaced repetition |

**Overall: 6 Strong, 2 Good, 2 Partial**

### Top 3 Quick Wins

1. **Voice dictation** (Tip 7) — fn x2 on macOS, zero setup, 3x prompt detail
2. **`/statusline` customization** (Tip 7) — show context usage + git branch
3. **Spaced repetition for learnings** (Tip 10) — monthly `/recall-review` command over 100+ stored learnings
