#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

usage() {
  cat <<'EOF'
Usage:
  run_codex_reviewer.sh --repo PATH --prompt-file PATH --output-file PATH
                        [--stdin-file PATH]
                        [--model MODEL]
                        [--timeout-seconds N]
                        [--sandbox read-only]

Runs Codex CLI in non-interactive mode for read-only adversarial review.

Defaults:
  --sandbox read-only
  --model   use the CLI's configured default model
  --timeout-seconds 300

Outputs:
  - final markdown review at --output-file
  - raw JSONL event log at --output-file.raw.jsonl
  - stderr log at --output-file.stderr.log
EOF
}

repo=""
prompt_file=""
output_file=""
stdin_file=""
model=""
sandbox="read-only"
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
    --sandbox)
      sandbox="$(require_option_value "$1" "${2-}")"; shift 2 ;;
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

if [[ "$sandbox" != "read-only" ]]; then
  echo "CALLER_MISUSE: Codex reviewer only supports --sandbox read-only." >&2
  exit 2
fi

[[ "$timeout_seconds" =~ ^[0-9]+$ ]] || {
  echo "CALLER_MISUSE: --timeout-seconds must be a positive integer." >&2
  exit 2
}
(( timeout_seconds > 0 )) || {
  echo "CALLER_MISUSE: --timeout-seconds must be a positive integer." >&2
  exit 2
}

cli_cmd=()
resolve_cli_invocation cli_cmd codex || {
  echo "MISSING_CLI: Codex CLI ('codex') is not installed or not on PATH." >&2
  exit 127
}

ensure_parent_dir "$output_file"
raw_output="${output_file}.raw.jsonl"
stderr_output="${output_file}.stderr.log"
rm -f "$output_file" "$raw_output" "$stderr_output"

prompt_text="$(cat "$prompt_file")"

repo_arg="$repo"
output_file_arg="$output_file"
if [[ "${cli_cmd[0]}" == "powershell.exe" ]]; then
  repo_arg="$(to_windows_path "$repo")"
  output_file_arg="$(to_windows_path "$output_file")"
fi

cmd=(
  "${cli_cmd[@]}"
  --ask-for-approval never
  exec
  --cd "$repo_arg"
  --sandbox "$sandbox"
  --ephemeral
  --json
  --output-last-message "$output_file_arg"
)

if [[ -n "$model" ]]; then
  cmd+=(--model "$model")
fi

if ! command -v git >/dev/null 2>&1 || ! git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  cmd+=(--skip-git-repo-check)
fi

cmd+=("$prompt_text")

set +e
run_with_timeout "$repo" "$stdin_file" "$raw_output" "$stderr_output" "$timeout_seconds" "${cmd[@]}"
run_rc=$?
set -e
if (( run_rc != 0 )); then
  if (( run_rc == 124 )); then
    echo "TIMEOUT: Codex reviewer timed out. See $raw_output and $stderr_output." >&2
  elif log_matches 'unexpected argument|invalid value|requires a value|error:|usage:' "$raw_output" "$stderr_output"; then
    echo "INPUT_ERROR: Codex reviewer rejected the prompt or arguments. See $raw_output and $stderr_output." >&2
  elif log_matches 'TokenRefreshFailed|invalid_grant|access token could not be refreshed|token_expired|Unauthorized' "$raw_output" "$stderr_output"; then
    echo "AUTH_FAILURE: Codex reviewer failed because authentication is stale or unavailable. See $raw_output and $stderr_output." >&2
  elif log_matches 'rate limit|429|quota|capacity|overloaded' "$raw_output" "$stderr_output"; then
    echo "CAPACITY_FAILURE: Codex reviewer failed because capacity or rate limits are unavailable. See $raw_output and $stderr_output." >&2
  else
    echo "CLI_FAILURE: Codex reviewer failed. See $raw_output and $stderr_output." >&2
  fi
  exit 1
fi

[[ -s "$output_file" ]] || {
  echo "MALFORMED_OUTPUT: Codex reviewer completed without producing a non-empty output file: $output_file" >&2
  exit 1
}

echo "Wrote Codex review to $output_file"
echo "Wrote Codex raw log to $raw_output"
echo "Wrote Codex stderr log to $stderr_output"
