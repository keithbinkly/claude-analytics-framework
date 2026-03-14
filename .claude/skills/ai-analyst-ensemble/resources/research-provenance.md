# Research Provenance: AI Analyst Ensemble

How each academic paper and practitioner article shaped the ensemble's design.
Updated: 2026-02-19 (Phase 7 implementation + Round 2 + Round 3 research sweeps + Implementation batches 1-6).

---

## Source Index

| # | Source | Type | Key Contribution |
|---|--------|------|------------------|
| 1 | Caitlin Sullivan, Lenny's Newsletter | Practitioner | Decision framing, evidence verification, actionability gate |
| 2 | DataNarrative (EMNLP 2024) | Academic | Critic agent architecture (73% quality loss without it) |
| 3 | MultiVis-Agent (SIGMOD 2026) | Academic | Causal language enforcement, logic rules, VE Agent pattern |
| 4 | ProactiveVA (arXiv 2507.18165) | Academic | Verification agent as separate role, claim classification inversion |
| 5 | IEEE VOICE + surveys | Academic | InsightBench 4-category rubric, RLHF misleading helpfulness |
| 6 | DAgent (PVLDB 2025) | Academic | Reverse-question validation, 3 quality criteria |
| 7 | awesome-data-agents (GitHub) | Survey | CHASE-SQL pairwise selection, Table-Critic curator pattern |
| 8 | Corr2Cause (arXiv 2406.12158) | Academic | GPT-4 near-random on causal inference (F1=29.08) |
| 9 | MAC-SQL (EMNLP 2023) | Academic | Context reduction gate, progressive anchoring, failure taxonomy |
| 10 | ReFoRCE (ICLR 2025 VerifAI) | Academic | Two-stage consensus, column exploration, content-convergence stopping |
| 11 | Alpha-SQL (ICML 2025) | Academic | MCTS for analytical reasoning, 7 typed actions, UCT exploration |
| 12 | SiriusBI (VLDB 2025) | Academic | Production BI guardrails, Data Preparation Agent, knowledge graph grounding |
| 13 | DataPuzzle (arXiv 2504.10036) | Academic | Representation-gated generation, six desiderata checklist |
| 14 | Insight Agents / Amazon (SIGIR 2025) | Academic | AE-based OOD gate (0.969 precision), 3-dimension rubric |
| 15 | DataSage (arXiv 2511.14299) | Academic | Negative Reasoning prompt, 4-criterion judge, iterative QA with history |
| 16 | Data Interpreter / MetaGPT (ACL 2025) | Academic | Two-code verification ACV (+17%), experience pool (78% debug reduction) |
| 17 | NAACL Insight Cluster (2503.11664 + 6 papers) | Academic | SMART goal (-34% without), domain detection (+28% novelty), QUIS statistical thresholds |

---

## Applied Changes (with provenance)

### 1. Critic Agent — 5th verification stage

