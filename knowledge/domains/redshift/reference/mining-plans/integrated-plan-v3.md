# Enterprise SQL Corpus Mining: Integrated Plan v3

**Status:** Post-Adversarial Review (Converged)
**Date:** 2026-01-15
**Integrates:** v2 + Gemini 3 Pro Review + GPT 5.2 Review

---

## What Changed from v2 → v3

| Gap | Source | Fix Applied |
|-----|--------|-------------|
| Expensive staleness signals | Gemini | Added Stage 0.5 heuristic pre-filter |
| Context window waste | Gemini | LSH similarity batching (not folder) |
| Dedup threshold missing | Gemini | MinHash @ 0.85; variants preserved |
| Shadow schemas ignored | Gemini | `shadow_inventory.json` for unmodeled tables |
| PII/secrets exposure | Gemini | Regex scrubber before API calls |
| sqlglot fallback risky | GPT-5.2 | Added `parse_quality` fields + confidence caps |
| Redshift coverage unclear | GPT-5.2 | Explicit constructs checklist |
| Query log mapping undefined | GPT-5.2 | Fingerprinting + log window parameter |
| Staleness weighting missing | GPT-5.2 | Deterministic scoring + poison pills |
| Concept taxonomy sprawl | Both | Hybrid seeding (20-50 seed + guarded induction) |
| Conflict review overload | Both | Auto-resolve ≥90% + active + non-sensitive |
| "amount" disambiguation | GPT-5.2 | Explicit heuristic ladder |
| Test over-generation | GPT-5.2 | rule_type classification |
| Chunking beyond CTEs | GPT-5.2 | Statement boundaries + state header |

---

## Executive Summary

We have ~42,000 legacy SQL files. **89% is noise.** After filtering: **~4,600 actionable files.**

| Stage | Files | Notes |
|-------|-------|-------|
| Raw corpus | 42,287 | Eng ETL + BIA folders |
| After filtering | ~4,600 | Remove stale releases, archives |
| Phase 1 scope | ~1,300 | Prove approach first |

**Goal:** Extract semantic infrastructure that makes AI agents 10x more effective at enterprise data work.

---

## Part 1: Scope (Unchanged from v2)

### Keeping (~4,600 files)

| Source | Files | Priority |
|--------|-------|----------|
| MSTR SQL | 435 | P0 |
| BIA Library/Current | 352 | P0 |
| BIA RPT_tickets | 239 | P0 |
| greendot/master/Objects | 532 | P1 |
| bau/data feeds | 883 | P1 |
| bau/Objects | 788 | P1 |
| Partner folders | 956 | P1 |

### Excluding (~37,600 files)

| Source | Files | Reason |
|--------|-------|--------|
| greendot/releases | 32,746 | 2015-2017 snapshots |
| Script Library/Archive | 1,784 | Explicitly archived |
| Informatica legacy | 85+ | ETL artifacts |

---

## Part 2: Phased Execution (UPDATED)

```
Stage 0.5: Heuristic Pre-Filter (NEW - per Gemini)
├── Regex scan for hardcoded dates in comments: "Created: 201X", "Copyright 201X"
├── Grep for obsolete WHERE clauses: "WHERE date < '2020..."
├── Detect deprecated syntax/UDFs (known legacy markers)
├── Output: pre_filter_flags.json (cheap signals only)
└── Purpose: Reduce Phase 0 load by 30-50%

Phase 0: Temporal Classification
├── Cross-reference with query logs (fingerprint matching)
├── Flag deprecated table references (DDL check)
├── Apply weighted scoring model (see Part 5)
├── Output: Files with temporal_status + score_breakdown
└── Scope: All files not pre-filtered as "historical"

Phase 1: Prove Approach (~1,300 files)
├── MSTR SQL (350)
├── BIA Script Library/Current (352)
├── BIA RPT_tickets (239)
├── BI Library (364)
├── Use LSH batching for context efficiency (NEW)
└── Validate extraction pipeline before scaling

Phase 2: Expand (+3,200 files)
├── greendot/master/Objects (532)
├── bau/data feeds (883)
├── bau/Objects (788)
└── Partner folders (956)

Phase 3: Consolidation
├── Merge patterns, resolve conflicts
├── Generate dbt test candidates (with rule_type)
├── Create shadow_inventory.json for unmodeled tables
└── Integrate into Knowledge Graph
```

---

## Part 3: Architecture (UPDATED)

### Agent Squad

| Agent | Model | Phase | Output |
|-------|-------|-------|--------|
| **Orchestrator** | Claude Opus 4.5 | All | Coordination, conflict triage |
| **Pre-Filter** | Regex (no LLM) | 0.5 | pre_filter_flags.json |
| **Scrubber** | Regex (no LLM) | Before all API | Sanitized SQL (PII/secrets removed) |
| **Discovery** | Gemini 3 Pro | 0-1 | inventory.json with temporal_status |
| **Extraction** | GPT-5.2-Codex | 1-2 | patterns.yaml with parse_quality |
| **Interpretation** | Claude Opus | 2-3 | logic_spec.json, business_concepts.yaml |
| **Consolidation** | Claude Opus | 3 | KG chunks, shadow_inventory.json |

### Scrubber Patterns (NEW - per Gemini)

Before ANY file is sent to LLM API:

```python
SCRUB_PATTERNS = [
    r"(?i)password\s*=\s*['\"]?[^'\";\s]+",  # Passwords
    r"(?i)credentials\s*['\"]?[^'\";\s]+",    # AWS credentials
    r"\b\d{3}-\d{2}-\d{4}\b",                 # SSN
    r"\b\d{16}\b",                             # Credit card
    r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", # IP addresses
    r"(?i)iam_role\s*['\"]arn:[^'\"]+",       # IAM roles (keep structure, redact ARN)
]
# Replace with <REDACTED:type>
```

### Context Window Strategy (NEW - per Gemini)

**Don't batch by folder. Batch by LSH similarity.**

1. Run MinHash LSH on all 4,600 files (structural similarity)
2. Group files with Jaccard ≥ 0.85 into clusters
3. Feed clusters of 50-200 files into Gemini's 1M context
4. Ask: "Find the invariant logic common to ALL these files"
5. This performs extraction AND concept induction simultaneously

---

## Part 4: Temporal Classification (UPDATED)

### Weighted Scoring Model (NEW - per GPT-5.2)

```python
def calculate_temporal_score(file):
    score = 0.0
    breakdown = {}

    # Query log match (strongest signal)
    if file.in_query_logs(window_days=90):
        score += 0.4
        breakdown['query_log_90d'] = 0.4
    elif file.in_query_logs(window_days=180):
        score += 0.25
        breakdown['query_log_180d'] = 0.25

    # Recent modification
    if file.modified_within_days(365):
        score += 0.2
        breakdown['recent_mod'] = 0.2

    # DDL exists for all referenced tables
    if file.all_tables_exist_in_ddl():
        score += 0.25
        breakdown['ddl_exists'] = 0.25

    # Folder trust (curated sources)
    if file.path.startswith('BIA_Script_Library/Current'):
        score += 0.15
        breakdown['folder_trust'] = 0.15

    return score, breakdown

def classify_status(score, signals):
    # Poison pills override everything
    if 'deprecated_schema_ref' in signals:
        return 'stale', 0.9
    if 'releases_folder' in signals:
        return 'historical', 1.0
    if 'hardcoded_old_date' in signals:
        return 'stale', 0.7

    # Score-based classification
    if score >= 0.6:
        return 'active', score
    elif score >= 0.3:
        return 'deprecated', score
    else:
        return 'stale', 1 - score
```

### Query Log Fingerprinting (NEW - per GPT-5.2)

```python
def fingerprint_sql(sql_text):
    """Create normalized fingerprint for query log matching."""
    normalized = sql_text.lower()
    normalized = re.sub(r'--.*$', '', normalized, flags=re.MULTILINE)  # Strip comments
    normalized = re.sub(r'/\*.*?\*/', '', normalized, flags=re.DOTALL)  # Strip block comments
    normalized = re.sub(r'\s+', ' ', normalized)  # Normalize whitespace
    normalized = re.sub(r"'[^']*'", "'?'", normalized)  # Normalize string literals
    normalized = re.sub(r'\b\d+\b', '?', normalized)  # Normalize numbers
    return hashlib.md5(normalized.encode()).hexdigest()
```

---

## Part 5: Pattern Extraction (UPDATED)

### Parse Quality Tracking (NEW - per GPT-5.2)

```yaml
# Added to patterns.schema.json
parse_metadata:
  parse_engine: sqlglot_redshift | sqlglot_postgres | regex | hybrid
  parse_quality: full_ast | partial_ast | surface_regex
  confidence_cap:
    full_ast: 1.0
    partial_ast: 0.8
    surface_regex: 0.6
  unparsed_snippets:
    - location: "lines 45-52"
      reason: "COPY command with IAM_ROLE"
      verbatim: "COPY table FROM 's3://...' IAM_ROLE <REDACTED>"
```

**Hard Rule:** No pattern enters consolidated registry unless:
1. Successful Redshift AST parse, OR
2. Successful statement-level parse with bounded extraction

### Redshift Constructs Checklist (NEW - per GPT-5.2)

