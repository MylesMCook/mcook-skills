# Private Plugins

Source pages:

- `https://help.trmnl.com/en/articles/9510536-private-plugins`
- `https://help.trmnl.com/en/articles/10546870-compare-custom-plugin-types`
- `https://help.trmnl.com/en/articles/10542599-importing-and-exporting-private-plugins`
- `https://docs.trmnl.com/go/how-it-works`

## Default recommendation

Recommend a Private Plugin first unless the user explicitly needs OAuth, user PII on their own server, or a self-hosted TRMNL stack.

## Strategies

### Polling

Use when TRMNL can fetch the data on the user's behalf.

- Supported source formats include JSON, RSS, XML, plaintext, and CSV.
- One polling URL exposes fields directly in Liquid.
- Multiple polling URLs expose responses as `IDX_0`, `IDX_1`, and so on.
- Polling URL, body, and headers can interpolate form field values with `##{{ keyname }}`.

### Webhook

Use when an external system pushes content to TRMNL or when the plugin maintains state over time.

- The plugin uses a TRMNL-generated webhook URL tied to the plugin setting UUID.
- The POST body must include `merge_variables`.
- Use `deep_merge` to update nested keys without replacing the entire payload.
- Use `stream` plus `stream_limit` to append new values to top-level arrays.

### Plugin Merge

Use when the plugin should render data from other installed plugins.

- This unlocks mashup-style reuse of existing TRMNL plugin data.
- The user's variables list in the editor is the source of truth for available merge data.

## Output checklist for agent responses

When you recommend a Private Plugin, include:

1. Plugin name.
2. Strategy and why it fits.
3. Polling URLs or webhook example.
4. Form field YAML if the user must supply settings.
5. Liquid markup.
6. Force Refresh or testing instructions.

## Practical guidance

- Prefer the in-app TRMNL markup editor unless the user explicitly wants a repo workflow.
- If the user wants import/export artifacts, use a flat `settings.yml` plus viewport-specific `.liquid` files.
- Keep `custom_fields` in `settings.yml` aligned with the same field entries that would work in the Form Fields box.
- Prefer root-level merge variables over deeply nested objects.
- Mention Force Refresh whenever the user is iterating on markup or testing new data.
