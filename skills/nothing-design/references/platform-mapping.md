# Nothing Design System — Platform Mapping

Use this file when turning the design language into real implementation details.

## 1. Raw web (HTML/CSS/JS)

### Fonts
- Load **Doto**, **Space Grotesk**, and **Space Mono** from a current Google Fonts
  snippet or self-host them if the project already self-hosts fonts.
- In the deliverable, state exactly which weights are required.

### CSS variable starter

```css
:root {
  --black: #000000;
  --surface: #111111;
  --surface-raised: #1A1A1A;
  --border: #222222;
  --border-visible: #333333;
  --text-disabled: #666666;
  --text-secondary: #999999;
  --text-primary: #E8E8E8;
  --text-display: #FFFFFF;
  --accent: #D71921;
  --accent-subtle: rgba(215, 25, 33, 0.15);
  --success: #4A9E5C;
  --warning: #D4A843;
  --interactive: #5B9BF6;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;
  --space-4xl: 96px;
}
```

### Implementation notes
- Prefer CSS custom properties over hard-coded one-off values.
- Use `rem` for type and `px` for borders, stroke-like details, and segmented bars.
- Support dark/light either with a class toggle or `prefers-color-scheme`.
- Avoid box-shadow and backdrop-filter as default styling tools.

## 2. React + Tailwind

### Mapping strategy
- Keep existing app logic and state.
- Add tokens through CSS variables in a global stylesheet or Tailwind theme extension.
- Use utility classes for spacing and layout, but keep the token names visible where possible.

### Recommended structure
- Typography classes:
  - body: `font-['Space_Grotesk']`
  - labels / metrics: `font-['Space_Mono']`
  - hero display: `font-['Doto']`
- Surfaces should be mostly flat: borders, background tone shifts, no shadows.
- Use one intentional visual accent per screen.

### Example direction
- `rounded-[16px]` for restrained cards
- `rounded-full` for pills and switches
- `tracking-[0.08em] uppercase` for labels
- `tabular-nums` and mono font for metrics
- segmented bars built from flex rows with square child divs and `gap-[2px]`

If the repo already defines a design token layer, map the semantics into that layer instead
of hard-coding new values everywhere.

## 3. SwiftUI / iOS

### Fonts
- Explain whether fonts must be bundled in the app, downloaded, or substituted.
- If custom fonts are unavailable, fall back to Space Grotesk / Space Mono equivalents
  already present in the project.

### Color and shape
- Model tokens as `Color` extensions or a small theme object.
- Use flat fills, borders, and shape overlays rather than shadows/material effects.
- Prefer `RoundedRectangle` and `Capsule` with restrained radii.

### Interaction
- Use the system's accessibility and hit-target behavior; do not shrink controls to fit the aesthetic.
- Keep animations subtle and mechanical, with no spring by default.

## 4. Design-tool outputs (Paper, Figma-like tools, mockup specs)

- Verify font availability before writing the spec.
- If the exact fonts are unavailable, specify fallback mapping explicitly.
- Separate dark and light mode as two artboards or variants rather than deriving one lazily from the other.
- Include the token values in the handoff, not just visual descriptions.

## 5. Editing existing code

When the user asks for implementation instead of concepting:

1. Inspect the existing stack and styling primitives first.
2. Change the minimum number of files needed.
3. Keep business logic and data flow intact unless the user requests architectural change.
4. Mention any new font, asset, or token dependency you introduced.
5. Preserve accessibility, responsiveness, and keyboard/focus behavior.
