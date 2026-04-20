#!/usr/bin/env bash
set -euo pipefail

state_dir="${FIXTURE_STATE_DIR:?}"
args_file="$state_dir/claude.args"
stdin_file="$state_dir/claude.stdin"

mkdir -p "$state_dir"
{
  for arg in "$@"; do
    printf '%q\n' "$arg"
  done
} > "$args_file"
cat > "$stdin_file"

mode="${FIXTURE_CLAUDE_MODE:-success}"

case "$mode" in
  success)
    printf '{"is_error":false,"result":"Claude OK"}\n'
    ;;
  auth_failure)
    printf '{"is_error":true,"result":"Not logged in"}\n'
    echo "not logged in" >&2
    exit 1
    ;;
  turn_limit)
    printf '{"is_error":true,"result":"turn limit exceeded"}\n'
    echo "turn limit exceeded" >&2
    exit 1
    ;;
  input_error)
    printf '{"is_error":true,"result":"Invalid prompt"}\n'
    echo "invalid prompt" >&2
    exit 1
    ;;
  *)
    echo "unknown fixture mode: $mode" >&2
    exit 1
    ;;
esac
