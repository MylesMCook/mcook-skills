#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURE_DIR="$SCRIPT_DIR/fixtures"

real_codex="$(command -v codex || true)"
real_claude="$(command -v claude || true)"
real_gemini="$(command -v gemini || true)"

scratch_root="$(mktemp -d "${TMPDIR:-/tmp}/adversarial-review-matrix.XXXXXX")"
cleanup() {
  rm -rf "$scratch_root"
}
trap cleanup EXIT

repo_dir="$scratch_root/repo"
prompt_file="$scratch_root/prompt.md"
stdin_file="$scratch_root/stdin.md"
output_dir="$scratch_root/out"
state_dir="$scratch_root/state"
shim_dir="$scratch_root/bin"

mkdir -p "$repo_dir" "$output_dir" "$state_dir" "$shim_dir"

printf '# scratch repo\n' > "$repo_dir/README.md"
printf 'review prompt line 1\nreview prompt line 2\n' > "$prompt_file"
printf 'attached context line 1\nattached context line 2\n' > "$stdin_file"

for name in codex claude gemini; do
  cp "$FIXTURE_DIR/$name.sh" "$shim_dir/$name"
  chmod +x "$shim_dir/$name"
done

assert_file_equals() {
  local path="$1"
  local expected="$2"

  python3 - "$path" "$expected" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
expected = sys.argv[2]
actual = path.read_text(encoding="utf-8")
if actual != expected:
    raise SystemExit(f"file mismatch: {path}\nEXPECTED:\n{expected!r}\nACTUAL:\n{actual!r}")
PY
}

assert_file_contains() {
  local path="$1"
  local needle="$2"

  python3 - "$path" "$needle" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
needle = sys.argv[2]
text = path.read_text(encoding="utf-8")
if needle not in text:
    raise SystemExit(f"missing substring {needle!r} in {path}")
PY
}

arg_index() {
  local path="$1"
  local needle="$2"

  python3 - "$path" "$needle" <<'PY'
import pathlib
import shlex
import sys

path = pathlib.Path(sys.argv[1])
needle = sys.argv[2]
for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
    if not line:
        continue
    value = shlex.split(line)[0]
    if value == needle:
        print(idx)
        raise SystemExit(0)
raise SystemExit(1)
PY
}

assert_arg_present() {
  local path="$1"
  local needle="$2"

  arg_index "$path" "$needle" >/dev/null
}

assert_arg_order() {
  local path="$1"
  local first="$2"
  local second="$3"

  local first_index second_index
  first_index="$(arg_index "$path" "$first")"
  second_index="$(arg_index "$path" "$second")"
  if (( first_index >= second_index )); then
    echo "argument order mismatch in $path: $first_index !< $second_index" >&2
    exit 1
  fi
}

run_wrapper() {
  local wrapper="$1"
  local mode="$2"
  local out_file="$3"
  local expected_rc="$4"
  shift 4

  local stdout_file="$scratch_root/${wrapper##*/}.stdout"
  local stderr_file="$scratch_root/${wrapper##*/}.stderr"

  rm -f "$stdout_file" "$stderr_file" "$out_file" "${out_file}.raw.json" "${out_file}.raw.jsonl" "${out_file}.stderr.log"

  local rc=0
  set +e
  env \
    ADVERSARIAL_REVIEW_USE_PATH_ONLY=1 \
    FIXTURE_STATE_DIR="$state_dir" \
    FIXTURE_MODE="$mode" \
    PATH="$shim_dir:$PATH" \
    bash "$wrapper" \
    --repo "$repo_dir" \
    --prompt-file "$prompt_file" \
    --stdin-file "$stdin_file" \
    --output-file "$out_file" \
    "$@" \
    >"$stdout_file" 2>"$stderr_file"
  rc=$?
  set -e

  if [[ "$expected_rc" != "*" ]] && (( rc != expected_rc )); then
    echo "unexpected rc for $wrapper: got $rc expected $expected_rc" >&2
    echo "--- stdout ---" >&2
    cat "$stdout_file" >&2 || true
    echo "--- stderr ---" >&2
    cat "$stderr_file" >&2 || true
    exit 1
  fi

  printf '%s\n' "$stdout_file" "$stderr_file" "$rc"
}

