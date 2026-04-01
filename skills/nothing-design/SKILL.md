---
name: nothing-design
description: >-
  Use this skill when the user wants a Nothing-inspired interface or a monochrome,
  industrial, typography-led UI: OLED-black or off-white surfaces, Swiss-style
  structure, dot-matrix hero moments, segmented progress bars, instrument-like
  controls, or an explicit “Nothing style” / “Nothing design” request. Apply it
  when designing, restyling, or implementing screens in HTML/CSS, React/Tailwind,
  or SwiftUI. Do not use it for generic UI work unless the requested aesthetic
  clearly matches this visual language.
---

# Nothing-Inspired UI Design System

Use this skill to produce interfaces that feel monochrome, mechanical, typographic,
and precise. The goal is to capture the visual language faithfully, not to claim the
result is official Nothing software or branding.

## When to use this skill

Use it when the user:
- explicitly asks for Nothing style, Nothing design, or `/nothing-design`
- wants a monochrome, industrial, OLED-black or off-white interface
- wants dot-matrix hero moments, segmented indicators, or instrument-panel widgets
- wants dense but uncluttered data presentation
- wants to restyle an existing screen or app into this direction

Do **not** use it for generic "clean", "modern", or "minimal" UI unless the requested
traits clearly point to this aesthetic.

## Defaults and boundaries

- Match the existing platform or codebase. If the project is already React/Tailwind,
  SwiftUI, or plain web, stay in that stack.
- If the user did not specify dark or light mode and you need to deliver a one-shot
  draft, start with **dark mode** and note that the same token system supports light
  mode. If the choice is central to the task and conversation flow allows it, ask.
- Declare the required fonts and the correct loading method for the platform before
  or alongside the deliverable.
- Default typography uses **Geist Sans** for primary UI text, **Geist Mono** for
  labels, values, and technical accents, and **Geist Pixel** only for occasional
  display moments. Favor Geist Sans + Geist Mono as the everyday pair; treat Geist
  Pixel as a restrained accent, not a blanket identity layer.
- Avoid official Nothing logos, wordmarks, product renders, or proprietary brand
  assets unless the user provided them and asked to use them.
- When restyling existing product code, preserve information architecture, behavior,
  and business logic unless the user explicitly asks for deeper changes.

## Load references intentionally

Load only what you need:

- Read `references/tokens.md` before choosing exact typography, color, spacing,
  radius, border, or motion values.
- Read `references/components.md` when composing buttons, forms, lists, tables,
  navigation, overlays, or data widgets.
- Read `references/platform-mapping.md` before generating production code for web,
  React/Tailwind, SwiftUI, or design-tool outputs.
- Read `references/review-checklist.md` before finalizing any design, code, or
  restyle.

## Core craft rules

### 1) Three-layer hierarchy

Every screen should have exactly three levels of importance.

| Layer | Role | Typical treatment |
|---|---|---|
| Primary | The first thing the user sees | Large Geist Sans with an occasional Geist Pixel hero number or status readout, high contrast, generous breathing room |
| Secondary | Supporting context and useful adjacent information | Geist Sans at body or subheading scale |
| Tertiary | Metadata, navigation, labels, status framing | Geist Mono, lower contrast, edge-anchored; ALL CAPS only when it improves clarity |

Squint test: if two things compete for attention, one must shrink, fade, or move.

### 2) Type budget

Per screen, default to:
- **2 working families max**: Geist Sans + Geist Mono
- **Geist Pixel only for a rare hero or display accent**
- **3 font sizes max**
- **2 font weights max**

Before adding a new size or weight, try solving the problem with spacing, contrast, or alignment.

### 3) Spacing carries meaning

Use spacing as the main signal for relationships:

- **4-8px**: same unit
- **16px**: same group, different items
- **32-48px**: new group
- **64-96px**: new context

If you want a divider everywhere, the spacing rhythm is probably too weak.

### 4) Container strategy

Prefer the lightest possible separation, in this order:

1. spacing only
2. one divider line
3. subtle outline
4. raised surface

Do not trap the most important element inside a heavy card unless the task explicitly
needs enclosure.

### 5) Monochrome hierarchy first

