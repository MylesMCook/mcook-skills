# Validation

Use this file to validate a Pi package through the real install path.

Start with concrete paths and keep these variables in the same shell session for
the rest of the flow:

```bash
PACKAGE_PATH=./relative/path/to/package
ARTIFACT_DIR=$(mktemp -d)
TMP_PI_DIR=$(mktemp -d)
```

## Local checks first

Run the package's own checks first, if present:

```bash
npm test
npm run build
```

Or the equivalent for the package's stack.

## Structural preflight before install

Before calling `pi install`, run a deterministic manifest preflight:

```bash
python3 - "$PACKAGE_PATH/package.json" <<'PY'
import json
import pathlib
import sys

manifest_path = pathlib.Path(sys.argv[1]).resolve()
root = manifest_path.parent
data = json.loads(manifest_path.read_text())
name = data.get("name")
if not isinstance(name, str) or not name.strip():
    raise SystemExit("package.json is missing a valid name")
pi_manifest = data.get("pi", {})
allowed = {"extensions", "skills", "prompts", "themes"}
unknown = sorted(set(pi_manifest) - allowed)
if unknown:
    raise SystemExit(f"unknown pi manifest keys: {unknown}")
for key, paths in pi_manifest.items():
    values = paths if isinstance(paths, list) else [paths]
    for value in values:
        if not isinstance(value, str):
            raise SystemExit(f"{key} entries must be strings: {value!r}")
        if not value.startswith("!"):
            candidate = root / value
            if "*" not in value and not candidate.exists():
                raise SystemExit(f"missing {key} path: {value}")
print("pi manifest preflight passed")
PY
```

## Install into a temporary Pi agent dir

Avoid polluting real agent state while validating:

```bash
set -euo pipefail
PACKAGE_NAME=$(python3 - "$PACKAGE_PATH/package.json" <<'PY'
import json
import sys
print(json.load(open(sys.argv[1]))["name"])
PY
)
PI_CODING_AGENT_DIR="$TMP_PI_DIR" pi install "$PACKAGE_PATH" >"$ARTIFACT_DIR/pi-install.log" 2>&1
PI_CODING_AGENT_DIR="$TMP_PI_DIR" pi list >"$ARTIFACT_DIR/pi-list.log" 2>&1
grep -F "$PACKAGE_NAME" "$ARTIFACT_DIR/pi-list.log"
```

During package creation, the default validation source is a local path. Use
`PI_CODING_AGENT_DIR="$TMP_PI_DIR"` on every validation command so the package
is exercised against an isolated Pi agent dir instead of real agent state.
If you are unsure about the env var on the installed Pi version, confirm it
with the same `pi` binary you will validate with:

```bash
pi --help | grep PI_CODING_AGENT_DIR
```

Keep the validation environment isolated until the package has already passed:
- confirm `pi list` in `$TMP_PI_DIR` shows the test package
- confirm it does not show packages from real agent state

Other install sources exist, but they are secondary to local-path validation
while the package is still being built.

## Smoke the public surface

Validate the thing the user will actually use, and capture one concrete success
artifact for it. A smoke step only counts if it exits `0` and leaves a log in
`$ARTIFACT_DIR`.

### Extension package

- run the command it registers through Pi's non-interactive `--print, -p`
  mode when possible, for example:

  ```bash
  PI_CODING_AGENT_DIR="$TMP_PI_DIR" pi -p "/your-command" >"$ARTIFACT_DIR/extension-smoke.log" 2>&1
  ```

- or exercise the hook/tool behavior it claims to add and capture visible
  output with the smallest command path the package actually exposes

### Skill package

- invoke the skill explicitly via `/skill:name` and capture one realistic run:

  ```bash
  PI_CODING_AGENT_DIR="$TMP_PI_DIR" pi -p "/skill:your-skill smallest realistic task" >"$ARTIFACT_DIR/skill-smoke.log" 2>&1
  ```

### Prompt package

- expand the prompt template through its slash command and capture one run:

  ```bash
  PI_CODING_AGENT_DIR="$TMP_PI_DIR" pi -p "/your-template args" >"$ARTIFACT_DIR/prompt-smoke.log" 2>&1
  ```

### Theme package

- enable the theme through `pi config` in the temp agent dir and capture the
  visible change in a named screenshot or terminal recording under
  `$ARTIFACT_DIR`

## Dogfood after temp install

If the package mutates repos or real agent state:
- prove it in a scratch repo first
- then dogfood it in a real repo

Treat a package as mutating if it creates, edits, or deletes files under the
working repo, `.pi/`, or `.agents/`.

For a scratch repo, use a temporary git repo with the smallest fixture that
matches the package's mutation surface.

```bash
SCRATCH_REPO=$(mktemp -d)
git init "$SCRATCH_REPO"
```

If the package has a meaningful public UX:
- verify README/package metadata match the actual install and smoke flow

## Teardown

After you have reviewed and saved the artifacts you need:

```bash
rm -rf "$TMP_PI_DIR"
# remove ARTIFACT_DIR too if you do not need to keep the logs
rm -rf "$ARTIFACT_DIR"
```

## Typical validation artifacts

Treat these as required evidence for calling the package done:
- test/build output
- `pi install` output in `$ARTIFACT_DIR/pi-install.log`
- `pi list` output in `$ARTIFACT_DIR/pi-list.log`
- one successful smoke command or prompt log in `$ARTIFACT_DIR`
- for mutating packages, a focused diff that shows only the expected changes

## Common failures

- package works with direct `--extension` or `--skill` loading but fails through
  `pi install`
- README implies a registry install when only local-path install works
- package metadata widens scope beyond the actual package behavior
- temp install succeeds, but no one verified the user-facing command or skill
