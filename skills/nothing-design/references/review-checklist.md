# Nothing Design System — Review Checklist

Use this as the last pass before finalizing. Fix anything that fails.

## Activation and scope

- [ ] The user's request clearly matches a Nothing-inspired / industrial / monochrome / typography-led UI direction
- [ ] The deliverable stayed within the user's platform and scope
- [ ] Existing logic and IA were preserved unless the user asked for deeper redesign

## Hierarchy and composition

- [ ] The screen has one clear primary element
- [ ] Supporting information is secondary, not competing
- [ ] Labels / metadata are tertiary and edge-anchored where appropriate
- [ ] There is exactly one expressive moment, not several

## Typography

- [ ] Fonts are declared along with the platform-appropriate loading/setup method
- [ ] Doto is used only for display moments
- [ ] Labels are Space Mono-style, compact, and usually ALL CAPS
- [ ] Metrics and units read as a deliberate pair

## Tokens and components

- [ ] Exact values come from `references/tokens.md` or a sensible mapping into the host system
- [ ] Components match the patterns in `references/components.md`
- [ ] Grayscale carries most of the hierarchy
- [ ] Status colors are applied to values/signals, not sprayed across whole surfaces

## Style integrity

- [ ] No gradients, glossy glass, ornamental blur, or heavy shadows slipped in
- [ ] Tables avoid zebra striping
- [ ] Card radii stay restrained
- [ ] Motion is subtle and non-bouncy
- [ ] The result feels sparse and precise, not empty and underdesigned

## Accessibility and implementation quality

- [ ] Text contrast is strong in the chosen mode
- [ ] Focus states are visible
- [ ] Hit targets are at least 44px where interactive
- [ ] Code edits are localized and do not rewrite unrelated logic
- [ ] Assumptions, substitutions, or unresolved font constraints are stated clearly
