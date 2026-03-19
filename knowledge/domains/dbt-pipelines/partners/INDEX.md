# BaaS Partner Analytical Briefs

Per-partner living documents that combine business context, available metrics, data quality notes, and accumulated analyst findings. These files are the **single source of truth** for partner intelligence and are updated by both human research and AI analyst writeback.

## Partners

| Partner | File | Domain Coverage | Last Updated |
|---------|------|-----------------|--------------|
| Dayforce | [dayforce.md](dayforce.md) | Merchant Spend, Disbursements, Registrations | 2026-02-12 |
| Amazon Flex | [amazon-flex.md](amazon-flex.md) | Merchant Spend, Disbursements, Registrations | 2026-02-12 |
| QuickBooks | [quickbooks.md](quickbooks.md) | Merchant Spend, Disbursements, Registrations | 2026-02-12 |
| Wealthfront | [wealthfront.md](wealthfront.md) | Merchant Spend, Disbursements, Registrations | 2026-02-12 |
| Credibly | [credibly.md](credibly.md) | Merchant Spend, Disbursements, Registrations | 2026-02-12 |

## Architecture

**Design Pattern**: Living documents with insight writeback (research-grounded from 6 proven patterns).

**How findings accumulate**:
1. `/analyze` dispatches 4 analyst agents + synthesizer
2. After synthesis, the writeback step appends findings to the relevant partner file(s)
3. Each finding uses the evidence chain schema: **Claim / Evidence / Confidence / Gap**
4. Disproven findings are kept (marked `DISPROVEN`) — not deleted
5. Superseded findings are moved to archive section at compaction time
6. Progressive disclosure: `/analyze` reads only the most recent + relevant findings, not the full history

**Compaction cadence**: Quarterly. Move superseded/stale findings (>90 days) to `## Archived Findings` section.

**Cross-partner analysis**: When partners are similar enough, compile benchmarks on-demand by reading multiple partner files in parallel (5 reads, negligible cost).

## Source Material

Original unified document preserved at:
```
dbt-enterprise/docs/business_context/Company-level-context/baas_division_partner_overviews.md
```

## For AI Agents

Before querying metrics for a partner:
1. **Read the partner file first** (NVIDIA memory-first pattern)
2. Use business context + recent developments to interpret metric changes
3. After analysis, append findings to the `## Analyst Findings` section using the evidence chain template
4. Timestamp every finding. Include session GUID for traceability.
