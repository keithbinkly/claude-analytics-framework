# Self-Verify HTML Changes Before Reporting Done

## When This Applies

After editing any HTML visualization, data story, or interactive page — before telling the user the change is complete.

## Required Verification Steps

After making changes, check your own work:

1. **Functions called?** Every new or modified function must be actually invoked. Search for `function NAME` and confirm `NAME(` appears in a call site (not just the definition).

2. **Data paths valid?** If referencing a data file, JSON key, or TopoJSON `objects.*` property, confirm the key exists in the actual data structure. Don't assume — read the file or the fetch response format.

3. **CDN URLs resolve?** If adding or changing a library CDN URL, verify the URL pattern is correct for that library and version. Don't guess version numbers.

4. **Elements visible?** Check for CSS that would hide new elements: `display: none`, `opacity: 0`, `height: 0`, `visibility: hidden`, or a parent with `overflow: hidden` that clips children.

5. **Event wiring complete?** If adding interactive elements (buttons, sliders, dropdowns), confirm the event listener is attached and the handler function exists.

6. **Screenshot verify?** For dashboards, maps, or multi-panel layouts — code review alone misses rendering issues (alignment, overflow, label truncation, color contrast, empty space). Serve the page locally and screenshot with Chrome headless:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless=new --disable-gpu --no-sandbox --virtual-time-budget=5000 \
  --screenshot=/tmp/verify.png --window-size=1440,900 \
  "http://localhost:<port>/<path>" 2>/dev/null
```
Read the screenshot and check the render matches intent before reporting done.

## How to Report

After verification, state what you checked:

```
Changes made: [what changed]
Verified: functions called, data keys match, elements visible
```

If you find an issue during self-verification, fix it before reporting — don't report the change and the bug separately.

## Why This Exists

Across 133 sessions, the most common friction pattern was: Claude edits HTML, reports done, user discovers a rendering bug (uncalled function, wrong data key, blank chart area). The user should never be the one catching mechanical errors that a code review would find.
