#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

usage() {
  cat <<'EOF'
Usage:
  run_gemini_reviewer.sh --repo PATH --prompt-file PATH --output-file PATH
                         [--stdin-file PATH]
                         [--model MODEL]
                         [--timeout-seconds N]

Runs Gemini CLI in headless mode for read-only adversarial review.

Defaults:
  --model pro
  --timeout-seconds 300

Outputs:
  - final markdown review at --output-file
  - raw JSON response at --output-file.raw.json
  - stderr log at --output-file.stderr.log
EOF
}

repo=""
prompt_file=""
output_file=""
stdin_file=""
model="pro"
timeout_seconds="300"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="$(require_option_value "$1" "${2-}")"; shift 2 ;;
    --prompt-file)
      prompt_file="$(require_option_value "$1" "${2-}")"; shift 2 ;;
    --output-file)
      output_file="$(require_option_value "$1" "${2-}")"; shift 2 ;;
    --stdin-file)
      stdin_file="$(require_option_value "$1" "${2-}")"; shift 2 ;;
    --model)
      model="$(require_option_value "$1" "${2-}")"; shift 2 ;;
    --timeout-seconds)
      timeout_seconds="$(require_option_value "$1" "${2-}")"; shift 2 ;;
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

repo="$(abs_path "$repo")"
prompt_file="$(abs_path "$prompt_file")"
output_file="$(abs_path "$output_file")"
if [[ -n "$stdin_file" ]]; then
  stdin_file="$(abs_path "$stdin_file")"
fi

require_dir "$repo"
require_file "$prompt_file"
if [[ -n "$stdin_file" ]]; then
  require_file "$stdin_file"
fi

[[ "$timeout_seconds" =~ ^[0-9]+$ ]] || {
  echo "CALLER_MISUSE: --timeout-seconds must be a positive integer." >&2
  exit 2
}
(( timeout_seconds > 0 )) || {
  echo "CALLER_MISUSE: --timeout-seconds must be a positive integer." >&2
  exit 2
}

command -v gemini >/dev/null 2>&1 || {
  echo "MISSING_CLI: Gemini CLI ('gemini') is not installed or not on PATH." >&2
  exit 127
}

ensure_parent_dir "$output_file"
raw_output="${output_file}.raw.json"
stderr_output="${output_file}.stderr.log"

cleanup_files=()
cleanup() {
  if [[ ${#cleanup_files[@]} -gt 0 ]]; then
    rm -f "${cleanup_files[@]}"
  fi
}
trap cleanup EXIT

input_file="$(merge_reviewer_input "$prompt_file" "$stdin_file")"
cleanup_files+=("$input_file")

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

guarded_input_file="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini.XXXXXX")"
cleanup_files+=("$guarded_input_file")
{
  printf '%s\n\n' "$readonly_guardrails"
  cat "$input_file"
} > "$guarded_input_file"

cmd=(
  gemini
  --approval-mode plan
  --sandbox
  --output-format json
  --model "$model"
)
cmd+=(-p "Read the attached reviewer prompt from stdin and follow it exactly. Inspect the repository directly when needed. Return only the final markdown review.")

set +e
run_with_timeout "$repo" "$guarded_input_file" "$raw_output" "$stderr_output" "$timeout_seconds" "${cmd[@]}"
run_rc=$?
set -e
if (( run_rc != 0 )); then
  if (( run_rc == 124 )); then
    echo "TIMEOUT: Gemini reviewer timed out. See $raw_output and $stderr_output." >&2
  elif log_matches 'MODEL_CAPACITY_EXHAUSTED|No capacity available|rate limit|quota' "$raw_output" "$stderr_output"; then
    echo "CAPACITY_FAILURE: Gemini reviewer failed because capacity or rate limits are unavailable. See $raw_output and $stderr_output." >&2
  elif log_matches 'not logged in|invalid credentials|credential.*invalid|login required|unauthori[sz]ed' "$raw_output" "$stderr_output"; then
    echo "AUTH_FAILURE: Gemini reviewer failed because authentication is unavailable. See $raw_output and $stderr_output." >&2
  else
    echo "CLI_FAILURE: Gemini reviewer failed. See $raw_output and $stderr_output." >&2
  fi
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
    print("MALFORMED_OUTPUT: Gemini reviewer produced empty JSON output", file=sys.stderr)
    sys.exit(1)

try:
    data = json.loads(text)
except json.JSONDecodeError as exc:
    print(f"MALFORMED_OUTPUT: Could not parse Gemini JSON output: {exc}", file=sys.stderr)
    sys.exit(1)

error = data.get("error")
if error:
    if isinstance(error, dict):
        message = error.get("message") or json.dumps(error)
    else:
        message = str(error)
    lowered = message.lower()
    if "capacity" in lowered or "rate limit" in lowered or "quota" in lowered:
        print(f"CAPACITY_FAILURE: {message}", file=sys.stderr)
    elif any(token in lowered for token in ("not logged in", "invalid credentials", "credential", "login required", "unauthorized", "unauthorised")):
        print(f"AUTH_FAILURE: {message}", file=sys.stderr)
    else:
        print(f"CLI_FAILURE: {message}", file=sys.stderr)
    sys.exit(1)

response = (data.get("response") or "").strip()
if not response:
    print("MALFORMED_OUTPUT: Gemini reviewer JSON did not include a non-empty response field", file=sys.stderr)
    sys.exit(1)

out_path.write_text(response + "\n", encoding="utf-8")
PY

[[ -s "$output_file" ]] || {
  echo "MALFORMED_OUTPUT: Gemini reviewer completed without producing a non-empty output file: $output_file" >&2
  exit 1
}

echo "Wrote Gemini review to $output_file"
echo "Wrote Gemini raw response to $raw_output"
echo "Wrote Gemini stderr log to $stderr_output"