live_smoke() {
  command -v node >/dev/null 2>&1 || return 0

  if [[ -n "$real_codex" ]] && "$real_codex" --help >/dev/null 2>&1; then
    "$real_codex" --help | grep -Fq -- "--ask-for-approval"
  fi

  if [[ -n "$real_claude" ]] && "$real_claude" --help >/dev/null 2>&1; then
    "$real_claude" --help | grep -Fq -- "--bare"
    "$real_claude" --help | grep -Fq -- "--allowedTools"
  fi

  if [[ -n "$real_gemini" ]] && "$real_gemini" --help >/dev/null 2>&1; then
    "$real_gemini" --help | grep -Fq -- "--output-format"
    "$real_gemini" --help | grep -Fq -- "--delete-session"
    "$real_gemini" --help | grep -Fq -- "--list-sessions"
  fi
}

live_smoke

codex_out="$output_dir/codex.md"
codex_meta="$(run_wrapper "$SCRIPT_DIR/run_codex_reviewer.sh" success "$codex_out" 0 --model "codex-test-model")"
codex_stdout="$(sed -n '1p' <<<"$codex_meta")"
codex_stderr="$(sed -n '2p' <<<"$codex_meta")"
codex_rc="$(sed -n '3p' <<<"$codex_meta")"

assert_file_equals "$codex_out" "Codex OK"$'\n'
assert_file_contains "${codex_out}.raw.jsonl" '"type":"thread.started"'
assert_arg_present "$state_dir/codex.args" "--ask-for-approval"
assert_arg_present "$state_dir/codex.args" "never"
assert_arg_present "$state_dir/codex.args" "exec"
assert_arg_order "$state_dir/codex.args" "--ask-for-approval" "exec"
assert_arg_present "$state_dir/codex.args" "--json"
assert_arg_present "$state_dir/codex.args" "--ephemeral"
assert_arg_present "$state_dir/codex.args" "--sandbox"
assert_arg_present "$state_dir/codex.args" "read-only"
assert_arg_present "$state_dir/codex.args" "--skip-git-repo-check"
assert_file_equals "$state_dir/codex.stdin" "attached context line 1"$'\n'"attached context line 2"$'\n'

claude_out="$output_dir/claude.md"
claude_meta="$(run_wrapper "$SCRIPT_DIR/run_claude_reviewer.sh" success "$claude_out" 0 --model "claude-test-model")"
claude_stdout="$(sed -n '1p' <<<"$claude_meta")"
claude_stderr="$(sed -n '2p' <<<"$claude_meta")"
claude_rc="$(sed -n '3p' <<<"$claude_meta")"

assert_file_equals "$claude_out" "Claude OK"$'\n'
assert_file_contains "${claude_out}.raw.json" '"result":"Claude OK"'
assert_arg_present "$state_dir/claude.args" "--output-format"
assert_arg_present "$state_dir/claude.args" "json"
assert_arg_present "$state_dir/claude.args" "--no-session-persistence"
assert_arg_present "$state_dir/claude.args" "--permission-mode"
assert_arg_present "$state_dir/claude.args" "plan"
assert_arg_present "$state_dir/claude.args" "--strict-mcp-config"
assert_arg_present "$state_dir/claude.args" "--disable-slash-commands"
assert_arg_present "$state_dir/claude.args" "--tools"
assert_arg_present "$state_dir/claude.args" "Read,Grep,Glob"
assert_arg_present "$state_dir/claude.args" "--allowedTools"
assert_arg_present "$state_dir/claude.args" "Read,Grep,Glob"
assert_arg_present "$state_dir/claude.args" "--max-turns"
assert_arg_present "$state_dir/claude.args" "10"
assert_file_equals "$state_dir/claude.stdin" "attached context line 1"$'\n'"attached context line 2"$'\n'

