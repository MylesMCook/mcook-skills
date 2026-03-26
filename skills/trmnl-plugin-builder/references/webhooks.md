# Webhooks

Source page:

- `https://docs.trmnl.com/go/private-plugins/webhooks`

## When to use

Choose webhook strategy when:

- data is pushed from another system
- the plugin maintains state between updates
- polling would be wasteful or awkward

## Limits

Standard limits:

- up to 12 requests per hour
- up to 2 KB payload size

TRMNL+ limits:

- up to 30 requests per hour
- up to 5 KB payload size

## Base payload shape

```json
{
  "merge_variables": {
    "text": "You can do it!",
    "author": "Rob Schneider"
  }
}
```

## Update strategies

### `deep_merge`

Use for partial updates to nested objects.

```json
{
  "merge_variables": {
    "sensor": {
      "temperature": 42
    }
  },
  "merge_strategy": "deep_merge"
}
```

### `stream`

Use for append-only top-level arrays.

```json
{
  "merge_variables": {
    "temperatures": [40, 42]
  },
  "merge_strategy": "stream",
  "stream_limit": 10
}
```

## Agent guidance

- Do not recommend webhook when polling already solves the problem cleanly.
- Mention payload and rate limits whenever the user asks for high-frequency or stateful updates.
- Keep webhook examples root-level and small.
