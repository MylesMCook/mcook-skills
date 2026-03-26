# Vega-Lite Invalid Data

Purpose: Guidance for null and NaN handling in continuous scales and path marks.

## Stable rules

- Invalid-data behavior in Vega-Lite is driven mainly by `mark.invalid` and `config.scale.invalid`.
- Use `filter` when invalid rows should disappear entirely.
- Use path-breaking modes when line, area, or trail continuity should reflect missing data.
- Use `show` only when explicit invalid outputs are meaningful and not misleading.
- Treat invalid-data handling as a chart-design choice, not just a cleanup step.

## Common failure modes

- Letting the default mode hide a real data-quality issue.
- Using `show` without deciding what invalid scale output should mean visually.
- Forgetting that non-path marks and path marks behave differently under path-breaking modes.
- Solving missing-data problems with composition or manual hacks before checking `mark.invalid`.
- Assuming categorical null handling works the same way as continuous null handling.

## Safe defaults

- For point, bar, and similar non-path charts, start with `filter` when invalid values should not render.
- For line, area, or trail charts, start with a path-breaking mode when gaps should remain visible.
- Use `config.scale.invalid` only when the chart truly benefits from explicit visual output for invalid values.
- If behavior is confusing, isolate invalid handling in a minimal spec before debugging the rest of the chart.

## Version caveats

- Invalid-data defaults and naming follow the active Vega-Lite runtime.
- Hosts that compile Vega-Lite may surface missing-data behavior differently than the online editor.

## Source URLs

- https://vega.github.io/vega-lite/docs/invalid-data.html

## Verified version/date

- Vega-Lite invalid-data docs checked 2026-03-26.
