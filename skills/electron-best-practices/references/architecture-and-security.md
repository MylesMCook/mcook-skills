# Architecture And Security

Use this file for durable decisions about process boundaries and app hardening.

## Process Roles

- Main process
  - Own app lifecycle, top-level window creation, native integrations, menus, tray, updates, and privileged OS interactions.
- Preload
  - Expose a small reviewed bridge from main capabilities to renderer code.
  - Keep this layer narrow, explicit, and typed.
- Renderer
  - Treat renderer code like a web app.
  - Keep business UI logic here, not privileged Node or OS access.

## Secure Default Shape

- Create BrowserWindow instances with security reviewed intentionally, not by habit.
- Prefer `contextIsolation: true`.
- Prefer `nodeIntegration: false`.
- Use preload to expose only the minimum needed surface.
- Validate IPC payloads at the receiving side, especially for file paths, shell execution, and update actions.
- Avoid broad event buses when a narrow request-response API is enough.
- Block unexpected navigation and unreviewed window creation when loading remote or semi-trusted content.
- Treat remote content as hostile unless the app design explicitly depends on it and has compensating controls.

## IPC Design Rules

- Use named channels that reflect one business action, not generic transport.
- Keep renderer-to-main APIs task-oriented.
  - Good: `dialog:openFile`, `settings:load`, `updates:check`
  - Bad: `system:exec`, `bridge:any`
- Return plain serializable data.
- Do not leak Electron objects, file handles, or privileged runtime references into renderer code.
- Keep write actions and destructive operations explicit.

## BrowserWindow Decision Points

- Decide early whether the app is:
  - fully local content
  - hybrid local plus remote
  - primarily remote
- The more remote content you load, the tighter the BrowserWindow and navigation rules should be.
- Keep window creation centralized so new windows inherit the same security baseline.

## Hardening Checklist

- Confirm preload is the only renderer bridge for privileged work.
- Confirm IPC handlers validate arguments and fail closed.
- Confirm the app does not silently widen permissions for convenience.
- Confirm external URLs open intentionally and outside the privileged renderer when appropriate.
- Confirm auto-update and installer flows are treated as trusted release infrastructure, not ad hoc downloads.

## When To Open Official Docs

- Open the Electron security docs for exact recommendations and newly added cautions.
- Open the BrowserWindow API docs for precise option names and defaults.
- Open the context isolation docs when designing or reviewing preload exposure patterns.
