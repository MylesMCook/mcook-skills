---
name: vega-authoring
description: Author and debug raw Vega specifications when lower-level control over dataflow, scales, axes, legends, marks, signals, or event streams is required. Use for raw Vega authoring, advanced signal/event-stream interaction, or cases where Vega-Lite cannot express the required behavior cleanly. Do not use as the lead skill for Deneb/Power BI host work or for straightforward Vega-Lite-first chart authoring.
---

# Vega Authoring

Guide for authoring and debugging raw Vega specifications.

## Use when

- The task explicitly requires raw Vega rather than Vega-Lite.
- You need direct control over `signals`, event streams, scales, axes, legends, marks, or post-encoding transforms.
- You are debugging lower-level Vega structure or runtime behavior.

## Do not use when

- The chart can be expressed cleanly in Vega-Lite with normal encodings, params, and view composition.
- The real task is authoring a Deneb visual inside Power BI; `deneb-authoring` should lead and apply raw Vega only if needed.
- The user mainly needs grammar selection help for a basic analytic chart.

## Precedence / handoff

- If the host is Power BI or Deneb, let `deneb-authoring` lead and take only the grammar-specific portion after host constraints are locked.
- If Vega-Lite can express the chart without awkward workarounds, hand off to `vega-lite-authoring`.
- Stay in raw Vega only when lower-level control materially reduces ambiguity or unlocks required behavior.

## Required reasoning steps

1. Confirm raw Vega is actually necessary.
2. Lock dataset names and the top-level structure before writing marks.
3. Decide which scales, axes, legends, and marks are first-class top-level objects.
4. For interaction, model state with `signals` and event streams, not Vega-Lite params or selections.
5. Build the smallest working spec first, then add transforms, nested groups, or interaction.

## Output contract

Always return:

- the chosen grammar and why raw Vega is necessary
- assumptions about data shape, field names, and host/runtime
- a minimal working Vega spec first
- optional refinements separately
- version caveats when syntax may depend on runtime
- likely host or interaction risks
- the next debugging step if the first attempt fails

## Version policy

- Default to stable Vega docs and the current v6 schema reference.
- If the host embeds an older Vega runtime, the host version wins over upstream docs.
- Do not import Vega-Lite concepts such as params or selections into raw Vega guidance.
- Prefer curated references in this skill over copied doc prose; load the smallest relevant file first.

## Known failure modes

- Overusing raw Vega when Vega-Lite would be shorter and safer.
- Missing top-level `data`, `scales`, `axes`, `legends`, or `marks` structure.
- Treating signals like one-off expressions instead of durable interaction state.
- Losing mark/data alignment by renaming datasets or scales mid-spec.
- Mixing data transforms, mark transforms, and scenegraph ordering without a clear model.

## Load references

- Load `references/spec-structure.md` first for top-level shape and safe defaults.
- Load `references/scales-axes-legends.md` when structure, guides, or ranges are in question.
- Load `references/signals-and-interactivity.md` for signals, event streams, nested scope, or interaction state.
- Load `references/marks.md` for mark-level encoding details.
- Load `references/transforms.md` when derived fields, grouping, or layout transforms are required.
