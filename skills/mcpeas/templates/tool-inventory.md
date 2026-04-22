# Tool inventory

| Tool | Use this when... | Do not use when... | Read/write | Input schema | Output schema | Annotations | Auth | Widget |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

## Design checks

- [ ] One job per tool.
- [ ] Description starts with "Use this when..."
- [ ] Inputs use enums, bounds, and descriptions.
- [ ] Expected failures return graceful errors.
- [ ] Writes are separated from reads.
- [ ] Payload split is documented.
- [ ] Widget-only data stays in `_meta`.
