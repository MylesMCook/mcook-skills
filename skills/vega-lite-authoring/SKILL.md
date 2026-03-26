---
name: vega-lite-authoring
description: Use when authoring or refining Vega-Lite specifications, choosing encodings and mark types, or composing layered, faceted, repeated, or concatenated views. Prefer this skill for high-level chart authoring before dropping to raw Vega.
---

# Vega-Lite Authoring

Use this skill for high-level Vega-Lite work: encodings, marks, layered views, composition, concise specs.

## Workflow

1. Start from the analytical question, dataset fields, and intended mark before deciding channels and transforms.
2. Build the smallest valid spec first, then add encoding channels, transforms, and composition operators one layer at a time.
3. Escalate from Vega-Lite to raw Vega only when the requested interaction or layout exceeds the high-level grammar cleanly.
4. If a preview or validation MCP server is installed in the host, run it after each spec revision.

## Load References

- `references/overview-and-spec.md`: Load first for the overall Vega-Lite grammar and top-level spec structure.
- `references/encoding-and-marks.md`: Load when deciding channels, field definitions, mark types, or tooltip behavior.
- `references/transforms.md`: Load when the spec depends on derived fields, aggregation, filtering, binning, or time/unit transforms.
- `references/composition-and-authoring.md`: Load when layering, faceting, repeating, concatenating, or teaching someone how to author the spec progressively.
- `references/schema-summary.md`: Load when exact schema entry points or top-level property names matter.

## High-Value Gotchas

- Encoding channels often determine the right chart faster than mark choice alone. Start with field roles and aggregation intent.
- Layer, facet, repeat, and concat solve different composition problems. Choose one deliberately rather than combining them casually.
- When a requirement starts depending on explicit signals, custom event streams, or deeply bespoke dataflow, that is a cue to drop to raw Vega.
