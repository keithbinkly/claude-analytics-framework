# Using the EDW Data Dictionary for Staging Model Documentation

## Overview
The `r1_edw_dictionary.csv` seed file contains **1,084 field definitions** from our EDW (Enterprise Data Warehouse) sourced from Confluence documentation. This serves as the authoritative business glossary for staging model documentation.

## File Structure
```csv
Release,ODS Entity,ODS Attribute,ODS Attribute Position,EDW Entity,EDW Attribute,Definition,Data Type,PK,FK
```

**Key columns:**
- `EDW Entity`: Table name (e.g., `FCT_POSTED_TRANSACTION`, `DIM_ACCOUNT`)
- `EDW Attribute`: Column name (e.g., `POSTED_TXN_UID`, `MERCHANT_NM`)
- `Definition`: Business definition from Confluence
- `Data Type`: Redshift data type
- `PK`: Primary key flag (YES/NO)
- `FK`: Foreign key flag (YES/NO)

## Naming Convention Mapping

**EDW → dbt Staging Model:**
```
FCT_POSTED_TRANSACTION     →  stg_edw__fct_posted_transaction
FCT_AUTHORIZATION_TRANSACTION  →  stg_edw__fct_authorization_transaction
DIM_ACCOUNT                →  stg_edw__dim_account
DIM_PRODUCT                →  stg_edw__dim_product
```

**Column naming:**
- EDW uses `UPPER_SNAKE_CASE`
- dbt staging uses `lower_snake_case`
- Names are otherwise identical

## Usage: Generate YAML Documentation

### Quick Method: Python Script

```bash
# Generate YAML for a specific entity
python .claude/quick-reference/generate_staging_yml_from_dictionary.py FCT_POSTED_TRANSACTION > temp_yml.txt

# Then copy/paste relevant columns into your schema.yml
```

### Manual Lookup: Query the CSV

```bash
# Search for specific table
grep "FCT_POSTED_TRANSACTION" seeds/r1_edw_dictionary.csv | head -20

# Search for specific column across all tables
grep -i "merchant_nm" seeds/r1_edw_dictionary.csv
```

### Python Interactive Lookup

```python
import csv

# Load the dictionary
with open('seeds/r1_edw_dictionary.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Find all fields for a table
posted_fields = [r for r in rows if r['EDW Entity'] == 'FCT_POSTED_TRANSACTION']

# Print field names with definitions
for field in posted_fields:
    print(f"{field['EDW Attribute']}: {field['Definition'][:80]}...")
```

## Example: Adding Definitions to Staging YML

**Before:**
```yaml
# models/staging/edw/stg_edw__fct_posted_transaction.yml
models:
  - name: stg_edw__fct_posted_transaction
    columns:
      - name: posted_txn_uid
      - name: merchant_nm
      - name: total_post_amt
```

**After (with dictionary definitions):**
```yaml
# models/staging/edw/stg_edw__fct_posted_transaction.yml
models:
  - name: stg_edw__fct_posted_transaction
    description: "Staging model for posted (settled) transactions from EDW"
    columns:
      - name: posted_txn_uid
        description: "Unique Transaction Identifier assigned to the transaction in ODS"
        meta:
          is_primary_key: true
          edw_data_type: bigint
      
      - name: merchant_nm
        description: "Name of the Merchant where the Posted transaction originated"
        meta:
          edw_data_type: varchar(100)
      
      - name: total_post_amt
        description: "Total transaction amount in USD"
        meta:
          edw_data_type: decimal(20,4)
```

## Coverage Statistics

```bash
# Count fields per entity
python3 << 'EOF'
import csv
from collections import Counter

with open('seeds/r1_edw_dictionary.csv') as f:
    reader = csv.DictReader(f)
    entities = Counter(row['EDW Entity'] for row in reader if row['EDW Entity'] != 'NULL')

print("Top 10 EDW Entities by field count:")
for entity, count in entities.most_common(10):
    print(f"  {entity}: {count} fields")
EOF
```

## Common EDW Entities in Our Project

