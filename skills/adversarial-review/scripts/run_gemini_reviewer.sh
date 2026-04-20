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

Runs Gemini CLI in strict scripted review mode with session cleanup.

Defaults:
  --model pro
  --timeout-seconds 300

Outputs:
  - final markdown review at --output-file
  - raw JSONL event log at --output-file.raw.jsonl
  - stderr log at --output-file.stderr.log

Isolation:
  - default: disposable copy sandbox, no mutation of the real repo
  - optional: set ADVERSARIAL_REVIEW_GEMINI_SANDBOX_MODE=process to require Gemini --sandbox
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

cli_cmd=()
resolve_cli_invocation cli_cmd gemini || {
  echo "MISSING_CLI: Gemini CLI ('gemini') is not installed or not on PATH." >&2
  exit 127
}

ensure_parent_dir "$output_file"
raw_output="${output_file}.raw.jsonl"
stderr_output="${output_file}.stderr.log"
rm -f "$output_file" "$raw_output" "$stderr_output"

cleanup_files=()
cleanup_dirs=()
cleanup() {
  if [[ ${#cleanup_files[@]} -gt 0 ]]; then
    rm -f "${cleanup_files[@]}"
  fi
  if [[ ${#cleanup_dirs[@]} -gt 0 ]]; then
    rm -rf "${cleanup_dirs[@]}"
  fi
}
trap cleanup EXIT

sandbox_mode="${ADVERSARIAL_REVIEW_GEMINI_SANDBOX_MODE:-copy}"
run_repo="$repo"
case "$sandbox_mode" in
  copy)
    scratch_parent="$(mktemp -d "$(dirname "$output_file")/adversarial-review-gemini-repo.XXXXXX")"
    cleanup_dirs+=("$scratch_parent")
    run_repo="$scratch_parent/repo"
    python3 - "$repo" "$run_repo" <<'PY'
import pathlib
import shutil
import sys

src = pathlib.Path(sys.argv[1])
dst = pathlib.Path(sys.argv[2])
ignore_names = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".next",
    ".turbo",
    "dist",
    "build",
}

def ignore(_dir, names):
    return [name for name in names if name in ignore_names]

shutil.copytree(src, dst, ignore=ignore)
PY
    ;;
  process)
    ;;
  *)
    echo "CALLER_MISUSE: ADVERSARIAL_REVIEW_GEMINI_SANDBOX_MODE must be 'copy' or 'process'." >&2
    exit 2
    ;;
esac

guarded_input_file="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini.XXXXXX")"
cleanup_files+=("$guarded_input_file")

guardrails_prompt=$(
  cat <<'EOF'
You are running as an external adversarial code reviewer.
Stay strictly read-only.
Do not modify files.
Do not create or edit plan files.
Do not exit plan mode.
Do not write task-tracker updates.
Do not activate skills.
Do not call save_memory.
Do not implement fixes.
Do not ask for interactive approval.
Return the review directly in markdown.
EOF
)

{
  cat "$prompt_file"
  if [[ -n "$stdin_file" ]]; then
    printf '\n## Attached Review Context\n\n'
    cat "$stdin_file"
  fi
} > "$guarded_input_file"

gemini_no_sandbox_cmd=(env GEMINI_SANDBOX=false "${cli_cmd[@]}")

cmd=(
  "${gemini_no_sandbox_cmd[@]}"
  --approval-mode plan
  --output-format stream-json
  --model "$model"
  -p "$guardrails_prompt"
)
if [[ "$sandbox_mode" == "process" ]]; then
  cmd=(
    "${cli_cmd[@]}"
    --approval-mode plan
    --sandbox
    --output-format stream-json
    --model "$model"
    -p "$guardrails_prompt"
  )
fi

before_sessions_stdout="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-before.out.XXXXXX")"
before_sessions_stderr="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-before.err.XXXXXX")"
cleanup_files+=("$before_sessions_stdout" "$before_sessions_stderr")
before_list_rc=0
set +e
run_with_timeout "$run_repo" "" "$before_sessions_stdout" "$before_sessions_stderr" 30 "${gemini_no_sandbox_cmd[@]}" --list-sessions
before_list_rc=$?
set -e

set +e
run_with_timeout "$run_repo" "$guarded_input_file" "$raw_output" "$stderr_output" "$timeout_seconds" "${cmd[@]}"
run_rc=$?
set -e

session_id_file="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-session.XXXXXX")"
cleanup_files+=("$session_id_file")

parse_rc=0
python3 - "$raw_output" "$output_file" "$session_id_file" "$run_rc" <<'PY'
import json
import pathlib
import sys

raw_path = pathlib.Path(sys.argv[1])
out_path = pathlib.Path(sys.argv[2])
session_path = pathlib.Path(sys.argv[3])
run_rc = int(sys.argv[4])

