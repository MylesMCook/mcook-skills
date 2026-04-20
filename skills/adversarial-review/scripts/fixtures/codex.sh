#!/usr/bin/env bash
set -euo pipefail

state_dir="${FIXTURE_STATE_DIR:?}"
args_file="$state_dir/codex.args"
stdin_file="$state_dir/codex.stdin"
out_file=""

mkdir -p "$state_dir"
{
  for arg in "$@"; do
    printf '%q\n' "$arg"
  done
} > "$args_file"
cat > "$stdin_file"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-last-message)
      out_file="${2-}"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

mode="${FIXTURE_CODEX_MODE:-${FIXTURE_MODE:-success}}"

case "$mode" in
  success)
    [[ -n "$out_file" ]] || { echo "missing output-last-message" >&2; exit 1; }
    printf 'Codex OK\n' > "$out_file"
    printf '{"type":"thread.started","thread_id":"fixture-thread"}\n'
    printf '{"type":"turn.completed","usage":{"output_tokens":1}}\n'
    ;;
  auth_failure)
    echo "authentication unavailable" >&2
    exit 1
    ;;
  input_error)
    echo "error: invalid prompt" >&2
    exit 2
    ;;
  *)
    echo "unknown fixture mode: $mode" >&2
    exit 1
    ;;
esac
