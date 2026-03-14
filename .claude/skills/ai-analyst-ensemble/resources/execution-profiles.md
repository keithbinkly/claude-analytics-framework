# Execution Profiles

Named configurations for the adaptive depth engine.
Referenced by analyze.md Step 0 when user specifies a profile or flag.

| Profile | Initial Analyst | Source Tie-Out | Max Escalation | Token Ceiling | Trigger |
|---|---|---|---|---|---|
| `quick_scan` | 1 (best-fit) | Skip | verify only | ~150K | `--quick` flag |
| `standard` | 1 (best-fit) | Yes (2 metrics) | ensemble | ~400K | Default (no flag) |
| `deep_analysis` | Full ensemble | Yes (5 metrics) | full + stats | ~700K | `--deep` flag |
| `presentation_ready` | Full ensemble | Yes (5 metrics) | full + story + output | ~1M | `--present` flag |
| `validate_only` | Result-Checker only | Skip | re-derivation | ~100K | `--validate` flag |

## Profile Behavior

**quick_scan**: One analyst answers the question. Depth check always returns `none`.
No source tie-out (speed over validation). Good for daily check-ins and known-answer questions.

**standard**: One analyst answers. Source tie-out runs (2 metrics). Depth check may escalate
if findings are surprising or ambiguous. Most questions finish at ~200K.

**deep_analysis**: Full 4-analyst ensemble from the start. Source tie-out runs all metrics.
Statistical Analyst included. Good for high-stakes decisions and threshold changes.

**presentation_ready**: Everything in deep_analysis, plus auto-chains to /data-story
(with Story Architect) and /present all (all output formats).

**validate_only**: No new analysis. Result-Checker runs re-derivation on a previous
analysis to verify conclusions still hold. Good for periodic validation.

## Token Ceilings

Ceilings are guidelines, not hard limits. The system reports actual token spend after
each analysis. If a `standard` analysis escalates to ensemble, it may exceed 400K —
that's expected and correct. The ceiling helps set expectations, not enforce caps.

## Resource Loading Schedule

Which resources load at which step, by profile. This is the runtime contract — analyze.md gates loading based on ACTIVE_PROFILE.

| Resource | quick_scan | standard | escalated | deep | validate |
|----------|-----------|----------|-----------|------|----------|
| SKILL.md + execution-profiles.md | Step 0 | Step 0 | Step 0 | Step 0 | Step 0 |
| shared-constraints.md | Step 3 | Step 3 | Step 3 | Step 3 | -- |
| {best-fit}-analyst.md | Step 3 | Step 3 | Step 3 | -- | -- |
| all 4 analyst.md files | -- | -- | Step 4.5 | Step 3 | -- |
| anomaly + cache + sql-patterns | Step 3 | Step 3 | Step 3 | Step 3 | -- |
| critic-agent.md + failure-library | -- | Step 5.5 | Step 5.5 | Step 5.5 | -- |
| synthesizer.md | -- | Step 6 | Step 6 | Step 6 | -- |

## Conflict Resolution Priorities

When design decisions conflict during implementation, resolve using these priorities in order:
1. Dependency order wins (don't break what's downstream)
2. Fewer integration points wins (simpler is better)
3. Existing patterns win (don't reinvent unless forced)
4. User-facing impact breaks ties
