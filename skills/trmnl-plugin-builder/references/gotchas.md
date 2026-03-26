# Gotchas

Cross-checked against official TRMNL docs and this repo's existing Cursor rule.

## High-value corrections

- **Private Plugin first is the safest default.** The docs explicitly position Private Plugins as the easiest custom-plugin path.
- **Recipe is not a separate build system.** It is a publication and installation mode layered on top of a Private Plugin.
- **`settings.yml`, `full.liquid`, and `shared.liquid` are repo-local conveniences here.** Official TRMNL docs focus on web UI editors and API responses, not a required repo file layout.
- **One polling URL and many polling URLs behave differently.** Single URL data is direct; multiple URLs become `IDX_0`, `IDX_1`, and so on.
- **Webhook payloads are small.** If the user wants a large or high-frequency state feed, call out the hard limits instead of hand-waving.
- **Form YAML failures can be silent.** If fields do not appear, suspect YAML syntax first.
- **Nested payloads make Liquid worse.** Prefer root-level keys when designing example JSON.
- **Public Third Party plugins must return all layout nodes.** Do not emit only `markup` for a marketplace plugin.
- **TRMNL devices poll the server.** Do not describe the hosted model as push-to-device.

## Guidance retained from the repo Cursor rule

Retained because it matches official docs:

- 800x480 is the standard OG device target.
- Liquid, YAML, TRMNL Framework markup, and light JavaScript are valid building blocks.
- E-ink friendly, low-motion UI is the right default.

Not treated as official TRMNL requirements:

- the `trmnlp` file layout
- `.trmnlp.yml`
- `src/settings.yml`
- `src/full.liquid`
- `src/shared.liquid`

Use those only if the user explicitly wants local source files.
