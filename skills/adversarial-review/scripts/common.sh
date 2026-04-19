#!/usr/bin/env bash
set -euo pipefail

abs_path() {
  python3 - "$1" <<'PY'
import os
import sys

print(os.path.abspath(sys.argv[1]))
PY
}

require_dir() {
  local path="$1"
  [[ -d "$path" ]] || {
    echo "CALLER_MISUSE: Directory does not exist: $path" >&2
    exit 2
  }
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] || {
    echo "CALLER_MISUSE: File does not exist: $path" >&2
    exit 2
  }
}

require_option_value() {
  local option="$1"
  local value="${2-}"

  if [[ -z "$value" || "$value" == --* ]]; then
    echo "CALLER_MISUSE: $option requires a value." >&2
    exit 2
  fi

  printf '%s\n' "$value"
}

ensure_parent_dir() {
  mkdir -p "$(dirname "$1")"
}

merge_reviewer_input() {
  local prompt_file="$1"
  local stdin_file="${2:-}"
  local merged_file

  merged_file="$(mktemp "${TMPDIR:-/tmp}/adversarial-review.XXXXXX")"
  {
    cat "$prompt_file"
    if [[ -n "$stdin_file" ]]; then
      printf '\n\n## Attached Review Context\n\n'
      cat "$stdin_file"
    fi
  } > "$merged_file"

  printf '%s\n' "$merged_file"
}

run_with_timeout() {
  local cwd="$1"
  local stdin_file="${2:-}"
  local stdout_file="$3"
  local stderr_file="$4"
  local timeout_seconds="$5"
  shift 5

  python3 - "$cwd" "$stdin_file" "$stdout_file" "$stderr_file" "$timeout_seconds" "$@" <<'PY'
import pathlib
import subprocess
import sys

cwd = sys.argv[1]
stdin_file = sys.argv[2]
stdout_path = pathlib.Path(sys.argv[3])
stderr_path = pathlib.Path(sys.argv[4])
timeout_seconds = int(sys.argv[5])
cmd = sys.argv[6:]

stdin_data = None
if stdin_file:
    stdin_data = pathlib.Path(stdin_file).read_bytes()

try:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        input=stdin_data,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
except subprocess.TimeoutExpired as exc:
    stdout_path.write_bytes(exc.stdout or b"")
    stderr_path.write_bytes(exc.stderr or b"")
    print(
        f"TIMEOUT: reviewer timed out after {timeout_seconds} seconds.",
        file=sys.stderr,
    )
    sys.exit(124)

stdout_path.write_bytes(result.stdout)
stderr_path.write_bytes(result.stderr)
sys.exit(result.returncode)
PY
}

log_matches() {
  local pattern="$1"
  shift

  local paths=()
  local path
  for path in "$@"; do
    if [[ -n "$path" && -f "$path" ]]; then
      paths+=("$path")
    fi
  done

  [[ ${#paths[@]} -gt 0 ]] || return 1
  grep -Eiq -- "$pattern" "${paths[@]}"
}
