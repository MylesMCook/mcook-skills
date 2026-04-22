---
name: laws-of-taste
description: >-
  Use when a UI, dashboard, landing page, deck, document, or other
  human-facing surface needs stronger hierarchy, typography, spacing, color,
  motion, or coherence. Trigger on critique, redesign, polish, or
  implementation guidance. Skip backend-only work, data modeling, and
  copyediting-only tasks.
---

# Laws of Taste

Apply this skill when a visual surface needs better taste, not more decoration.

## Core stance

Taste shapes attention, meaning, rhythm, and trust.

- Purpose before ornament.
- Establish order, then break it on purpose.
- Make hierarchy obvious at a glance.
- Use restraint unless intensity is the job.
- Build systems for trust; use exceptions for life.

If something feels templated, muddy, loud without reason, or visually unserious, say so and improve it.

## When to use

- UIs, sites, apps, dashboards, decks, documents, and other designed surfaces
- critique, redesign direction, polish passes, or implementation guidance
- requests about hierarchy, spacing, typography, color, components, motion, or overall coherence

Do not use this skill for backend-only work, copyediting-only work, or brand strategy with no visual surface.

## Working order

Use this sequence unless the task clearly needs another order:

1. Find the job of the surface.
   What must a person notice, understand, trust, or do first?
2. Diagnose the real visual failure.
   Name design problems, not vibes: hierarchy, grouping, type, color, rhythm, components, motion, responsiveness, coherence.
3. Choose one design thesis.
   One sentence should govern the redesign.
4. Make 3-7 strong moves.
   For deep redesigns or explicit audits, read `references/LAWS.md` and apply hierarchy, structure, spacing, typography, color, components, imagery, motion, and finish in that order.
5. Explain tradeoffs.
   Say what got stronger and what was intentionally restrained.
6. If working in code, translate intent into tokens, layout primitives, component states, data-viz rules, motion, and responsive behavior.

## Guardrails

- Taste is not minimalism; the right answer might be quiet, dense, playful, loud, luxurious, brutal, editorial, or warm.
- Do not let everything shout at once.
- Do not use color as a substitute for structure.
- Do not add decoration that weakens clarity.
- Do not sacrifice accessibility, legibility, responsiveness, or interaction clarity for style.
- If no artifact is provided, state assumptions and give a strong provisional direction.
- Ask only when missing context would materially change the recommendation.

## Response default

Choose the lightest useful format. Read `references/OUTPUTS.md` only when the deliverable shape is unclear.

- With an artifact, critique what is there, point to concrete visual problems, and propose specific improvements.
- Without an artifact, state assumptions and give a concrete direction, not vague inspiration.
- If color, typography, density, motion, or interaction states change materially, read `references/ACCESSIBILITY.md`.
- When useful, end with a short self-check on hierarchy, structure, typography, color, what was removed, and what still feels generic.

## Reference files — load on demand

Do not read every reference file on every activation. Load only what the task needs.

- `references/LAWS.md` — the 22 operating laws. Read for deep redesigns, explicit audits, unfamiliar surfaces, or whenever recommendations should be mapped to named laws.
- `references/ENVIRONMENTS.md` — adaptation by surface type. Read when the medium is unfamiliar, mixed, or spans multiple environments.
- `references/OUTPUTS.md` — response formats and deliverables. Read when choosing between output modes or when the user wants a particular deliverable shape.
- `references/EVALUATION.md` — scorecard for audits and polish passes. Read only for QA, audit, acceptance, or final-review tasks.
- `references/ACCESSIBILITY.md` — accessibility floor for tasteful design. Read when changing color, typography, motion, dense data views, or interaction states.
- `references/FOUNDATIONS.md` — documented basis from the source books. Read only if the user asks why a principle exists or challenges the rationale.
- `references/FORMS.md` — optional intake prompts. Read only when context is genuinely too thin to proceed confidently.
