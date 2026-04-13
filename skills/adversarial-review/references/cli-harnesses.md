# CLI Harness Defaults

Always prefer the bundled scripts over manual CLI assembly.

## Host -> default reviewer order

- Codex host -> Claude Code, then Gemini CLI only as an optional third reviewer, then Codex only as a fallback or tie-breaker
- Claude host -> Codex CLI, then Gemini CLI only as an optional third reviewer, then Claude only as a fallback or tie-breaker
- Gemini host -> Codex CLI, Claude Code, then Gemini only as a third reviewer or fallback
- Any other host -> Codex CLI, Claude Code by default; Gemini CLI is optional

## Default reviewer set

- **Small change:** Skeptic + Architect from Codex + Claude when both primary harnesses are available
- **Medium or risky change:** Skeptic + Architect are mandatory; add Minimalist through Gemini only when the harness is installed and smoke-tested
- **Architecture plan:** Architect is mandatory
- **Deletion / simplification decision:** Minimalist is strongly preferred, but absence of Gemini should not block the review; use the strongest available harness on the Minimalist lens instead

## Availability policy

- Treat Codex CLI and Claude Code as the primary reviewer dependencies.
- Treat Gemini CLI as optional and best-effort.
- If Gemini is missing, unauthenticated, or fails, continue with Codex + Claude and report reduced reviewer diversity.
- Only promote Gemini back into the default path after successful smoke tests in the target environment.

## Codex CLI

Use `scripts/run_codex_reviewer.sh`.

Why this wrapper exists:

- It uses `codex exec`, the non-interactive interface intended for scripted runs.
- It forces a read-only sandbox and disables approval prompts so the reviewer does not stall on sandbox questions.
- It writes a raw JSONL log and a separate final markdown result file.

Default behavior:

- working directory is the repo root
- sandbox is `read-only`
- approvals are `never`
- prompt is read from `--prompt-file`
- optional large context can be merged with `--stdin-file`

Do not use `--full-auto`, `--yolo`, or `danger-full-access` for review runs.

## Claude Code

Use `scripts/run_claude_reviewer.sh`.

Why this wrapper exists:

- It uses `claude -p`, the official headless / print-mode interface.
- It disables session persistence, limits turns, and locks the run to read-only review tooling.
- It parses the JSON result into a clean markdown file.

Default behavior:

- print mode only
- tools limited to `Read,Grep,Glob`
- permission mode is `dontAsk`
- no session persistence
- optional system prompt file supported

Important note:

- In `claude -p`, slash commands and skills are not available. Describe the task directly in the prompt.
- Do not use `bypassPermissions` for reviewer runs.

## Gemini CLI

Use `scripts/run_gemini_reviewer.sh` only as an optional third reviewer or fallback.

Why this wrapper exists:

- It uses headless `gemini -p` with structured JSON output.
- It turns on sandboxing and keeps the run in read-only plan mode.
- It parses the `.response` field into a markdown output file.

Default behavior:

- approval mode is `plan`
- sandboxing is on
- prompt is compact and may be combined with large stdin context
- wrapper prepends read-only guardrails so Gemini returns findings directly instead of drifting into implementation

Important note:

- Keep the prompt compact.
- Do not ask Gemini to implement, create plan artifacts, or exit plan mode during a reviewer run.
