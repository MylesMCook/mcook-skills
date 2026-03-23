# mcook-skills

A small catalog of custom agent skills built to stay useful over time.

## Layout

Skills live under `skills/<skill-name>/` so they can be installed with `skills.sh`-compatible tooling.

## Current Skills

- `electron-best-practices` - Thin Electron guidance for agents with Forge-first defaults and links to current official docs.

## Install

From a published GitHub repo:

```bash
npx skills add <your-owner>/mcook-skills --skill electron-best-practices
```

From a local checkout:

```bash
npx skills add ./mcook-skills --skill electron-best-practices
```

## Validate

List discoverable skills:

```bash
npx skills add ./mcook-skills --list
```

Install the Electron skill locally:

```bash
npx skills add ./mcook-skills --skill electron-best-practices -a codex -y
```

## Publish Checklist

- Push the repo to GitHub as `mcook-skills`.
- Keep skills in `skills/<skill-name>/`.
- Keep each skill installable with a valid `SKILL.md`.
- Prefer official vendor documentation for fast-changing syntax and config details.
- Avoid mirrored documentation trees that will stale quickly.

## Design Principles

- Keep `SKILL.md` short and procedural.
- Put durable guidance in `references/`.
- Link to official vendor docs for fast-changing syntax and configuration.
- Avoid mirrored doc dumps that will stale quickly.