| Category | Constructs | Detection Method |
|----------|------------|------------------|
| **Table Design** | DISTKEY, SORTKEY, INTERLEAVED, DISTSTYLE, ENCODE | Regex + AST |
| **Data Movement** | COPY, UNLOAD, manifest, IAM_ROLE | Regex (AST often fails) |
| **Time Functions** | DATEADD, DATEDIFF, GETDATE, SYSDATE | AST |
| **Idioms** | NVL, DECODE, LISTAGG, QUALIFY | AST (may need fallback) |
| **Semi-structured** | json_extract_path_text, json_parse, SUPER | Regex + partial AST |
| **Staging** | CREATE TABLE AS, temp tables, BEGIN/END | Statement boundary detection |

If construct detected but not parsed → store verbatim snippet with location.

### Chunking Strategy (UPDATED - per GPT-5.2)

**Don't assume CTE-based structure.**

```python
def chunk_large_file(sql_text):
    """Chunk by statement boundaries, not just CTEs."""
    chunks = []
    state_header = {
        'temp_tables': [],
        'session_vars': [],
        'file_context': filename
    }

    # Split by statement boundaries
    statements = split_by_semicolon_aware(sql_text)

    for stmt in statements:
        # Track state across statements
        if is_temp_table_create(stmt):
            state_header['temp_tables'].append(extract_table_name(stmt))

        chunks.append({
            'sql': stmt,
            'state_header': state_header.copy(),
            'statement_type': classify_statement(stmt)
        })

    return chunks
```

---

## Part 6: Business Concepts (UPDATED)

### Hybrid Seeding Strategy (NEW - per Both)

**Phase 1: Seed 20-50 High-Leverage Concepts**

```yaml
# business_concepts_seed.yaml
seeded_concepts:
  - id: owned_product_filter
    canonical_name: "Owned Product Filter"
    definition: "Excludes TPG, DS partnerships"
    domain: finance

  - id: active_account
    canonical_name: "Active Account"
    definition: "Transaction in trailing 30 days"
    domain: operations

  - id: interchange_fee
    canonical_name: "Interchange Fee"
    definition: "Card network transaction fee"
    domain: finance

  # ... 17-47 more core concepts
```

**Phase 2: Guarded Induction**

Allow new concepts ONLY when:
- Frequency ≥ 50 occurrences
- Appears in ≥ 2 source folders
- Has stable SQL signature (low variance)
- Links to at least one seeded domain
- Includes negative examples ("what it is NOT")

```yaml
# Induced concept example
induced_concepts:
  - id: induced_merchant_tier
    canonical_name: "Merchant Tier Classification"
    induced_from_cluster: "cluster_47"
    frequency: 73
    sources: [MSTR_SQL, BIA_Library]
    links_to_seeded: [interchange_fee, owned_product_filter]
    negative_examples:
      - "NOT merchant_category (MCC is separate)"
      - "NOT merchant_id (this is classification, not identity)"
    induction_confidence: 0.78
    status: pending_review  # Human must approve
```

---

## Part 7: Conflict Resolution (UPDATED)

### Auto-Resolution Rules (NEW - per Both)

```python
def can_auto_resolve(conflict):
    """Determine if conflict can be auto-resolved."""
    dominant = max(conflict.meanings, key=lambda m: m.frequency)
    total = sum(m.frequency for m in conflict.meanings)
    dominance_ratio = dominant.frequency / total

    # All conditions must be true
    conditions = [
        dominance_ratio >= 0.90,  # ≥90% dominance
        dominant.champion_status == 'active',  # Champion is active
        dominant.confidence >= 0.7,  # High confidence
        conflict.domain not in ['risk', 'compliance', 'pii'],  # Non-sensitive
    ]

    return all(conditions)

def resolve_conflict(conflict):
    if can_auto_resolve(conflict):
        return {
            'decision': 'auto_resolved',
            'chosen_meaning': dominant.concept,
            'action': f"Standardize to {dominant.concept}",
            'migration_notes': generate_migration_notes(conflict),
            'requires_review': False
        }
    else:
        return {
            'decision': 'pending_human_review',
            'recommended_meaning': dominant.concept,
            'confidence': dominance_ratio,
            'requires_review': True
        }
```

### Alias Disambiguation Ladder (NEW - per GPT-5.2)

For ambiguous aliases like "amount":

```yaml
disambiguation_heuristics:
  1_column_lineage:
    description: "Check source table column"
    example: "If from fee_table.amount → fee_amount"
    confidence: 0.95

  2_join_context:
    description: "Check joined tables"
    example: "Joined to interchange_rates → interchange_amount"
    confidence: 0.85

  3_arithmetic_context:
    description: "Check nearby operations"
    example: "Multiplied by basis_points → fee calculation"
    confidence: 0.75

  4_naming_context:
    description: "Check file/folder/report name"
    example: "File: Fee_Analysis.sql → fee_amount"
    confidence: 0.65

  5_aggregation_pattern:
    description: "Check aggregation style"
    example: "SUM with net/gross pattern → transaction_amount"
    confidence: 0.55
```

