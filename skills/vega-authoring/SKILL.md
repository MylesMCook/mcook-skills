---
name: vega-authoring
description: Use when authoring or debugging raw Vega specifications, explicit dataflow, custom marks, transforms, scales, or signals. Prefer this skill when Vega-Lite is too limiting or when the user explicitly needs low-level Vega control.
---

# Vega Authoring

Use this skill for raw Vega work: bespoke specs, explicit dataflow, custom interaction, low-level debugging.

## Workflow

1. Confirm the chart goal, data shape, and whether Vega-Lite would be sufficient before committing to raw Vega.
2. Start with a minimal valid spec: data, scales, axes, and one mark definition before layering transforms or signals.
3. Add transforms and signals incrementally, validating after each change so broken dataflow is isolated quickly.
4. If a preview or validation MCP server is installed in the host, use it after every meaningful revision.

## Load References

- `references/overview-and-spec.md`: Load first for the overall spec shape, data/scale/mark layout, and top-level grammar.
- `references/marks.md`: Load when choosing or debugging individual mark definitions.
- `references/transforms.md`: Load when dataflow behavior, derived fields, or transform ordering is the main problem.
- `references/signals-and-interactivity.md`: Load when the request involves interaction, parameters, selections, or event-driven behavior.
- `references/schema-summary.md`: Load when exact property names or schema entry points matter.

## High-Value Gotchas

- Transform order is semantic in Vega. Mutating the primary dataset too early can invalidate later marks or interactions.
- Signals are the control plane for interaction. Keep signal names explicit and trace how they feed scales, marks, and event handlers.
- When the design is mostly declarative encodings, step back and consider Vega-Lite instead of overbuilding in raw Vega.
