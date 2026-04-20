#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

scratch_root="$(mktemp -d "${PWD}/.adversarial-review-doctor.XXXXXX")"
cleanup() {
  rm -rf "$scratch_root"
}
trap cleanup EXIT

repo_dir="$scratch_root/repo"
mkdir -p "$repo_dir"
printf '# adversarial-review doctor scratch repo\n' > "$repo_dir/README.md"

run_check() {
  local name="$1"
  local wrapper="$2"
  local expected="$3"

  local prompt_file="$scratch_root/${name}.prompt.md"
  local out_file="$scratch_root/${name}.out.md"
  local stdout_file="$scratch_root/${name}.stdout"
  local stderr_file="$scratch_root/${name}.stderr"

  printf 'Reply with exactly %s.\n' "$expected" > "$prompt_file"

  local rc=0
  set +e
  bash "$wrapper" \
    --repo "$repo_dir" \
    --prompt-file "$prompt_file" \
    --output-file "$out_file" \
    --timeout-seconds 180 \
    >"$stdout_file" 2>"$stderr_file"
  rc=$?
  set -e

  if (( rc == 0 )) && [[ -s "$out_file" ]] && grep -Fq "$expected" "$out_file"; then
    printf '%s: PASS\n' "$name"
    return 0
  fi

  local reason="FAILED"
  if [[ -s "$stderr_file" ]]; then
    reason="$(grep -Eo '^[A-Z_]+:' "$stderr_file" | head -n 1 | tr -d ':' || true)"
    if [[ -z "$reason" ]]; then
      reason="$(head -n 1 "$stderr_file")"
    fi
  fi

  printf '%s: FAIL - %s\n' "$name" "$reason"
  return 1
}

printf 'adversarial-review doctor\n\n'

ready=0
run_check "Codex" "$SCRIPT_DIR/run_codex_reviewer.sh" "codex-doctor-ok" || ready=1
run_check "Claude" "$SCRIPT_DIR/run_claude_reviewer.sh" "claude-doctor-ok" || ready=1
run_check "Gemini" "$SCRIPT_DIR/run_gemini_reviewer.sh" "gemini-doctor-ok" || ready=1

if (( ready == 0 )); then
  printf '\nReady: YES\n'
else
  printf '\nReady: NO\n'
fi

exit "$ready"
