# mcook-skills

Public `skills.sh` catalog of durable agent skills.

This catalog changes often. Use the CLI or [`skills/`](./skills) as the source of truth, not a hand-maintained list in this README.

## Browse

List everything currently available:

```bash
npx skills add MylesMCook/mcook-skills --list
```

## Install

Install the catalog into the current project:

```bash
npx skills add MylesMCook/mcook-skills
```

Install one skill to a generic agent layout:

```bash
npx skills add MylesMCook/mcook-skills --skill simple-code -a universal -y
```

Install from a local checkout while developing:

```bash
npx skills add ./mcook-skills
```

## Stay Current

Use the documented update command:

```bash
npx skills update
```

`npx skills upgrade` currently resolves to the same behavior in testing, but it is not documented by the upstream CLI, so this repo should point people to `update`.

If you want tracked updates for this catalog, install it globally:

```bash
npx skills add MylesMCook/mcook-skills -g
npx skills check
npx skills update
```

If you install the catalog with the default project-scoped command, the current CLI writes a local `skills-lock.json`, but `check` and `update` do not currently use that project lock file. To refresh a project install, rerun the original `add` command with the same flags you used the first time.

## Maintain This Repo

```bash
npx skills add . --list
npx skills add . --skill simple-code -a universal -y
```
