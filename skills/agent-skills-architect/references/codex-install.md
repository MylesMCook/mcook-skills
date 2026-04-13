# Codex install and distribution notes

Use this file when the user wants the skill to work smoothly in Codex or asks where to place or install it.

## Codex activation

Codex can use a skill in two ways:

- explicit invocation, such as mentioning the skill directly
- implicit invocation when the user request matches the skill description

That makes the description the most important trigger surface.

## Codex skill layout

A Codex skill is a directory with:

- `SKILL.md` (required)
- optional `scripts/`
- optional `references/`
- optional `assets/`
- optional `agents/openai.yaml`

## Manual placement for local authoring

For repository-scoped authoring, prefer placing the skill in:

- `.agents/skills/<skill-name>/`

Codex scans `.agents/skills` directories from the current working directory upward to the repository root, so repo-local placement is the safest default for project work.

For user-level manual authoring, consult current Codex docs before placing the skill by hand.

## `npx skills` installation

When the user wants an install command rather than manual copying, prefer `npx skills`:

```bash
npx skills add <repo-or-path> --skill <skill-name> -a codex
```

Useful variants:

```bash
# list available skills before installing
npx skills add <repo-or-path> --list

# install globally for Codex
npx skills add <repo-or-path> --skill <skill-name> -a codex -g

# copy instead of symlink
npx skills add <repo-or-path> --skill <skill-name> -a codex --copy
```

If the user is installing from a local folder, the source can be a local path.

## Manual vs CLI path nuance

The current Codex docs describe repository discovery through `.agents/skills` and document a user scope for manually authored skills.

The current `vercel-labs/skills` README separately documents Codex-specific install targets for the CLI.

When these appear different, use this rule:

- for manual authoring and discovery behavior, prefer the Codex docs
- for `npx skills` installation behavior, prefer the `npx skills` README
- when in doubt, prefer repo-local `.agents/skills/<skill-name>` or let `npx skills` place the files for you

## `agents/openai.yaml`

Use `agents/openai.yaml` when Codex-specific metadata or policy helps:

- `interface.display_name`
- `interface.short_description`
- `interface.default_prompt`
- `policy.allow_implicit_invocation`
- optional tool dependencies

Keep it lightweight. Most skills do not need more than a display name, short description, and maybe `allow_implicit_invocation`.

## Packaging

For direct handoff, ZIP the skill directory root so the folder structure stays intact after extraction.

Good default contents:

- the skill folder
- no extra nested parent directory levels
- no unrelated repo files
