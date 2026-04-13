#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  run_gemini_reviewer.sh --repo PATH --prompt-file PATH --output-file PATH
                         [--stdin-file PATH]
                         [--model MODEL]
                         [--include-directory PATH]

Runs Gemini CLI in headless mode for read-only adversarial review.

Defaults:
  --model pro

Outputs:
  - final markdown review at --output-file
  - raw JSON response at --output-file.raw.json
EOF
}

repo=""
prompt_file=""
output_file=""
stdin_file=""
model="pro"
declare -a include_directories=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="${2:-}"; shift 2 ;;
    --prompt-file)
      prompt_file="${2:-}"; shift 2 ;;
    --output-file)
      output_file="${2:-}"; shift 2 ;;
    --stdin-file)
      stdin_file="${2:-}"; shift 2 ;;
    --model)
      model="${2:-}"; shift 2 ;;
    --include-directory)
      include_directories+=("${2:-}"); shift 2 ;;
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
[[ -z "$stdin_file" || -f "$stdin_file" ]] || { echo "Stdin file does not exist: $stdin_file" >&2; exit 2; }

command -v gemini >/dev/null 2>&1 || {
  echo "Gemini CLI ('gemini') is not installed or not on PATH" >&2
  exit 127
}

mkdir -p "$(dirname "$output_file")"
raw_output="${output_file}.raw.json"

readonly_guardrails=$(
  cat <<'EOF'
You are running as an external adversarial code reviewer.
Stay strictly read-only.
Do not modify files.
Do not create or edit plan files.
Do not exit plan mode.
Do not implement fixes.
Do not ask for interactive approval.
Return the review directly in markdown.
EOF
)

full_prompt="${readonly_guardrails}

$(cat "$prompt_file")"

cmd=(
  gemini
  --approval-mode plan
  --sandbox
  --output-format json
  --model "$model"
)

if [[ ${#include_directories[@]} -gt 0 ]]; then
  for dir in "${include_directories[@]}"; do
    cmd+=(--include-directories "$dir")
  done
fi

cmd+=(-p "$full_prompt")

if [[ -n "$stdin_file" ]]; then
  if ! (
    cd "$repo"
    cat "$stdin_file" | "${cmd[@]}"
  ) > "$raw_output"; then
    echo "Gemini reviewer failed. See $raw_output for details." >&2
    exit 1
  fi
else
  if ! (
    cd "$repo"
    "${cmd[@]}"
  ) > "$raw_output"; then
    echo "Gemini reviewer failed. See $raw_output for details." >&2
    exit 1
  fi
fi

python3 - "$raw_output" "$output_file" <<'PY'
import json
import pathlib
import sys

raw_path = pathlib.Path(sys.argv[1])
out_path = pathlib.Path(sys.argv[2])

text = raw_path.read_text(encoding="utf-8").strip()
if not text:
    print("Gemini reviewer produced empty JSON output", file=sys.stderr)
    sys.exit(1)

try:
    data = json.loads(text)
except json.JSONDecodeError as exc:
    print(f"Could not parse Gemini JSON output: {exc}", file=sys.stderr)
    sys.exit(1)

error = data.get("error")
if error:
    if isinstance(error, dict):
      message = error.get("message") or json.dumps(error)
    else:
      message = str(error)
    print(f"Gemini CLI reported an error: {message}", file=sys.stderr)
    sys.exit(1)

response = (data.get("response") or "").strip()
if not response:
    print("Gemini reviewer JSON did not include a non-empty response field", file=sys.stderr)
    sys.exit(1)

out_path.write_text(response + "\n", encoding="utf-8")
PY

[[ -s "$output_file" ]] || {
  echo "Gemini reviewer completed without producing a non-empty output file: $output_file" >&2
  exit 1
}

echo "Wrote Gemini review to $output_file"
echo "Wrote Gemini raw response to $raw_output"
