# Dayforce (formerly Ceridian)

> Analytical brief for Green Dot's BaaS partnership with Dayforce. Living document — accumulates analyst findings over time.

**Last Updated**: 2026-02-12
**Last Researched**: 2026-02-11
**Data Quality Grade**: B+ (merchant spend validated; disbursement mapping needs confirmation)

---

## Business Context

| Metric | Value |
|--------|-------|
| Public Listing | **Private** (Thoma Bravo acquired for $12.3B, completed Feb 4, 2026; formerly NYSE: DAY) |
| FY2025 Revenue | ~$1.9B (Q3 2025: $481.6M, +9.5% YoY) |
| Customer Base | 7,025+ live customers (Q3 2025) |
| Dayforce Wallet | $5B+ cumulative payroll delivered (Dec 2024); ~$30M ARR (FY2024), projected "$40s" FY2025 |

**Product**: Dayforce is a global HCM platform integrating payroll, workforce management, and financial wellness. The Dayforce Wallet provides real-time wage access (EWA) and a linked debit card. Green Dot powers the card and instant transfer rails.

**Strategic Position**: Thoma Bravo take-private ($12.3B, Feb 2026) means no more public earnings disclosures. PE ownership typically drives margin optimization — watch for investment changes in Wallet features. Thoma Bravo also owns UKG (direct HCM competitor), creating portfolio consolidation risk.

**Key Relationship Dynamics**:
- Push-to-Debit and ACH Out are core Green Dot revenue drivers from this partnership
- CFPB EWA ruling (Dec 2025) is the single biggest tailwind for Wallet adoption
- Direct-to-bank pay expansion means some users may bypass the Wallet card entirely
- Wallet revenue trajectory: ~150% growth in FY2024 ($12M→$30M)

---

## Customer Segments

**By Employer Industry**:
- **Retail/Hospitality**: High turnover, hourly workers, heavy wallet adoption for instant pay
- **Healthcare**: Shift workers, moderate adoption, focus on benefits integration
- **Professional Services**: Salaried employees, lower wallet usage, higher direct deposit adoption
- **Manufacturing**: Union environments, scheduled pay cycles, lower real-time wage access needs

**By Employee Type**:
- **Hourly/Frontline Workers**: Core wallet users, high transaction frequency, smaller transaction sizes
- **Salaried Office Workers**: Lower adoption, use for occasional transfers, larger average transactions
- **Gig/Seasonal Workers**: Sporadic usage tied to work schedules, high early churn risk

**Segmentation Implications**:
- Churn rates vary 3-5x between hourly vs. salaried segments
- Transaction volume heavily driven by retail/hospitality employers
- Adoption growth should be measured by segment, not aggregate
- EWA expanded to salaried employees (Feb 2025) — monitor as new segment

---

## Recent Developments

| Date | Development | Type | Metric Impact |
|------|-------------|------|---------------|
| 2026-02-04 | Thoma Bravo completed acquisition — NYSE: DAY delisted, company now private | Strategic | All metrics — no more public disclosures; PE margin focus |
| 2025-12-23 | CFPB ruled employer-integrated EWA is NOT credit under TILA | Market | wallet_adoption_rate, push_to_debit_volume — major regulatory tailwind |
| 2025-10-07 | Dayforce AI Workspace launched — AI-powered HR assistant | Product | feature_engagement_rate — platform stickiness increase |
| 2025-08-21 | Thoma Bravo announced $12.3B take-private acquisition | Strategic | All metrics — ownership change implications |
| 2025-Q3 | Q3 2025 earnings: $481.6M (+9.5% YoY), 7,025 live customers | Financial | employer_retention_rate — 41 net new customers |
| 2025-Q2 | Q2 2025 earnings: $465M (+10% YoY), recurring ex-float +14% | Financial | Recurring growth outpacing headline — float income declining |
| 2025-07-03 | Instant Transfer fee restructured: 2% variable → flat $3.49 | Product | push_to_debit_volume, avg_transaction_value — benefits larger transfers |
| 2025-Q1 | Direct-to-bank pay launched — employees can route to any personal bank | Product | push_to_debit_volume up, but wallet_adoption_rate may decline |
| 2025-02 | EWA expanded to corporate/white-collar salaried employees | Product | wallet_adoption_rate, wallet_daily_active_users — new user segment |

---

## Available Metrics (Semantic Layer)

