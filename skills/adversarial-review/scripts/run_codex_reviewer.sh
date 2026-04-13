#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  run_codex_reviewer.sh --repo PATH --prompt-file PATH --output-file PATH
                        [--stdin-file PATH]
                        [--model MODEL]
                        [--sandbox read-only|workspace-write|danger-full-access]
                        [--add-dir PATH]

Runs Codex CLI in non-interactive mode for read-only adversarial review.

Defaults:
  --sandbox read-only
  --model   use the CLI's configured default model

Outputs:
  - final markdown review at --output-file
  - raw JSONL event log at --output-file.raw.jsonl
EOF
}

repo=""
prompt_file=""
output_file=""
stdin_file=""
model=""
sandbox="read-only"
declare -a add_dirs=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="${2:-}"; shift 2 ;;
    --prompt-file)
      prompt_file="${2:-}"; shift 2 ;;
    --output-file)
      output_file="${2:-}"; shift 2 ;;
    --stdin-file)
      stdin_file="${2:-}"; shift 2 ;;
    --model)
      model="${2:-}"; shift 2 ;;
    --sandbox)
      sandbox="${2:-}"; shift 2 ;;
    --add-dir)
      add_dirs+=("${2:-}"); shift 2 ;;
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

[[ -d "$repo" ]] || { echo "Repo directory does not exist: $repo" >&2; exit 2; }
[[ -f "$prompt_file" ]] || { echo "Prompt file does not exist: $prompt_file" >&2; exit 2; }
[[ -z "$stdin_file" || -f "$stdin_file" ]] || { echo "Stdin file does not exist: $stdin_file" >&2; exit 2; }

command -v codex >/dev/null 2>&1 || {
  echo "Codex CLI ('codex') is not installed or not on PATH" >&2
  exit 127
}

mkdir -p "$(dirname "$output_file")"
raw_output="${output_file}.raw.jsonl"

cleanup_files=()
cleanup() {
  if [[ ${#cleanup_files[@]} -gt 0 ]]; then
    for f in "${cleanup_files[@]}"; do
      if [[ -n "$f" && -e "$f" ]]; then
        rm -f "$f"
      fi
    done
  fi
  return 0
}
trap cleanup EXIT

input_file="$prompt_file"
if [[ -n "$stdin_file" ]]; then
  merged_input="$(mktemp)"
  cleanup_files+=("$merged_input")
  {
    cat "$prompt_file"
    printf '\n\n## Attached Review Context\n\n'
    cat "$stdin_file"
  } > "$merged_input"
  input_file="$merged_input"
fi

cmd=(
  codex
  --ask-for-approval never
  exec
  --cd "$repo"
  --sandbox "$sandbox"
  --ephemeral
  --json
  --output-last-message "$output_file"
)

if [[ -n "$model" ]]; then
  cmd+=(--model "$model")
fi

if [[ ${#add_dirs[@]} -gt 0 ]]; then
  for dir in "${add_dirs[@]}"; do
    cmd+=(--add-dir "$dir")
  done
fi

if [[ ! -d "$repo/.git" ]]; then
  cmd+=(--skip-git-repo-check)
fi

cmd+=(-)

if ! (
  cd "$repo"
  cat "$input_file" | "${cmd[@]}"
) > "$raw_output"; then
  echo "Codex reviewer failed. See $raw_output for details." >&2
  exit 1
fi

[[ -s "$output_file" ]] || {
  echo "Codex reviewer completed without producing a non-empty output file: $output_file" >&2
  exit 1
}

echo "Wrote Codex review to $output_file"
echo "Wrote Codex raw log to $raw_output"
