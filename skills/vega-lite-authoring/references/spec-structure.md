# Vega-Lite Spec Structure

Purpose: Compact structure guidance for common, top-level, and single-view Vega-Lite specifications.

## Stable rules

- Use a Vega-Lite schema URL such as `https://vega.github.io/schema/vega-lite/v6.json` unless the active host requires an older runtime.
- Treat `data`, `transform`, and `params` as common spec properties.
- Treat `resolve` as a composition-only property for `layer`, `facet`, `concat`, and `repeat`.
- Keep top-level settings such as `$schema`, `background`, `padding`, `autosize`, `config`, and `usermeta` at the root.
- For single-view charts, keep the core shape small: `mark`, `encoding`, optional `width` and `height`, then only the overrides you really need.

## Common failure modes

- Starting with a complex multi-view spec before proving a single view.
- Putting composition-only settings like `resolve` in the wrong place.
- Forgetting that `params` are top-level/common objects, not mark-level shortcuts.
- Mixing too many inline encoding transforms with top-level transforms without a clear reason.
- Using stale or host-incompatible schema assumptions.

## Safe defaults

- Start with `$schema`, `data`, one `mark`, and the minimum `encoding`.
- Add top-level `transform` only when field-level shorthand becomes hard to read.
- Add `params` only when the interaction or reusable state is clear.
- Let Vega-Lite generate scales, axes, and legends unless the default behavior is wrong.
- Keep `autosize: "pad"` and default backgrounds unless the host requires different sizing behavior.

## Version caveats

- Current stable Vega-Lite docs use schema v6.
- Hosts that embed Vega-Lite may lag upstream; embedded runtime wins when syntax conflicts with the latest docs.
- Some interaction and composition behavior changes across major versions, so verify the active runtime when debugging unexpected output.

## Source URLs

- https://vega.github.io/vega-lite/docs/spec.html
- https://vega.github.io/vega-lite/docs/

## Verified version/date

- Vega-Lite spec docs using schema v6, checked 2026-03-26.
