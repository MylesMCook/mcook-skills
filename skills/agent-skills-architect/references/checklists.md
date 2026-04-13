# Checklists

Use this file as a quick pass before handing off an audit or revised skill.

## Frontmatter checklist

- `name` exists, matches the folder name, and uses lowercase letters, numbers, and hyphens only
- `description` exists, is non-empty, and is specific about what the skill does and when it should trigger
- `description` is not overly broad and stays under the spec limit
- optional fields are justified rather than decorative
- `compatibility` only appears if the environment requirements matter
- `metadata` only stores small, stable key-value data
- `allowed-tools` is omitted unless the target client meaningfully supports it

## Trigger checklist

- Should-trigger cases are obvious from the description
- Should-not-trigger boundaries are implied or stated where false positives are likely
- The description names actual jobs, not only general topics
- The description uses task language a real user would say

## `SKILL.md` body checklist

- The body is concise and task-specific
- The instructions are imperative and actionable
- The skill does not waste context on generic “be careful” advice
- The deliverable is clear
- Failure modes or boundaries are stated when they matter
- Reference files are named and used intentionally

## Progressive disclosure checklist

- Always-needed instructions live in `SKILL.md`
- Heavier reference material lives in `references/`
- Templates or sample files live in `assets/`
- Scripts are present only when the payoff is real
- File references are shallow and easy to follow

## Script checklist

Use scripts only when they improve determinism, validation, or repeated execution.

If scripts exist, check:

- dependencies are documented
- error messages are helpful
- edge cases are handled
- paths are portable
- the skill body says when to run the script
- the script is not duplicating what a short instruction already covers

## `agents/openai.yaml` checklist

Add this file only when Codex-specific metadata or policy adds value.

Check:

- display text is useful and short
- `default_prompt` helps users invoke the skill
- `allow_implicit_invocation` matches the intended behavior
- dependencies are declared only when real tooling is required

## Packaging checklist

- the folder is drop-in ready
- no broken relative links
- filenames are stable and descriptive
- the updated skill preserves the original intent unless a rename is clearly necessary
- the final handoff includes a ZIP when feasible
- install notes are brief and accurate

## Evaluation checklist

- there are example prompts that should trigger
- there are example prompts that should not trigger
- output expectations are concrete
- assertions are observable and not vague
- unverified areas are called out plainly
