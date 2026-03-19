# Graph Search on Task Start

## When to Query the Knowledge Graph

Before planning or implementing, query the unified KG to surface related learnings, traces, rules, and skills.

### Explicit Triggers (user says these)

- "search for relevant context"
- "check for context"
- "what do we know about X"
- "have we done this before"
- "inform our approach/plan"

### Implicit Triggers (detect task transitions)

- "ok now let's work on X"
- "switching to X"
- "next up: X"
- "let's start on X"
- Starting a new pipeline, model, or feature

### How to Query

```bash
python3 knowledge/platform/graph/graph_search.py "<task keywords>" --max 5
```

Extract 2-4 keywords from the task description. For pipeline work, include the pipeline name and domain terms.

### What to Do With Results

1. Briefly summarize what the graph found (1-3 sentences)
2. Flag anything directly relevant: "We hit this exact issue before — efx-007 says use delete+insert"
3. Note related skills that should be loaded
4. If nothing relevant found, say so and proceed

### When NOT to Query

- Quick fixes, typos, formatting
- Continuing work already in progress (context is loaded)
- Simple Q&A that doesn't involve planning or building
- User explicitly says to skip and just do it