gemini_out="$output_dir/gemini.md"
gemini_meta="$(run_wrapper "$SCRIPT_DIR/run_gemini_reviewer.sh" success "$gemini_out" 0 --model "gemini-test-model")"
gemini_stdout="$(sed -n '1p' <<<"$gemini_meta")"
gemini_stderr="$(sed -n '2p' <<<"$gemini_meta")"
gemini_rc="$(sed -n '3p' <<<"$gemini_meta")"

assert_file_equals "$gemini_out" "Gemini OK"$'\n'
assert_file_contains "${gemini_out}.raw.jsonl" '"type":"result"'
assert_arg_present "$state_dir/gemini.main.args" "--approval-mode"
assert_arg_present "$state_dir/gemini.main.args" "plan"
if arg_index "$state_dir/gemini.main.args" "--sandbox" >/dev/null 2>&1; then
  echo "gemini copy sandbox mode should not pass --sandbox" >&2
  exit 1
fi
assert_arg_present "$state_dir/gemini.main.args" "--output-format"
assert_arg_present "$state_dir/gemini.main.args" "stream-json"
assert_arg_present "$state_dir/gemini.main.args" "--model"
assert_arg_present "$state_dir/gemini.main.args" "gemini-test-model"
expected_gemini_stdin=$'review prompt line 1\nreview prompt line 2\n\n## Attached Review Context\n\nattached context line 1\nattached context line 2\n'
assert_file_equals "$state_dir/gemini.main.stdin" "$expected_gemini_stdin"
assert_file_equals "$state_dir/gemini.delete" "1"$'\n'
[[ ! -e "$state_dir/gemini.active" ]]
if [[ "$(cat "$state_dir/gemini.main.cwd")" == "$repo_dir" ]]; then
  echo "gemini copy sandbox mode ran in the original repo" >&2
  exit 1
fi

set +e
env \
  ADVERSARIAL_REVIEW_USE_PATH_ONLY=1 \
  FIXTURE_STATE_DIR="$state_dir" \
  FIXTURE_CODEX_MODE=input_error \
  PATH="$shim_dir:$PATH" \
  bash "$SCRIPT_DIR/run_codex_reviewer.sh" \
  --repo "$repo_dir" \
  --prompt-file "$prompt_file" \
  --stdin-file "$stdin_file" \
  --output-file "$output_dir/codex-input-error.md" \
  >/dev/null 2>"$scratch_root/codex-input-error.stderr"
rc=$?
set -e
if (( rc == 0 )); then
  echo "codex input-error case unexpectedly succeeded" >&2
  exit 1
fi
assert_file_contains "$scratch_root/codex-input-error.stderr" 'INPUT_ERROR'

set +e
env \
  ADVERSARIAL_REVIEW_USE_PATH_ONLY=1 \
  FIXTURE_STATE_DIR="$state_dir" \
  FIXTURE_GEMINI_MODE=input_error \
  PATH="$shim_dir:$PATH" \
  bash "$SCRIPT_DIR/run_gemini_reviewer.sh" \
  --repo "$repo_dir" \
  --prompt-file "$prompt_file" \
  --stdin-file "$stdin_file" \
  --output-file "$output_dir/gemini-input-error.md" \
  >/dev/null 2>"$scratch_root/gemini-input-error.stderr"
rc=$?
set -e
if (( rc == 0 )); then
  echo "gemini input-error case unexpectedly succeeded" >&2
  exit 1
fi
assert_file_contains "$scratch_root/gemini-input-error.stderr" 'INPUT_ERROR'

set +e
env \
  ADVERSARIAL_REVIEW_USE_PATH_ONLY=1 \
  FIXTURE_STATE_DIR="$state_dir" \
  FIXTURE_GEMINI_MODE=turn_limit \
  PATH="$shim_dir:$PATH" \
  bash "$SCRIPT_DIR/run_gemini_reviewer.sh" \
  --repo "$repo_dir" \
  --prompt-file "$prompt_file" \
  --stdin-file "$stdin_file" \
  --output-file "$output_dir/gemini-turn-limit.md" \
  >/dev/null 2>"$scratch_root/gemini-turn-limit.stderr"
