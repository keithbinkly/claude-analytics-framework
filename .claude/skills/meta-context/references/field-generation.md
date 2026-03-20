# Context Field Generation Framework

When encountering business context that doesn't fit any existing schema field, use this framework to decide what to do.

## Four Tests

Every proposed new field must pass all four:

### Test 1: The Failure Test

**Question:** Does the absence of this context cause a *specific, identifiable* failure in LLM analytical reasoning?

- If yes → the field addresses a real gap
- If no → "nice to have" is not schema-worthy

**Method:** Construct a question where the answer depends on this context. Run WITH and WITHOUT. If the LLM's answer doesn't meaningfully change, the field doesn't earn its place.

### Test 2: The Decay Test

**Question:** Is this context at risk of being lost through personnel rotation, temporal drift, or inadequate storage?

- If easily re-derivable from data → belongs in automated metadata, not `meta:`
- If lives in experts' heads → belongs in the schema
- If documented elsewhere durably → reference it, don't duplicate

### Test 3: The Dual-Audience Test

**Question:** Is this field interpretable by both human analysts AND LLM agents?

- Both must parse and use the field
- Only humans can use it → documentation, not schema
- Only machines can use it → technical metadata, not business context

### Test 4: The Layer Fit Test

**Question:** Which layer's question does this context answer?

| Layer | Question |
|---|---|
| 1. Context | "Who cares and why does this exist?" |
| 2. Expectations | "What does good look like?" |
| 3. Investigation | "When it breaks, where do I look first?" |
| 4. Relationships | "What else moves when this moves?" |
| 5. Decisions | "What do I do about it?" |
| None → | New layer? Cross-cutting? Or out of scope? |

## Decision Tree

```
Does absence cause identifiable LLM failure?
├── NO → Don't add. Nice-to-have is not schema-worthy.
└── YES →
    Is this context at risk of decay?
    ├── NO → Reference existing source. Don't duplicate.
    └── YES →
        Is it interpretable by both humans and LLMs?
        ├── NO → Wrong format. Rework as natural language + typed structure.
        └── YES →
            Does it answer one of the 5 layer questions?
            ├── YES → Add to that layer. Use existing key patterns.
            └── NO →
                Is this a pattern across 3+ metrics?
                ├── NO → Document as metric-specific note, not schema field.
                └── YES → Propose as new field or layer. Validate with eval.
```

## Worked Example: Evaluating `data_freshness`

**Candidate:** `data_freshness: "Updated every 15 minutes via streaming pipeline"`

1. **Failure Test:** Does an LLM give wrong answers without knowing freshness? Sometimes — if asked "is this real-time?" But most analytical questions don't hinge on freshness. **Partial pass.**
2. **Decay Test:** Freshness is derivable from pipeline metadata. **Fail.** This is automated metadata.
3. **Dual-Audience Test:** Both can read it. **Pass.**
4. **Layer Fit Test:** Answers "what does this metric look like?" → Expectations? Not quite. It's about the *data*, not the *metric behavior*.

**Verdict:** Don't add. This is pipeline metadata belonging in dbt's `freshness:` config, not `meta:`.

## Worked Example: Evaluating `known_root_causes`

**Candidate:** `known_root_causes: [{date: "2025-11-15", description: "Black Friday carrier overwhelm", root_cause: "FedEx hub overflow", resolution: "Rerouted to UPS regional"}]`

1. **Failure Test:** Without this, an LLM investigating a November drop would miss that this exact pattern happened before. It would treat it as novel. **Pass.**
2. **Decay Test:** This lives in post-mortem docs and senior analyst memory. Both decay (docs get buried, analysts rotate). **Pass.**
3. **Dual-Audience Test:** Human-readable narrative + structured fields. **Pass.**
4. **Layer Fit Test:** "When it breaks, where do I look first?" → Layer 3 (Investigation). **Pass.**

**Verdict:** Add to Layer 3. Recommended tier (requires post-mortem archaeology to populate).
