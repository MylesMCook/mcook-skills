---
name: trmnl-plugin-builder
description: Build TRMNL plugins with a strong bias toward Private Plugins and Recipes. Use when you need help choosing Private Plugin vs Recipe vs Third Party vs BYOS, generating TRMNL Form Fields YAML, picking polling vs webhook vs plugin_merge, writing Liquid and Framework markup, or producing TRMNL private-plugin import/export starters.
---

# TRMNL Plugin Builder

Build the simplest viable TRMNL solution first.

## Workflow

1. Use the decision rules below to choose the path.
2. Read `references/private-plugins.md` for most Private Plugin and import/export work.
3. Read `references/form-fields.md` before emitting bare Form Fields YAML.
4. Read `references/framework-liquid.md` before emitting markup.
5. Read `references/webhooks.md` for push updates, stateful dashboards, or merge strategies.
6. Read `references/recipes.md` for sharing or publishing.
7. Read `references/advanced-third-party.md` only for OAuth, server-backed marketplace flows, or external account management.
8. Read `references/byos.md` only for self-hosting and device API work.
9. Read `references/gotchas.md` before finalizing.

## Decision Rules

- Choose **Private Plugin** by default when TRMNL can poll an endpoint or accept webhook pushes.
- Choose **Recipe** when the logic still fits Private Plugin and the user wants a no-server shareable install flow.
- Choose **Third Party** only when the request needs OAuth, user identity or PII on the author's server, a custom management UI, or a public marketplace integration backed by the author's server.
- Choose **BYOS** only when the request is about self-hosting the TRMNL server/device relationship or `/api/setup`, `/api/display`, `/api/log`.

## Output Contract

- For direct UI answers, emit bare Form Fields YAML, not a `custom_fields:` wrapper.
- Emit Liquid markup plus concrete TRMNL setup steps.
- Use `assets/settings.yml` and `assets/full.liquid` only when the user explicitly wants import/export artifacts or repo-local starter files.
- Mention webhook rate and payload limits whenever the requested update frequency pushes against them.
- Do not pretend a Private Plugin can satisfy a Third Party or BYOS requirement.

## Assets

- `assets/settings.yml` - official-shape private-plugin import/export starter
- `assets/full.liquid` - official-shape full-screen template starter
- `assets/shared.liquid` - optional shared helper example
- `assets/polling-response.json` - polling payload example
- `assets/webhook-payload.json` - webhook payload example
