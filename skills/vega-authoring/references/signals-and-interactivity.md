# Vega Signals and Interactivity

Purpose: Raw Vega interaction guidance built around signals, event streams, and explicit state updates.

## Stable rules

- Use signals as the durable source of interaction state in raw Vega.
- Use event streams to decide when signals change.
- Keep signal names stable and valid JavaScript identifiers.
- Treat nested group signals as scoped unless you are explicitly pushing updates outward.
- Use signal-driven behavior for interaction; do not describe raw Vega interaction in Vega-Lite param or selection terms.

## Common failure modes

- Writing a complex event stream before the static chart structure works.
- Reusing a reserved signal name such as `datum`, `event`, `item`, or `parent`.
- Forgetting that nested signals shadow outer scope unless `push: "outer"` is used.
- Binding interaction to marks that are not actually interactive event sources.
- Encoding interaction state in ad hoc derived fields when a signal would be clearer.

## Safe defaults

- Start with one or two top-level signals only after the non-interactive chart works.
- Use simple event streams first, then add compound or filtered streams only when needed.
- Keep signal updates local to one clear responsibility: hover, selection, cursor, zoom, or filter state.
- When nested groups are involved, prefer local signals until an outer update is clearly necessary.
- If cursor state should persist through a drag, use the dedicated `cursor` signal rather than only mark properties.

## Version caveats

- Signal and event-stream behavior follows the active Vega runtime.
- Some signal conveniences have version floors; verify the active runtime before using newer behavior.

## Source URLs

- https://vega.github.io/vega/docs/signals/
- https://vega.github.io/vega/docs/event-streams/

## Verified version/date

- Vega signal and event-stream docs checked 2026-03-26.
