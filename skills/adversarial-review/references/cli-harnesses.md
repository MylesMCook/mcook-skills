# CLI Harness Defaults

Always prefer the bundled scripts over manual CLI assembly.

## Host -> default reviewer order

- Codex host -> Claude Code and Gemini CLI first, then Codex CLI to complete the trio
- Claude host -> Codex CLI and Gemini CLI first, then Claude Code to complete the trio
- Gemini host -> Codex CLI and Claude Code first, then Gemini CLI to complete the trio
- Any other host -> Codex CLI, Claude Code, and Gemini CLI by default

## Default reviewer set

- **Small change:** Skeptic + Architect + Minimalist from Codex + Claude + Gemini when all three are available
- **Medium or risky change:** Skeptic + Architect + Minimalist from Codex + Claude + Gemini when all three are available
- **Architecture plan:** Architect is mandatory
- **Deletion / simplification decision:** Minimalist is mandatory; use Gemini by default, or the strongest available harness if Gemini is unavailable

## Availability policy

- Treat Codex CLI and Claude Code as the primary reviewer dependencies.
- Treat Gemini CLI as a default reviewer dependency when it is installed and authenticated.
- If Gemini is missing, unauthenticated, or fails, continue with Codex + Claude and report reduced reviewer diversity.
- If Gemini has not passed a smoke test in the target environment, run Codex + Claude and report that the Minimalist reviewer was skipped.

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

Use `scripts/run_gemini_reviewer.sh` for the default Minimalist reviewer when Gemini CLI is installed and authenticated.

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
