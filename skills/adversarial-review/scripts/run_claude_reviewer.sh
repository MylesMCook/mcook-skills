#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  run_claude_reviewer.sh \
    --repo /path/to/repo \
    --prompt-file /tmp/task.txt \
    --output-file /tmp/review.md \
    [--system-prompt-file /tmp/system.txt] \
    [--name skeptic] \
    [--model claude-sonnet-4-6] \
    [--tools "Read,Grep,Glob"] \
    [--max-turns 8] \
    [--effort medium]

Runs Claude Code in native repo-tool mode and writes the parsed markdown review
to --output-file. A raw JSON response is also written beside the output file
with a .raw.json suffix.
EOF
}

repo=""
prompt_file=""
system_prompt_file=""
output_file=""
name=""
model=""
tools="Read,Grep,Glob"
max_turns="8"
effort="medium"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="${2:?missing value for --repo}"
      shift 2
      ;;
    --prompt-file)
      prompt_file="${2:?missing value for --prompt-file}"
      shift 2
      ;;
    --system-prompt-file)
      system_prompt_file="${2:?missing value for --system-prompt-file}"
      shift 2
      ;;
    --output-file)
      output_file="${2:?missing value for --output-file}"
      shift 2
      ;;
    --name)
      name="${2:?missing value for --name}"
      shift 2
      ;;
    --model)
      model="${2:?missing value for --model}"
      shift 2
      ;;
    --tools)
      tools="${2:?missing value for --tools}"
      shift 2
      ;;
    --max-turns)
      max_turns="${2:?missing value for --max-turns}"
      shift 2
      ;;
    --effort)
      effort="${2:?missing value for --effort}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$repo" || -z "$prompt_file" || -z "$output_file" ]]; then
  usage >&2
  exit 2
fi

if [[ ! -d "$repo" ]]; then
  echo "Repo directory not found: $repo" >&2
  exit 2
fi

if [[ ! -f "$prompt_file" ]]; then
  echo "Prompt file not found: $prompt_file" >&2
  exit 2
fi

if [[ -n "$system_prompt_file" && ! -f "$system_prompt_file" ]]; then
  echo "System prompt file not found: $system_prompt_file" >&2
  exit 2
fi

mkdir -p "$(dirname "$output_file")"
raw_output="${output_file}.raw.json"

cmd=(
  claude
  -p
  --output-format json
  --no-session-persistence
  --permission-mode bypassPermissions
  --tools "$tools"
  --add-dir "$repo"
  --max-turns "$max_turns"
  --effort "$effort"
)

if [[ -n "$name" ]]; then
  cmd+=(--name "$name")
fi

if [[ -n "$model" ]]; then
  cmd+=(--model "$model")
fi

if [[ -n "$system_prompt_file" ]]; then
  cmd+=(--append-system-prompt "$(cat "$system_prompt_file")")
fi

# Important: pass the prompt after `--` so Claude's variadic flags do not
# consume it as another tool name or option payload.
cmd+=(-- "$(cat "$prompt_file")")

json_output="$(
  cd "$repo"
  "${cmd[@]}"
)"

printf '%s\n' "$json_output" > "$raw_output"

python3 - "$raw_output" "$output_file" <<'PY'
import json
import pathlib
import sys

raw_path = pathlib.Path(sys.argv[1])
out_path = pathlib.Path(sys.argv[2])
data = json.loads(raw_path.read_text())

if data.get("is_error"):
    message = data.get("result") or "Claude reviewer failed"
    print(message, file=sys.stderr)
    sys.exit(1)

result = (data.get("result") or "").rstrip()
if not result:
    print("Claude reviewer returned an empty result", file=sys.stderr)
    sys.exit(1)

out_path.write_text(result + "\n")
PY
