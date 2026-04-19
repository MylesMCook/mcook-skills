#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

usage() {
  cat <<'EOF'
Usage:
  run_claude_reviewer.sh --repo PATH --prompt-file PATH --output-file PATH
                         [--stdin-file PATH]
                         [--model MODEL]
                         [--timeout-seconds N]

Runs Claude Code in print mode for locked-down adversarial review.

Defaults:
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
model=""
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

command -v claude >/dev/null 2>&1 || {
  echo "MISSING_CLI: Claude Code CLI ('claude') is not installed or not on PATH." >&2
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

cmd=(
  claude -p
  --output-format json
  --no-session-persistence
  --permission-mode dontAsk
  --tools Read,Grep,Glob
  --disable-slash-commands
  --add-dir "$repo"
  --max-turns 10
  --effort medium
)
if [[ -n "$model" ]]; then
  cmd+=(--model "$model")
fi
cmd+=(-- "Read the attached reviewer prompt from stdin and follow it exactly. Inspect the repository directly when needed. Return only the final markdown review.")

set +e
run_with_timeout "$repo" "$input_file" "$raw_output" "$stderr_output" "$timeout_seconds" "${cmd[@]}"
run_rc=$?
set -e
if (( run_rc != 0 )); then
  if (( run_rc == 124 )); then
    echo "TIMEOUT: Claude reviewer timed out. See $raw_output and $stderr_output." >&2
  elif log_matches 'not logged in|invalid credentials|subscription|plan required|unauthori[sz]ed|login required' "$raw_output" "$stderr_output"; then
    echo "AUTH_FAILURE: Claude reviewer failed because authentication or entitlement is unavailable. See $raw_output and $stderr_output." >&2
  else
    echo "CLI_FAILURE: Claude reviewer failed. See $raw_output and $stderr_output." >&2
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
    print("MALFORMED_OUTPUT: Claude reviewer produced empty JSON output", file=sys.stderr)
    sys.exit(1)

try:
    data = json.loads(text)
except json.JSONDecodeError as exc:
    print(f"MALFORMED_OUTPUT: Could not parse Claude JSON output: {exc}", file=sys.stderr)
    sys.exit(1)

if data.get("is_error"):
    message = (data.get("result") or "Claude CLI reported an error").strip()
    lowered = message.lower()
    if any(token in lowered for token in ("not logged in", "invalid credentials", "subscription", "plan required", "unauthorized", "unauthorised", "login required")):
        print(f"AUTH_FAILURE: {message}", file=sys.stderr)
    elif any(token in lowered for token in ("capacity", "rate limit", "overloaded")):
        print(f"CAPACITY_FAILURE: {message}", file=sys.stderr)
    else:
        print(f"CLI_FAILURE: {message}", file=sys.stderr)
    sys.exit(1)

result = (data.get("result") or "").strip()
if not result:
    print("MALFORMED_OUTPUT: Claude reviewer JSON did not include a non-empty result field", file=sys.stderr)
    sys.exit(1)

out_path.write_text(result + "\n", encoding="utf-8")
PY

[[ -s "$output_file" ]] || {
  echo "MALFORMED_OUTPUT: Claude reviewer completed without producing a non-empty output file: $output_file" >&2
  exit 1
}

echo "Wrote Claude review to $output_file"
echo "Wrote Claude raw response to $raw_output"
echo "Wrote Claude stderr log to $stderr_output"
