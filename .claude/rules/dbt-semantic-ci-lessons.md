# Semantic Layer CI Lessons

Learned 2026-03-04 from PR #135 debugging. Prevents multi-hour CI iteration loops.

## 1. Semantic Model Name Must Match Model Filename Exactly

When using `name:` override in a semantic model definition, the value must match the model's actual filename **exactly** — including double underscores (`__`).

```yaml
# ❌ WRONG — causes "not in the graph" error
- name: mart_oct_daily_metrics        # single underscore
  config:
    semantic_model:
      enabled: true

# ✅ RIGHT — matches the .sql filename
- name: mart_oct__daily_metrics       # double underscore, same as file
  config:
    semantic_model:
      enabled: true
```

**Why:** dbt Cloud's MetricFlow resolver uses the model file's identity to build the semantic graph. A name mismatch creates a phantom node that metrics can't reference. Local Fusion may tolerate this; CI MetricFlow does not.

**Tension:** The Fusion semantic spec lint rule says "no `__` in semantic names." Resolution: don't override `name:` at all — let dbt infer it from the filename. Only override if absolutely necessary.

## 2. Disable Partial Parse After File Renames/Deletes

After renaming or deleting any YAML file that contains semantic definitions, dbt Cloud CI's partial parse cache may retain references to the old file path.

**Symptom:** Duplicate metric errors, "already in graph" errors, or unresolved references to deleted files — even though your local parse is clean.

**Fix:** Add to `dbt_project.yml`:
```yaml
flags:
  partial_parse: false
```

Remove this flag after 1-2 clean CI runs, once the cache is flushed.

## 3. Never Mix Inline and Dedicated Semantic Files

For any given model, define semantic models + metrics in **one place only**:
- Either inline in the model's `schema.yml` (new dbt 1.11+ format)
- Or in a dedicated `sem_*.yml` file (traditional format)

**Never both.** Mixed definitions cause duplicate metric names and graph resolution failures that are invisible locally but fatal in CI.

## 4. Local Parse ≠ CI MetricFlow Resolver

`dbt parse --no-partial-parse` passing locally does **NOT** guarantee CI will pass. dbt Fusion and dbt Cloud CI use different MetricFlow resolver implementations. Always:

1. Run the semantic spec lint: `python3 scripts/lint_semantic_spec.py`
2. Validate with MetricFlow locally: `source .venv/bin/activate && mf validate-configs`
3. If both pass but CI fails, the issue is likely a graph identity mismatch (see Rule 1)

## 5. Stop Iterating After 2-3 CI Failures

If the same semantic layer CI error persists after 2-3 fix commits:

1. **Stop pushing commits.** Each attempt pollutes the PR with fix-on-fix noise.
2. **Write a bug report** with exact error messages and reproduction steps.
3. **Research the root cause** using dbt docs, semantic layer migration guide, and the lint tool.
4. **Fix comprehensively** in a single commit.

The pattern `fix → push → CI fails → different fix → push → CI fails` wastes 2-5 hours. Stopping to research takes 15 minutes.
