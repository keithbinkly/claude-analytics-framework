# Section Tab Navigation Standard

All `/data-story` visualizations with 3+ sections MUST include a sticky section tab bar.

Reference implementation: `disbursement-dossier-2025-02-22.html`

## Layout

- Tab bar is the **FIRST element** inside `.container` — BEFORE the hero, not after it
- `position: sticky; top: 0; z-index: 100`
- Frosted glass background: `rgba(15,17,23,0.92)` + `backdrop-filter: blur(12px)`
- Bottom border: `1px solid var(--surface-2)`
- Includes a `.nav-brand` label on the left (short title, e.g. "Geo Intel")

## Active vs Inactive Tabs

### Inactive tabs — plain text, no shape
```css
.toc a {
  color: var(--ink-dim);
  font-size: 12px; font-weight: 500;
  padding: 14px 10px;
  border-bottom: 2px solid transparent;
  /* NO background, NO border-radius, NO box-shadow */
}
.toc a:hover { color: var(--ink); }
```

### Active tab — accent text + bottom underline only
```css
.toc a.active {
  color: var(--positive);
  border-bottom-color: var(--positive);
  /* That's it. No background, no shadow, no raised shape. */
}
```

**Key principle:** Active tab is distinguished ONLY by accent color text and a 2px bottom border. No backgrounds, no shadows, no raised shapes, no `::before`/`::after` pseudo-elements.

## HTML Structure

```html
<nav class="toc" id="toc" aria-label="Section navigation">
  <span class="nav-brand">Short Title</span>
  <a href="#sec-map" class="active"><span class="tab-num">1</span> Map</a>
  <a href="#sec-other"><span class="tab-num">2</span> Other</a>
</nav>
```

- Use `<nav>` with `aria-label`
- Use `<a href="#sec-...">` elements (anchor links)
- First `<a>` gets `class="active"` on load
- `.tab-num` spans for numbered sections (optional)
- Labels: **1-2 words max**

## JavaScript Behavior

1. **Click handler:** `e.preventDefault()`, smooth scroll to section offset by tab bar height + 8px
2. **IntersectionObserver:** Auto-activates the tab for the currently visible section
3. **Scroll debounce:** `_isScrolling` flag (800ms) prevents observer from fighting click scrolls
4. **Tab bar auto-scroll:** Active tab scrolls into horizontal view via `scrollIntoView({ inline: 'center' })`

## Palette Switch Safety

- Tab bar uses CSS variables — PaletteModule switches update automatically
- **No rebuild needed** in `buildCharts()` — static HTML, not chart-dependent
- Frosted glass uses fixed `rgba()` for dark themes; switch to `var(--bg)` with opacity if light themes needed

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tabs start mid-page | Place `<nav>` BEFORE the hero, as first child of `.container` |
| All tabs have visible shapes/borders | Only `.active` gets accent color + bottom border |
| Active tab has background/shadow/radius | NO — just text color + 2px bottom line |
| Tab bar scrolls off screen | Must be `position: sticky; top: 0` |
| Opaque background looks flat | Use frosted glass: `rgba()` + `backdrop-filter: blur(12px)` |
