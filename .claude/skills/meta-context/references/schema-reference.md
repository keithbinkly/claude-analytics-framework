# Meta Context Schema Reference

Complete field inventory: 36 fields across 5 layers + cross-cutting metadata.

## Tier Definitions

| Tier | Meaning | Adoption Level |
|---|---|---|
| **Core** | Minimum viable. Addresses a failure mode demonstrated in ablation eval. | Bronze (~45 min/metric) |
| **Recommended** | Significant analytical value. Adds historical knowledge, downstream tracking. | Silver (~90 min/metric) |
| **Optional** | Useful but situational. Full organizational memory encoding. | Gold (~2 hrs/metric) |

## Placement: Model-Level vs. Metric-Level

The meta context schema supports **inheritance**. Fields can live at the semantic model level (shared across all metrics on that model) or at the metric level (specific to one metric). Metric-level values override model-level values.

**Rule of thumb:** If changing a field's value for one metric but not another would be *wrong*, it belongs at the metric level. If changing it for one but not another would be *redundant*, it belongs at the model level.

### Model-Level Fields (shared)

These fields describe the data source, not the individual metric:

| Field | Why shared |
|---|---|
| `owner` | Same team owns all metrics on the model |
| `data_source` | Same underlying table/pipeline |
| `grain` / `granularity` | Same model grain |
| `latency` | Same pipeline schedule |
| `history_start` | Same table history |
| `known_limitations` | Model-level quirks (e.g., triple-count, ABS handling) |
| `causal_dimensions` | Same dimensions available on the model |
| `affected_by` | Same external events hit all metrics |
| `escalation_path` | Usually same team/process |
| `last_validated` | Often validated together |

### Metric-Level Fields (diverge per metric)

These fields depend on what the specific metric measures:

| Field | Why metric-specific |
|---|---|
| `purpose`, `business_question` | Count ≠ amount ≠ rate |
| `healthy_range`, `warning_threshold`, `critical_threshold` | Ranges are per-metric by definition |
| `investigation_path` | Different metrics break differently |
| `correlates_with` | Typed edges are metric-specific |
| `when_this_drops`, `when_this_spikes` | Actions diverge per metric |
| `business_rules` | SLAs and policies are metric-specific |

### Mixed Fields (judgment call)

| Field | Guidance |
|---|---|
| `seasonality` | Share if same business process drives all metrics; override if metrics have different seasonal patterns |
| `common_false_positives` | Some are model-level (data quality), some are metric-specific (formula interpretation) |
| `stakeholders` | Often shared but rate metrics may have different audiences than volume metrics |

### YAML Structure

```yaml
models:
  - name: my_daily_metrics
    semantic_model:
      meta:
        context:
          owner: "Analytics Team"
          data_source: "Snowflake, T+1 batch"
        investigation:
          causal_dimensions:
            - name: program_code
              why: "Primary segmentation"
              priority: 1
      metrics:
        - name: my_success_rate
          meta:
            context:
              purpose: "Share of transactions completing successfully"
            expectations:
              healthy_range: [0.94, 0.99]
              warning_threshold: 0.92
            decisions:
              when_this_drops:
                - threshold: 0.92
                  action: "Check program_code breakdown"
```

### Approximate Shareability by Layer

| Layer | % Shareable | Why |
|---|---|---|
| Context (base) | ~70% | Describes the model/source |
| Expectations | ~20% | Ranges are per-metric |
| Investigation | ~50% | Same dimensions, different paths |
| Relationships | ~30% | Typed edges are metric-specific |
| Decisions | ~20% | Actions diverge per metric |

This maps to the pyramid: the base (Context) is broadest and most shared; the apex (Decisions) is narrowest and most metric-specific.

---

## Layer 1: Context — "Who cares and why does this exist?"

Closes: Interpretation failures.

| Key | Type | Tier | Description |
|---|---|---|---|
| `purpose` | string | **Core** | What this metric measures and why. Scope-bounded: "from X through Y." |
| `business_question` | string | **Core** | The decision question this metric answers. |
| `owner` | string | **Core** | Primary team or role responsible. |
| `stakeholders` | list[string] | Recommended | Other teams who consume or are affected. |
| `definition` | string | Recommended | Precise business definition distinguishing from similar metrics. |
| `aliases` | list[string] | Optional | Other names this metric goes by in the org. |
| `data_domain` | string | Optional | Business domain (e.g., "fulfillment", "finance"). |
| `granularity` | string | Optional | Grain the metric is computed at (daily, per-order, etc.). |

