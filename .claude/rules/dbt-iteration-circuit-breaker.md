# Iteration Circuit Breaker

## Hard Stops

- **Same error 2+ times** → Stop. Re-diagnose root cause. You're treating symptoms, not the cause.
- **3 compile failures** → Stop. Report what you tried. Ask the user.
- **No progress after 3 iterations** on any issue → Stop and ask the user.

## Why This Exists

Sessions run 2-4x longer than expected due to iteration loops. The pattern: wrong diagnosis → fix attempt → same error → different fix attempt → same error → frustration → worse fix. A wrong diagnosis never resolves through persistence.

## Instead of Iterating

1. Re-read the error message (the actual one, not your interpretation)
2. Check if compiled SQL != materialized data (see `dbt-warehouse-vs-code` rule)
3. Search decision traces for similar past cases
4. Ask the user
