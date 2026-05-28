# OneDrive and SharePoint Excel safety

## Contents

- Non-negotiable default
- Decision table
- Agent response policy
- Pre-mutation checklist
- Office Scripts implementation pattern
- Graph Excel API branch
- File-level libraries: allowed and blocked uses
- When the user asks "can I still use openpyxl?"

Load this when the workbook is in OneDrive, SharePoint, Teams, an Office 365 Group drive, a synced OneDrive/SharePoint folder, or when the user mentions corruption, locks, coauthoring, cloud storage, `openpyxl`, pandas, `xlsxwriter`, SheetJS, LibreOffice, raw `.xlsx` edits, or overwriting a workbook.

## Non-negotiable default

For an existing production workbook in OneDrive/SharePoint, do not mutate the `.xlsx` package directly by default.

Unsafe default pattern:

```text
download workbook -> openpyxl/pandas/xlsxwriter/SheetJS/LibreOffice/raw XML -> save over original -> upload/let sync replace source
```

Safe default pattern:

```text
Office Script -> ExcelScript workbook objects -> targeted table/range/worksheet update -> typed JSON result
```

Cloud API escape hatch:

```text
Microsoft Graph Excel API -> workbook session -> sequential table/range calls -> persist changes
```

Use the escape hatch only when the user needs a service/app/API workflow outside Excel or Power Automate. This skill may name the Graph branch and session rules, but should not become a full Graph authentication, app registration, or tenant-admin skill.

## Decision table

| Situation | Default path | Avoid |
|---|---|---|
| Existing SharePoint/OneDrive workbook needs cell/table/sheet edits | Office Scripts / ExcelScript | `openpyxl` overwrite, pandas `to_excel` overwrite, raw ZIP/XML |
| Power Automate needs to update workbook data | Power Automate `Run script` with typed parameters | `fetch` inside the script; selected-range assumptions |
| External service must update workbook without Excel UI | Microsoft Graph Excel APIs with workbook session | parallel writes; sessionless multi-step updates |
| Need a new workbook artifact from scratch | file-level library is acceptable | replacing the production workbook in place |
| Need offline analysis only | copy/export data; read-only inspection | writing back to source workbook |
| Workbook has pivots, charts, Power Query, slicers, macros, protection, external links, or heavy formatting | Office Scripts or Excel/Graph object model | generic package rewrite |

## Agent response policy

When a prompt proposes file-level libraries against a cloud workbook:

1. State that direct `.xlsx` mutation is the wrong default for an existing cloud workbook.
2. Name the safer mutation layer: Office Scripts first, Graph Excel API only for explicit service/API workflows.
3. Convert the task into an Office Script plan or script.
4. Preserve the source workbook by default.
5. If the user explicitly insists on local library mutation, require a copy/new output file path and state that rich workbook features may not be preserved. Do not overwrite the original.

Useful phrasing:

```text
I will not use openpyxl on the live SharePoint workbook. I will write an Office Script that updates the target table/range through ExcelScript. The script can be run from Excel or called by Power Automate.
```

## Pre-mutation checklist

Before writing or changing a script, identify:

- Workbook location: local file, OneDrive, SharePoint, Teams, Office 365 Group, or synced folder.
- Source workbook preservation rule: original preserved, copied first, or explicit overwrite.
- Concurrent writers: Excel desktop/web users, Power Automate flows, Logic Apps, Power Apps, other connectors, or agent jobs.
- Workbook features: tables, pivots, charts, formulas, named ranges, slicers, Power Query, data validation, comments, external links, macros, protection.
- Required objects: sheet names, table names, headers, range addresses.
- Automation run mode: Excel Code Editor, workbook button, Power Automate Run script, or Graph API.
- Rollback path: SharePoint version history, copied workbook, or exported input data.

If the prompt lacks these details, make minimal assumptions and choose the least destructive path.

## Office Scripts implementation pattern

Prefer object-level edits:

```ts
interface ScriptResult {
  ok: boolean;
  rowsUpdated: number;
  message: string;
}

function main(workbook: ExcelScript.Workbook): ScriptResult {
  const table = workbook.getTable("Orders");
  if (!table) {
    throw new Error('Required table "Orders" was not found.');
  }

  const headers = table.getHeaderRowRange().getValues()[0] as string[];
  const statusIndex = headers.indexOf("Status");
  if (statusIndex < 0) {
    throw new Error('Required column "Status" was not found.');
  }

  const body = table.getRangeBetweenHeaderAndTotal().getValues() as (string | number | boolean)[][];
  const output = body.map((row) => {
    const next = row.slice();
    if (String(next[statusIndex]).trim() === "") {
      next[statusIndex] = "Pending";
    }
    return next;
  });

  table.getRangeBetweenHeaderAndTotal().setValues(output);

  return {
    ok: true,
    rowsUpdated: output.length,
    message: "Statuses normalized."
  };
}
```

This changes table data through Excel's workbook model rather than rewriting the `.xlsx` file.

## Graph Excel API branch

Use this branch only when the task must be driven by an external app/service or agent with cloud API access.

Rules:
- Use Microsoft Graph Excel workbook APIs for OneDrive for Business, SharePoint sites, or Group drives.
- Create a workbook session for more than one or two calls.
- Use a persistent session when changes should be saved.
- Use a non-persistent session only for analysis/calculation results that should not affect source state.
- Pass `workbook-session-id` on subsequent requests.
- Send writes to the same workbook sequentially. Do not parallelize write requests against the same workbook.
- Respect throttling and `Retry-After`.
- Keep operations targeted to ranges/tables/worksheets; avoid replacing the whole file.
- Handoff to a Graph/API skill for authentication, permissions, SDK code, or tenant-specific setup.

## File-level libraries: allowed and blocked uses

Allowed:
- Creating a brand-new workbook artifact.
- Reading a downloaded copy for offline analysis.
- Writing to a new file name after explicit approval.
- Building a recovery copy when the original is preserved.

Blocked by default:
- Saving over an existing SharePoint/OneDrive workbook.
- Letting a synced local path upload an in-place package rewrite.
- Rebuilding a rich workbook from scratch and uploading it over the original.
- Using local libraries against a workbook with pivots, slicers, Power Query, macros, external connections, or important formatting.

Library-specific notes:
- `xlsxwriter` is writer-only; it cannot read or modify an existing workbook.
- `openpyxl` can read/write `.xlsx`, but rich features such as PivotTables have limited management support and should not be treated as a complete Excel preservation layer.
- pandas Excel writers are data-export tools, not a safe mutation layer for rich production workbooks.
- LibreOffice/headless conversion is not a safe default for preserving complex Microsoft 365 workbook state.

## When the user asks "can I still use openpyxl?"

Answer with this default:

```text
Yes for new files, read-only inspection, or explicitly approved copies. No as the default way to mutate an existing OneDrive/SharePoint production workbook. For that, use Office Scripts or Graph Excel APIs.
```