### Merchant Spend (via `product_stack` = Dayforce)
- `total_auth_amount`, `total_auth_count` — transaction volume
- `total_approved_amount`, `total_approved_count` — successful transactions
- `total_decline_amount`, `total_decline_count` — failed transactions (operational cost)
- `decline_rate`, `ewallet_decline_rate` — health indicators
- Dimensions: `merchant`, `mcc_category`, `mcc_desc`, `card_present`, `pos_entry_mode`, `responsecode`

### Disbursements (via `program_code` = Dayforce programs)
- `total_completed_count`, `total_completed_amount` — successful transfers
- `total_declined_count`, `total_failed_count` — failed transfers
- `oct_success_rate`, `oct_decline_rate`, `oct_failure_rate` — OCT health
- `avg_transaction_size`, `fee_to_amount_ratio` — economics
- `cumulative_count`, `cumulative_amount` — adoption trajectory
- Dimensions: `transfer_type`, `global_fund_transfer_status_reason`, `debit_network`

### Registrations (via `product_stack` = Dayforce)
- `registration_started`, `registration_passed`, `registration_failed` — funnel steps
- `activation_rate`, `pass_rate` — conversion health
- `cumulative_registrations`, `cumulative_activations` — growth trajectory
- Dimensions: `event_date`, `days_since_start`

---

## Data Quality Notes

