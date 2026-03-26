# Electron Doc Index

Use this file to route to the current official documentation before writing version-sensitive Electron code or config.

## Electron Core Docs

- Process model
  - Use for main process, renderer process, preload, and process ownership questions.
  - https://www.electronjs.org/docs/latest/tutorial/process-model
- IPC
  - Use for `ipcMain`, `ipcRenderer`, request-response patterns, and event boundaries.
  - https://www.electronjs.org/docs/latest/tutorial/ipc
- Security
  - Use for hardening guidance, untrusted content, permissions, navigation, and content isolation rules.
  - https://www.electronjs.org/docs/latest/tutorial/security
- Context isolation
  - Use when designing preload APIs and deciding what the renderer may access.
  - https://www.electronjs.org/docs/latest/tutorial/context-isolation
- BrowserWindow API
  - Use for exact constructor options, lifecycle hooks, and `webContents` interactions.
  - https://www.electronjs.org/docs/latest/api/browser-window
- Auto updates
  - Use for current updater flow, platform expectations, and release hosting requirements.
  - https://www.electronjs.org/docs/latest/tutorial/updates
- Debugging the main process
  - Use for current debugging flags and inspector workflows.
  - https://www.electronjs.org/docs/latest/tutorial/debugging-main-process

## Electron Forge Docs

- Getting started
  - Use for new app setup and the current recommended Forge entrypoint.
  - https://www.electronforge.io/
- TypeScript setup
  - Use when adding or correcting TypeScript support in a Forge project.
  - https://www.electronforge.io/guides/typescript
- Vite plugin
  - Use for current Vite plugin config, entry setup, and caveats.
  - https://www.electronforge.io/config/plugins/vite
- Webpack plugin
  - Use for existing Webpack-based Forge apps or when the project already chose Webpack.
  - https://www.electronforge.io/config/plugins/webpack
- Makers
  - Use for platform-specific distributables such as DMG, Squirrel, ZIP, AppImage, or Flatpak.
  - https://www.electronforge.io/config/makers
- Publishers
  - Use for release publishing and distribution automation.
  - https://www.electronforge.io/config/publishers
- Debugging
  - Use for current Forge debugging workflows and tooling integration.
  - https://www.electronforge.io/advanced/debugging

## How To Use This Skill

- Read the matching local reference file first for durable decisions.
- Open the official page above when you need exact syntax, current defaults, or release-sensitive behavior.
- Prefer the official doc over old snippets copied from prior Electron projects.
