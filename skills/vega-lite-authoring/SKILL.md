---
name: vega-lite-authoring
description: Author and debug Vega-Lite specifications for chart design, encoding choice, transforms, view composition, params, and invalid-data handling. Use for general Vega-Lite authoring and keep the solution in Vega-Lite unless the requirement clearly needs raw Vega. Do not use as the lead skill for Deneb/Power BI host work.
---

# Vega-Lite Authoring

Guide for authoring and debugging Vega-Lite specifications.

## Use when

- The task is general Vega-Lite authoring, chart design, encoding choice, transform design, or multi-view composition.
- You need params, selections, conditional encodings, or invalid-data handling in a Vega-Lite-first chart.
- The chart should stay high-level and declarative unless a lower-level grammar is clearly required.

## Do not use when

- The real task is Deneb or Power BI host work; `deneb-authoring` should lead and apply Vega-Lite after host constraints are locked.
- The requirement depends on lower-level signals, event streams, or scenegraph control that Vega-Lite cannot express cleanly.
- The user only needs raw Vega structure or debugging.

## Precedence / handoff

- If the host is Deneb or Power BI, let `deneb-authoring` lead and keep this skill focused on the Vega-Lite grammar portion.
- If the design becomes awkward because of low-level interaction or scenegraph requirements, hand off to `vega-authoring`.
- Stay in Vega-Lite when a minimal spec with marks, encodings, transforms, params, and composition remains readable.

## Required reasoning steps

1. Confirm Vega-Lite is sufficient before escalating to raw Vega.
2. Start with the smallest valid spec: data, mark, and the minimum encoding.
3. Decide whether a transform belongs in top-level `transform` or inline encoding shorthand.
4. For interaction, choose params deliberately and distinguish simple variables from selection params.
5. For multi-view work, choose `layer`, `facet`, `concat`, or `repeat` intentionally and define `resolve` only when defaults are wrong.

## Output contract

Always return:

- the chosen grammar and why Vega-Lite is appropriate
- assumptions about data shape, field names, and host/runtime
- a minimal working Vega-Lite spec first
- optional refinements separately
- version caveats when syntax may depend on runtime
- likely host or interaction risks
- the next debugging step if the first attempt fails

## Version policy

- Default to stable Vega-Lite docs and the current v6 schema reference.
- If the host embeds an older Vega-Lite runtime, the host version wins over upstream docs.
- Keep the solution in Vega-Lite unless the requirement clearly needs raw Vega.
- Prefer curated references in this skill over copied tutorials; load the smallest relevant file first.

## Known failure modes

- Escalating to raw Vega too early for work Vega-Lite handles well.
- Starting with layered or faceted complexity before proving the single-view spec.
- Treating params, invalid-data handling, or `resolve` as afterthoughts.
- Mixing incompatible composition operators or forgetting where `resolve` applies.
- Relying on defaults when invalid values, sorting, or layout behavior actually need explicit control.

## Load references

- Load `references/spec-structure.md` first for common and top-level Vega-Lite structure.
- Load `references/encoding-and-marks.md` for channels, field definitions, and mark choice.
- Load `references/transforms.md` for transformation order and shaping logic.
- Load `references/view-composition.md` for `layer`, `facet`, `concat`, `repeat`, and `resolve`.
- Load `references/params-and-interactivity.md` for params, selections, predicates, and interaction behavior.
- Load `references/invalid-data.md` when nulls, NaNs, or missing values affect marks or scales.
