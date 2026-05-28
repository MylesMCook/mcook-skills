# Office Scripts code patterns

## Contents

- Required worksheet/table helpers
- Create or clear a report sheet
- Header index map
- Append rows to a table
- Batch write values
- Power Automate result envelope
- Excel-only fetch with typed JSON
- Cloud workbook safety contract
- Replace all table body rows

Load this when a task needs copyable TypeScript patterns. Adapt names and contracts before using.

## Required worksheet/table helpers

```ts
function requireWorksheet(
  workbook: ExcelScript.Workbook,
  name: string
): ExcelScript.Worksheet {
  const sheet = workbook.getWorksheet(name);
  if (!sheet) {
    throw new Error(`Required worksheet "${name}" was not found.`);
  }
  return sheet;
}

function requireTable(
  workbook: ExcelScript.Workbook,
  name: string
): ExcelScript.Table {
  const table = workbook.getTable(name);
  if (!table) {
    throw new Error(`Required table "${name}" was not found.`);
  }
  return table;
}
```

## Create or clear a report sheet

```ts
function getOrCreateWorksheet(
  workbook: ExcelScript.Workbook,
  name: string
): ExcelScript.Worksheet {
  const existing = workbook.getWorksheet(name);
  if (existing) {
    return existing;
  }
  return workbook.addWorksheet(name);
}

function clearUsedRange(sheet: ExcelScript.Worksheet) {
  const used = sheet.getUsedRange();
  if (used) {
    used.clear(ExcelScript.ClearApplyTo.all);
  }
}
```

## Header index map

```ts
function getHeaderIndexes(table: ExcelScript.Table): Record<string, number> {
  const headerValues = table.getHeaderRowRange().getValues()[0] as string[];
  const indexes: Record<string, number> = {};
  headerValues.forEach((header, index) => {
    indexes[String(header)] = index;
  });
  return indexes;
}
```

## Append rows to a table

```ts
type CellValue = string | number | boolean;

function appendRows(table: ExcelScript.Table, rows: CellValue[][]) {
  if (rows.length === 0) {
    return;
  }
  table.addRows(-1, rows);
}
```

## Batch write values

```ts
type CellValue = string | number | boolean;

function writeValuesInBatches(
  sheet: ExcelScript.Worksheet,
  startRow: number,
  startColumn: number,
  values: CellValue[][],
  rowsPerBatch: number
) {
  if (values.length === 0) {
    return;
  }

  for (let row = 0; row < values.length; row += rowsPerBatch) {
    const batch = values.slice(row, row + rowsPerBatch);
    sheet
      .getRangeByIndexes(startRow + row, startColumn, batch.length, batch[0].length)
      .setValues(batch);
  }
}
```

## Power Automate result envelope

```ts
interface ScriptResult {
  ok: boolean;
  rowsProcessed: number;
  message: string;
}

function main(workbook: ExcelScript.Workbook): ScriptResult {
  return {
    ok: true,
    rowsProcessed: 0,
    message: "No rows to process."
  };
}
```

## Excel-only fetch with typed JSON

```ts
interface ApiRow {
  id: string;
  amount: number;
}

async function main(workbook: ExcelScript.Workbook): Promise<number> {
  const response = await fetch("https://example.com/api/rows");
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  const rows = await response.json() as ApiRow[];
  return rows.length;
}
```

Do not use this pattern for scripts that must run in Power Automate.


## Cloud workbook safety contract

Use this at the top of an agent answer or code review when the workbook is cloud-hosted.

```text
Workbook access plan:
- Source workbook is preserved.
- Mutations happen through Office Scripts / ExcelScript, not by overwriting the .xlsx package.
- Writes target named worksheets, tables, headers, and bounded ranges.
- Power Automate receives/returns typed JSON only.
- Any external HTTP call happens outside the Office Script when running in Power Automate.
```

## Replace all table body rows

```ts
type CellValue = string | number | boolean;

function replaceTableBody(table: ExcelScript.Table, rows: CellValue[][]) {
  const rowCount = table.getRowCount();
  if (rowCount > 0) {
    // Batch deletes for large tables in Power Automate-sensitive flows.
    for (let remaining = rowCount; remaining > 0;) {
      const count = Math.min(remaining, 1000);
      table.deleteRowsAt(0, count);
      remaining -= count;
    }
  }

  if (rows.length > 0) {
    table.addRows(-1, rows);
  }
}
```

Use this only when replacing the table body is intended. For append-only workflows, use `appendRows` instead.
