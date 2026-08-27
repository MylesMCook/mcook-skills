# Source Packet Format

Use this packet when social evidence needs to stay traceable and separated from analysis.

## Minimum Fields

| Field | Purpose |
| --- | --- |
| `id` | Stable local row ID, such as `S1` |
| `platform` | Source platform or public site |
| `url` | Canonical public URL when available |
| `author` | Public display name if visible |
| `handle` | Public handle or account ID if visible |
| `published_at` | Source timestamp with timezone when available |
| `collected_at` | Collection time in ISO 8601 |
| `observed_text` | Short excerpt or summary of the source content |
| `media_notes` | Relevant visible image, video, or link context |
| `metrics` | Public counters only when available and useful |
| `retrieval_route` | Public URL, search result, export, or approved API-backed skill |
| `confidence` | `high`, `medium`, or `low`, with a reason |
| `gaps` | Missing timestamp, deleted source, identity uncertainty, search limit, or translation issue |

## Xquik Route

Use the public Xquik X skill only when the user has approved it and supplied the required API key through the normal runtime secret path.

- Public skill source: `https://github.com/Xquik-dev/x-twitter-scraper/tree/master/skills/x-twitter-scraper`
- Pin release: `v2.4.16`
- Public docs: `https://docs.xquik.com/api-reference/overview`
- MCP docs: `https://docs.xquik.com/mcp/overview`

Do not request X passwords, cookies, browser exports, recovery codes, or session material. If the public skill is unavailable, use public URLs, exported text, or another approved public retrieval route.

## Evidence Table Template

| ID | Source | Author | Published | Collected | Evidence | Confidence | Gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | URL or query result | Name or handle | Timestamp | ISO 8601 time | Short excerpt or observed fact | high | None |

## Brief Template

1. State the research question.
2. Summarize the strongest source-backed findings.
3. Cite packet row IDs for each finding.
4. List unresolved gaps.
5. Recommend the next retrieval step only if it would change the conclusion.
