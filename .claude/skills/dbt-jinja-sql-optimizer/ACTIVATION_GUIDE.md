# Jinja SQL Optimizer Skill - Activation Guide

## How Skill Activation Works

There are **two mechanisms** that work together to activate this skill:

### 1. Automatic Activation (Built-in Claude Code)

Claude Code automatically scans `.claude/skills/` and reads the YAML frontmatter:

```yaml
# From SKILL.md frontmatter
triggers:
  - "jinja macro"
  - "optimize jinja"
  - "dbt macro"
  - "dynamic sql"
  - "sql generation"
  - "dbt-utils"
  - "codegen"
  - "template sql"
```

**How it works:**
1. User message contains ANY trigger keyword
2. Claude Code automatically loads `jinja-sql-optimizer/SKILL.md`
3. Skill context is available for answering

**Example:**
```
You: "How do I use dbt-utils pivot?"
     ↓
Claude Code detects "dbt-utils" keyword
     ↓
Loads jinja-sql-optimizer/SKILL.md (16 KB)
     ↓
Responds with pivot pattern from SKILL.md
```

---

### 2. Manual Keyword Rules (Explicit in CLAUDE.md)

For reliability, we **also** add explicit instructions in `CLAUDE.md`:

```markdown
### Jinja & SQL Generation Keywords
**Keywords:** jinja, macro, dbt macro, template, dynamic sql, dbt-utils,
              codegen, generate sql, pivot, union, surrogate key, etc.
**Action:** Read .claude/skills/jinja-sql-optimizer/SKILL.md
```

**Why both mechanisms?**
- **Automatic**: Fast, built-in to Claude Code
- **Manual**: Ensures reliability, provides context about WHEN to use skill
- **Together**: Best of both worlds - automatic detection + explicit guidance

---

## Activation Keywords (Complete List)

### Core Jinja Keywords
- `jinja`
- `macro`
- `dbt macro`
- `template`
- `for loop`
- `if statement`
- `control flow`

### SQL Generation Keywords
- `dynamic sql`
- `generate sql`
- `code generation`
- `repetitive sql`
- `refactor sql`

### Utility Package Keywords
- `dbt-utils`
- `codegen`
- `star()`
- `pivot`
- `union`
- `surrogate key`
- `date spine`
- `deduplicate`
- `generate_source`
- `generate_base_model`

### Use Case Keywords
- `optimize jinja`
- `create macro`
- `dynamic columns`
- `environment logic`

---

## Progressive Loading

The skill uses **progressive loading** to optimize token usage:

```
User Query with Keyword
        ↓
[ALWAYS LOADED]
  SKILL.md (16 KB)
  - Quick reference
  - Decision trees
  - Common patterns
        ↓
Need More Detail?
        ↓
[ON-DEMAND LOADING]
  references/jinja_basics.md (12 KB)
  references/dbt_functions.md (886 KB)
  references/utility_packages.md (627 B)
  references/advanced_jinja.md (152 KB)
  references/examples.md (151 KB)
```

**Claude automatically loads additional references when:**
- User asks for detailed documentation
- SKILL.md doesn't have enough info
- Complex use case requires deep examples

---

## Testing Skill Activation

### Test 1: Basic Keyword
```
You: "How do I use dbt-utils star()?"

Expected:
✅ Loads jinja-sql-optimizer/SKILL.md
✅ Provides star() example from SKILL.md
✅ Shows except parameter usage
```

### Test 2: Pattern Request
```
You: "Show me how to pivot payment methods dynamically"

Expected:
✅ Loads jinja-sql-optimizer/SKILL.md
✅ Provides Pattern 2: Pivot Operations
✅ Shows get_column_values + pivot example
```

### Test 3: Macro Creation
```
You: "Help me create a macro to convert cents to dollars"

Expected:
✅ Loads jinja-sql-optimizer/SKILL.md
✅ Shows macro creation template
✅ Provides cents_to_dollars example
```

### Test 4: Debugging
```
You: "My Jinja macro isn't working, how do I debug it?"

Expected:
✅ Loads jinja-sql-optimizer/SKILL.md
✅ Shows debugging tips section
✅ Mentions dbt compile, log(), --debug flag
```

---

