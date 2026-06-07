# Image Prompt Template

Load this when writing a final prompt, using an image-generation tool, or editing a generated image. Use one prompt per final illustration.

## Generation prompt

Replace every brace. Do not paste placeholders into the image tool.

```text
Generate one standalone 16:9 horizontal US English article body illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly thin pen lines. Lots of empty white space. Sparse red/orange/blue handwritten American English notes. Clean weird product-sketch feeling. No gradients, shadows, paper texture, beige background, complex scenery, commercial vector style, PPT infographic look, children’s cartoon, cute mascot poster, realistic UI, or polished brand hero.

Recurring character required:
Inkblot, a small solid-black abstract blob worker with white dot eyes, tiny thin legs, a blank serious expression, and a slightly uneven hand-drawn body. Inkblot must perform the core conceptual action, not decorate the scene. Inkblot is deadpan, strange, and useful; not cute, not racialized, not human, not a logo.

Theme:
{article illustration theme}

Structure type:
{workflow machine / system slice / before-after contrast / character state / concept metaphor / method stack / map-route / tiny comic strip}

Core idea:
{one sentence explaining what this image should make the reader understand}

Composition:
{specific scene: where Inkblot is, what Inkblot is doing, key object(s), how information or attention moves}

Suggested elements:
{element 1} / {element 2} / {element 3} / {optional element 4}

Handwritten English labels:
{label 1} / {label 2} / {label 3} / {optional label 4} / {optional label 5}

Color use:
Black for main line art, Inkblot, key objects, and most labels. Orange only for the main flow/path/arrow/handoff. Red only for warnings, friction, problems, or a key result. Blue only for secondary notes, feedback, AI/system state, or optional context.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas and preserve at least 35% blank white space. Use at most 3-5 very short handwritten English labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make a formal diagram, course slide, dense explainer, patriotic collage, or generic Americana scene. Do not copy source-project example compositions; invent a fresh metaphor for this article.

The result should be clear but not instructional, interesting but not childish, strange but clean.
```

## Edit prompts

### Remove accidental title

```text
Edit the provided image. Remove only the handwritten title "{text to remove}" and any underline or title mark near it. Fill that area with the same clean white background. Preserve everything else: Inkblot, labels, paths, line style, composition, aspect ratio, and image quality. Do not add new text or objects.
```

### Make Inkblot central

```text
Regenerate this illustration with the same core meaning and simple layout, but make Inkblot perform the central conceptual action. Inkblot should be doing the strange physical work that explains the idea, not standing beside a diagram. Keep it sparse, hand-drawn, deadpan, and not cute.
```

### Reduce text

```text
Regenerate with the same visual metaphor but reduce all in-image wording to 3-5 short American English handwritten labels, each 1-3 words. Remove any sentence-length explanations, titles, subtitles, or numbered instructions.
```

### Remove unwanted patriotic clichés

```text
Regenerate with the same US English article-illustration style, but remove flags, eagles, monuments, bunting, baseball/cowboy symbols, and patriotic color blocks unless the article specifically requires them. Keep only everyday editorial objects that support the metaphor.
```
