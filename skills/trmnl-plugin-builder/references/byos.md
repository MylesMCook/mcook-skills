# BYOS

Source pages:

- `https://docs.trmnl.com/go/diy/byos`
- `https://docs.trmnl.com/go/how-it-works`

## When to recommend

Recommend BYOS only when the user wants to run the TRMNL server/device relationship themselves.

This is not the normal "build me a plugin" path.

## Quick start

- TRMNL recommends starting with Terminus.
- Multiple self-hosted implementations exist with different feature coverage.
- Feature parity with the hosted TRMNL platform is not guaranteed.

## Minimum API expectations

At minimum, BYOS implementations should support:

- `/api/setup`
- `/api/display`
- `/api/log`

Each example request uses the device MAC address in the `ID` header.

## Important posture

- TRMNL devices poll the server; the server does not directly control devices.
- BYOS is for self-hosting and fleet control, not for basic plugin authoring.

## Agent guidance

- If the user only wants a custom screen or plugin, steer away from BYOS.
- Recommend BYOS only for self-hosting, infrastructure, or device-control requirements.