Use grayscale for hierarchy. Red is an interrupt, not a decorative accent.

- `--text-display`: hero content
- `--text-primary`: main content
- `--text-secondary`: labels and metadata
- `--text-disabled`: hints and inactive states

Status colors are allowed when encoding data values. Color the **value**, not the label
or the whole row.

### 6) One expressive moment

Each screen gets **one** break from the pattern: a Geist Pixel clock or headline, a
circular instrument, a red signal, or an unusually large negative-space gap. More than
one expressive moment
turns the system noisy.

### 7) Asymmetry over symmetry

Favor edge anchoring, top-heavy compositions, and deliberate imbalance. Nothing-inspired
layouts should feel composed, not centered-and-generic.

### 8) Data form variation

When a screen contains multiple data sections, vary the visual form while keeping the
same voice. Example progression:

- one hero number
- one segmented progress bar or circular gauge
- one lighter stat row or sparkline block

The form changes; the tone stays monochrome, precise, and restrained.

## Anti-patterns

Never introduce these unless the user explicitly overrides the style system:

- gradients, glassmorphism, heavy blur, or decorative shadows
- oversized radii on cards
- zebra striping in tables
- colorful icon sets, filled icons, or emoji as interface chrome
- spring/bounce motion
- decorative red accents unrelated to urgency or status
- illustration-heavy empty states or chatty toast notifications

## Workflow

Track progress explicitly:

- [ ] Identify deliverable, platform, and whether this is net-new UI or a restyle
- [ ] Load the relevant reference files
- [ ] Name the primary, secondary, and tertiary layers
- [ ] Choose the single expressive moment
- [ ] Build the layout and component treatment
- [ ] Validate against `references/review-checklist.md`
- [ ] Deliver the artifact with assumptions called out

### For net-new screens

1. Start from hierarchy, not decoration.
2. Establish the main metric, headline, or state first.
3. Add only the supporting structure needed to explain that primary element.
4. Choose component patterns from `references/components.md`.
5. Apply exact tokens from `references/tokens.md`.

### For restyling existing screens

1. Keep the current user flow and content structure unless asked to redesign them.
2. Remove decorative chrome before adding new style.
3. Convert labels, metrics, and navigation into the Nothing voice.
4. Replace generic cards, charts, and toggles with the component treatments in
   `references/components.md`.
5. Preserve accessibility, spacing, and legibility while simplifying.

## Output contract

When you deliver work with this skill, include:

1. **Fonts + loading/setup** for the target platform
2. **Mode + assumptions** (dark/light, substitutions, constraints)
3. **The artifact itself** (code, spec, or edited file content)
4. **A short rationale** tied to hierarchy, expressive moment, and component choices
5. **Any unresolved substitutions** (for example, unavailable fonts on native platforms)

For code edits, prefer changing the fewest files needed. Do not rewrite unrelated logic.

## Gotchas

- Geist Pixel is display-only. Do not use it for body copy, long labels, dense forms, or
  repeated component headings across the interface.
- Geist Mono labels can use ALL CAPS sparingly, but default to readability over affect.
- Numeric readouts should normally use Geist Mono, with units visually smaller and adjacent.
- Most buttons, inputs, navigation, and dense UI should default to Geist Sans unless the
  text is intentionally technical or measurement-driven.
- Data visualizations should try opacity, pattern, or line style before adding more colors.
- Web output should include actual font-loading guidance, not just font names.
- Native output should explain whether fonts must be bundled, substituted, or downloaded,
  with Geist Pixel treated as the least portable option.
- Always keep visible focus states, 44px minimum hit targets, and strong text contrast.
- If the user wants a faithful *product* implementation, adapt the style to the existing
  component/API constraints instead of inventing a totally new architecture.

## Final self-check

Before finishing, read `references/review-checklist.md` and make sure the result passes
every applicable item.

## Reference files

- `references/tokens.md` — exact type, color, spacing, motion, and iconography tokens
- `references/components.md` — component and state patterns
- `references/platform-mapping.md` — implementation guidance for web, React/Tailwind,
  SwiftUI, and design-tool outputs
- `references/review-checklist.md` — validation checklist