## Activation Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ User Message: "How do I use dbt-utils pivot?"              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Keyword Detection                                  │
│                                                             │
│ Claude Code scans message for trigger keywords:            │
│ ✓ Found: "dbt-utils"                                       │
│ ✓ Found: "pivot"                                           │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Automatic Skill Loading                            │
│                                                             │
│ Claude Code reads:                                          │
│ .claude/skills/jinja-sql-optimizer/SKILL.md (16 KB)       │
│                                                             │
│ Frontmatter triggers matched ✓                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Check CLAUDE.md Instructions                       │
│                                                             │
│ CLAUDE.md lines 102-108:                                    │
│ "### Jinja & SQL Generation Keywords"                      │
│ → Confirms: Load jinja-sql-optimizer FIRST                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Response Generation                                │
│                                                             │
│ Claude uses SKILL.md to answer:                            │
│ - Checks "Pattern 2: Pivot Operations"                     │
│ - Provides code example                                     │
│ - Explains get_column_values + pivot combo                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: On-Demand Loading (if needed)                      │
│                                                             │
│ If user asks "Tell me more about pivot parameters"         │
│ → Claude loads references/utility_packages.md              │
│ → Provides detailed dbt-utils.pivot() documentation        │
└─────────────────────────────────────────────────────────────┘
```

---

## Skill Invocation Methods

### Method 1: Natural Language (Recommended)
```
"How do I create a Jinja macro?"
"Show me how to use dbt-utils star"
"Help me pivot these columns dynamically"
```
→ Claude automatically detects keywords and loads skill

### Method 2: Explicit Skill Call
```
"Use the jinja-sql-optimizer skill to help me..."
"Load the Jinja optimizer and show me..."
```
→ Direct skill invocation

### Method 3: Direct File Reference
```
"Read .claude/skills/jinja-sql-optimizer/SKILL.md"
```
→ Manual loading (useful for testing)

---

## Integration with Other Skills

The Jinja optimizer often works alongside:

### With dbt-migration
```
User: "Migrate this legacy SQL script"
      ↓
Loads: dbt-migration (analyzes script)
      ↓
User: "Refactor this repetitive CASE statement"
      ↓
Loads: jinja-sql-optimizer (creates macro)
```

### With redshift-optimization
```
User: "This query is slow"
      ↓
Loads: redshift-optimization (analyzes performance)
      ↓
User: "Generate surrogate keys for these columns"
      ↓
Loads: jinja-sql-optimizer (shows generate_surrogate_key)
```

### With dbt-style-evaluator
```
User: "Check the style of this model"
      ↓
Loads: dbt-style-evaluator (runs checks)
      ↓
User: "How do I extract this logic into a macro?"
      ↓
Loads: jinja-sql-optimizer (macro template)
```

---

## Troubleshooting Activation

### Problem: Skill not loading automatically

**Check:**
1. ✅ Is your message in the dbt-agent working directory?
2. ✅ Does your message contain a trigger keyword?
3. ✅ Is `.claude/skills/jinja-sql-optimizer/SKILL.md` present?

**Solution:**
```bash
# Verify skill file exists
ls -la /Users/kbinkly/git-repos/dbt-agent/.claude/skills/jinja-sql-optimizer/

# Should show:
# SKILL.md
# README.md
# skill_seeker_config.json
# references/
```

### Problem: Getting generic response instead of skill-specific

**Try:**
- Use more specific keywords: "dbt-utils pivot" instead of "pivot data"
- Explicitly mention skill: "Use the Jinja optimizer to..."
- Reference skill directly: "According to jinja-sql-optimizer..."

### Problem: Skill loads but missing information

**This is expected!** Progressive loading means:
- SKILL.md (16 KB) loads first - quick reference
- Additional references load on-demand

**Solution:**
```
"Load references/dbt_functions.md for more detail on ref()"
"What does the complete dbt-utils documentation say?"
```

---

## Keyword Expansion Opportunities

Consider adding these keywords in future updates:

### Additional Trigger Words
- `loop through columns`
- `conditional SQL`
- `environment variables`
- `target.name`
- `var()` function
- `ref()` and `source()`
- `statement blocks`
- `run_query`

### Use Case Keywords
- `reduce duplication`
- `DRY principle`
- `reusable SQL`
- `templated model`

### Update Process
1. Edit `SKILL.md` frontmatter `triggers:` section
2. Update `CLAUDE.md` keyword list
3. Test with new keywords
4. Document in ACTIVATION_GUIDE.md

---

## Summary

✅ **Automatic**: Claude Code scans for 8 trigger keywords in SKILL.md frontmatter
✅ **Manual**: CLAUDE.md provides explicit keyword rules (lines 102-108)
✅ **Progressive**: Loads 16 KB SKILL.md always, 9 MB references on-demand
✅ **Integrated**: Works alongside dbt-migration, redshift-optimization, etc.
✅ **Testable**: Try "How do I use dbt-utils star()?" to verify

**Result**: Skill activates reliably whenever user mentions Jinja, macros, dbt-utils, codegen, or related SQL generation topics!

---

**Last Updated**: 2025-11-03
**Related Files**:
- `.claude/skills/jinja-sql-optimizer/SKILL.md` (main skill)
- `CLAUDE.md` (lines 102-108, keyword rules)
- `.claude/skills/SKILLS_REGISTRY.md` (skill catalog)