## Layer 2: Expectations — "What does good look like?"

Closes: Calibration failures.

| Key | Type | Tier | Description |
|---|---|---|---|
| `healthy_range` | list[number, number] | **Core** | P5/P95 operating range from trailing 12 months. |
| `warning_threshold` | number | **Core** | Value warranting attention (not yet critical). |
| `critical_threshold` | number | **Core** | Emergency value requiring immediate action. |
| `seasonality` | string | **Core** | When, how much, and why. Include magnitude. |
| `trend` | string | Recommended | Current direction and cause. |
| `target` | number | Recommended | Aspirational goal (distinct from healthy_range). |
| `segment_expectations` | list[object] | Optional | Different thresholds per segment (enterprise vs SMB). |
| `volatility` | string | Optional | Normal day-to-day variance to distinguish signal from noise. |
| `baseline_date` | string | Optional | When thresholds were last calibrated. |

## Layer 3: Investigation — "When it breaks, where do I look first?"

Closes: Framing failures.

| Key | Type | Tier | Description |
|---|---|---|---|
| `causal_dimensions` | list[object] | **Core** | Dimensions to slice by. Each: `{name, why, priority}`. |
| `investigation_path` | string | **Core** | Conditional decision tree (not flat list). |
| `common_false_positives` | list[string] | Recommended | Known scenarios that look like problems but aren't. |
| `known_root_causes` | list[object] | Recommended | Historical incidents: `{date, description, root_cause, resolution}`. |
| `data_quality_gotchas` | list[string] | Optional | Upstream data issues that mimic real drops. |

## Layer 4: Relationships — "What else moves when this moves?"

Closes: Reasoning failures.

| Key | Type | Tier | Description |
|---|---|---|---|
| `correlates_with` | list[object] | **Core** | Each: `{metric, relationship}`. Relationship must be typed: "inverse", "leading indicator", "upstream cause", etc. |
| `affected_by` | list[object] | **Core** | External events: `{event, impact}` with magnitude. |
| `leads_to` | list[object] | Recommended | Downstream metrics this feeds. Directional. |
| `decomposes_into` | list[object] | Optional | Sub-metrics that compose to this one. |
| `shared_dimensions` | list[string] | Optional | Dimensions shared with correlated metrics. |

## Layer 5: Decisions — "What do I do about it?"

Closes: Action failures + false confidence.

| Key | Type | Tier | Description |
|---|---|---|---|
| `when_this_drops` | list[object] | **Core** | Action protocols: `{threshold, action}`. |
| `business_rules` | list[string] | **Core** | SLAs, regulatory requirements, internal policies. **Without this, Layers 2-4 create false confidence.** |
| `when_this_spikes` | list[object] | Recommended | Action protocols for upward anomalies. |
| `escalation_path` | list[object] | Recommended | Who to escalate to: `{severity, contact, requires}`. |
| `notification_channels` | list[object] | Optional | Where alerts go: `{severity, channel}`. |
| `review_cadence` | string | Optional | How often formally reviewed. |

## Cross-Cutting Metadata

| Key | Type | Tier | Description |
|---|---|---|---|
| `last_validated` | string (date) | Recommended | When the meta block was last reviewed. |
| `context_authored_by` | string | Optional | Who authored or last reviewed. |
| `schema_version` | string | Optional | Schema version for migration. |

## Summary

| Layer | Core | Recommended | Optional | Total |
|---|---|---|---|---|
| 1. Context | 3 | 2 | 3 | **8** |
| 2. Expectations | 4 | 2 | 3 | **9** |
| 3. Investigation | 2 | 2 | 1 | **5** |
| 4. Relationships | 2 | 1 | 2 | **5** |
| 5. Decisions | 2 | 2 | 2 | **6** |
| Cross-cutting | — | 1 | 2 | **3** |
| **Total** | **13** | **10** | **13** | **36** |
