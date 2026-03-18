# Extended Thinking Guide

**Created:** 2025-12-28

## Overview

Extended thinking allows Claude to reason through complex problems before responding. This guide documents when and how to apply it in the dbt-agent workflow.

## Current Status

- **Opus 4.5**: Thinking enabled by default (since Claude Code v2.0.67)
- **Toggle**: `Alt+T` in Claude Code (changed from Tab in v2.0.72)
- **API**: `thinking: { type: "enabled", budget_tokens: 10000 }`

## When to Use Extended Thinking

### High Value (Always Recommended)

| Task Type | Why Thinking Helps |
|-----------|-------------------|
| **Architecture Design** | Multi-factor tradeoff analysis |
| **QA Strategy** | Edge case identification |
| **Migration Planning** | Dependency mapping, risk assessment |
| **SQL Optimization** | Query plan reasoning |
| **Code Review** | Pattern recognition across contexts |

### Medium Value (Optional)

| Task Type | Consider When |
|-----------|---------------|
| **Data Discovery** | Complex schema relationships |
| **Pattern Learning** | Cross-session insight synthesis |
| **Orchestration** | Multi-agent coordination decisions |

### Low Value (Skip)

| Task Type | Why Skip |
|-----------|----------|
| **Simple Lookups** | Adds latency without benefit |
| **Status Checks** | Deterministic operations |
| **File Operations** | No reasoning required |

## Agent Command Recommendations

```
HIGH THINKING VALUE:
  /architect       - Design decisions require multi-factor reasoning
  /qa-agent        - Validation logic benefits from edge case thinking
  /migration-agent - Transformation planning needs dependency analysis
  /analyst-agent   - Data analysis requires pattern synthesis

MEDIUM THINKING VALUE:
  /orchestrator    - Coordination logic (enable for complex workflows)
  /discovery-agent - Schema analysis (enable for complex sources)
  /learner         - Pattern extraction (enable for cross-session synthesis)

LOW THINKING VALUE (DISABLE):
  /check-join      - Simple registry lookup
  /check-mail      - Status check only
```

## How to Apply

### Per-Session Control

Press `Alt+T` to toggle thinking on/off during a session.

### Per-Request Control (API)

```python
# Enable with budget
thinking: {
    "type": "enabled",
    "budget_tokens": 10000  # Adjust based on complexity
}

# Disable
thinking: {
    "type": "disabled"
}
```

### Budget Guidelines

| Complexity | Budget Tokens | Example |
|------------|--------------|---------|
| Simple | 5,000 | Single model optimization |
| Medium | 10,000 | Multi-model pipeline |
| Complex | 25,000+ | Full architecture design |

## Interleaved Thinking (Beta)

For tool-using workflows, interleaved thinking allows reasoning between tool calls:

```
# Requires beta header
anthropic-beta: interleaved-thinking-2025-05-14
```

Benefits:
- Reasoning preserved across tool boundaries
- Better decision-making on multi-step tasks
- Useful for agent workflows with many tool calls

## Cost Considerations

- Thinking tokens count toward input token limits
- Thinking is not cached (repeated each request)
- Use minimum necessary budget for cost efficiency

## Metrics to Track

When evaluating thinking effectiveness:

1. **Decision Quality** - Are architectural choices better?
2. **Error Reduction** - Fewer iterations to correct solution?
3. **Latency Impact** - Acceptable response time increase?

## Related

- [Claude Code Changelog](https://claude.com/changelog)
- [Anthropic Extended Thinking Docs](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
