# mcook-skills

Public `skills.sh` catalog of reusable agent skills.

This catalog changes often. Treat the CLI and [`skills/`](./skills) as the source of truth.

## Quick Start

List skills:

```bash
npx skills add MylesMCook/mcook-skills --list
```

Install catalog in the current project:

```bash
npx skills add MylesMCook/mcook-skills
```

Install one skill:

```bash
npx skills add MylesMCook/mcook-skills --skill simple-code -a universal -y
```

## Local Development

Install from a local checkout:

```bash
npx skills add ./mcook-skills
```

## Updates

Use the documented command:

```bash
npx skills update
```

Use `update`, not `upgrade`. `upgrade` may work today, but it is not documented upstream.

For tracked catalog updates, install globally:

```bash
npx skills add MylesMCook/mcook-skills -g
npx skills check
npx skills update
```

Project-scoped installs write `skills-lock.json`, but current `check` and `update` flows do not use that lock file. To refresh a project-scoped install, rerun your original `add` command with the same flags.

## Repo Maintenance

```bash
npx skills add . --list
npx skills add . --skill simple-code -a universal -y
```
