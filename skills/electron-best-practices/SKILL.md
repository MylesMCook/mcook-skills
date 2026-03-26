---
name: electron-best-practices
description: Practical Electron guidance for building and maintaining desktop apps with clear main process, renderer, preload, IPC, BrowserWindow, packaging, Electron Forge, debugging, and security defaults. Use when working on Electron app creation, Electron Forge setup, preload or IPC design, window lifecycle, security hardening, packaging or distribution, auto-update work, or Electron debugging.
---

# Electron Best Practices

Use this skill for Electron work that needs durable guidance without relying on copied docs.

## Default Stance

- Prefer Electron Forge for new apps.
- Prefer TypeScript unless the project is already committed to plain JavaScript.
- Prefer preload scripts with `contextIsolation: true` and narrow IPC bridges.
- Prefer Vite for a new modern frontend build, but stay with Webpack or another existing toolchain when the project already uses it.
- Defer version-sensitive config, CLI flags, and API edge cases to the official docs in `references/doc-index.md`.

## Workflow

1. Identify whether the task is about architecture, security, IPC, packaging, updates, or tooling.
2. Open `references/doc-index.md` first to choose the right official source.
3. Open one focused reference file from this skill for durable guidance:
   - `references/architecture-and-security.md`
   - `references/forge-workflows.md`
   - `references/common-recipes.md`
4. Preserve the current project stack when it already exists. Only apply the Forge-first defaults when the user has not chosen another path.
5. When exact config or command syntax matters, verify it against the linked Electron or Electron Forge docs instead of guessing or reusing stale snippets.

## Reference Routing

- Use `references/architecture-and-security.md` for main vs renderer vs preload boundaries, secure IPC design, BrowserWindow defaults, and hardening.
- Use `references/forge-workflows.md` for scaffolding, TypeScript setup, Vite vs Webpack, makers, publishers, debugging, and update planning.
- Use `references/common-recipes.md` for evergreen implementation shapes such as secure IPC bridges, window lifecycle, menus and tray, native dialogs, and updater entrypoints.
- Use `references/doc-index.md` whenever you need the current official page for syntax, options, or release-sensitive behavior.

## Guardrails

- Do not expose raw Node access to renderer code unless the project has a deliberate and reviewed reason.
- Do not widen IPC channels more than the task requires.
- Do not migrate an existing build tool without a user reason.
- Do not treat this skill as a local mirror of Electron docs; treat it as a routing and decision layer over official docs.
