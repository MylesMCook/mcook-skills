# Nothing Design System — Components

Choose component patterns from here after the hierarchy is clear. The component should
support the information architecture, not become the star of the screen.

## 1. Cards and surfaces

- Background: `--surface` or `--surface-raised`
- Border: `1px solid var(--border)` or `var(--border-visible)` when the outline should read clearly
- Radius: 12-16px on cards, 8px compact, 4px technical
- Padding: 16-24px
- No shadows; separate surfaces with tone and border

Use cards when enclosure is useful. Do not wrap the primary hero element in a card by default.

## 2. Buttons

| Variant | Background | Border | Text | Radius |
|---|---|---|---|---|
| Primary | `--text-display` | none | `--black` | pill |
| Secondary | transparent | `1px solid var(--border-visible)` | `--text-primary` | pill |
| Ghost | transparent | none | `--text-secondary` | 0-8px |
| Destructive | transparent | `1px solid var(--accent)` | `--accent` | pill |

Shared rules:
- Font: Geist Sans by default; switch to Geist Mono only for highly technical controls
- Size: 13px or `--caption`
- Treatment: ALL CAPS, letter-spacing around `0.06em`
- Padding: around `12px 24px`
- Minimum height: 44px

## 3. Inputs and forms

- Prefer underline or thin-outline fields over heavy filled inputs
- Labels sit above fields in Geist Mono, `--text-secondary`; use ALL CAPS only when
  the extra rigidity helps clarity
- Input text can use Geist Sans for prose and Geist Mono for numeric or code-like data
- Focus should brighten the border; error states use `--accent`
- Avoid decorative helper text blocks; keep guidance short and inline

## 4. Lists and stat rows

- Dividers: `1px solid var(--border)`
- Row padding: 12-16px vertical
- Label: Geist Mono, `--text-secondary`
- Value: `--text-primary`, often right-aligned; use Geist Mono when the value is
  numeric or system-like
- No alternating row backgrounds

For hierarchical rows, indent sub-items instead of adding tree chrome.

## 5. Tables and data grids

- Header: Geist Mono labels, bottom border with `--border-visible`
- Numeric cells: Geist Mono, right-aligned
- Text cells: Geist Sans, left-aligned
- No zebra striping or colored cell backgrounds
- Active row can use `--surface-raised` plus a 2px accent or signal marker

## 6. Navigation

### Desktop
- Horizontal text bar, often edge-aligned
- Primary nav text should default to Geist Sans; reserve Geist Mono for utilities,
  counters, or compact technical rails
- Active item uses `--text-display`
- Inactive items use `--text-disabled` or `--text-secondary`

### Mobile
- Bottom bar or top text rail
- Labels default to Geist Sans; use Geist Mono sparingly if the rail needs a more
  technical feel
- Pair the active item with a dot, underline, or bracket treatment

### Back affordance
- 40-44px circular or rounded control
- Thin chevron, minimal chrome

## 7. Tags and segmented controls

### Tags / chips
- Border only, no filled color by default
- Geist Sans label by default; use Geist Mono when the chip reads like a status code,
  short measurement, or technical state
- Pill or technical 4px style depending on context

### Segmented controls
- Border container with 2-4 segments max
- Active segment uses inverted contrast
- Height: 36-44px
- Transition: subtle ease-out only

## 8. Toggles and switches

- Pill track with circular thumb
- Off: border-visible track, disabled thumb
- On: display text color track, black/off-white thumb
- Keep the gesture mechanical and obvious

## 9. Segmented progress bars

This is a signature Nothing-like data treatment.

Anatomy:
- label + value above
- discrete rectangular segments below
- square ends and 2px gaps
- numeric readout always paired with the bar

Suggested states:
- neutral: `--text-display`
- good: `--success`
- warning: `--warning`
- over-limit / urgent: `--accent`

Suggested heights:
- hero: 16-20px
- standard: 8-12px
- compact: 4-6px

## 10. Gauges, charts, and data widgets

Use chart forms sparingly and keep them technical:

- **Hero number**: use once per screen
- **Gauge / ring**: thin stroke, numeric readout adjacent or centered
- **Bar chart**: square-ended bars, monochrome remainder
- **Sparkline**: 1.5-2px line, minimal axis chrome
- **Dot grid / heatmap**: use opacity or density to encode value
- **Stat row**: label + value + compact trend mark

Always show the number alongside the visual.

## 11. Overlays and drawers

- Prefer sheets, drawers, or framed panels over glossy modals
- Background blur should be absent or minimal enough to remain effectively flat
- Overlay chrome should stay monochrome; avoid "floating glass" styling
- Header can carry the single expressive moment if the base screen is very restrained
- Use inline confirmation states where possible instead of stacking multiple modal steps

## 12. Empty, loading, saved, and error states

### Empty
- Short, matter-of-fact copy
- Optional dot-grid or mono illustration treatment, but keep it sparse

### Loading
- Use text or segmented indicators such as `[LOADING...]`
- Avoid skeleton shimmer placeholders

### Saved / success
- Prefer inline confirmations such as `[SAVED]`
- Green should signal state, not decorate the whole component

### Error
- Use concise inline messaging like `[ERROR: NETWORK TIMEOUT]`
- Accent red belongs on the message or signal marker, not the entire surface

## 13. Restyle mapping cheatsheet

When converting a generic UI into this design language:

- colorful badge -> monochrome chip or signal-colored value
- large filled card grid -> open layout with one or two restrained surfaces
- standard slider -> segmented control / bar / technical toggle when appropriate
- soft dashboard chart -> sharper instrument-style chart with visible numeric readout
- verbose helper copy -> shorter labels + clearer hierarchy
