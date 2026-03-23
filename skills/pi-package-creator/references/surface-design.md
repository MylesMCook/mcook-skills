# Surface Design

Use this file when deciding what a Pi package should contain.

## Supported package resource types

Pi packages can bundle:
- `extensions`
- `skills`
- `prompts`
- `themes`

Use the exact `package.json` `pi` manifest keys above. Do not invent aliases.

## Pick the right surface

### extensions

Use for:
- slash commands
- hooks
- tools
- ambient behavior
- UI or TUI additions
- plumbing that should not live in a skill

### skills

Use for:
- reusable workflows
- domain-specific guidance
- tasks that should trigger from user intent

Keep skills narrow. Good descriptions matter more than lots of body text.

### prompts

Use for:
- reusable prompt templates
- opinionated session starters

Do not add prompts unless the prompt itself is part of the package's user value.

### themes

Use for:
- appearance only

Do not mix a theme into a package unless the theme is part of the actual
product, not just a nice extra.

## Minimal `package.json` shape

```json
{
  "name": "@scope/example",
  "version": "0.1.0",
  "license": "MIT",
  "keywords": ["pi-package"],
  "pi": {
    "extensions": ["./extensions"]
  }
}
```

Notes:
- include only the keys you actually use
- other supported keys are `skills`, `prompts`, and `themes`
- manifest values are relative paths
- advanced package manifests can use glob patterns and `!exclusions`, but keep
  the first package shape literal and minimal unless you need that extra power
- this example shows one valid directory-based shape; check the installed Pi
  docs before copying it to another surface mechanically
- keep `files` tight if you ship to npm

## Public-surface rules

- Lead with what the package is, not what it might become later.
- If the package is Pi-only, say so early.
- If install is local-path-only today, say so literally.
- Do not widen the audience with metadata or keywords the package does not
  actually support.
- Keep internal strategy docs out of the public docs surface unless they are
  meant for users.

## Smells

- a `v1` package ships every resource type "just in case"
- README promises a generic agent product but the package only works in Pi
- metadata links or install instructions point somewhere that is not real yet
