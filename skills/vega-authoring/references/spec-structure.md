# Vega Spec Structure

Purpose: Compact top-level structure guidance for raw Vega specifications.

## Stable rules

- Use a Vega schema URL such as `https://vega.github.io/schema/vega/v6.json` unless the active host requires an older runtime.
- Treat `data`, `scales`, `axes`, `legends`, `marks`, and `signals` as first-class top-level building blocks.
- Keep sizing and layout primitives at top level: `width`, `height`, `padding`, `autosize`, optionally `background` and `title`.
- Use `config` for defaults and `usermeta` only for metadata ignored by Vega.
- Expect to define more structure manually than you would in Vega-Lite.

## Common failure modes

- Missing or stale `$schema`.
- Writing marks before dataset, scale, and guide names are stable.
- Expecting Vega-Lite conveniences such as automatic axes, legends, params, or encoding shorthand.
- Hiding essential structure inside marks when it belongs in top-level `scales`, `axes`, or `legends`.
- Using reserved names like `datum`, `event`, `item`, or `parent` as signal names.

## Safe defaults

- Start with `width`, `height`, `padding`, one named dataset, one or two scales, optional axes, and one mark block.
- Keep `autosize: "pad"` unless fit behavior is clearly needed.
- Add `signals` only for shared state, dynamic sizing, or interaction.
- Add `legends` only when a scale drives color, size, or shape and the legend is actually needed.
- Keep `config` minimal until the chart works.

## Version caveats

- Current stable Vega docs use schema v6.
- Embedded hosts may lag upstream; if host validation conflicts with docs, the host runtime wins.
- Some newer behaviors have version floors in the Vega docs, so check the active runtime before using recent syntax.

## Source URLs

- https://vega.github.io/vega/docs/specification/
- https://vega.github.io/vega/docs/

## Verified version/date

- Vega spec docs using schema v6, checked 2026-03-26.