def text_from(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = [text_from(item) for item in value]
        parts = [part for part in parts if part]
        return "\n".join(parts).strip()
    if isinstance(value, dict):
        for key in ("response", "text", "output", "message", "content"):
            if key in value:
                extracted = text_from(value[key])
                if extracted:
                    return extracted
        if "parts" in value:
            extracted = text_from(value["parts"])
            if extracted:
                return extracted
    return ""

def find_session_id(value):
    if isinstance(value, dict):
        for key in ("session_id", "sessionId", "id"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
        for key in ("session", "metadata", "data"):
            candidate = find_session_id(value.get(key))
            if candidate:
                return candidate
    if isinstance(value, list):
        for item in value:
            candidate = find_session_id(item)
            if candidate:
                return candidate
    return None

lines = raw_path.read_text(encoding="utf-8").splitlines()
if not lines:
    if run_rc == 0:
        print("MALFORMED_OUTPUT: Gemini reviewer produced empty JSONL output", file=sys.stderr)
        sys.exit(1)
    raise SystemExit(0)

session_id = None
response = ""
parse_error = None

for line in lines:
    line = line.strip()
    if not line:
        continue
    try:
        event = json.loads(line)
    except json.JSONDecodeError as exc:
        if run_rc == 0:
            parse_error = f"MALFORMED_OUTPUT: Could not parse Gemini stream JSON: {exc}"
        continue

    if session_id is None:
        session_id = find_session_id(event)

    if response:
        continue

    if isinstance(event, dict):
        event_type = event.get("type")
        if event_type in {"result", "message"}:
            if event_type == "message" and event.get("role") not in {None, "assistant"}:
                pass
            else:
                response = text_from(event)
        elif "response" in event:
            response = text_from(event["response"])

if session_id:
    session_path.write_text(session_id + "\n", encoding="utf-8")

if run_rc == 0:
    if parse_error:
        print(parse_error, file=sys.stderr)
        sys.exit(1)
    if not session_id:
        print("MALFORMED_OUTPUT: Gemini reviewer stream did not include a session id", file=sys.stderr)
        sys.exit(1)
    if not response:
        print("MALFORMED_OUTPUT: Gemini reviewer stream did not include a final response", file=sys.stderr)
        sys.exit(1)
    out_path.write_text(response + "\n", encoding="utf-8")
PY
parse_rc=$?
if (( parse_rc != 0 )); then
  if [[ -s "$session_id_file" ]]; then
    session_id="$(cat "$session_id_file" | tr -d '\r\n')"
    cleanup_stdout="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-cleanup.out.XXXXXX")"
    cleanup_stderr="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-cleanup.err.XXXXXX")"
    cleanup_files+=("$cleanup_stdout" "$cleanup_stderr")
    session_index="$(
      python3 - "$run_repo" "$session_id" "${gemini_no_sandbox_cmd[@]}" --list-sessions <<'PY'
import pathlib
import re
import subprocess
import sys

repo = sys.argv[1]
session_id = sys.argv[2]
result = subprocess.run(
    sys.argv[3:],
    cwd=repo,
    capture_output=True,
    text=True,
    timeout=30,
    check=False,
)
if result.returncode != 0:
    sys.stderr.write(result.stderr)
    raise SystemExit(result.returncode or 1)

pattern = re.compile(r"^\s*(\d+)\.\s+.*\[(?P<session>[^\]]+)\]\s*$")
for line in result.stdout.splitlines():
    match = pattern.match(line)
    if match and match.group("session") == session_id:
        print(match.group(1))
        raise SystemExit(0)
PY
    )" || {
      rm -f "$output_file"
      echo "CLEANUP_FAILURE: Gemini reviewer session cleanup failed before delete. See $stderr_output." >&2
      exit 1
    }
    if [[ -n "$session_index" ]]; then
      set +e
      run_with_timeout "$run_repo" "" "$cleanup_stdout" "$cleanup_stderr" "$timeout_seconds" "${gemini_no_sandbox_cmd[@]}" --delete-session "$session_index"
      cleanup_rc=$?
      set -e
      if (( cleanup_rc != 0 )); then
        rm -f "$output_file"
        echo "CLEANUP_FAILURE: Gemini reviewer session cleanup failed. See $cleanup_stdout and $cleanup_stderr." >&2
        exit 1
      fi
    fi
  elif (( before_list_rc == 0 )); then
    after_sessions_stdout="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-after.out.XXXXXX")"
    after_sessions_stderr="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-after.err.XXXXXX")"
    cleanup_files+=("$after_sessions_stdout" "$after_sessions_stderr")
    set +e
    run_with_timeout "$run_repo" "" "$after_sessions_stdout" "$after_sessions_stderr" 30 "${gemini_no_sandbox_cmd[@]}" --list-sessions
    after_list_rc=$?
    set -e
    if (( after_list_rc != 0 )); then
      rm -f "$output_file"
      echo "CLEANUP_FAILURE: Gemini reviewer session cleanup failed after malformed output. See $after_sessions_stdout and $after_sessions_stderr." >&2
      exit 1
    fi

    session_index="$(
      python3 - "$before_sessions_stdout" "$after_sessions_stdout" <<'PY'
import pathlib
import re
import sys

pattern = re.compile(r"^\s*(\d+)\.\s+.*\[(?P<session>[^\]]+)\]\s*$")

