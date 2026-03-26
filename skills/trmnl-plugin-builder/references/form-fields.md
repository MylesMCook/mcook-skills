# Form Fields

Source page:

- `https://help.trmnl.com/en/articles/10513740-custom-plugin-form-builder`

## Core shape

Each YAML list item pasted directly into TRMNL's Form Fields box needs:

- `keyname`
- `field_type`
- `name`

Useful optional keys:

- `description`
- `help_text`
- `optional`
- `default`
- `placeholder`
- `rows`
- `options`
- `value`
- `min`
- `max`
- `step`
- `maxlength`
- `endpoint`
- `http_verb`

## High-value field types

- `string`
- `text`
- `number`
- `password`
- `code`
- `date`
- `time`
- `select`
- `xhrSelect`
- `xhrSelectSearch`
- `plugin_instance_select`
- `time_zone`
- `copyable`
- `copyable_webhook_url`
- `boolean`
- `author_bio`

## Important patterns

### Basic string

```yaml
- keyname: api_key
  field_type: string
  name: API Key
  description: Paste your token from the source service.
```

### Select with a direct string default

This snippet is already in the exact shape TRMNL expects in the Form Fields box.

```yaml
- keyname: units
  field_type: select
  name: Units
  options:
    - metric
    - imperial
  default: metric
```

If you use `yes` or `no` style defaults, quote them so YAML does not coerce them.

### Dynamic select

Use `xhrSelect` or `xhrSelectSearch` when the options come from a remote endpoint.

- Default verb is `POST`.
- `query` is sent for `xhrSelectSearch`.
- `depends_on` creates chained selects.

### Conditional validation

Use `conditional_validation` to hide fields or require different fields depending on a parent value.

## Agent guidance

- Emit only the YAML field list that can be pasted directly into TRMNL's Form Fields box.
- Do not wrap field YAML in `settings.yml`, `custom_fields:`, or any other top-level keys unless the user explicitly asks for a full import/export file.
- Keep field count small; only ask users for settings the plugin truly needs.
- If the plugin will be shared as a Recipe, prefer friendlier labels and `help_text`.
