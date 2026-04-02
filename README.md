# mcook-skills

Public `skills.sh` compatible catalog of custom agent skills designed to stay useful over time.

## Repository Layout

Each skill lives in `skills/<skill-name>/` and can be installed directly from the catalog.

Skills should stay agent-agnostic by default. Put client-specific metadata in optional `agents/` files only when a client can use it.

## Skill Catalog

Custom workflow skills:
- `adversarial-review`
- `agent-browser`
- `browser-probe`
- `electron-best-practices`
- `github-gem-seeker`
- `simple-code`
- `trmnl-plugin-builder`

Visualization skills:
- `vega-authoring`
- `vega-lite-authoring`
- `deneb-authoring`

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
npx skills add MylesMCook/mcook-skills
```

From a local checkout:

```bash
npx skills add ./mcook-skills
```

## Validate

List all discoverable skills:

```bash
npx skills add . --list
```

Install one skill into a generic agent layout:

```bash
npx skills add . --skill simple-code -a universal -y
```

## Design Principles

- Keep `SKILL.md` short and procedural.
- Put durable guidance in `references/`.
- Add scripts only when they improve install behavior.
- Prefer official vendor documentation for fast-changing syntax and configuration.
- Avoid mirrored doc dumps that will stale quickly.
