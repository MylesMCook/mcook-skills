# AGENTS.md

Guidance for agents maintaining this skill catalog.

## Scope

- This repo is a public `skills.sh`-compatible catalog.
- Keep skills under `skills/<skill-name>/`.
- Keep repo-level docs short.

## Skill Rules

- Every skill must have a valid `SKILL.md` with only `name` and `description` in frontmatter unless a broader spec clearly requires more.
- Keep `SKILL.md` concise and procedural.
- Put durable supporting material in `references/`.
- Prefer linking to official vendor docs instead of mirroring large documentation sets.
- Avoid adding bulky examples, templates, or copied API references unless they provide durable value.

## Validation

- Run `npx skills add . --list` from the repo root before publishing changes.
- Confirm the target skill installs with `npx skills add . --skill <name> -a universal -y` in a temporary workspace when making structural changes. Use a specific agent target only when the skill truly depends on that agent.
