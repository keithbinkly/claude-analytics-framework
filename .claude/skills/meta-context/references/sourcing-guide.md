# Value Sourcing Guide

Where to get the value for each schema field.

## Sourcing Methods

| Method | Description | Time | Best For |
|---|---|---|---|
| **Domain expert interview** | Interview metric owner or most experienced analyst | 30-60 min | investigation_path, causal_dimensions, business_rules, seasonality |
| **Historical data analysis** | Percentile analysis on trailing 12 months | 1-2 hrs | healthy_range, trend, correlations |
| **Operational documentation** | Extract from contracts, runbooks, PagerDuty | 15-30 min | business_rules, thresholds, SLAs |
| **Query log mining** | Analyze warehouse query history for GROUP BY patterns | 2-4 hrs | causal_dimensions priority ordering |
| **Organizational memory** | Post-incident reviews, Slack archaeology | Variable | affected_by events, known_root_causes |
| **Automated inference** | Statistical correlation analysis across metrics | 1-2 hrs | correlates_with pairs + relationship types |

## Field-by-Field Sourcing

### Layer 1: Context

| Field | Primary Source | Secondary Source |
|---|---|---|
| `purpose` | Metric owner interview | Existing documentation / wiki |
| `business_question` | Stakeholder interview ("What decision does this metric inform?") | Dashboard titles / report headers |
| `owner` | Org chart / on-call rotation | Data catalog |
| `stakeholders` | Metric owner ("Who asks you about this?") | Slack channel members |
| `definition` | Finance/accounting team for financial metrics; legal for compliance | Data dictionary |
| `aliases` | Ask 3 different stakeholders what they call it | Search Slack for the metric |
| `data_domain` | Obvious from context | Data catalog classification |
| `granularity` | dbt model grain | Metric YAML type_params |

### Layer 2: Expectations

| Field | Primary Source | Secondary Source |
|---|---|---|
| `healthy_range` | P5/P95 from trailing 12 months data | Metric owner gut check |
| `warning_threshold` | Metric owner ("When do you start worrying?") | P10 from historical data |
| `critical_threshold` | Incident runbook / PagerDuty thresholds | Metric owner ("When do you page someone?") |
| `seasonality` | Historical data + metric owner explanation of WHY | Business calendar events |
| `trend` | Time series analysis + metric owner context | QBR presentations |
| `target` | OKR/KPI documents | Leadership communications |
| `segment_expectations` | Contracts / SLA documents per customer tier | Account management team |
| `volatility` | Standard deviation from rolling 30-day window | Metric owner ("What's normal noise?") |
| `baseline_date` | Record when you calibrate | Calendar reminder to recalibrate |

### Layer 3: Investigation

| Field | Primary Source | Secondary Source |
|---|---|---|
| `causal_dimensions` | Senior analyst interview: "What do you check first?" | Query log mining (most common GROUP BY) |
| `investigation_path` | Senior analyst walkthrough of their decision tree | Post-incident review docs |
| `common_false_positives` | Senior analyst: "What trips up new people?" | Incident false-alarm history |
| `known_root_causes` | Post-incident reviews (last 12 months) | Slack #incidents channel archaeology |
| `data_quality_gotchas` | Data engineering team + pipeline monitoring | Known data delays / SLAs |

### Layer 4: Relationships

| Field | Primary Source | Secondary Source |
|---|---|---|
| `correlates_with` | Statistical correlation analysis | Analyst intuition + confirmation |
| `affected_by` | Organizational memory (major events log) | News monitoring for external factors |
| `leads_to` | Business process knowledge: what downstream metrics this feeds | Analyst interview |
| `decomposes_into` | Metric definition: what sub-metrics compose this | dbt model lineage |
| `shared_dimensions` | dbt model inspection: which dimensions appear in both models | Analyst: "I always join these on..." |

### Layer 5: Decisions

| Field | Primary Source | Secondary Source |
|---|---|---|
| `when_this_drops` | Incident runbook / escalation playbook | Senior analyst: "What do you do when X drops?" |
| `business_rules` | Contracts, SLAs, regulatory docs | Legal/compliance team, account management |
| `when_this_spikes` | Incident runbook for upward anomalies | Data engineering: "What could cause a false spike?" |
| `escalation_path` | On-call rotation docs | Metric owner: "Who do you call when..." |
| `notification_channels` | PagerDuty/Slack/OpsGenie config | Incident response playbook |
| `review_cadence` | Team standup schedule, QBR calendar | Metric owner |

## Adoption Sequence

**Start with the cheapest sources:**

1. **30 min: Documentation extraction** — Pull from existing runbooks, contracts, wikis. Fills: business_rules, owner, purpose, thresholds.
2. **1 hour: Historical data analysis** — P5/P95, correlations, trend. Fills: healthy_range, trend, correlates_with, seasonality.
3. **1 hour: Senior analyst interview** — The highest-value hour. Fills: investigation_path, causal_dimensions, common_false_positives, known_root_causes.
4. **Variable: Cross-team coordination** — For relationships and escalation. Fills: affected_by, leads_to, escalation_path, segment_expectations.
