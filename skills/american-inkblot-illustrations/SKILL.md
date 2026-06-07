---
name: american-inkblot-illustrations
description: "Use when creating, planning, prompting, generating, or editing quirky US English article illustrations: blog, newsletter, essay, Notion, document body art, editorial explainer, workflow/methodology visual, concept metaphor, shot list, or sparse handwritten-label image prompt. Produces 16:9 clean white-background hand-drawn Inkblot-character illustrations with sparse red/orange/blue American English notes. Do NOT use for polished brand key visuals, PPT decks, complex architecture diagrams, children's cartoons, logos, memes, Chinese annotation workflows, or generic image prompts."
---

# American Inkblot Illustrations

Use this skill to plan, prompt, generate, or edit body illustrations for US English articles. The job is not “make a picture.” The job is to find one cognitive move in the article and turn it into a sparse, memorable, weird-but-clear 16:9 hand-drawn explainer.

Default visual character: **Inkblot**, a small solid-black deadpan worker with white dot eyes and thin legs. Inkblot must do the conceptual work in the drawing, not stand beside it as decoration.

## Route: load only what the task needs

| Situation | Load |
|---|---|
| Style fidelity matters, or any image prompt/generation/edit is requested | `references/style-dna.md` |
| Inkblot’s shape, role, action, or “too cute / too decorative” issue matters | `references/inkblot-mascot.md` |
| Creating a shot list, choosing a structure type, or inventing a metaphor | `references/composition-patterns.md` |
| Calling an image tool or writing a final image prompt | `references/prompt-template.md` |
| Reviewing generated images or planning edits/regenerations | `references/qa-checklist.md` |
| Need short US English label ideas | `assets/label-bank.md` |

Do not preload all references. Read the narrow file named above when the branch applies.

## Workflow

1. **Digest the source.** Read the user’s article, Markdown, Notion export, screenshot text, pasted draft, or concept. If the user gave a URL and the runtime can browse, fetch it; otherwise ask for the text only if there is no usable content.
2. **Pick cognitive anchors, not paragraphs.** Good anchors are decisions, bottlenecks, before/after contrasts, system loops, evidence chains, trust gaps, handoffs, tradeoffs, and stuck-to-running state changes. Skip generic intros and paragraphs that are already visually obvious.
3. **Decide the mode.**
   - Planning only: output a shot list.
   - Generate/create/make/draw: generate each image separately when an image tool exists; otherwise deliver final prompts.
   - Edit/fix/remove title/reduce text: write or run the narrow edit instruction, then QA.
4. **Create the shot list.** Default to 4-8 shots for a normal article, 1-3 for a short piece, and no more than 9 for a long piece. Each shot gets one structure type and one core idea.
5. **Generate or prompt one image at a time.** Read `references/prompt-template.md`. Never pack multiple final illustrations into one collage unless the user explicitly requested a comic strip.
6. **QA before delivery.** Read `references/qa-checklist.md` after generation/editing. Regenerate or edit if the image is too dense, too cute, too PPT-like, too text-heavy, too patriotic by default, or if Inkblot is decorative.
7. **Save when working in a workspace.** Put finished images under `assets/<article-slug>-illustrations/` as `01-topic-name.png`, `02-topic-name.png`, etc. Do not overwrite existing assets unless asked.

## Shot list format

Use a compact table:

| Placement | Theme | Core idea | Structure | Inkblot action | Elements | Labels |
|---|---|---|---|---|---|---|

Labels must be American English, usually 1-3 words each. Use 3-5 labels per image unless the user asks for no text.

## Generation defaults

Use these defaults unless the user overrides them:

- 16:9 horizontal article body illustration.
- Pure white background; no paper texture, beige, shadows, gradients, or noise.
- Black hand-drawn line art with slightly wobbly thin lines.
- Sparse red/orange/blue handwritten English notes.
- Main subject covers roughly 40%-60% of the canvas; keep at least 35% empty white space.
- One core action, structure, state, or metaphor per image.
- Inkblot is the active subject of the conceptual action.
- Weird, clever, clean, and editorial; not cute, not childish, not brand-polished.

## Gotchas

- **“American” means US English and everyday US editorial grounding, not flags/eagles/Uncle Sam.** Use civic or patriotic symbols only when the article is actually about those topics.
- **Inkblot is abstract, not racialized.** Do not call it “Little Black” in US-facing output; do not add human ethnicity, race-coded features, gender, or costumes.
- **Text in generated images is fragile.** Fewer labels beat more labels. If text fails, remove labels, regenerate, or keep labels outside the image.
- **This is not a PPT infographic skill.** Remove titles, grids, tidy corporate boxes, and dense arrows.
- **Do not copy examples from the source project.** Reuse the style DNA, not old object layouts or compositions.
- **If no image-generation tool exists, still do the useful work:** output shot lists and ready-to-run prompts.
