# Framework and Liquid

Source pages:

- `https://docs.trmnl.com/go/private-plugins/templates`
- `https://docs.trmnl.com/go/private-plugins/templates-advanced`
- `https://docs.trmnl.com/go/plugin-marketplace/plugin-screen-generation-flow`

## Device baseline

- TRMNL OG is `800x480`.
- The default display profile is e-ink friendly and grayscale-focused.
- Prefer TRMNL Framework classes over custom CSS.

## Markup posture

For Private Plugins:

- Use the TRMNL editor's markup area.
- Return one strong full-screen layout unless the user asks for mashup layouts.

For public Third Party plugins:

- Return all layout nodes:
  - `markup`
  - `markup_half_horizontal`
  - `markup_half_vertical`
  - `markup_quadrant`
  - `shared`

## Layout skeleton

Use a simple full-screen structure:

```html
<div class="view view--full">
  <div class="layout">
    ...
  </div>
</div>
```

## Liquid guidance

- Use Liquid interpolation for dynamic values.
- Use `default` filters to avoid blank output.
- Use loops only when the data shape clearly supports them.
- If multiple polling URLs are used, reference `IDX_0`, `IDX_1`, etc.

Example:

```liquid
<span class="title">{{ title | default: "Untitled" }}</span>
<span class="value value--tnums">{{ metric_value | default: "--" }}</span>
```

## Shared markup

Use shared markup only when it reduces repetition.

- Shared helpers are good for repeated title bars, formatting helpers, or small scripts.
- Avoid stuffing the shared file with custom CSS unless the user truly needs behavior the framework cannot express.

## Charts and graphics

- TRMNL allows richer chart libraries such as Highcharts.
- Keep graphics e-ink friendly and static.
- Avoid animations and interaction-heavy assumptions.

## Agent guidance

- Prefer clean, readable markup over clever Liquid.
- Prefer Framework classes over inline styles.
- If the user says "no code", still emit copy-pasteable markup, but explain where it goes in TRMNL.