Store `disambiguation_evidence` in conflict files.

---

## Part 8: Test Generation (UPDATED)

### Rule Type Classification (NEW - per GPT-5.2)

```yaml
# Added to patterns.schema.json for business_filters
rule_classification:
  type: business_policy | data_quality | performance_window | operational_exception
  evidence_score: 0.0-1.0
  evidence_sources:
    - frequency_across_sources
    - appears_in_curated_folders
    - corroborated_by_comments
    - ticket_context_match
```

**Only auto-suggest dbt tests for:**
- `rule_type: business_policy`
- `evidence_score >= 0.7`

Everything else becomes:
- Audit queries (data_quality)
- Documentation notes (performance_window, operational_exception)

---

## Part 9: Shadow Assets (NEW - per Gemini)

### Shadow Inventory

Tables referenced in SQL but NOT in dbt manifest:

```json
// shadow_inventory.json
{
  "shadow_assets": [
    {
      "table": "analytics.legacy_merchant_mapping",
      "reference_count": 47,
      "source_files": ["Revenue Report.sql", "Merchant Analysis.sql"],
      "status": "unmodeled",
      "priority": "high",
      "recommended_action": "Create dbt source definition",
      "notes": "Active in query logs, appears in P0 scripts"
    }
  ],
  "summary": {
    "total_shadow_tables": 23,
    "high_priority": 8,
    "medium_priority": 10,
    "low_priority": 5
  }
}
```

**These are the highest-priority candidates for new dbt models.**

---

## Part 10: Deduplication (UPDATED - per Gemini)

### MinHash LSH Strategy

```python
SIMILARITY_THRESHOLDS = {
    'exact_match': 1.0,      # Discard duplicate
    'high_similarity': 0.85,  # Preserve as "variant"
    'distinct': 0.0           # Treat as separate
}

def deduplicate_files(files):
    lsh = MinHashLSH(threshold=0.85, num_perm=128)

    for file in files:
        minhash = compute_minhash(file.normalized_sql)

        # Check for similar files
        similar = lsh.query(minhash)

        if similar:
            # High similarity → variant
            primary = similar[0]
            file.status = 'variant'
            file.variant_of = primary.path
            file.diff_from_primary = compute_diff(primary, file)
            # Extract diff as potential Logic Spec annotation
        else:
            # Distinct file
            lsh.insert(file.path, minhash)
            file.status = 'primary'

    return files
```

---

## Part 11: Output Schemas (UPDATED)

### New Fields Added

| Schema | New Fields |
|--------|------------|
| `inventory.schema.json` | `pre_filter_flags`, `temporal_score_breakdown` |
| `patterns.schema.json` | `parse_metadata`, `rule_classification`, `disambiguation_evidence` |
| `conflict.schema.json` | `auto_resolution_eligible`, `dominance_ratio` |

### New Outputs

| File | Purpose |
|------|---------|
| `pre_filter_flags.json` | Stage 0.5 heuristic results |
| `shadow_inventory.json` | Unmodeled tables (high priority for dbt) |
| `business_concepts_seed.yaml` | 20-50 seeded concepts |
| `lsh_clusters.json` | Similarity-based file groupings |

---

## Part 12: Success Metrics (UPDATED)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Files inventoried | 4,600+ | With temporal classification |
| Pre-filter accuracy | 95%+ | Heuristics vs full classification |
| Temporal classification accuracy | 90%+ | Validated against query logs |
| Parse quality: full_ast | 70%+ | Files fully parsed |
| Unique patterns extracted | 500+ | Deduplicated (0.85 threshold) |
| Patterns mapped to concepts | 80%+ | Not orphaned |
| Shadow assets identified | 20+ | Tables needing dbt models |
| Conflicts auto-resolved | 40%+ | High-confidence cases |
| dbt test candidates (business_policy) | 20+ | With evidence_score ≥ 0.7 |
| PII/secrets scrubbed | 100% | Zero exposure to LLM APIs |

---

## Appendix: Convergence Declaration

**GPT 5.2 Issues:** 9 raised → 9 addressed
**Gemini 3 Pro Issues:** 5 raised → 5 addressed
**Overlapping Issues:** 3 (concept seeding, conflict resolution, dedup)

**Status: CONVERGED**

All substantive issues have been incorporated. Remaining differences are implementation details, not architectural gaps.

---

**Ready for execution.**
