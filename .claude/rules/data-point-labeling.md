# Data Point Labeling Standards

Every data point presented to the user MUST include its unit. No exceptions.

## Required Labels

| Data Type | Label Format | Examples |
|---|---|---|
| Transaction count | "auth attempt count", "txn count" | 7.6M auth attempt count |
| Dollar amount | "$X" or "dollar volume" | $12.4M dollar volume |
| Rate or share | Always suffix with "%" | 67.2% approval rate |

## Rules

1. **Never use naked "volume"** — always qualify: "txn count" or "$X dollar volume"
2. **Dollar amounts always get `$` prefix**
3. **Rates always get `%` suffix**
4. **When presenting query results, always include:**
   - Exact metric name from the semantic layer (e.g., `spend_total_auth_attempts`)
   - All applied filters (product_stack, pos_entry_mode, etc.)
   - Time grain (MONTH, WEEK, etc.)
   - Time range
   - What is NOT filtered (explicit "no MCC filter applied")
5. **Purpose:** User must be able to reproduce the exact number in Tableau from the description alone