rc=$?
set -e
if (( rc == 0 )); then
  echo "gemini turn-limit case unexpectedly succeeded" >&2
  exit 1
fi
assert_file_contains "$scratch_root/gemini-turn-limit.stderr" 'TURN_LIMIT'

set +e
env \
  ADVERSARIAL_REVIEW_USE_PATH_ONLY=1 \
  FIXTURE_STATE_DIR="$state_dir" \
  FIXTURE_GEMINI_MODE=success \
  FIXTURE_GEMINI_DELETE_FAIL=1 \
  PATH="$shim_dir:$PATH" \
  bash "$SCRIPT_DIR/run_gemini_reviewer.sh" \
  --repo "$repo_dir" \
  --prompt-file "$prompt_file" \
  --stdin-file "$stdin_file" \
  --output-file "$output_dir/gemini-cleanup-fail.md" \
  >/dev/null 2>"$scratch_root/gemini-cleanup-fail.stderr"
rc=$?
set -e
if (( rc == 0 )); then
  echo "gemini cleanup-failure case unexpectedly succeeded" >&2
  exit 1
fi
assert_file_contains "$scratch_root/gemini-cleanup-fail.stderr" 'CLEANUP_FAILURE'

set +e
env \
  ADVERSARIAL_REVIEW_USE_PATH_ONLY=1 \
  FIXTURE_STATE_DIR="$state_dir" \
  FIXTURE_GEMINI_MODE=missing_session_id \
  PATH="$shim_dir:$PATH" \
  bash "$SCRIPT_DIR/run_gemini_reviewer.sh" \
  --repo "$repo_dir" \
  --prompt-file "$prompt_file" \
  --stdin-file "$stdin_file" \
  --output-file "$output_dir/gemini-missing-session-id.md" \
  >/dev/null 2>"$scratch_root/gemini-missing-session-id.stderr"
rc=$?
set -e
if (( rc == 0 )); then
  echo "gemini missing-session-id case unexpectedly succeeded" >&2
  exit 1
fi
assert_file_contains "$scratch_root/gemini-missing-session-id.stderr" 'MALFORMED_OUTPUT'
assert_file_equals "$state_dir/gemini.delete" "1"$'\n'

set +e
env \
  ADVERSARIAL_REVIEW_USE_PATH_ONLY=1 \
  FIXTURE_STATE_DIR="$state_dir" \
  FIXTURE_CLAUDE_MODE=auth_failure \
  PATH="$shim_dir:$PATH" \
  bash "$SCRIPT_DIR/run_claude_reviewer.sh" \
  --repo "$repo_dir" \
  --prompt-file "$prompt_file" \
  --stdin-file "$stdin_file" \
  --output-file "$output_dir/claude-auth-failure.md" \
  >/dev/null 2>"$scratch_root/claude-auth-failure.stderr"
rc=$?
set -e
if (( rc == 0 )); then
  echo "claude auth-failure case unexpectedly succeeded" >&2
  exit 1
fi
assert_file_contains "$scratch_root/claude-auth-failure.stderr" 'AUTH_FAILURE'

set +e
env \
  ADVERSARIAL_REVIEW_USE_PATH_ONLY=1 \
  FIXTURE_STATE_DIR="$state_dir" \
  FIXTURE_CLAUDE_MODE=turn_limit \
  PATH="$shim_dir:$PATH" \
  bash "$SCRIPT_DIR/run_claude_reviewer.sh" \
  --repo "$repo_dir" \
  --prompt-file "$prompt_file" \
  --stdin-file "$stdin_file" \
  --output-file "$output_dir/claude-turn-limit.md" \
  >/dev/null 2>"$scratch_root/claude-turn-limit.stderr"
rc=$?
set -e
if (( rc == 0 )); then
  echo "claude turn-limit case unexpectedly succeeded" >&2
  exit 1
fi
assert_file_contains "$scratch_root/claude-turn-limit.stderr" 'TURN_LIMIT'

printf 'Harness matrix passed.\n'