**What changed:** Added `resources/critic-agent.md` and rewired the ensemble from
4 analysts → synthesizer to 4 analysts → **critic** → synthesizer. Updated SKILL.md
execution protocol (Steps 3-5) and `/analyze` command (Step 5.5).

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/resources/critic-agent.md` (NEW)
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (Steps 3-5, resources section)
- `.claude/commands/analyze.md` (Step 5.5)

**Sources:**

| Paper | What it said | How we used it |
|-------|-------------|----------------|
| **DataNarrative** (EMNLP 2024) | Removing the verification step caused 73% quality loss — highest single-component impact measured (Table 7, p.19260). Critic prompt structure: role separation, cross-match instruction, null case handling. | Directly adopted as the architectural justification for adding a 5th stage. The critic prompt structure (cross-match, specificity requirement, explicit null case) was adapted from Figs. 19/22/25 of the paper. |
| **ProactiveVA** (arXiv 2507.18165) | Semantic verification should be a separate agent, not part of the analyst's own reasoning. Issue taxonomy: factual error, internal conflict, task omission. | Confirmed that verification must be a separate role. The issue taxonomy influenced the critic's 5 verification dimensions. |
| **MultiVis-Agent** (SIGMOD 2026) | VE Agent provides dedicated verification with dual-layer evaluation. Separation from analysis agents is the architectural guarantee. | The VE Agent pattern directly maps to our critic — an agent that ONLY validates, never generates findings. Confirmed the "separation is the point" principle. |
| **Table-Critic** (ACL 2025, via awesome-data-agents) | 4-agent loop: Judge → Critic → Refiner → Curator. The Curator distills critique patterns into a reusable template tree. | Influenced the critic's structured output format (per-analyst reviews with typed issues). The Curator pattern is noted as P6 future work (self-evolving failure library). |
| **AutoTQA** (VLDB 2024, via awesome-data-agents) | 5-agent pipeline with Critic for task completion verification, gap identification, and re-execution routing. | Validated the "gap detection" role of the critic — checking whether analysts actually answered the original question (coverage gaps dimension). |

**Cross-paper consensus:** 6/6 deep-read papers confirmed that a separate verification stage is the highest-impact architectural addition. This was the clearest signal in the entire research sweep.

---

### 2. Causal Language Enforcement

**What changed:** Added shared constraint #11 (blocked phrases, allowed alternatives) to
SKILL.md. Added full causal language audit as dimension #2 of the critic agent prompt.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (Constraint #11)
- `.claude/skills/ai-analyst-ensemble/resources/critic-agent.md` (Dimension #2)

**Sources:**

| Paper | What it said | How we used it |
|-------|-------------|----------------|
| **Corr2Cause** (arXiv 2406.12158) | GPT-4 achieves F1=29.08 on causal inference vs F1=20.38 random baseline — barely better than chance. LLMs are "causal parrots" relying on position heuristics. | This is the statistical justification for treating causal language as a structural problem, not a prompting problem. We blocked causal verbs ("driven by", "caused by", "due to", etc.) rather than asking analysts to "be careful." |
| **MultiVis-Agent** (SIGMOD 2026) | "Causal language is the highest-priority guardrail: LLMs at all scales fail causal inference at near-random rates." System prompt should specify: directional pattern / associated factor / hypothesized cause. | Directly adopted the tri-level causal strength classification. Influenced the blocked/allowed phrases in constraint #11 and the critic's causal language dimension. |
| **DataNarrative** (EMNLP 2024) | The paper does NOT address causal language — "highlight any causal relationships... that emerge from the data" — this is a notable absence of a guardrail. Explicitly identified as the paper's gap. | DataNarrative's gap in causal language handling is what made us fill it ourselves. Their ecological fallacy example (Trump approval scope extension) further motivated the scope check dimension. |
| **IEEE VOICE surveys** (arXiv 2510.04023) | "LLMs' tuning for helpfulness can result in computed data that is incredibly misleading" — RLHF teaches models to omit caveats because hedging reads as uncertainty. | Explains WHY the ecological fallacy slipped through in our Test 3 — the model was trained to sound confident. Causal language enforcement is structural compensation for RLHF bias. |

---

### 3. Decision Framing (threaded through all analysts)

**What changed:** Added mandatory decision framing to SKILL.md Step 1 and the `/analyze`
command Step 1. All analyst prompts now receive: what decision, who decides, what changes action.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (Step 1)
- `.claude/commands/analyze.md` (Step 1, analyst dispatch template)

**Sources:**

| Paper | What it said | How we used it |
|-------|-------------|----------------|
| **Caitlin Sullivan** (Lenny's Newsletter) | Context loading formula: (1) what does the company do, (2) what problem are we solving, (3) what data do we have, (4) what format does the decision-maker need. Without context, every analysis produces generic insights. | Adapted her 4-component formula into 3 decision-framing questions. The "what format" component maps to our existing output schema rather than a new field. |
| **DataNarrative** (EMNLP 2024) | "Intention anchor" threaded through every pipeline stage. Every prompt from Outline onward includes the user's intention/theme. Prevents narrative drift. | The intention-threading pattern was the implementation model. We thread the decision frame into all analyst prompts and the critic, exactly as DataNarrative threads the intention. |

---

### 4. Evidence Verification (Constraint #9)

**What changed:** Added shared constraint #9 requiring VERIFIED/PARAPHRASED/NOT_FOUND
classification for every data point cited. NOT_FOUND = delete the finding.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (Constraint #9)
- `.claude/skills/ai-analyst-ensemble/resources/critic-agent.md` (Dimension #1: Citation Verification)

**Sources:**

| Paper | What it said | How we used it |
|-------|-------------|----------------|
| **Caitlin Sullivan** (Lenny's Newsletter) | "Quote verification" pattern: every quote attributed to a source must be checked as VERIFIED (exact match), PARAPHRASED (accurate gist), or NOT FOUND (fabricated). "The LLM will confidently cite things people never said." | Directly adapted from quotes to data citations. Every number in a finding must trace to a specific query result, not LLM memory. |
| **ProactiveVA** (arXiv 2507.18165) | Semantic verification: "compare the note content with the system's data. If data facts are inconsistent, the user should be reminded." Every finding cites retrieved evidence. | Reinforced the structural requirement: findings must cite their data source. The "untraceable LLM explanations" failure mode = our unverified citations anti-pattern. |
| **Self-RAG** (ICLR 2024, via awesome-data-agents) | Per-segment citation with self-assessed support scores. Reflection tokens encode whether output is supported by retrieved evidence. | The reflection token pattern (mark each claim with its source) is implementable via our structured output schema. Each finding now has `evidence_status` and `queries_used`. |
| **ReportGPT** (EMNLP Industry 2024, via awesome-data-agents) | DSL expressions as "proof mechanisms" for table commentary. Users scan DSL proofs to verify factuality without reading full text. | Influenced the structured citation format (`tool: ..., input: ..., result_summary: ...`) in the output schema — machine-readable evidence trace. |

---

### 5. Actionability Gate (Constraint #10)

**What changed:** Added shared constraint #10: "If a business manager reads this, what would
they do differently?" If the answer is "nothing," the finding is noise.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (Constraint #10)
- `.claude/skills/ai-analyst-ensemble/resources/critic-agent.md` (Dimension #5: Banality Filter)

**Sources:**

| Paper | What it said | How we used it |
|-------|-------------|----------------|
| **Caitlin Sullivan** (Lenny's Newsletter) | The 4th failure mode: "Signal That Doesn't Guide Decisions." An insight can be true, novel, and data-grounded — but if no one would change their behavior based on it, it's noise. | Directly adopted as constraint #10. The formulation "what would they do differently?" is Caitlin's test. |
| **NAACL 2025 insight generation** (via MultiVis-Agent report) | Correctness + Insightfulness are necessary but not sufficient. The paper acknowledges actionability as an open gap — "even correct + insightful insights may not be actionable." | Confirmed that actionability requires a separate check (not derivable from correctness or novelty). We implemented it as a constraint rather than leaving it as a gap. |
| **DAgent** (PVLDB 2025) | Three quality criteria: completeness, correctness, conciseness. But no actionability criterion. | DAgent's "conciseness" (avoid redundant information) maps to our banality filter. But conciseness != actionability — you can be concise and still banal. |

---

### 6. InsightBench Category Tagging

**What changed:** Critic agent tags each finding as Descriptive, Diagnostic, Predictive, or
Prescriptive — with Diagnostic flagged as highest risk for causal language violations.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/resources/critic-agent.md` (Dimension #4: Insight Category + Risk Tagging)

**Sources:**

| Paper | What it said | How we used it |
|-------|-------------|----------------|
| **InsightBench/AgentPoirot** (ICLR 2025, via IEEE VOICE survey) | Four analytics categories requiring progressively higher-order reasoning: Descriptive → Diagnostic → Predictive → Prescriptive. Diagnostic = "why did it happen?" = highest hallucination risk. | Directly adopted as the category tagging system. Diagnostic claims get extra scrutiny (mandatory causal language audit) because that's where LLMs most often fabricate explanations. |
| **MultiVis-Agent** (SIGMOD 2026) | CR-Rule 1: Deterministic task classification before routing. "Classify the request type before routing to analysts" using rules, not LLM judgment. | Confirmed that classification should gate the verification intensity — Descriptive claims need citation checks, Diagnostic claims need causal language + citation + scope checks. |

---

### 7. OBSERVED/INFERRED/SPECULATIVE Claim Classification

**What changed:** Updated SKILL.md constraint #6 with the tri-level claim classification,
evidence-level-appropriate language rules, and the ecological fallacy warning. Updated output
schema with `claim_type` field.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (Constraint #6, output schema)

**Sources:**

| Paper | What it said | How we used it |
|-------|-------------|----------------|
| **ProactiveVA** (arXiv 2507.18165) | Invert the claim classification order: declare claim type BEFORE writing the interpretation, not after. "Before writing your interpretation, state whether this is OBSERVED, INFERRED, or SPECULATIVE." | The output schema now requires `claim_type` as the first field of each finding, before the evidence and interpretation. Classification gates the narrative. |
| **DataNarrative** (EMNLP 2024) | Structural separation: Reflection stage = observations, Outline/Narration = inferences. The pipeline architecture enforces the observation/inference boundary. | While we don't have a separate Reflection stage (P3 future work), the claim classification serves as an inline proxy — forcing analysts to mark what's observation vs. interpretation within their output. |
| **MultiVis-Agent** (SIGMOD 2026) | `causal_strength: "directional_pattern | associated_factor | hypothesized_cause"` with `mechanism: "stated or null"`. | The SPECULATIVE level maps to "hypothesized_cause with no mechanism." The INFERRED level maps to "associated_factor." OBSERVED maps to "directional_pattern." |

---

### 8. Synthesizer Updates (Critic Integration)

**What changed:** Rewrote `resources/synthesizer.md` to consume the critic's verification
report first, apply block/warn/info severity flags, and include a "Verification Summary"
section in output.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/resources/synthesizer.md` (full rewrite)

**Sources:**

| Paper | What it said | How we used it |
|-------|-------------|----------------|
| **DataNarrative** (EMNLP 2024) | The Critic produces revision plans; the Generator applies them. The Critic never generates content — it only flags and suggests. | Our synthesizer reads the critic report FIRST, then applies its flags. Block = remove, Warn = revise, Info = note. The critic never writes the final answer. |
| **CHASE-SQL** (ICLR 2025, via awesome-data-agents) | Self-consistency (majority voting among multiple outputs) leaves a 14% performance gap. Pairwise comparison by a dedicated selection agent outperforms. | Our synthesizer doesn't average or vote across analysts. It evaluates disagreements explicitly, uses the critic's contradiction analysis, and presents both sides when unresolvable. |
| **ChartInsighter** (IEEE TVCG 2025, via awesome-data-agents) | Self-consistency test phase after multi-agent generation. Check where claims contradict each other or contradict the underlying data. | The synthesizer's cross-analyst consistency check (using the critic's contradiction flags) is the ChartInsighter pattern applied to text analysis. |

---

### 9. Napkin Anti-Patterns

**What changed:** Added 2 new anti-patterns to Analytics Manager napkin.md.

**Files modified:**
- `.claude/agent-memory/analytics-manager/napkin.md`

| Anti-Pattern | Source |
|-------------|--------|
| Generic/Banal Insights | Caitlin Sullivan (actionability test) |
| Unverified Data Citations | Caitlin Sullivan (quote verification) + ProactiveVA (untraceable explanations) |

---

### 10. Round 3 Research Batch — 6 Improvements (2026-02-19)

**What changed:** Applied 6 research-backed improvements from Round 3 academic sweep (20+ papers across 3 rounds). All 6 have ablation evidence.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (Step 1 rewrite + 3 new shared constraints #12-14)
- `.claude/commands/analyze.md` (Step 1 rewrite + analyst dispatch template update in Step 4)
- `.claude/skills/ai-analyst-ensemble/resources/critic-agent.md` (Dimension #4 expanded, coverage audit + output section added)

| Change | Backlog ID | Source | Evidence | Where |
|--------|-----------|--------|----------|-------|
| Domain detection priming | P23 | Data-to-Dashboard (NAACL cluster) | +28% novelty, +31% depth | SKILL.md Step 1, analyze.md Step 1 |
| SMART goal constraint | P24 | AgentPoirot / InsightBench (ICLR 2025) | -34% quality without it | SKILL.md Step 1, analyze.md Step 1 |
| Negative Reasoning prompt | P19 | DataSage (InsightBench +7.5%) | Complementary CoT strategy | SKILL.md constraint #12 |
| Representation-gated generation | P16 | DataPuzzle | Completeness improvement | SKILL.md constraint #13 |
| QUIS statistical pre-filters | P25 | QUIS (EMNLP 2024, IBM) | Mann-Kendall, 1.4x, 50%, JS≥0.2 | SKILL.md constraint #14 |
| 6-type coverage taxonomy | P26 | InsightBench + InsightEval | 4→6 types + coverage audit | critic-agent.md Dimension #4 |

---

### 11. Implementation Batch 2 — 3 Improvements (2026-02-19)

**What changed:** Applied 3 more research-backed improvements — 2 new shared constraints + synthesizer selection criteria.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (2 new shared constraints #15-16)
- `.claude/commands/analyze.md` (updated constraint reference #1-16, analyst dispatch reminder)
- `.claude/skills/ai-analyst-ensemble/resources/synthesizer.md` (new INSIGHT SELECTION CRITERIA section)

| Change | Backlog ID | Source | Evidence | Where |
|--------|-----------|--------|----------|-------|
| Observation-before-interpretation | P2 | DataNarrative (EMNLP 2024) | 64% quality loss without reflection stage | SKILL.md constraint #15 |
| Progressive anchoring | P14 | MAC-SQL + Alpha-SQL + SiriusBI | -3.85pts without (largest single-agent contribution) | SKILL.md constraint #16 |
| 4-criterion judge selection | P20 | DataSage | Higher diversity + coverage scores | synthesizer.md INSIGHT SELECTION CRITERIA |

---

### 12. Implementation Batch 3 — 3 Improvements (2026-02-19)

**What changed:** Applied 3 more research-backed improvements — 1 new shared constraint + synthesizer confidence scoring (merging 2 backlog items).

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (1 new shared constraint #17)
- `.claude/commands/analyze.md` (updated constraint reference #1-17)
- `.claude/skills/ai-analyst-ensemble/resources/synthesizer.md` (new CONFIDENCE SCORING section)

| Change | Backlog ID | Source | Evidence | Where |
|--------|-----------|--------|----------|-------|
| Execute-before-claim | P9 | ReFoRCE + Alpha-SQL + QUIS (3 papers) | Column exploration prevents referencing unverified values | SKILL.md constraint #17 |
| Confidence via analyst agreement | P5 | MultiVis-Agent + ICLR 2025 + InsightLens | LLMs cannot self-report confidence; use structural agreement | synthesizer.md CONFIDENCE SCORING |
| InsightLens scoring formula | P29 | InsightLens (arXiv 2404.01644) | Sfinal = (Ssem × 0.6) + (Sstat × 0.4) outperforms pure scoring | Merged into P5 implementation |

---

### 13. Implementation Batch 4 — 3 Improvements (2026-02-19)

**What changed:** Strengthened the critic→synthesizer pipeline with formalized scoring, quantitative consensus, and drift detection.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/resources/critic-agent.md` (new Dimension #5: Quantitative Quality Scoring, 5→6 dimensions)
- `.claude/skills/ai-analyst-ensemble/resources/synthesizer.md` (TWO-STAGE CONSENSUS replacing CONSENSUS WEIGHTING, REVERSE-QUESTION VALIDATION section)
- `.claude/commands/analyze.md` (updated critic dispatch: 5→6 dimensions)

| Change | Backlog ID | Source | Evidence | Where |
|--------|-----------|--------|----------|-------|
| 3-Dimension Insight Rubric | P18 | Insight Agents / Amazon (SIGIR 2025) | 89.5% question-level accuracy in production, 0.8 threshold | critic-agent.md Dimension #5 |
| Two-Stage Consensus | P10 | ReFoRCE + Alpha-SQL | +32% vs SOTA (ReFoRCE), +14% vs self-consistency (Alpha-SQL) | synthesizer.md TWO-STAGE CONSENSUS |
| Reverse-Question Validation | P7 | DAgent (PVLDB 2025) | Drift detection that forward-only verification misses | synthesizer.md REVERSE-QUESTION VALIDATION |

---

### 14. Implementation Batch 5 — 1 Improvement (2026-02-19)

**What changed:** Added the last prompt-level constraint — question-first planning to prevent confirmatory analysis.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (new shared constraint #18)
- `.claude/commands/analyze.md` (updated constraint reference #1-18)

| Change | Backlog ID | Source | Evidence | Where |
|--------|-----------|--------|----------|-------|
| Question-first planning | P3 | NAACL 2025 + DataSage | Hypothesis-first pipeline improves insight quality; divergent→convergent = higher diversity | SKILL.md constraint #18 |

---

### 15. Implementation Batch 6 — 5 Structural Improvements (2026-02-19)

**What changed:** Shifted from prompt-level constraints to structural/workflow improvements. Added data sufficiency pre-check, difficulty-gated routing, self-evolving failure library, knowledge graph validation, and iterative follow-up rounds.

**Files modified:**
- `.claude/skills/ai-analyst-ensemble/SKILL.md` (new shared constraint #19, failure_library resource, provenance description update)
- `.claude/commands/analyze.md` (Step 0 rewrite with 3-tier routing, constraint refs #1-19, Step 5.5 failure library loading, Step 8.5 failure library writeback, Step 9 iterative follow-up)
- `.claude/skills/ai-analyst-ensemble/resources/failure-library.yaml` (NEW — self-evolving error pattern library)

| Change | Backlog ID | Source | Evidence | Where |
|--------|-----------|--------|----------|-------|
| Data Sufficiency Check | P12 | SiriusBI + ReFoRCE | Data Prep Agent fires mid-analysis when insufficient; Column Exploration validates pre-analysis | SKILL.md constraint #19 |
| Difficulty-Gated Routing | P13 | MAC-SQL + SiriusBI + Insight Agents | BERT router 0.83 acc vs LLM 0.60; simple→direct, complex→decompose | analyze.md Step 0 |
| Self-Evolving Failure Library | P6 | Table-Critic (ACL 2025) | Curator agent distills critique patterns into reusable template tree | failure-library.yaml + analyze.md Steps 5.5/8.5 |
| Knowledge Graph Validation | P15 | SiriusBI | -23-27% accuracy without knowledge management module | Pre-existing (constraint #1) — marked applied |
| Iterative QA with History | P27 | DataSage + QUIS | 6 questions with history > 12 without for diversity/coverage | analyze.md Step 9 |

---

## Extracted But Not Yet Implemented (Remaining Backlog)

These ideas were extracted from papers but not implemented in Phase 7. Captured here for
future phases.

### P2: Observation-Before-Interpretation (Reflection Stage) ✅ APPLIED
**Source:** DataNarrative (Figs. 18-26) — "Reflection" as mandatory data-reading step.
**Applied:** 2026-02-19. Added as shared constraint #15 in SKILL.md. Analysts produce bullet-point observations before any interpretive narrative.

Removing the Reflection stage caused 64% loss rate — the largest single-stage ablation
result in DataNarrative's pipeline.

### P3: Question-First Planning (Hypothesis Generator) ✅ APPLIED
**Source:** NAACL 2025 insight generation paper (via MultiVis-Agent report) +
DataSage divergent-convergent debate.
**Applied:** 2026-02-19. Added as shared constraint #18 in SKILL.md. Analysts articulate 3-5 specific questions linked to SMART goal before any querying. Prevents confirmatory analysis.

### P4: Structured Citation Format
**Source:** ReportGPT DSL proofs + Self-RAG reflection tokens + Chain-of-Table
transformation chains.

**What it would do:** Require analysts to express evidence in machine-readable format
(metric + value + segment + period) rather than prose citations. Enables automated
citation verification.

**Implementation:** Already partially implemented in the output schema (`queries_used`
field). Full implementation would validate citations programmatically.

### P5: Confidence via Analyst Agreement (Semantic Entropy) ✅ APPLIED
**Source:** MultiVis-Agent + ICLR 2025 "Do LLMs Estimate Uncertainty Well?" + InsightLens.
**Applied:** 2026-02-19. Added CONFIDENCE SCORING section to synthesizer.md. Sfinal = (Ssem × 0.6) + (Sstat × 0.4) with thresholds. Confidence derived from analyst agreement, not self-reports.

### P6: Self-Evolving Failure Library (Table-Critic Curator Pattern) ✅ APPLIED
**Source:** Table-Critic (ACL 2025) — Curator agent distills critique patterns into a
reusable template tree that guides future error detection.
**Applied:** 2026-02-19. Created `resources/failure-library.yaml` (max 50 entries, frequency-tracked). Wired into `/analyze`: Step 5.5 loads library into critic prompt as KNOWN ERROR PATTERNS, Step 8.5 writes back block/warn issues with deduplication.

### P7: Reverse-Question Validation ✅ APPLIED
**Source:** DAgent (PVLDB 2025, Section 6.1.3) — generate questions from the report,
check semantic similarity to the original query. Low similarity = drift/hallucination.
**Applied:** 2026-02-19. Added REVERSE-QUESTION VALIDATION section to synthesizer.md. Post-synthesis self-check: generate 3-5 questions the output answers, compare to original, flag drift.

---

## Round 2 Research (2026-02-19): Data Analysis Techniques for Agents

Round 2 broadened the research scope from "verification and critique" to the full analytical
lifecycle: exploring data, establishing benchmarks, identifying trends/anomalies/variation,
finding drivers, understanding user intent, and presenting to humans.

4 papers deep-read: MAC-SQL, ReFoRCE, Alpha-SQL, SiriusBI.

### P8: Scoper Agent (Context Reduction Gate)
**Sources:** MAC-SQL (Selector agent), ReFoRCE (schema compression 50MB→manageable),
SiriusBI (I(Q) = 0/1/2 classification gate).

Three independent systems converge on the same pattern: before an analytical agent sees
the data, a dedicated scoping agent strips irrelevant context. MAC-SQL's Selector retains
only "pertinent table and column name information." ReFoRCE compresses 1,000+ column schemas
via pattern-based grouping. SiriusBI refuses to proceed until both metric AND dimension
are specified (I(Q) ≥ 2).

**What it would do:** Add a Scoper step (new Step 1.7) that returns
`{relevant_dimensions, time_range, granularity, question_restatement}`. Analysts receive
this scope object plus the original question, not the full data catalog.

**Implementation:** Step 1.7 between partner context loading and MCP tool verification.
Could be a lightweight agent or a structured prompt.

### P9: Execute-Before-Claim Protocol ✅ APPLIED
**Sources:** ReFoRCE (Column Exploration — `SELECT DISTINCT` before referencing values),
Alpha-SQL (Column Value Identification as explicit action type), QUIS (schema-only hypothesis).
**Applied:** 2026-02-19. Added as shared constraint #17 in SKILL.md. Analysts must verify dimension values exist via discovery query before referencing them in claims.

ReFoRCE's key insight: "The agent cannot reference a column value it hasn't verified via
execution." Before writing any main query, ReFoRCE runs 10+ `SELECT DISTINCT` queries
(capped at 100 rows/5KB each) and injects actual sample data into the prompt. Alpha-SQL
codifies this as one of 7 typed action types — it's not a pre-step, it's an explicit
reasoning move within the analytical process. QUIS adds: "form hypotheses from schema, not data."

### P10: Two-Stage Consensus (Structural → LLM) ✅ APPLIED
**Sources:** ReFoRCE (programmatic equality check → LLM tiebreaker), Alpha-SQL
(cross-attempt agreement scoring feeds tree search, not just final selection).
**Applied:** 2026-02-19. Replaced CONSENSUS WEIGHTING with TWO-STAGE CONSENSUS in synthesizer.md. Stage 1: numerical check (±1% match = NUMERICALLY VERIFIED). Stage 2: qualitative consensus (4/4, 3/4, 2/2, all differ).

Both systems beat self-consistency voting. ReFoRCE: 31.26 vs 23.58 SOTA on Spider 2.0
(+32%). Alpha-SQL: beats self-consistency by 14%.

### P11: Typed Analytical Actions
**Sources:** Alpha-SQL (7 action types: rephrase, select, filter, aggregate, generate,
revise, terminate), MAC-SQL (difficulty-gated routing: simple → direct, complex → decompose).

Alpha-SQL: "Don't ask an LLM to 'analyze this data' in one shot. Force it through typed
reasoning moves with explicit state transitions." MAC-SQL: "dynamically judging the
difficulty of the user's question — if simple, generate directly; if complex, decompose
starting from the simplest sub-problem."

The analytical equivalent of Alpha-SQL's 7 actions:
1. Clarify the question (rephrase)
2. Identify relevant metrics/dimensions (select)
3. Determine filters/segments/cohorts (filter)
4. Choose aggregation/statistical treatment (aggregate)
5. Generate the analytical claim (generate)
6. Revise based on critic feedback (revise)
7. Determine when analysis is sufficient (terminate)

**What it would do:** Restructure analyst prompts to follow explicit typed moves rather
than free-form analysis. Each move gets its own verification opportunity.

**Implementation:** Update analyst resource files. Would require significant prompt
restructuring — treat as a major version change.

### P12: Data Preparation as First-Class Agent Role ✅ APPLIED
**Sources:** SiriusBI (dedicated Data Preparation Agent), ReFoRCE (Column Exploration
phase as pre-analysis data validation).
**Applied:** 2026-02-19. Added as shared constraint #19 (DATA SUFFICIENCY CHECK) in SKILL.md. Analysts verify grain, time range, and dimensional coverage before generating any finding. Constraint approach chosen over separate agent for v1.

### P13: Difficulty-Gated Routing ✅ APPLIED
**Sources:** MAC-SQL (simple→direct generation, complex→progressive decomposition),
SiriusBI (descriptive→single-hop SQL, diagnostic→multi-agent orchestration),
Insight Agents (BERT router 0.83 accuracy vs LLM router 0.60).
**Applied:** 2026-02-19. Added automatic 3-tier difficulty classification (LOOKUP/FOCUSED/DIAGNOSTIC) to analyze.md Step 0. LOOKUP routes to ai-analyst-profile, FOCUSED runs 1-2 analysts, DIAGNOSTIC runs full ensemble. Builds on existing Quick Mode flags.

### P14: Progressive Anchoring (Baseline → Deviation → Driver) ✅ APPLIED
**Sources:** MAC-SQL, Alpha-SQL, SiriusBI (3 papers converge).
**Applied:** 2026-02-19. Added as shared constraint #16 in SKILL.md. 4-step sequence: baseline → deviation → co-occurrence → mechanism.

MAC-SQL's ablation: removing progressive decomposition costs 3.85 points (largest
single-agent contribution in their multi-agent system).

### P15: Knowledge Graph as Primary Guardrail ✅ APPLIED (pre-existing)
**Source:** SiriusBI (removing knowledge management module → -23-27% accuracy).
**Applied:** Pre-existing. Our shared constraint #1 (dbt MCP Semantic Layer API only for certified metrics) IS the knowledge graph pattern. SiriusBI's ablation (-23-27% accuracy without it) validates this as the primary quality driver.

SiriusBI's knowledge graph has 6 node types: databases, tables, columns, values, UDFs,
terms/aliases. Our semantic layer (dbt metrics + dimensions) maps directly to this pattern.
Constraint #1 + MCP tool gating = knowledge graph grounding.

---

## Round 3 Research (2026-02-19): Empirically Proven Agent Patterns

Round 3 shifted focus per user directive: "we're hoping for *effective/proven agent patterns*
to accomplish high quality data analysis & insights. We want to learn what they learned from
their experimentation." Emphasis on ablation evidence and quantified impact.

5 papers/clusters deep-read: DataPuzzle, Insight Agents (Amazon), DataSage, Data Interpreter, NAACL Insight Generation cluster (8 papers).

### P16: Representation-Gated Generation ✅ APPLIED
**Sources:** DataPuzzle (core concept), NAACL cluster (implementation evidence).
**Applied:** 2026-02-19. Added as shared constraint #13 in SKILL.md. Analysts must produce evidence table before narrative.

Before each analyst writes a narrative conclusion, require them to produce a **structured
evidence table** (columns: metric, value, segment, time period, source, direction). The
narrative can only reference what is in the table. This gates generation upstream — the table
is inspectable by the critic before the narrative is even requested.

**Structure-type selection per question type:**
- Comparisons → tables
- Causal/diagnostic → directed graphs / chain-of-causation lists
- Trend questions → time-ordered sequences

**What it would do:** Force an intermediate representation between data retrieval and narrative.
Makes each claim's evidence base explicit and machine-readable.

**Implementation:** Update analyst resource files to require a structured evidence artifact
before narrative generation. Strengthens P4 (Structured Citation Format).

### P17: AE-Based OOD Gate
**Source:** Insight Agents / Amazon (SIGIR 2025, production deployment).

Auto-encoder trained on in-domain question embeddings detects out-of-scope queries before
any analyst fires. Threshold: `μ_id + λ * σ_id` of reconstruction loss.

**Ablation evidence:** AE precision 0.969 vs LLM few-shot 0.616 (+57%). Latency 0.009s vs
1.665s (185x faster). Training data: only 301 questions needed.

**Design bias:** High precision over recall — better to let an OOD query through than block
a valid one.

**What it would do:** Pre-computation scope check saving 4 analyst + 1 critic token spend
on out-of-scope questions.

**Implementation:** New Step 0 before any analyst dispatch. Requires a training set of
150-200 valid analytical questions for our domain.

### P18: 3-Dimension Insight Rubric (Formalized Critic Scoring) ✅ APPLIED
**Source:** Insight Agents / Amazon (89.5% question-level accuracy in production).
**Applied:** 2026-02-19. Added as critic-agent.md Dimension #5 (Quantitative Quality Scoring). Three keyword-ratio scores (relevance, correctness, completeness) with 0.8 threshold. Critic now has 6 dimensions total.

Three dimensions with keyword-ratio formulas:
- **Relevance:** `#question_keywords_in_response / total_question_keywords`
- **Correctness:** `#correct_insights / total_insights`
- **Completeness:** `#required_insights / total_required_insights`

**Threshold:** ALL THREE must exceed 0.8 for a finding to pass.

### P19: Negative Reasoning Prompt Pattern ✅ APPLIED
**Source:** DataSage (+7.5% insight, +13.9% summary over AgentPoirot on InsightBench).
**Applied:** 2026-02-19. Added as shared constraint #12 in SKILL.md. Analysts enumerate 3-5 calculation risks before code.

Before generating analytical code, explicitly enumerate 3-5 plausible calculation mistakes:
double-counting, incorrect joins, NULL handling, date boundary errors, fan-out from
one-to-many joins. Then generate code defensively.

One of 3 parallel CoT strategies tested — all complementary, no single strategy dominates.

**What it would do:** Add a pre-generation defensive reasoning step. Analysts enumerate
risks before executing.

**Implementation:** Add to shared constraints or as a variant analyst prompt. Low cost,
high impact.

### P20: 4-Criterion Judge Selection ✅ APPLIED
**Source:** DataSage (global judge sees ALL analyst output simultaneously).
**Applied:** 2026-02-19. Added INSIGHT SELECTION CRITERIA section to synthesizer.md. 4 criteria: non-trivial, aligned, diverse, complementary.

Selection criteria for which insights survive to synthesis:
1. **Non-trivial / surprising** — screens against obvious/expected findings
2. **Aligned with data + analysis goal** — feasibility filter
3. **Diverse across question types** — prevents thematic clustering
4. **Complementary with already-answered questions** — avoids redundancy with history

DataSage: These criteria produced "significantly higher diversity and coverage scores."

### P21: Two-Code Verification (ACV)
**Source:** Data Interpreter / MetaGPT (ACL Findings 2025).

After executing analysis code, generate a **second independent validation code block** that
tests the result programmatically. Score: True=1.0, False=0.2, Exception=0.5.

**Ablation evidence:** +17.29% average improvement across all task categories vs version
without ACV. +26% vs AutoGen.

**What it would do:** Add executable verification alongside text-based critic verification.
Each analyst claim gets independent code-level validation.

**Implementation:** New validation sub-step within the critic stage. For MCP-based queries:
run the same question through an alternative query path and compare results.

### P22: Experience Pool (Failures + Successes)
**Source:** Data Interpreter (ACL Findings 2025).

Archive every analyst execution (claim + code + result + confidence). Both successes AND
failures stored. Top-k retrieval by task similarity informs future runs.

**Ablation evidence:** Pool size 0→200 reduced debugging attempts from 1.48 to 0.32 per
task (**78% reduction**), costs from $0.80 to $0.24.

**Key insight:** 200 items is the meaningful threshold, not thousands. Failures are as
valuable as successes for learning.

**What it would do:** Build institutional memory for the ensemble. Past analyses inform
future ones.

**Implementation:** Maps to our existing `shared/learnings/` and experience store
infrastructure. The delta is adding per-question code-level retrieval and explicitly
storing failure cases.

### P23: Domain Detection Priming ✅ APPLIED
**Source:** NAACL cluster / Data-to-Dashboard (arXiv 2505.23695).
**Applied:** 2026-02-19. Added to Step 1 in SKILL.md and analyze.md. "Name the business domain" before dispatch.

One LLM call before analysis: "Name the business domain of this dataset." This primes all
subsequent analysis by triggering the LLM's implicit domain knowledge frame.

**Ablation evidence:** +28% novelty and +31% depth improvement vs GPT-4o baseline.
Multi-agent architecture was the causal factor.

**What it would do:** Zero-cost intervention. Add "name the domain" to Step 1 before
analyst dispatch.

**Implementation:** One additional line in the analyst dispatch template.

### P24: SMART Goal Constraint ✅ APPLIED
**Source:** NAACL cluster / InsightBench AgentPoirot (ICLR 2025).
**Applied:** 2026-02-19. Added SMART reframing to Step 1 in SKILL.md and analyze.md. Question rewritten as S/M/A/R/T before dispatch.

Reformulate vague "analyze this" inputs into Specific/Measurable/Attainable/Relevant/Timely
goal statements before analyst dispatch.

**Ablation evidence:** Removing SMART goal drops LLaMA-3-Eval from 0.59→0.39 for GPT-4o
(**34% degradation**). The strongest single ablation result in the cluster.

**What it would do:** Strengthen Step 1 (decision framing). Currently we ask "what decision?"
— SMART adds measurability and time-boundedness.

**Implementation:** Update Step 1 in SKILL.md and analyze.md. Strengthens existing
decision framing with explicit measurability requirements.

### P25: QUIS Statistical Pre-Filters ✅ APPLIED
**Source:** NAACL cluster / QUIS (EMNLP 2024, IBM Research).
**Applied:** 2026-02-19. Added as shared constraint #14 in SKILL.md. Trend/outstanding/attribution/distribution thresholds + triviality filter.

Pattern-specific significance thresholds BEFORE LLM narrative generation:

| Pattern | Test / Threshold |
|---------|-----------------|
| Trend | Mann-Kendall test, p < 0.05 |
| Outstanding value | Ratio ≥ 1.4 between largest values |
| Attribution | ≥ 50% contribution threshold |
| Distribution shift | Jensen-Shannon divergence ≥ 0.2 |

Plus triviality filter: questions returning single-row results are discarded.

**What it would do:** Prevent LLMs from narrating noise. Statistical pre-filter before
any narrative is generated.

**Implementation:** New shared constraint or analyst-internal check. Requires pattern
classification before applying appropriate threshold. Strengthens the existing banality
filter (constraint #10) with statistical backing.

### P26: 6-Type Coverage Taxonomy ✅ APPLIED
**Source:** NAACL cluster / InsightBench (ICLR 2025) + InsightEval (2025).
**Applied:** 2026-02-19. Updated critic-agent.md Dimension #4 from 4→6 types (added Evaluative + Exploratory). Added coverage audit + insight_type_coverage output section.

Extends the existing 4-category InsightBench rubric with 2 new types:

1. Descriptive (41%) — what happened
2. Diagnostic (36%) — why it happened
3. Predictive (14%) — what will happen
4. Prescriptive (9%) — what to do about it
5. **Evaluative** (NEW) — did the intervention work?
6. **Exploratory** (NEW) — open-ended pattern surfacing

The Evaluative type is the most underrepresented — "was the goal achieved?" closes the
loop on prior recommendations.

**InsightLens evidence:** Users explored 12.4 vs 9.3 attributes (p=0.006) and 6.5 vs 5.3
topics (p=0.03) when given explicit coverage tracking.

**What it would do:** Update the critic's category tagging from 4 to 6 types. Add coverage
audit: after all analysts run, check which types are missing.

**Implementation:** Update critic-agent.md category tagging. Add coverage check to
synthesizer.

### P27: Iterative QA with History ✅ APPLIED
**Source:** DataSage (iterative QA loop), NAACL cluster / QUIS (iterative bootstrapping).
**Applied:** 2026-02-19. Added Step 9 to analyze.md — optional follow-up rounds where analysts build on prior synthesis. Max 2 follow-up rounds (3 total). Prior findings injected as PRIOR FINDINGS context, analysts blocked from rediscovery. Cumulative history across rounds.

**DataSage evidence:** 6 questions (vs AgentPoirot's 12) achieved "significantly higher
diversity and coverage scores" — quality over quantity via history-aware generation.

**What it would do:** Enable multi-round analysis where each round gets progressively
deeper. Analysts are blocked from re-asking what is already answered.

**Implementation:** Post-synthesis, optional follow-up round. Pass synthesis output as
"prior knowledge" into a second analyst dispatch.

### P28: Fork-and-Regenerate Replanning
**Source:** Data Interpreter (ACL Findings 2025).

When consensus fails, identify the fork point via topological sort + prefix matching.
Preserve completed sub-analyses before the fork. Only regenerate for the disputed
sub-question.

**What it would do:** Efficient recovery from analyst disagreement without full re-run.

**Implementation:** Post-critic, when contradictions are detected. Preserve agreed-upon
findings, re-dispatch only for contested claims with enriched context.

### P29: InsightLens Scoring Formula ✅ APPLIED (merged into P5)
**Source:** NAACL cluster / InsightLens (arXiv 2404.01644).
**Applied:** 2026-02-19. The Sfinal formula was implemented as part of P5's CONFIDENCE SCORING section in synthesizer.md.

`Sfinal = (Ssem × 0.6) + (Sstat × 0.4)`
- Ssem = semantic significance (1-5, business relevance via LLM)
- Sstat = statistical significance (1-5, computed from pattern thresholds)

The 60/40 weighting explicitly deprioritizes statistical extremity in favor of business
meaning. A statistically extreme outlier with no semantic context scores lower than a
moderate finding with clear business implications.

**What it would do:** Formalize the banality filter with a composite score.

**Implementation:** Integrate with P18 (rubric) and P25 (statistical pre-filters) for a
complete scoring pipeline.

---

## Cross-Paper Convergence Map

Ideas that appeared in 3+ papers independently have the highest implementation confidence.

| Idea | Papers | Convergence |
|------|--------|-------------|
| Separate verification agent | DataNarrative, ProactiveVA, MultiVis-Agent, Table-Critic, AutoTQA, Caitlin Sullivan, **Data Interpreter (ACV)** | **7 sources** — strongest signal. R3 adds executable verification (not just text-based). |
| Context reduction before analysis | MAC-SQL (Selector), ReFoRCE (schema compression), SiriusBI (I(Q) gate), **Insight Agents (OOD gate)** | **4 sources** — R3 adds production-deployed AE gate (0.009s, 0.969 precision) |
| Execute before claim (data verification) | ReFoRCE (Column Exploration), Alpha-SQL (Column Value ID), **QUIS (schema-only hypothesis)** | **3 sources** — R3 adds "form hypotheses from schema, not data" variant |
| Evidence must cite specific data | Sullivan, ProactiveVA, Self-RAG, ReportGPT, DAgent, ReFoRCE, **DataPuzzle (structured evidence table)** | **7 sources** — R3 adds representation-gated generation |
| Causal language is unreliable | Corr2Cause, MultiVis-Agent, IEEE surveys, DataNarrative (gap) | **4 sources** — no R3 additions |
| Self-consistency voting fails | CHASE-SQL, Hallucination surveys, MultiVis-Agent, ReFoRCE, Alpha-SQL, **Data Interpreter (ACV ≠ voting)** | **6 sources** — R3 confirms: independent validation code > voting |
| Planning before execution | DataNarrative, DAgent, NAACL 2025, DataSage, Alpha-SQL, MAC-SQL, **AgentPoirot (SMART goal -34%)**, **Data-to-Dashboard (+28% novelty)** | **8 sources** — R3 provides strongest ablation evidence (34% degradation, 28% improvement) |
| Knowledge graph as primary guardrail | SiriusBI (-23-27% without it), our constraint #1 | **Validated by production** — no R3 additions |
| Typed reasoning moves | Alpha-SQL (7 actions), MAC-SQL (difficulty routing), **DataSage (3 CoT strategies)** | **3 sources** — R3 adds Negative Reasoning as a typed move |
| Data sufficiency as first-class check | SiriusBI (Data Prep Agent), ReFoRCE (Column Exploration) | **2 sources** — no R3 additions |
| Difficulty-gated routing | MAC-SQL, SiriusBI, **Insight Agents (BERT router 0.83 acc)** | **3 sources** — R3 adds production BERT router (vs LLM router 0.60 acc) |
| Progressive anchoring (baseline → driver) | MAC-SQL, Alpha-SQL (UCT), SiriusBI, **AgentPoirot (simplest sub-problem first)** | **4 sources** — R3 adds InsightBench evidence |
| Scope extension = common hallucination | DataNarrative, ProactiveVA, DAgent | **3 sources** — no R3 additions |
| LLMs cannot self-report confidence | ICLR 2025, MultiVis-Agent, Hallucination surveys | **3 sources** — no R3 additions |
| Verbosity signals quality loss | DataNarrative, DAgent (conciseness criterion) | **2 sources** — no R3 additions |
| **Structured intermediate representation** | **DataPuzzle (core thesis), NAACL/AgentPoirot (one question→one insight), DataSage (3 CoT)** | **3 NEW sources** — force structured form before narrative |
| **Statistical pre-filters before narrative** | **QUIS (4 pattern thresholds), InsightLens (Sfinal 60/40), InsightBench (slope>0.1)** | **3 NEW sources** — prevent LLMs from narrating noise |
| **Coverage taxonomy enforcement** | **InsightBench (4 types), InsightEval (+2 types), InsightLens (attribute tracking p=0.006), DataSage (judge diversity criterion)** | **4 NEW sources** — explicit type coverage > hope for breadth |
| **History-aware iterative analysis** | **DataSage (QA loop with H), QUIS (iterative bootstrapping), AgentPoirot (follow-up branching)** | **3 NEW sources** — each round builds on prior findings |
| **Experience accumulation across sessions** | **Data Interpreter (pool 200→78% reduction), DataSage (RAKG=largest ablation delta)** | **2 NEW sources** — institutional memory with quantified impact |
| **Insight scoring formula** | **InsightLens (Sfinal=0.6×Ssem+0.4×Sstat), Insight Agents (3-dim rubric, 0.8 threshold), InsightEval (multi-LLM novelty)** | **3 NEW sources** — formalized quality scoring |

---

## Full Bibliography

### Primary Sources (deep-read by oracle agents)

1. **Caitlin Sullivan.** "How to Do AI Analysis You Can Actually Trust." *Lenny's Newsletter*, 2026. [Paywalled]

2. **Islam, Laskar, Parvez, Hoque, Joty.** "DataNarrative: Automated Data-Driven Storytelling with Visualizations and Texts." *EMNLP 2024 Main*, pp. 19253-19286. [aclanthology.org/2024.emnlp-main.1073](https://aclanthology.org/2024.emnlp-main.1073/)

3. **arXiv:2601.18320.** "MultiVis-Agent: A Multi-Agent Framework with Logic Rules for Reliable and Comprehensive Cross-Modal Data Visualization." *SIGMOD 2026*. [arxiv.org/abs/2601.18320](https://arxiv.org/abs/2601.18320)

4. **Zhao et al.** "ProactiveVA: Proactive Visual Analytics with LLM-Based UI Agent." Fudan/Oxford, July 2025. [arxiv.org/abs/2507.18165](https://arxiv.org/abs/2507.18165)

5. **VOICE authors.** "VOICE: Visual Oracle for Interaction, Conversation, and Explanation." *IEEE TVCG 2025*. [ieeexplore.ieee.org/document/11037292](https://ieeexplore.ieee.org/document/11037292/)

6. **Xu et al.** "DAgent: A Relational Database-Driven Data Analysis Report Generation Agent." *PVLDB 2025*. [arxiv.org/abs/2503.13269](https://arxiv.org/abs/2503.13269)

7. **HKUSTDial.** "awesome-data-agents." GitHub repository, companion to arXiv:2510.23587. [github.com/HKUSTDial/awesome-data-agents](https://github.com/HKUSTDial/awesome-data-agents)

### Secondary Sources (referenced within oracle reports)

8. **arXiv:2406.12158.** "LLMs Are Prone to Fallacies in Causal Inference." GPT-4 F1=29.08 vs 20.38 random baseline on Corr2Cause.

9. **arXiv:2407.06423.** "InsightBench: Evaluating Business Analytics Agents." *ICLR 2025*. Four-category rubric (Descriptive/Diagnostic/Predictive/Prescriptive).

10. **arXiv:2511.14299.** "DataSage: Multi-agent Collaboration for Insight Discovery." Multi-role debate + multi-path reasoning.

11. **arXiv:2412.02205.** "DataLab: Unified Platform for LLM-Powered Business Intelligence." Enterprise schema grounding.

12. **arXiv:2601.20048.** "Insight Agents." Amazon production system. OOD detection + hierarchical manager-worker.

13. **arXiv:2502.11799.** "Table-Critic: A Multi-Agent Framework for Collaborative Criticism and Refinement." *ACL 2025*. 4-agent loop with Curator.

14. **arXiv:2504.10036.** "DataPuzzle: Breaking Free from the Hallucinated Promise of LLMs in Data Analysis." Structure-first decomposition.

15. **arXiv:2310.11511.** "Self-RAG: Learning to Retrieve, Generate, and Critique." *ICLR 2024 Oral*. Reflection tokens.

16. **arXiv:2410.01943.** "CHASE-SQL: Multi-Path Reasoning and Preference Optimized Candidate Selection." *ICLR 2025*. Self-consistency voting has 14% gap to pairwise selection.

17. **ICLR 2025.** "Do LLMs Estimate Uncertainty Well?" LLMs do not reliably self-report uncertainty.

18. **arXiv:2309.10947.** "How Do Analysts Understand and Verify AI-Assisted Data Analyses?" *CHI 2024*. Procedure-oriented vs data-oriented verification.

19. **arXiv:2503.11664.** "An LLM-Based Approach for Insight Generation in Data Analysis." *NAACL 2025*. Hypothesis-first pipeline.

20. **arXiv:2501.09349.** "ChartInsighter." *IEEE TVCG (PacificVis 2025)*. Self-consistency test phase.

21. **aclanthology.org/2024.emnlp-industry.39.** "ReportGPT." *EMNLP Industry 2024*. DSL proof mechanism.

22. **arXiv:2402.18679.** "Data Interpreter: An LLM Agent For Data Science." *ACL Findings 2025*. Per-node verification.

23. **arXiv:2401.04398.** "Chain-of-Table: Evolving Tables in the Reasoning Chain." *ICLR 2024*. Table transformation reasoning.

### Round 2 Primary Sources (deep-read 2026-02-19)

24. **Wang et al.** "MAC-SQL: Multi-Agent Collaboration for Text-to-SQL." *EMNLP 2023 Findings*. [arxiv.org/abs/2312.11242](https://arxiv.org/abs/2312.11242). Context reduction gate, progressive anchoring, failure taxonomy.

25. **Li et al.** "ReFoRCE: A Text-to-SQL Agent with Self-Refinement, Consensus Enforcement, and Column Exploration." *ICLR 2025 VerifAI Workshop*. [arxiv.org/abs/2502.00675](https://arxiv.org/abs/2502.00675). Two-stage consensus, execute-before-claim, content-convergence stopping.

26. **Li et al.** "Alpha-SQL: Zero-Shot Text-to-SQL using Monte Carlo Tree Search." *ICML 2025*. [arxiv.org/abs/2502.17248](https://arxiv.org/abs/2502.17248). MCTS for analytical reasoning, 7 typed actions, UCT exploration-exploitation.

27. **Luo et al.** "SiriusBI: A Comprehensive LLM-Powered Solution for Data Analytics in Business Intelligence." *PVLDB Vol.18(12) 2025*. [arxiv.org/abs/2411.06102](https://arxiv.org/abs/2411.06102). Production BI guardrails, Data Preparation Agent, knowledge graph grounding (-23-27% without).

### Round 3 Primary Sources (deep-read 2026-02-19)

28. **Zhang et al.** "DataPuzzle: Breaking Free from the Hallucinated Promise of LLMs in Data Analysis." April 2025. [arxiv.org/abs/2504.10036](https://arxiv.org/abs/2504.10036). Representation-gated generation, six desiderata. Vision paper — no implementation.

29. **Bai et al.** "Insight Agents: An LLM-Based Multi-Agent System for Data Insights." *SIGIR 2025*. Amazon production. [arxiv.org/abs/2601.20048](https://arxiv.org/abs/2601.20048). AE-based OOD gate (0.969 precision, 0.009s), 3-dimension rubric (0.8 threshold), 89.5% production accuracy.

30. **DataSage authors.** "DataSage: Multi-agent Collaboration for Insight Discovery with External Knowledge Retrieval, Multi-role Debating, and Multi-path Reasoning." [arxiv.org/abs/2511.14299](https://arxiv.org/abs/2511.14299). +7.5% insight / +13.9% summary over AgentPoirot. Negative Reasoning, 4-criterion judge, iterative QA.

31. **Hong, Lin et al.** "Data Interpreter: An LLM Agent For Data Science." *ACL Findings 2025*. [arxiv.org/abs/2402.18679](https://arxiv.org/abs/2402.18679). Two-code verification ACV (+17.29%), experience pool (200→78% debug reduction), fork-and-regenerate.

32. **Sanchez Perez, Boukhary, Papotti et al.** "An LLM-Based Approach for Insight Generation in Data Analysis." *NAACL 2025*. [arxiv.org/abs/2503.11664](https://arxiv.org/abs/2503.11664). Hypothesis-first pipeline.

33. **InsightBench / AgentPoirot.** "InsightBench: Evaluating Business Analytics Agents Through Multi-Step Insight Generation." *ICLR 2025*. [arxiv.org/abs/2407.06423](https://arxiv.org/abs/2407.06423). SMART goal ablation (-34%), k=3 roots + n=4 follow-ups, 4-category taxonomy.

34. **QUIS authors.** "QUIS: Question-guided Insights Generation for Automated Exploratory Data Analysis." *EMNLP 2024*. [arxiv.org/abs/2410.10270](https://arxiv.org/abs/2410.10270). Statistical pre-filters (Mann-Kendall, 1.4x ratio, 50% attribution, JS≥0.2), schema-only hypothesis generation.

35. **InsightLens authors.** "InsightLens: Augmenting LLM-Powered Data Analysis with Interactive Insight Management and Navigation." [arxiv.org/abs/2404.01644](https://arxiv.org/abs/2404.01644). Sfinal = 0.6×Ssem + 0.4×Sstat, attribute coverage tracking (p=0.006).

36. **Data-to-Dashboard authors.** "Data-to-Dashboard: Multi-Agent LLM Framework for Insightful Visualization in Enterprise Analytics." [arxiv.org/abs/2505.23695](https://arxiv.org/abs/2505.23695). Domain detection priming (+28% novelty, +31% depth), 6-agent sequential pipeline.

37. **InsightEval authors.** "InsightEval: An Expert-Curated Benchmark for Assessing Insight Discovery in LLM-Driven Data Agents." [arxiv.org/abs/2511.22884](https://arxiv.org/abs/2511.22884). Multi-LLM consensus novelty metric, Evaluative + Exploratory types.

---

## Empirically Proven Patterns: Cross-Round Ablation Evidence

The strongest findings across all 3 rounds, ranked by the magnitude of their measured impact.
These are techniques where papers provided ablation data — removing the technique and
measuring the degradation — not just comparative benchmarks.

| Technique | Ablation Evidence | Source | Round |
|-----------|------------------|--------|-------|
| Experience pool (200 items) | 78% reduction in debugging attempts ($0.80→$0.24/task) | Data Interpreter | R3 |
| Critic/verification stage | 73% quality loss when removed | DataNarrative | R1 |
| SMART goal constraint | 34% performance degradation when removed | InsightBench/AgentPoirot | R3 |
| Domain detection priming | +28% novelty, +31% depth vs baseline | Data-to-Dashboard | R3 |
| Knowledge graph grounding | 23-27% accuracy drop when removed | SiriusBI | R2 |
| Two-code verification (ACV) | +17.29% across all task categories | Data Interpreter | R3 |
| Multi-hop dialogue (MRD-Q) | 15-34% accuracy drop when removed | SiriusBI | R2 |
| Progressive decomposition | 3.85 point drop when removed (largest single-agent) | MAC-SQL | R2 |
| Multi-agent vs single-model | +12 points on diagnostic tasks (95% vs 83%) | SiriusBI | R2 |
| AE OOD gate vs LLM gate | +57% precision (0.969 vs 0.616), 185x faster | Insight Agents | R3 |
| BERT router vs LLM router | +38% accuracy (0.83 vs 0.60), 7x faster | Insight Agents | R3 |
| Self-consistency voting gap | -14% vs pairwise selection; -32% vs structural consensus | CHASE-SQL; ReFoRCE | R1/R2 |
| Observation/Reflection stage | 64% loss rate when removed | DataNarrative | R1 |
| RAKG (external knowledge) | Largest single ablation delta in DataSage (0.3530→0.3316) | DataSage | R3 |
| Multi-path reasoning | 0.3530→0.3417 when removed | DataSage | R3 |
| Coverage tracking UI | 12.4 vs 9.3 attributes explored (p=0.006) | InsightLens | R3 |
