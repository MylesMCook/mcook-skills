#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  run_claude_reviewer.sh --repo PATH --prompt-file PATH --output-file PATH
                         [--system-prompt-file PATH]
                         [--name NAME]
                         [--model MODEL]
                         [--tools TOOLS]
                         [--max-turns N]
                         [--effort low|medium|high]

Runs Claude Code in print mode for locked-down adversarial review.

Defaults:
  --tools     Read,Grep,Glob
  --max-turns 6
  --effort    medium

Outputs:
  - final markdown review at --output-file
  - raw JSON response at --output-file.raw.json
EOF
}

repo=""
prompt_file=""
output_file=""
system_prompt_file=""
name=""
model=""
tools="Read,Grep,Glob"
max_turns="6"
effort="medium"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="${2:-}"; shift 2 ;;
    --prompt-file)
      prompt_file="${2:-}"; shift 2 ;;
    --output-file)
      output_file="${2:-}"; shift 2 ;;
    --system-prompt-file)
      system_prompt_file="${2:-}"; shift 2 ;;
    --name)
      name="${2:-}"; shift 2 ;;
    --model)
      model="${2:-}"; shift 2 ;;
    --tools)
      tools="${2:-}"; shift 2 ;;
    --max-turns)
      max_turns="${2:-}"; shift 2 ;;
    --effort)
      effort="${2:-}"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2 ;;
  esac
done

[[ -n "$repo" ]] || { echo "--repo is required" >&2; exit 2; }
[[ -n "$prompt_file" ]] || { echo "--prompt-file is required" >&2; exit 2; }
[[ -n "$output_file" ]] || { echo "--output-file is required" >&2; exit 2; }

[[ -d "$repo" ]] || { echo "Repo directory does not exist: $repo" >&2; exit 2; }
[[ -f "$prompt_file" ]] || { echo "Prompt file does not exist: $prompt_file" >&2; exit 2; }
[[ -z "$system_prompt_file" || -f "$system_prompt_file" ]] || { echo "System prompt file does not exist: $system_prompt_file" >&2; exit 2; }

command -v claude >/dev/null 2>&1 || {
  echo "Claude Code CLI ('claude') is not installed or not on PATH" >&2
  exit 127
}

mkdir -p "$(dirname "$output_file")"
raw_output="${output_file}.raw.json"

cmd=(
  claude -p
  --output-format json
  --no-session-persistence
  --permission-mode dontAsk
  --tools "$tools"
  --add-dir "$repo"
  --max-turns "$max_turns"
  --effort "$effort"
)

if [[ -n "$name" ]]; then
  cmd+=(--name "$name")
fi

if [[ -n "$model" ]]; then
  cmd+=(--model "$model")
fi

if [[ -n "$system_prompt_file" ]]; then
  cmd+=(--append-system-prompt "$(cat "$system_prompt_file")")
fi

prompt="$(cat "$prompt_file")"
cmd+=(-- "$prompt")

if ! (
  cd "$repo"
  "${cmd[@]}"
) > "$raw_output"; then
  echo "Claude reviewer failed. See $raw_output for details." >&2
  exit 1
fi

python3 - "$raw_output" "$output_file" <<'PY'
import json
import pathlib
import sys

raw_path = pathlib.Path(sys.argv[1])
out_path = pathlib.Path(sys.argv[2])

text = raw_path.read_text(encoding="utf-8").strip()
if not text:
    print("Claude reviewer produced empty JSON output", file=sys.stderr)
    sys.exit(1)

try:
    data = json.loads(text)
except json.JSONDecodeError as exc:
    print(f"Could not parse Claude JSON output: {exc}", file=sys.stderr)
    sys.exit(1)

if data.get("is_error"):
    print(data.get("result", "Claude CLI reported an error"), file=sys.stderr)
    sys.exit(1)

result = (data.get("result") or "").strip()
if not result:
    print("Claude reviewer JSON did not include a non-empty result field", file=sys.stderr)
    sys.exit(1)

out_path.write_text(result + "\n", encoding="utf-8")
PY

[[ -s "$output_file" ]] || {
  echo "Claude reviewer completed without producing a non-empty output file: $output_file" >&2
  exit 1
}

echo "Wrote Claude review to $output_file"
echo "Wrote Claude raw response to $raw_output"
