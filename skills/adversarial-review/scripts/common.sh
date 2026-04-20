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

resolve_cli_invocation() {
  local -n out="$1"
  local name="$2"

  out=()

  if [[ "${ADVERSARIAL_REVIEW_USE_PATH_ONLY:-0}" == "1" ]]; then
    command -v "$name" >/dev/null 2>&1 || return 1
    out+=("$(command -v "$name")")
    return 0
  fi

  if command -v powershell.exe >/dev/null 2>&1; then
    local source_path=""
    source_path="$(
      powershell.exe -NoProfile -Command "& { try { Get-Command '$name' -CommandType Application,ExternalScript -ErrorAction Stop | Select-Object -First 1 -ExpandProperty Source } catch { exit 1 } }" 2>/dev/null | tr -d '\r'
    )" || source_path=""

    if [[ -n "$source_path" ]]; then
      case "$source_path" in
        *.exe)
          if [[ -n "${WSL_DISTRO_NAME:-}" || -e /proc/sys/fs/binfmt_misc/WSLInterop || "$(uname -r 2>/dev/null)" == *[Mm]icrosoft* ]]; then
            local drive="${source_path:0:1}"
            local rest="${source_path:3}"
            rest="${rest//\\//}"
            out+=("/mnt/${drive,,}/$rest")
          else
            out+=("$source_path")
          fi
          return 0
          ;;
        *.ps1)
          out+=(powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "$source_path")
          return 0
          ;;
        *.cmd|*.bat)
          out+=(cmd.exe /c "$source_path")
          return 0
          ;;
      esac
    fi
  fi

  command -v "$name" >/dev/null 2>&1 || return 1
  out+=("$(command -v "$name")")
}

to_windows_path() {
  local path="$1"
  if [[ "$path" =~ ^/mnt/([a-zA-Z])/(.*)$ ]]; then
    local drive="${BASH_REMATCH[1]}"
    local rest="${BASH_REMATCH[2]//\//\\}"
    printf '%s:\\%s\n' "${drive^^}" "$rest"
    return 0
  fi

  printf '%s\n' "$path"
}
