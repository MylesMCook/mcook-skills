# Vega Scales, Axes, and Legends

Purpose: Guidance for the top-level guide objects that raw Vega requires you to define explicitly.

## Stable rules

- Define scales first; axes and legends are downstream views of scale behavior.
- Name scales once and reference those names consistently from marks, axes, and legends.
- Use axes for spatial encodings and legends for non-spatial encodings such as color, size, or shape.
- Prefer top-level axes and legends over mark-level reimplementation.
- Decide domain and range explicitly when defaults would hide important behavior.

## Common failure modes

- Mismatched scale names between marks and guides.
- Forgetting that legends only appear when a mark references a compatible scale.
- Using the wrong scale type for the data semantics, then debugging the wrong layer.
- Letting domains drift because transforms changed the data source used by the scale.
- Trying to solve layout issues inside marks instead of adjusting guide or autosize settings.

## Safe defaults

- Start with one position scale per axis and add non-position scales only when the chart proves it needs them.
- Add a single axis per spatial scale unless you need mirrored or specialized guides.
- Let guides inherit defaults first, then override titles, formats, or orientation only when the default is wrong.
- Keep legend titles aligned with the field or measure the user actually sees.
- If a guide is noisy, remove it explicitly rather than fighting defaults indirectly.

## Version caveats

- Guide and scale capabilities follow the active Vega runtime.
- Host layout behavior can make otherwise valid guide settings appear clipped or crowded.

## Source URLs

- https://vega.github.io/vega/docs/scales/
- https://vega.github.io/vega/docs/axes/
- https://vega.github.io/vega/docs/legends/

## Verified version/date

- Vega guide docs checked 2026-03-26.
