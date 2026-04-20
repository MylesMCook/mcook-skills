#!/usr/bin/env bash
set -euo pipefail

state_dir="${FIXTURE_STATE_DIR:?}"
main_args_file="$state_dir/gemini.main.args"
main_stdin_file="$state_dir/gemini.main.stdin"
main_cwd_file="$state_dir/gemini.main.cwd"
list_args_file="$state_dir/gemini.list.args"
delete_args_file="$state_dir/gemini.delete.args"
session_file="$state_dir/gemini.session_id"
active_file="$state_dir/gemini.active"
delete_file="$state_dir/gemini.delete"

mkdir -p "$state_dir"

record_args() {
  local file="$1"
  shift
  {
    for arg in "$@"; do
      printf '%q\n' "$arg"
    done
  } > "$file"
}

mode="${FIXTURE_GEMINI_MODE:-success}"
session_id="${FIXTURE_GEMINI_SESSION_ID:-11111111-1111-1111-1111-111111111111}"
args=("$@")
is_list=0
is_delete=0
delete_index=""

for ((i = 0; i < ${#args[@]}; i++)); do
  case "${args[$i]}" in
    --list-sessions)
      is_list=1
      ;;
    --delete-session)
      is_delete=1
      if (( i + 1 < ${#args[@]} )); then
        delete_index="${args[$((i + 1))]}"
      fi
      ;;
  esac
done

if (( is_list )); then
  record_args "$list_args_file" "${args[@]}"
  printf '%s\n' "$session_id" > "$session_file"
  printf 'Available sessions for this project (1):\n'
  printf '  1. Fixture session [%s]\n' "$session_id"
  exit 0
fi

if (( is_delete )); then
  record_args "$delete_args_file" "${args[@]}"
  if [[ "${FIXTURE_GEMINI_DELETE_FAIL:-0}" == "1" ]]; then
    echo "delete failed" >&2
    exit 1
  fi

  printf '%s\n' "$delete_index" > "$delete_file"
  rm -f "$active_file"
  printf 'Deleted session %s\n' "$delete_index"
  exit 0
fi

record_args "$main_args_file" "${args[@]}"
pwd > "$main_cwd_file"
cat > "$main_stdin_file"
printf '%s\n' "$session_id" > "$session_file"
printf '%s\n' "active" > "$active_file"

case "$mode" in
  success)
    printf '{"type":"init","session_id":"%s","model":"fixture-model"}\n' "$session_id"
    printf '{"type":"message","role":"assistant","content":[{"type":"text","text":"Gemini OK"}]}\n'
    printf '{"type":"result","response":"Gemini OK","stats":{"session":{"duration":1},"model":{"turns":1},"tools":{"calls":0}}}\n'
    ;;
  missing_session_id)
    printf '{"type":"init","model":"fixture-model"}\n'
    printf '{"type":"message","role":"assistant","content":[{"type":"text","text":"Gemini OK"}]}\n'
    printf '{"type":"result","response":"Gemini OK","stats":{"session":{"duration":1},"model":{"turns":1},"tools":{"calls":0}}}\n'
    ;;
  input_error)
    printf '{"type":"init","session_id":"%s","model":"fixture-model"}\n' "$session_id"
    printf '{"type":"error","error":{"message":"input error"}}\n'
    exit 42
    ;;
  turn_limit)
    printf '{"type":"init","session_id":"%s","model":"fixture-model"}\n' "$session_id"
    printf '{"type":"error","error":{"message":"turn limit exceeded"}}\n'
    exit 53
    ;;
  auth_failure)
    printf '{"type":"init","session_id":"%s","model":"fixture-model"}\n' "$session_id"
    printf '{"type":"error","error":{"message":"not logged in"}}\n'
    exit 1
    ;;
  *)
    echo "unknown fixture mode: $mode" >&2
    exit 1
    ;;
esac