| EDW Entity | Staging Model | Fields | Description |
|------------|---------------|--------|-------------|
| `FCT_POSTED_TRANSACTION` | `stg_edw__fct_posted_transaction` | 80 | Settled/posted transactions |
| `FCT_AUTHORIZATION_TRANSACTION` | `stg_edw__fct_authorization_transaction` | 70+ | Authorization attempts |
| `DIM_ACCOUNT` | `stg_edw__dim_account` | 60+ | Account master data |
| `DIM_PRODUCT` | `stg_edw__dim_product` | 30+ | Product definitions |
| `DIM_TXN_TYPE_HIERARCHY` | `stg_edw__dim_txn_type_hierarchy` | 15+ | Transaction type taxonomy |
| `DIM_MCC` | `stg_edw__dim_mcc` | 10+ | Merchant category codes |

## Best Practices

### 1. **Start with the Dictionary**
Before creating a new staging model, check if definitions exist:
```bash
grep "YOUR_TABLE_NAME" seeds/r1_edw_dictionary.csv | wc -l
```

### 2. **Document Key Fields First**
Prioritize definitions for:
- Primary keys (`PK = YES`)
- Foreign keys (`FK = YES`)
- Business-critical fields (amounts, dates, merchant info)

### 3. **Enhance with Business Context**
Dictionary definitions are technical. Add business context in your YML:
```yaml
- name: total_post_amt
  description: |
    Total transaction amount in USD (from EDW dictionary).
    
    **Business Context**: Includes merchant charges but excludes 
    separate fee transactions. For net customer impact, join with 
    fee transactions.
  meta:
    edw_data_type: decimal(20,4)
```

### 4. **Keep Definitions Synchronized**
When EDW schema changes:
1. Update `r1_edw_dictionary.csv` from Confluence
2. Re-run YAML generator
3. Update affected staging models

## Quick Reference: Common Fields

### Transaction Identifiers
- `POSTED_TXN_UID` / `AUTH_UID`: Primary keys
- `SOR_UID`: Source system identifier
- `PROCESSOR_UID`: Payment processor identifier

### Dates & Times
- `TXN_DTTM_LOCAL`: Transaction datetime (local timezone)
- `POSTED_DTTM_PT`: Posted datetime (Pacific Time)
- `PROCESSOR_BUSINESS_DT`: Processor business date

### Merchant Data
- `MERCHANT_NM`: Merchant name
- `MERCHANT_ID`: Merchant identifier
- `MCC`: Merchant Category Code
- `MERCHANT_CITY` / `MERCHANT_STATE_PROVINCE`: Location

### Amounts
- `TOTAL_POST_AMT` / `TOTAL_AUTH_AMT`: Transaction amount
- `TOTAL_FEE_AMT`: Fee amount
- `LEDGER_BALANCE` / `AVAILABLE_BALANCE`: Account balances

### Flags & Indicators
- `ATM_IND`: ATM transaction flag
- `PIN_USED_IND`: PIN verification flag
- `CARD_PRESENT_IND`: Card-present flag
- `FORCE_POST_IND`: Force-posted (no auth) flag

## Integration with dbt docs

Generate comprehensive documentation:
```bash
# 1. Generate YML from dictionary
python .claude/quick-reference/generate_staging_yml_from_dictionary.py FCT_POSTED_TRANSACTION > temp_yml.txt

# 2. Copy relevant sections into schema.yml

# 3. Generate dbt docs
dbt docs generate

# 4. View in browser - definitions now searchable!
dbt docs serve
```

## Known Limitations

1. **NULL Attributes**: Some rows have `EDW Attribute = NULL` - these are calculated/derived fields not in source
2. **Missing Definitions**: Some fields have empty `Definition` column
3. **Legacy References**: Some definitions reference deprecated tables/fields
4. **Multi-line Definitions**: Some definitions span multiple lines (handle carefully in YAML)

## Future Enhancements

- [ ] Create dbt macro to auto-generate schema.yml from dictionary
- [ ] Add dbt test to validate staging columns exist in dictionary
- [ ] Parse dictionary at compile-time to inject descriptions
- [ ] Create reverse lookup: staging model → EDW entity mapping
- [ ] Integrate with dbt-expectations for data type validation

## Related Files

- **Dictionary Source**: `seeds/r1_edw_dictionary.csv` (1,084 rows)
- **Generator Script**: `.claude/quick-reference/generate_staging_yml_from_dictionary.py`
- **Staging Models**: `models/staging/edw/`
- **Confluence Source**: [EDW Data Dictionary](https://confluence.example.com) *(update with actual link)*

---

**Pro Tip**: Keep this dictionary in `seeds/` so it's version-controlled and available in dbt Cloud for reference during development!
