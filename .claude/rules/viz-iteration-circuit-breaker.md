# Visualization Iteration Circuit Breaker

## Applies To
All HTML visualization work: ECharts, D3, Canvas, scrollytelling, maps, dashboards, any rendered output.

## The Pattern That Wastes Hours

```
Claude tries fix A → doesn't work → tries fix B → doesn't work → tries fix C → ...
→ User says "step back and think about this differently"
→ Claude researches, finds the actual root cause → fix works
```

The user should NEVER have to be the one who says "step back." That's Claude's job.

## Hard Rule: 2 Strikes → Research

After **2 failed fix attempts** on the same visual issue (rendering bug, layout problem, animation glitch, map not loading, chart not appearing):

1. **STOP fixing.** Do not attempt a third code change.

2. **Enumerate assumptions.** List every assumption being made about:
   - The library version and API being used
   - The data format and shape
   - The rendering lifecycle (when things initialize, load, resize)
   - The execution context (file:// vs http://, module vs script, async timing)

3. **Research.** Use Exa/Perplexity to search for:
   - The specific error + library name + version
   - The specific API being used (verify it works how you think it does)
   - Known issues, breaking changes, or migration gotchas

4. **Check memory.** Search auto-memory for known fixes:
   - ECharts map rendering: `MEMORY.md` has verified fix patterns
   - Past decision traces for similar issues

5. **Present the diagnosis** to the user before writing any more code:
   - "I've tried X and Y. Research shows the actual issue is likely Z because..."
   - Get alignment, THEN implement

## What Counts as a "Failed Attempt"

- You edit code to fix a rendering issue → user reports it's still broken
- You edit code to fix a rendering issue → you serve/check it and it's still broken
- You edit code → a different thing breaks (regression)

What does NOT count:
- Iterating on design/aesthetics (color tweaks, spacing, layout preferences) — that's normal iteration
- First attempt at building something new (no prior failure)

## Why Research Works

The user's observation is empirically correct: web research unlocks fixes that trial-and-error doesn't. This is because:

- **Library APIs have subtleties** that aren't in pre-training data (version-specific behavior, undocumented gotchas, CORS/protocol edge cases)
- **The bug is often in an assumption**, not the code — research challenges assumptions, more code doesn't
- **Stack Overflow / GitHub issues** contain the exact error + solution from someone who already solved it

## Examples from Real Sessions

| Issue | Failed Attempts | What Research Found |
|-------|----------------|-------------------|
| Map blank after TopoJSON fix | 3 CDN/format attempts | Wrong `objects` key in TopoJSON spec |
| ECharts areaColor ignored | 2 style attempts | `visualMap` overrides per-item colors |
| Scroll animation TDZ crash | 2 reorder attempts | Observer callback fires before class initialized |
| fetch() silently failing | 2 URL/CORS attempts | file:// protocol blocks all fetch() |

## The Anti-Pattern to Avoid

"Let me try one more thing" after 2 failures is the most expensive sentence in visualization work. It's always faster to research for 2 minutes than to guess for 20.