- Merchant spend data validated and accurate for Dayforce product_stack
- Disbursement `program_code` mapping to Dayforce needs verification — confirm which codes correspond
- Registration funnel is least documented; failure_reason dimension not yet available (Task #36)
- No revenue percentile segmentation available — requires on-the-fly computation via `execute_sql`
- Cardholder model is high-cardinality (10-20x auth model) — use aggregate metrics

---

## Analyst Findings

<!--
WRITEBACK SECTION — Appended by /analyze after each synthesis.
Schema per finding (danielrosehill evidence chain):

### [YYYY-MM-DD] [Brief title]
- **Claim**: [What the analysis found]
- **Evidence**: [Specific metrics, queries, and values that support the claim]
- **Confidence**: HIGH | MEDIUM | LOW
- **Gap**: [What additional data would strengthen or refute this claim]
- **Source**: [Which analyst(s) surfaced this — Forensic/Exploratory/Business/Statistical/Consensus]
- **Session**: [GUID of the /analyze session]
- **Status**: ACTIVE | SUPERSEDED | DISPROVEN

If disproven by later analysis, do NOT delete — mark as DISPROVEN with explanation.
If superseded by a more complete finding, mark SUPERSEDED with pointer to replacement.
-->

### 2026-02-12 Approval rate declining — CNP-driven, CP stable
- **Claim**: Overall approval rate declined 3.68pp over 3 months (69.36% Nov → 65.68% Jan), a 5.3% relative decline. Feb partial tracking worse at 62.87%.
- **Evidence**: `spend_approval_rate_by_count` monthly with `product_stack=Ceridian Dayforce`. Nov 69.36%, Dec 67.23%, Jan 65.68%, Feb(partial) 62.87%. Volume flat at ~5.1M approvals/month.
- **Confidence**: HIGH
- **Gap**: Feb 2026 partial month — final rate may differ +/-1pp. Top decline reason codes not yet queried.
- **Source**: Forensic analyst (single-analyst validation run)
- **Session**: 4d33b7d5-110f-4dc7-9b28-dbbd54918659
- **Status**: ACTIVE

### 2026-02-12 Insufficient Funds is dominant decline driver (60-70% of volume)
- **Claim**: Insufficient Funds accounts for 60-70% of all Dayforce declines (1.85M/month Jan 2026), growing 21% MoM from Nov.
- **Evidence**: `spend_total_declines` by responsecode. Nov: 1.52M → Dec: 1.73M → Jan: 1.85M. Combined with "Insufficient Balance" = ~69% of all declines.
- **Confidence**: HIGH
- **Gap**: No visibility into balance-at-time-of-decline. Is this genuine insufficient funds or timing (load delay)?
- **Source**: Consensus (4/4 analysts — Forensic, Exploratory, Business, Statistical all confirmed)
- **Session**: 4d33b7d5-110f-4dc7-9b28-dbbd54918659
- **Status**: ACTIVE

### 2026-02-12 Expiration Date Mismatch surging (+54% in 3 months)
- **Claim**: Expiration Date Mismatch declines grew 54% from 160K (Nov) to 246K (Jan), suggesting stale card-on-file credentials at merchants after card reissuance.
- **Evidence**: `spend_total_declines` by responsecode. Nov: 160K → Dec: 211K → Jan: 246K. Concentrated in CNP channel.
- **Confidence**: HIGH
- **Gap**: Confirm card reissuance schedule. Verify Visa VAU / MC ABU enrollment status.
- **Source**: Forensic analyst (unique quantification) + Business analyst (action recommendation)
- **Session**: 4d33b7d5-110f-4dc7-9b28-dbbd54918659
- **Status**: ACTIVE

### 2026-02-13 Portfolio leader by 2x — but near-parity decline ratio raises efficiency concern
- **Claim**: Dayforce is the #1 partner by auth attempt volume ($1.207B, Nov 2025 - Jan 2026), nearly 2x the #2 partner (QuickBooks $619M). However, decline volume ($581.5M) is at near-parity with approval volume ($625.8M) — 93 cents declined for every $1 approved. The 48.1% decline rate by dollar is highest among the top 3 partners.
- **Evidence**: `spend_total_auth_attempt_amount`, `spend_total_approval_amount`, `spend_total_decline_amount` by product_stack. Dayforce: $1.207B/$625.8M/$581.5M. QuickBooks: $619.3M/$354.9M/$264.4M. Amazon Flex: $563.9M/$314.6M/$249.3M.
- **Confidence**: HIGH (ranking) / MEDIUM (magnitudes — data 14 days stale)
- **Gap**: QoQ comparison unanswerable with current 3-month aggregate. Need monthly grain reporting for quarterly trend analysis. Cash App at $201M combined is #1 merchant across all partners — merchant-level analysis could reveal cross-cutting dynamics not visible at partner level.
- **Source**: Portfolio ensemble analysis (4 analysts + synthesizer). All 4 consensus on ranking. Exploratory surfaced near-parity ratio.
- **Session**: 554a4d45-a128-4e89-a345-a24975b6a5f0
- **Status**: ACTIVE

### 2026-02-12 CNP approval rate deteriorating sharply, CP healthy
- **Claim**: CNP approval rate dropped 6.75pp (48.22% → 41.47%) while CP held stable at ~95% (-0.70pp). CP-CNP gap widened from 47pp to 53pp.
- **Evidence**: `spend_cp_approval_rate` and `spend_cnp_approval_rate` monthly. CP: 95.38→95.32→95.23→94.68%. CNP: 48.22→46.21→44.93→41.47%. Chip decline rate stable at ~5.5%.
- **Confidence**: HIGH
- **Gap**: No visibility into top decline response codes by volume — need to determine if CNP declines are insufficient funds (balance issue) vs fraud controls (risk management issue).
- **Source**: Forensic analyst (single-analyst validation run)
- **Session**: 4d33b7d5-110f-4dc7-9b28-dbbd54918659
- **Status**: ACTIVE

### 2026-02-19 High eWallet adoption (27.6%) but low overall approval — CNP problem, not wallet
- **Claim**: Dayforce has the 2nd-highest eWallet share among volume partners (27.6%) but 48.5% overall approval. Wealthfront (31.8% share, 74.7% approval) breaks any "eWallet → lower approval" narrative. Dayforce's low approval is associated with CNP mix, not wallet channel.
- **Evidence**: `spend_ewallet_share_by_count` by product_stack: Dayforce 27.6%, Wealthfront 31.8%. `spend_approval_rate_by_count`: Dayforce 48.5%, Wealthfront 74.7%. CP approval: Dayforce 87.7%.
- **Confidence**: HIGH
- **Gap**: No eWallet-specific approval rate metric exists — cannot measure whether Dayforce eWallet transactions specifically have better/worse approval than chip. Semantic layer gap.
- **Source**: Forensic + Statistical (consensus on CNP attribution; Critic confirmed)
- **Session**: dafdc0f0-7a3e-41a1-b04c-84215ea1aa7a
- **Status**: ACTIVE

### 2026-02-19 ISF = 67.5% of decline $; Services MCC worst concentration (18.6 declines/CH)
- **Claim**: Insufficient Funds accounts for 67.5% of Dayforce decline dollars ($186.6M/4mo). Services MCC carries 52.2% of Dayforce decline dollars at $43.94 avg ticket. Portfolio-wide Services concentration is 18.6 declines per affected cardholder with 88% of cardholders affected — broad AND deep. Decline depth is increasing (+16.4% Nov→Jan) while breadth holds flat (+1.3%).
- **Evidence**: `mrt_merchant_auth_decline_analytics` by responsecode: ISF 67.5%. MCC: Services $144.5M (52.2%), Retail $51.3M (18.5%). Cardholder grain: 18.6 declines/affected CH (Services), up from 10.64 portfolio in Nov to 12.39 in Jan.
- **Confidence**: HIGH
- **Gap**: Cannot cross-tab cardholder concentration by partner (join path constraint). Services sub-MCC breakdown (mcc_desc) would reveal specific merchants driving repeat declines.
- **Source**: Consensus (4/4 analysts); Forensic quantified depth vs. breadth divergence
- **Session**: 3bf85050-88f8-403b-a3ae-c9de6e68ea53
- **Status**: ACTIVE

### 2026-02-19 Expiration Date Mismatch = $21.5-26.3M, fastest-growing actionable code (+30% Nov→Jan)
- **Claim**: Dayforce Expiration Date Mismatch = 762K declines ($21.5M 3-month, $26.3M 4-month incl partial Feb). Portfolio-wide this code grew +29.9% Nov→Jan (monotonic), fastest of any non-ISF code. Operationally fixable via Account Updater/network tokenization without cardholder action. Estimated 40-70% recovery rate.
- **Evidence**: `spend_total_declines` by responsecode and product_stack. Nov 263K → Dec 309K → Jan 342K portfolio. Prior finding confirmed +54% for Dayforce specifically.
- **Confidence**: HIGH (trend and volume); MEDIUM (recovery rate — industry benchmark, not measured)
- **Gap**: Current Account Updater enrollment rate unknown. Need to confirm which merchant billers are generating the most mismatch declines.
- **Source**: Consensus (4/4 analysts); Business analyst sized recovery opportunity
- **Session**: 3bf85050-88f8-403b-a3ae-c9de6e68ea53
- **Status**: ACTIVE

### 2026-02-19 Card in Pause Status = 601K declines ($15.5M) — active cardholder experience failure
- **Claim**: Dayforce "Card in Pause Status" = 601K declines ($15.5M) over 4 months. These are cardholders actively attempting transactions on paused cards — suggesting they don't know the card is paused or cannot self-service reactivation. Estimated $6-12M recoverable with improved notification.
- **Evidence**: `mrt_merchant_auth_decline_analytics` by responsecode: Card in Pause = 5.6% of Dayforce decline $.
- **Confidence**: MEDIUM (volume observed; recoverability speculative)
- **Gap**: Is pause employer-triggered or fraud-hold? If employer-triggered, recovery potential is lower.
- **Source**: Exploratory (surfaced) + Business (sized opportunity)
- **Session**: 3bf85050-88f8-403b-a3ae-c9de6e68ea53
- **Status**: ACTIVE

### 2026-02-23 Geographic: Employer-HCM footprint with Oregon EXTREME anomaly
- **Claim**: Dayforce shows a medium geographic deviation from population (w=0.25, KL=0.030). Oregon is a genuine statistical anomaly (PI=2.06, z=+3.48 EXTREME, 23% of Dayforce's total chi-sq) — no other partner exceeds PI 1.09 in OR. Minnesota over-indexes at PI~1.56–1.64 (NOTABLE, consistent with Ceridian Minneapolis HQ). NY under-indexes at PI=0.61, NJ at PI=0.62. Most similar to Amazon Flex (JS distance=0.11 — most similar partner pair in the portfolio). Geographic HHI=445 (second-least concentrated).
- **Evidence**: 225,198 accounts (2025), `int_baas_account_details_extended` joined to `stg_edw__dim_account`. OR: 5,893 accounts (Result-Checker verified exact). Chi-sq=14,147. OR contribution: 3,262 (23%). Nationally distributed across OH (PI=1.29), MO (PI=1.33), TN (PI=1.31).
- **Confidence**: HIGH (N=225,198; OR z=3.48 well above EXTREME threshold, N=5,893 not a small-cell artifact)
- **Gap**: Is Oregon's PI=2.06 driven by a small number of large employer client relationships (Fred Meyer/Kroger, PeaceHealth, OHSU) rather than broad market penetration? If top 5 employers account for >60% of OR volume, this is a client concentration risk, not a market signal. Follow-up query recommended.
- **Source**: Consensus (3/4 analysts — Forensic, Exploratory, Statistical); Business addressed in Q4 partner mix
- **Session**: geo-distribution-2026-02-23
- **Status**: ACTIVE

### 2026-02-24 Metro-level: Most geographically even partner, Miami gap = largest in dataset
- **Claim**: Consumer (Dayforce) is the most geographically even partner at metro level (narrowest PI range across 30 CBSAs, CV=0.257). Unique 50/50 metro/non-metro split (49.02%) suggests a fundamentally different distribution channel (employer-HR reach into mid-tier markets). However, Miami PI=0.52 represents the largest single partner×metro account gap in the dataset (-2,898 accounts below parity). Fortress metros: Minneapolis(1.43), Riverside(1.23), DFW(1.14). Positively correlated with Gig (r≈+0.50) — both favor interior metros.
- **Evidence**: `int_geo__account_geography` top 30 CBSAs, 2025 registrations (N=225,198). CBSA HHI=0.0334. 12 metros to 50%. DFW max PI spread only 0.29 (contested market for all partners).
- **Confidence**: MEDIUM-HIGH (evenness and Miami gap verified; distribution channel hypothesis is INFERRED)
- **Gap**: Miami root-cause unknown — is it channel absence (no Dayforce employers in Miami) or population segment mismatch? Employer client list needed. SMB PI=1.23 in same metro suggests market access exists for other partners.
- **Source**: Consensus (4/4 analysts); Business sized Miami gap; Statistical quantified CV; Exploratory flagged distribution channel hypothesis
- **Session**: a8d61a76-4442-4c03-a0ff-d8d899ecac9b
- **Status**: ACTIVE

### 2026-02-22 Disbursement Success Rate Recovery: 76.34% → 93.76% (+17.42pp), Declined $ Down 77%
- **Claim**: Dayforce disbursement success rate improved from 76.34% (Feb 2025) to 93.76% (Jul 2025), a +17.42pp gain. The improvement concentrated in July (+12.52pp single month), reducing declined dollars from $28.1M/mo (Feb-Jun avg) to $6.3M (Jul) — a 77.5% reduction. Statistical anomaly: z = +7.32σ. Co-occurs with N/A processor volume reduction (−37%) and A2AOut transfer type improvement (+12.40pp). Pattern consistent with routing intervention (discrete change, not gradual improvement).
- **Evidence**: dbt Semantic Layer `disbursement_success_rate` by program_code, Feb-Jul 2025. Feb: 76.34% / 369K txns / $24.0M declined. Jul: 93.76% / 554K txns / $6.3M declined. A2AOut transfer type: 77.76% → 90.16% same month. N/A processor: 122.9K → 77.7K txns (−37%).
- **Confidence**: HIGH (rates and dollars observed; routing intervention hypothesis inferred from co-occurrence)
- **Gap**: Need program_code × processor cross-dimension to confirm dayforce migrated away from N/A processor in July. Need operational logs to identify the specific routing change. Remaining $6.3M/mo failures may have different root cause than pre-July failures.
- **Source**: Consensus (4/4 analysts — forensic, exploratory, statistical, business); F3 + F7 in disbursement analysis
- **Session**: 3868b443-10cf-48f8-abfc-e22de7808031
- **Status**: ACTIVE

---

## Known Gaps

1. **No visibility into Wallet-specific metrics** — Dayforce Wallet ARR, active users, and adoption rate are not in our semantic layer (these are Dayforce's internal metrics)
2. **Push-to-Debit vs. ACH Out split** — Need to confirm if disbursement data distinguishes these transfer types for Dayforce
3. **Employer-level segmentation** — No employer_id or employer_industry dimension in semantic layer
4. **Post-acquisition disclosure gap** — No more quarterly earnings after Feb 2026 delisting
5. **Direct-to-bank cannibalization** — Can't measure whether employees bypass Wallet card in favor of personal bank routing

---

## Open Questions

- How does the flat $3.49 fee restructure (Jul 2025) show up in `avg_transaction_size` and `fee_to_amount_ratio`?
- What is the adoption trajectory for salaried employees (new segment since Feb 2025)?
- Is there a measurable impact from the CFPB ruling (Dec 2025) on wallet_adoption_rate?
- How does Dayforce's card-present vs. card-not-present mix compare to other partners?
- What are the top decline reasons (responsecode) specific to Dayforce cardholders?
