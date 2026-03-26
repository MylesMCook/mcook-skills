# Common Recipes

Use this file for stable implementation shapes. Treat the patterns below as design templates, not copy-paste canonical code.

## Secure IPC Bridge

- Define a narrow preload API with one method per user-facing action.
- Expose only those methods through the preload layer.
- Handle privileged work in the main process.
- Validate payloads in the main process before touching the filesystem, shell, or updater.

Preferred shape:

1. Renderer calls a small preload method.
2. Preload forwards to one named IPC channel.
3. Main validates input and performs the privileged action.
4. Main returns plain data or a typed error shape.

## Window Lifecycle

- Create windows from a single factory path.
- Apply one shared security baseline to every BrowserWindow.
- Restore or persist size and position only if the app actually needs it.
- Keep app lifecycle events, window recreation, and external link handling centralized in the main process.

## Menus And Tray

- Keep menu and tray actions as thin entrypoints into the same commands used elsewhere.
- Do not duplicate business logic in menu handlers.
- Route menu and tray actions into reviewed main-process actions or typed IPC contracts.

## Native Dialogs

- Open dialogs from the main process.
- Return only the result the renderer actually needs, such as selected paths or cancellation state.
- Normalize and validate selected paths before follow-up work.

## Updater Entry Points

- Keep updater initialization in the main process.
- Expose only user-relevant actions to renderer code, such as check status or restart-to-update.
- Keep release hosting, signing, and channel logic out of renderer code.

## Rule Of Thumb

- If a recipe needs exact API names, current flags, or platform caveats, switch to `doc-index.md` and verify against the official Electron or Forge page before implementing it.
