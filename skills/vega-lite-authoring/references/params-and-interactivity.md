# Vega-Lite Params and Interactivity

Purpose: First-class guidance for top-level params, selections, predicates, and interaction-driven encoding.

## Stable rules

- Define interaction state with top-level `params`.
- Distinguish simple variable params from selection params.
- Use variable params for reusable values or expressions.
- Use selection params when user interaction should filter, highlight, or condition encodings.
- Keep params close to the interaction goal: one clear responsibility per param.

## Common failure modes

- Treating params as ad hoc mark options instead of top-level state.
- Using a selection param when a simple variable param would be clearer.
- Duplicating params across composed views instead of sharing intentionally.
- Forgetting that predicates and conditions can reference params directly.
- Escalating to raw Vega before exhausting standard Vega-Lite param patterns.

## Safe defaults

- Start with one param at a time and prove its effect on a minimal chart.
- Use selection params for highlight/filter interactions and variable params for configurable thresholds or toggles.
- Keep selection names stable and descriptive.
- Combine params with conditional encodings before introducing heavier transform logic.
- If interaction changes multiple views, decide explicitly whether the param is shared across them.

## Version caveats

- Param behavior follows the active Vega-Lite runtime.
- Embedded hosts may lag newer param features or surface compiled behavior differently than the online editor.

## Source URLs

- https://vega.github.io/vega-lite/docs/parameter.html
- https://vega.github.io/vega-lite/docs/selection.html
- https://vega.github.io/vega-lite/docs/bind.html
- https://vega.github.io/vega-lite/docs/predicate.html

## Verified version/date

- Vega-Lite parameter and selection docs checked 2026-03-26.
