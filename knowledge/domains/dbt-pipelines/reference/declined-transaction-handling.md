# Declined Transaction Handling (All Products Except rapid! and Wave)

**Scope**: Green Dot legacy products, BaaS, and Go2bank. **Excludes**: rapid! and Wave.

**Primary intent of this doc**: Provide analyst-friendly context for decline/approval metrics and the `responsecode`/decline-reason values that appear in the Transaction Monitoring pipeline (e.g., MetricFlow semantic bases such as `mrt_merchant_auth_decline__semantic_base`).

**Source**: “Declined Transaction Handling - All Products Except Rapid! and Wave (Current)” (Item ID 202133, Version 5 published 2025-09-11; exported 2025-11-07).

## How this maps to our data models

In our Transaction Monitoring semantic bases, we typically see daily-grain aggregates by `calendar_date`, `product_stack`, `merchant`, and a response/decision field (`responsecode`). Measures commonly include:
- `attempt_cnt` / `attempt_amt`: authorization attempts
- `approve_cnt` / `approve_amt`: successful authorizations
- `decline_cnt` / `decline_amt`: declines

The source document describes **customer-service decline reason labels** and their operational meaning. In analytics, these labels are most useful for:
- **Interpreting `responsecode` breakdowns** (e.g., which declines are “true insufficient funds” vs “card-on-file expiration mismatch”).
- **Grouping response/decline reasons into consistent themes** (limits, card status, fraud/risk, terminal/network errors, product restrictions).

## Decline reason catalog (business meaning)

Note: Many letter buckets (G, H, J, K, O, Q, V, W, X, Y, Z) are placeholders in the source and do not include additional definitions beyond “End of process”. The list below covers the reasons that have explicit definitions.

### Card security / card data mismatch
- **Advice acknowledged; no financial liability accepted**: Incorrect PIN.
- **Invalid PIN** / **Exceeds Bad Pin Limit** / **Deny (keep card), call acquire security dept**: PIN errors or PIN-attempt limits (daily reset referenced as 10:00pm PST).
- **Invalid security code provided**: Incorrect CVV.
- **Denied, Expiration Date Mismatch** / **Deny, Do Not Honor** / **Card Not Effective**: Expiration date mismatch/invalid expiration date, often because card details in a digital wallet / card-on-file weren’t updated after card replacement/activation.

### Card/account status
- **Card in Pause Status**: Customer-initiated lock/pause.
- **Card In Potential Fraud Status**: Card/account status block due to suspected fraud/risk; source instructs to follow fraud text alert handling.
- **Card is closed and cannot be used**: Using an old/closed card.
- **Card is expired and cannot be used**: Expired card or unactivated card.
- **Lost or Stolen Card Status**: Card reported lost.
- **Deny, refer to card Issuer** / **Deny, restricted card**: Card not active / activation incomplete.

### Terminal/network/processing errors
These are frequently “retry” outcomes operationally; analytically they’re useful to separate from customer-fixable issues like funds.
- **Bad data from terminal or card**: Bad chip read.
- **Deny, ARQC Failure** / **Deny, ATC Failure** / **Refer, ATC Failure** / **Chip Transaction Limit Exceeded**: EMV/chip read or EMV protocol failures.
- **Decline, Response Received Too Late** / **Deny, In Stand in Processing** / **Format Error** / **No Security Box** / **PBF Record not Found** / **System Malfunction** / **Transaction Error (1088/1109)** / **TVR Capture**: Terminal/processor timeouts or system/format issues.

### Limits
- **Exceeded daily ATM limit** / **Exceeded daily ATM withdrawal limit**: ATM usage limits (daily reset referenced as 10:00pm PST; monthly reset referenced as “30th day of the month”).
- **Exceeded the maximum cash advance limit**: Teller cash withdrawal / cash advance limit.
- **Exceeds daily purchase limit**: Daily spend limit.
- **Spend Amount Exceeds Limit**: AFT or cash back limit (reset referenced as first of calendar month).

### Funds and balance (including “ghost/hidden authorization”)
- **Insufficient Funds**: Attempt exceeds available funds; the source notes overdraft protection nuances (some transaction types are not covered).
- **Purchase exceeded the available funds**: Similar “available balance not sufficient” framing.

The source also calls out two operational balance-discrepancy patterns that can be relevant when analysts see surprising insufficient-funds declines:
- **“Ghost authorization”**: Available balance shows *less* than running balance; pending authorization may have posted; guidance indicates the pending authorization should “fall off” within ~24 hours (and to file an SI case).
- **“Hidden authorization”**: Available balance shows *greater* than running balance; guidance references authorizations that show “released” and may take up to the release date / ~two business days.

### Product / transaction-type restrictions
- **Invalid transaction**: Account/product restriction; includes ATM selection guidance (“checking”) and notes about restricted card types (e.g., “NPNR” and “Temp Only restricted” behavior).
- **Transaction Type not allowed** / **Transaction Type Not allowed on this card**: Restrictions for temporary / specific card types; online/over-the-phone restrictions described for certain temporary cards.
- **MCC (Merchant Type) … not allowed for this product**: Merchant category restrictions.
- **Restricted Country Code**: Country is blocked.

### Fraud / risk pattern detection
- **Unusual transaction**: Purchase doesn’t fit usual spending patterns; treated as a fraud/risk confirmation flow in the source.

## Practical analytics guidance

When analyzing declines in Transaction Monitoring (e.g., by `merchant`, `product_stack`, `card_present`, or `pos_entry_mode`):
- Treat **network/timeout/system** reasons as a separate group from **funds** and **card status** to avoid misattributing customer behavior.
- Treat **expiration/CVV/PIN** reasons as “customer credential / card-on-file maintenance” issues (often clustered in digital wallet / card-on-file contexts).
- Treat **limits** as policy-driven; if you trend daily/weekly, be aware the source references resets (daily at 10:00pm PST, monthly resets).

## Keywords (for search)

decline reason, response code, do not honor, expiration date mismatch, invalid expiration, CVV, invalid security code, invalid pin, bad pin limit, card paused, card locked, card not effective, card expired, card closed, lost stolen, fraud text alert, unusual transaction, insufficient funds, overdraft protection, ghost authorization, hidden authorization, stand in processing, system malfunction, transaction error 1088, transaction error 1109, ARQC failure, ATC failure, EMV chip, format error, terminal timeout, PBF record not found, TVR capture, restricted country code, MCC not allowed, transaction type not allowed
