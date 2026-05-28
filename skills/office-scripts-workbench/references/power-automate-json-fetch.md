# Power Automate, JSON, and external calls

## Contents

- Run mode matters
- Main signatures for Power Automate
- JSON boundary pattern
- External calls from Excel
- External data in Power Automate
- Flow-safe error handling
- Security posture
- Cloud-hosted workbook posture

Load this for Power Automate integration, `Run script`, script parameters, returns, JSON conversion, `fetch`, CORS, external APIs, credentials, or connector issues.

## Run mode matters

There are two major run modes:

| Run mode | Good for | Important limitation |
|---|---|---|
| Excel Code Editor / Automate tab | Interactive workbook automation, buttons, direct debugging, `fetch` from Excel | User/workbook context matters |
| Power Automate `Run script` | Scheduled/event-driven flows, cross-app automation, passing parameters/return values | `fetch` is not available inside the Office Script action |

Do not debug a Power Automate issue as if it were only the Excel Code Editor runtime.

## Main signatures for Power Automate

Use typed parameters and typed return values. Keep inputs/outputs JSON-serializable.

```ts
interface ImportRow {
  id: string;
  status: string;
  amount: number;
}

interface ScriptResult {
  rowsAdded: number;
  skipped: number;
  message: string;
}

function main(workbook: ExcelScript.Workbook, rows: ImportRow[]): ScriptResult {
  return {
    rowsAdded: rows.length,
    skipped: 0,
    message: "Import complete"
  };
}
```

Power Automate can supply static values, expressions, and dynamic content as script parameters.

## JSON boundary pattern

For simple data from Power Automate, accept `object[]` at the boundary only if the shape is truly variable, then normalize it.

```ts
interface NormalizedRow {
  id: string;
  amount: number;
}

function normalizeRows(rows: object[]): NormalizedRow[] {
  return rows.map((row) => {
    const item = row as { id?: string; amount?: number };
    if (!item.id || typeof item.amount !== "number") {
      throw new Error("Invalid row payload: expected id and numeric amount.");
    }
    return { id: item.id, amount: item.amount };
  });
}
```

Prefer a strongly typed interface when the flow payload is known.

## External calls from Excel

External calls require `async main` and `await`.

```ts
interface ApiRow {
  id: string;
  amount: number;
}

async function main(workbook: ExcelScript.Workbook): Promise<number> {
  const response = await fetch("https://example.com/api/rows");
  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}.`);
  }
  const rows = await response.json() as ApiRow[];
  return rows.length;
}
```

Constraints:
- No OAuth sign-in flow inside the script.
- No built-in secure secret store for API keys.
- Document cookies, `localStorage`, and `sessionStorage` are unsupported.
- CORS policy matters. A restrictive origin can break calls from Office Scripts.
- Treat outbound calls as a data-loss risk; check organizational policy.

## External data in Power Automate

If a flow needs external data:
1. Get external data in Power Automate using HTTP or a connector.
2. Pass the result into the Office Script as parameters.
3. Let the script focus on Excel workbook manipulation.
4. Return a small typed result to the flow.

Do not use `fetch` in scripts that must run through Power Automate.

## Flow-safe error handling

Throw when the flow must stop.

```ts
if (!table) {
  throw new Error('Required table "Orders" was not found.');
}
```

Return a status object when the flow should continue and branch on the result.

```ts
return {
  ok: false,
  message: 'No rows matched the filter.'
};
```

## Security posture

Never silently hardcode credentials. If the user asks for an API-key pattern, state that Office Scripts has no secure secret store and recommend passing secrets through an approved connector or moving the external call into Power Automate.


## Cloud-hosted workbook posture

Power Automate and Office Scripts are the preferred automation boundary for existing Excel files in OneDrive/SharePoint.

For a flow that updates workbook data:
1. Get external data in the flow using approved connectors or HTTP actions.
2. Pass typed JSON into the Office Script.
3. Update tables/ranges/worksheets through `ExcelScript`.
4. Return a compact typed result.
5. Let the flow handle notifications, retries, branching, and downstream calls.

Do not replace this with a local `openpyxl`/pandas job that downloads, rewrites, and uploads the workbook unless the user explicitly wants a copied output file and accepts feature-loss risk.

Power Automate-specific design points:
- Avoid active selection APIs. Use explicit worksheet/table/range names.
- After changing the script signature, recreate the Run script action if fields do not refresh.
- Select the workbook with the file picker or stable file identifier, not a brittle display-name assumption.
- If the workbook is on SharePoint and the script uses `fetch`, expect failure; move external calls into the flow.
