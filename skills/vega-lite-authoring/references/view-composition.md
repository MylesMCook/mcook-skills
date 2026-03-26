# Vega-Lite View Composition

Purpose: Composition guidance for `layer`, `facet`, `concat`, `repeat`, and `resolve`.

## Stable rules

- Prove a single-view spec first, then compose.
- Use `layer` when multiple marks share the same base view and dataset context.
- Use `facet` for repeated small multiples driven by field values.
- Use `concat` for manually arranged sibling views.
- Use `repeat` when the same view pattern should be reused across multiple fields.
- Use `resolve` only when default shared scales, axes, or legends are wrong for the intended comparison.

## Common failure modes

- Reaching for `layer` when the real need is `facet` or `concat`.
- Forgetting that composition changes how scales, legends, and sizing behave.
- Applying `resolve` blindly and making comparisons harder instead of clearer.
- Duplicating transforms or params across child views without a clear reason.
- Making a composed view impossible to debug because the base single view never worked cleanly.

## Safe defaults

- Start with one validated child view and duplicate it only when the operator is clear.
- Keep shared scales and legends unless comparison quality or clutter forces independence.
- Use `facet` for data-driven repetition and `repeat` for field-driven repetition.
- Add `resolve` explicitly only for the channels that need different behavior.
- Keep titles, spacing, and layout overrides minimal until the composed chart works.

## Version caveats

- Composition syntax follows the active Vega-Lite runtime.
- Hosts may clip, resize, or validate multi-view charts differently than the online editor.

## Source URLs

- https://vega.github.io/vega-lite/docs/layer.html
- https://vega.github.io/vega-lite/docs/facet.html
- https://vega.github.io/vega-lite/docs/concat.html
- https://vega.github.io/vega-lite/docs/repeat.html
- https://vega.github.io/vega-lite/docs/resolve.html

## Verified version/date

- Vega-Lite composition docs checked 2026-03-26.
