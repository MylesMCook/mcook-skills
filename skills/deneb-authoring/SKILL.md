---
name: deneb-authoring
description: Use when authoring Vega or Vega-Lite for Deneb in Power BI, especially for dataset binding, templates, usermeta, interactivity, and PBIR-aware packaging. Keep the guidance conservative and grounded in current Deneb docs.
---

# Deneb Authoring

Use this skill for Deneb in Power BI: dataset binding, usermeta templates, interactivity, visual editor, PBIR.

## Workflow

1. Start from the Power BI model question first: what fields arrive in `dataset`, what cross-filter behavior must be preserved, and whether Vega or Vega-Lite is the right grammar.
2. Prefer specs whose primary data source is Deneb's injected `dataset`, and keep transformations on that primary table as simple as possible.
3. Use templates and `usermeta` deliberately so the visual remains portable and understandable when shared.
4. If a preview MCP server is installed, use it for structural preview only and remember it cannot fully simulate Power BI selection semantics.

## Load References

- `references/overview-and-dataset.md`: Load first for how Deneb fits into Power BI and how `dataset` binding works.
- `references/interactivity.md`: Load when the user cares about cross-filtering, selection, highlight behavior, or row identity.
- `references/templates-and-usermeta.md`: Load when authoring reusable templates or working with the Deneb template metadata shape.
- `references/pbir-and-editor.md`: Load when the request involves the visual editor workflow or PBIR packaging.
- `references/template-schema-summary.md`: Load when exact template metadata keys or schema entry points matter.

## High-Value Gotchas

- Current Deneb docs emphasize `dataset` as the primary binding and document helper fields such as `__selected__` and `__row__`. Do not assume additional identity helpers unless the target environment confirms them.
- Transforms that reshape or duplicate rows can break Power BI row reconciliation and therefore selection or cross-filter behavior. Call this risk out explicitly.
- A Vega or Vega-Lite spec that previews correctly outside Power BI can still be incompatible with Deneb interactivity expectations.
