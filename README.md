# mcook-skills

A public `skills.sh`-compatible catalog of custom agent skills built to stay useful over time.

## Layout

Skills live under `skills/<skill-name>/` so each skill can be installed directly from the catalog.

## Skill Catalog

Custom workflow skills:
- `adversarial-review`
- `simple-code`
- `browser-probe`

Brainerd skills:
- `brainerd`
- `brainerd-init`
- `brainerd-reflect`
- `brainerd-ruminate`

Pi skills:
- `pi-coding-agent-sdk`
- `pi-package-creator`

## Install

From GitHub:

```bash
npx skills add MylesMCook/mcook-skills --skill simple-code
```

From a local checkout:

```bash
npx skills add ./mcook-skills --skill simple-code
```

## Validate

List discoverable skills:

```bash
npx skills add . --list
```

Install one skill into Codex:

```bash
npx skills add . --skill simple-code -a codex -y
```

## Design Principles

- Keep `SKILL.md` short and procedural.
- Put durable guidance in `references/`.
- Keep scripts only when they materially improve installable behavior.
- Prefer official vendor documentation for fast-changing syntax and configuration.
- Avoid mirrored doc dumps that will stale quickly.