def read_sessions(path):
    sessions = {}
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            sessions[match.group("session")] = match.group(1)
    return sessions

before = read_sessions(sys.argv[1])
after = read_sessions(sys.argv[2])
new_ids = [session_id for session_id in after if session_id not in before]

if len(new_ids) > 1:
    sys.stderr.write(f"ambiguous new sessions: {new_ids}\n")
    raise SystemExit(1)
if len(new_ids) == 1:
    print(after[new_ids[0]])
PY
    )" || {
      rm -f "$output_file"
      echo "CLEANUP_FAILURE: Gemini reviewer session cleanup could not identify the new persisted session. See $after_sessions_stdout and $after_sessions_stderr." >&2
      exit 1
    }

    if [[ -n "$session_index" ]]; then
      cleanup_stdout="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-cleanup.out.XXXXXX")"
      cleanup_stderr="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-cleanup.err.XXXXXX")"
      cleanup_files+=("$cleanup_stdout" "$cleanup_stderr")
      set +e
      run_with_timeout "$run_repo" "" "$cleanup_stdout" "$cleanup_stderr" "$timeout_seconds" "${gemini_no_sandbox_cmd[@]}" --delete-session "$session_index"
      cleanup_rc=$?
      set -e
      if (( cleanup_rc != 0 )); then
        rm -f "$output_file"
        echo "CLEANUP_FAILURE: Gemini reviewer session cleanup failed after malformed output. See $cleanup_stdout and $cleanup_stderr." >&2
        exit 1
      fi
    fi
  fi
  exit 1
fi

session_id="$(cat "$session_id_file" | tr -d '\r\n')"

cleanup_stdout="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-cleanup.out.XXXXXX")"
cleanup_stderr="$(mktemp "${TMPDIR:-/tmp}/adversarial-review-gemini-cleanup.err.XXXXXX")"
cleanup_files+=("$cleanup_stdout" "$cleanup_stderr")

session_index="$(
  python3 - "$run_repo" "$session_id" "${gemini_no_sandbox_cmd[@]}" --list-sessions <<'PY'
import pathlib
import re
import subprocess
import sys

repo = sys.argv[1]
session_id = sys.argv[2]
result = subprocess.run(
    sys.argv[3:],
    cwd=repo,
    capture_output=True,
    text=True,
    timeout=30,
    check=False,
)
if result.returncode != 0:
    sys.stderr.write(result.stderr)
    raise SystemExit(result.returncode or 1)

pattern = re.compile(r"^\s*(\d+)\.\s+.*\[(?P<session>[^\]]+)\]\s*$")
for line in result.stdout.splitlines():
    match = pattern.match(line)
    if match and match.group("session") == session_id:
        print(match.group(1))
        raise SystemExit(0)
PY
)" || {
  rm -f "$output_file"
  echo "CLEANUP_FAILURE: Gemini reviewer session cleanup failed before delete. See $stderr_output." >&2
  exit 1
}

if [[ -n "$session_index" ]]; then
  set +e
  run_with_timeout "$run_repo" "" "$cleanup_stdout" "$cleanup_stderr" "$timeout_seconds" "${gemini_no_sandbox_cmd[@]}" --delete-session "$session_index"
  cleanup_rc=$?
  set -e
  if (( cleanup_rc != 0 )); then
    rm -f "$output_file"
    echo "CLEANUP_FAILURE: Gemini reviewer session cleanup failed. See $cleanup_stdout and $cleanup_stderr." >&2
    exit 1
  fi
fi

if (( run_rc != 0 )); then
  if (( run_rc == 124 )); then
    echo "TIMEOUT: Gemini reviewer timed out. See $raw_output and $stderr_output." >&2
  elif (( run_rc == 42 )); then
    echo "INPUT_ERROR: Gemini reviewer rejected the prompt or arguments. See $raw_output and $stderr_output." >&2
  elif (( run_rc == 53 )); then
    echo "TURN_LIMIT: Gemini reviewer exceeded the turn limit. See $raw_output and $stderr_output." >&2
  elif log_matches 'MODEL_CAPACITY_EXHAUSTED|No capacity available|rate limit|quota' "$raw_output" "$stderr_output"; then
    echo "CAPACITY_FAILURE: Gemini reviewer failed because capacity or rate limits are unavailable. See $raw_output and $stderr_output." >&2
  elif log_matches 'not logged in|invalid credentials|credential.*invalid|login required|unauthori[sz]ed|api key|oauth' "$raw_output" "$stderr_output"; then
    echo "AUTH_FAILURE: Gemini reviewer failed because authentication is unavailable. See $raw_output and $stderr_output." >&2
  else
    echo "CLI_FAILURE: Gemini reviewer failed. See $raw_output and $stderr_output." >&2
  fi
  exit 1
fi

[[ -s "$output_file" ]] || {
  echo "MALFORMED_OUTPUT: Gemini reviewer completed without producing a non-empty output file: $output_file" >&2
  exit 1
}

echo "Wrote Gemini review to $output_file"
echo "Wrote Gemini raw response to $raw_output"
echo "Wrote Gemini stderr log to $stderr_output"
