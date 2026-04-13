#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
DIST_CLI="${ROOT_DIR}/dist/src/codex-cli.js"
SOURCE_CLI="${ROOT_DIR}/src/codex-cli.ts"

show_help=false
if [[ "${1:-}" == "help" ]]; then
  show_help=true
else
  for arg in "$@"; do
    if [[ "${arg}" == "--help" || "${arg}" == "-h" ]]; then
      show_help=true
      break
    fi
  done
fi

if [[ "${show_help}" == "true" ]]; then
  if [[ -f "${DIST_CLI}" ]]; then
    node "${DIST_CLI}" __brainerd_help__ 2>&1 || true
    exit 0
  fi

  if command -v npx >/dev/null 2>&1 && [[ -f "${SOURCE_CLI}" ]]; then
    npx --yes tsx "${SOURCE_CLI}" __brainerd_help__ 2>&1 || true
    exit 0
  fi
fi

if [[ -f "${DIST_CLI}" ]]; then
  exec node "${DIST_CLI}" "$@"
fi

if command -v npx >/dev/null 2>&1 && [[ -f "${SOURCE_CLI}" ]]; then
  exec npx --yes tsx "${SOURCE_CLI}" "$@"
fi

echo "Brainerd runtime is missing. Rebuild the skill or reinstall the packaged copy." >&2
exit 1
