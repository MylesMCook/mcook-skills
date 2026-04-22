# {{PROJECT_NAME}} MCPeas spec

Date: {{DATE}}

## Architecture decision

Use the MCPeas default: a hosted TypeScript `mcp-use` MCP Apps project with Streamable HTTP at `/mcp`, widget capability from day one, and Codex harness files checked into the repo.

Hard-stop deviation: none.

## User job

Describe the primary job this MCP app performs.

## Non-goals

List what this app intentionally will not do.

## Tool inventory

| Tool | User job | Read/write | Input schema highlights | Output schema | Annotations | Auth | Errors |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `example-tool` | Use this when... | read | required fields, enums, bounds | structured output keys | `readOnlyHint: true`, `openWorldHint: false` | none/user OAuth/API key | expected error cases |

## Widget plan

Widget needed now: yes/no.

Use a widget when the user needs to browse, compare, select, visualize, edit, or interact repeatedly.

Resource URI:
MIME type: `text/html;profile=mcp-app`
CSP:
Widget domain:
Bridge behavior:
ChatGPT-only enhancements:

## Payload boundary

`structuredContent`:

`content`:

`_meta`:

Data that must never be returned:

## Auth and security

Secrets:
Env vars:
Rate limits:
Caching:
User data:
Write confirmation:

## Golden prompts

Maintain the canonical list in `evals/golden-prompts.json`.

Direct:
1.
2.
3.
4.
5.

Indirect:
1.
2.
3.
4.
5.

Negative:
1.
2.
3.
4.
5.

## Validation gates

- [ ] Source freshness checked.
- [ ] Tool schemas validated.
- [ ] Widget contract checked.
- [ ] `npm run build`
- [ ] tests
- [ ] MCP Inspector
- [ ] ChatGPT developer mode or API Playground, if applicable
- [ ] `python scripts/mcpeas_check.py .`

## Handoff notes

Files changed:
Commands run:
Known risks:
