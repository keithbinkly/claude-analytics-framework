  Three-Layer Map

  Layer 1: Global (~/.claude/)

  ┌──────────┬───────┬──────────────────────────────────────────────────────────────────────────────────────┐
  │ Category │ Count │                                        Notes                                         │
  ├──────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Agents   │ 30    │ General-purpose: kraken, spark, scout, oracle, architect, phoenix, etc.              │
  ├──────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Skills   │ ~80   │ Broad: TDD, security, refactoring, math, braintrust, agentica, MCP, etc.             │
  ├──────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Commands │ 20    │ designer, rams, frontend-design, life-admin, data-story, etc.                        │
  ├──────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Rules    │ 12    │ Meta-rules: no-haiku, claim-verification, destructive-commands, dynamic-recall, etc. │
  ├──────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Hooks    │ ~30   │ TS/bash: memory-awareness, file-claims, braintrust, pre-compact, etc.                │
  └──────────┴───────┴──────────────────────────────────────────────────────────────────────────────────────┘

  Layer 2: CAF / analytics-workspace (.claude/)

  ┌───────────┬───────────────────┬──────────────────────────────────────────────────────────────────────────────────────────┐
  │ Category  │       Count       │                                          Notes                                           │
  ├───────────┼───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Agents    │ 26                │ Domain-specific: ensemble-forensic/exploratory/business/statistical, qa, orchestrator,   │
  │           │                   │ etc.                                                                                     │
  ├───────────┼───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Skills    │ 27                │ All dbt/analytics: dbt-qa, dbt-migration, echarts, data-storytelling, etc.               │
  ├───────────┼───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Commands  │ 24                │ Pipeline lifecycle: pipeline-new/resume/gate/close, analyze, morning-review, etc.        │
  ├───────────┼───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Rules     │ 21                │ Hard-won lessons: compile-before-run, QA standards, circuit breakers, etc.               │
  ├───────────┼───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Knowledge │ 26+ reference     │ dbt-pipelines, redshift, decision-traces, canonical registries                           │
  │           │ docs              │                                                                                          │
  ├───────────┼───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Manifests │ 5                 │ workspace-manifest, repo-adapters, workflow-contracts, ccv3-deps, pipeline-state         │
  ├───────────┼───────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
  │ Hooks     │ 0                 │ None at CAF level                                                                        │
  └───────────┴───────────────────┴──────────────────────────────────────────────────────────────────────────────────────────┘

  Layer 3: dbt-agent (.claude/)

  ┌──────────────┬────────────┬──────────────────────────────────────────────────────────────────────────┐
  │   Category   │   Count    │                                  Notes                                   │
  ├──────────────┼────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ Agents       │ 26         │ Identical to CAF (promoted copies)                                       │
  ├──────────────┼────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ Skills       │ 45         │ CAF's 27 + 18 extras not yet promoted                                    │
  ├──────────────┼────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ Commands     │ 24         │ Identical to CAF                                                         │
  ├──────────────┼────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ Rules        │ 21         │ Identical to CAF                                                         │
  ├──────────────┼────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ Hooks        │ 20         │ Python hooks: skill-activation, dbt-quality-check, metricflow-lint, etc. │
  ├──────────────┼────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ Shared KB    │ rich       │ decision-traces, knowledge-base (partners, PKO), reference, templates    │
  ├──────────────┼────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ Agent Memory │ 5 personas │ analytics-manager, builder, context-builder, qa, system-architect        │
  └──────────────┴────────────┴──────────────────────────────────────────────────────────────────────────┘

  ---
  Key Issues for Team Release

  1. Duplication: Agents, commands, and rules are 100% identical between CAF and dbt-agent. This is the "copy-promote" migration
  in progress, but for a team tool you'd want one authoritative source.

  2. 18 un-promoted dbt-agent skills still only in dbt-agent:
  anthropic-docs-consultant, architecture-diagram-creator, autonomous-planning, context-graph-expert,
  dbt-knowledge-integrity-check, design-document-writer, explorer-ensemble, frontend-design, hypercontext, learner,
  pptx-powerpoint-generator, samwho-interactive-viz, session-search, skill-creator, synq-data-product-architect,
  synq-sla-monitor-designer, system-evolution-orchestrator, plus _archived

  3. Hooks live in two places — global (~30 TS/bash) and dbt-agent (20 Python). CAF has zero. A team member would get different
  behavior depending on which repo they open.

  4. Global layer is personal — the 80 global skills, 30 agents, and 12 rules in ~/.claude/ won't ship with the team tool.
  Anything essential for team workflows that lives there needs to be promoted into CAF.

  5. Knowledge split — rich reference content lives in both dbt-agent/shared/ and CAF knowledge/. Some is duplicated
  (canonical-models-registry, field-mappings), some is only in one place (partners/, PKO/ only in dbt-agent).

  ---
  Want me to produce a concrete reconciliation plan — what to consolidate, what to prune, what to promote — or do you want to
  discuss the target architecture first?

✻ Cooked for 32s
