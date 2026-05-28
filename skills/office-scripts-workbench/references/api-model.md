# Office Scripts API model

## Contents

- Runtime entry point
- Object model
- Required object guards
- Range values and formulas
- Header-driven table work
- Charts and PivotTables
- When to use Action Recorder output
- Cloud-safe workbook manipulation patterns

Load this when the task involves workbook structure, ExcelScript objects, ranges, tables, charts, PivotTables, or basic script design.

## Runtime entry point

Every Office Script starts from:

```ts
function main(workbook: ExcelScript.Workbook) {
  // work here
}
```

Power Automate can pass additional parameters and read a return value, but the workbook remains the first parameter.

Only code inside `main` or functions called from `main` executes. Top-level interfaces, type aliases, constants, and helper function declarations are fine; top-level workbook operations are not.

## Object model

Use this mental model:

```text
Workbook
  -> Worksheets
      -> Ranges
          -> values, formulas, formats
          -> Tables, Charts, Shapes, PivotTables, images, data validation
  -> Workbook-level collections: tables, worksheets, slicers, styles, named items, etc.
```

Default choices:
- Use `workbook.getWorksheet("Name")` for known worksheets; guard the result.
- Use `workbook.getActiveWorksheet()` only when the current active sheet is an intended input.
- Use `workbook.getTable("Name")` or `sheet.getTable("Name")` for stable data regions; guard the result.
- Use `sheet.getUsedRange(true)` when only value-containing cells matter.
- Use `getRangeByIndexes(row, col, rowCount, colCount)` for generated dynamic ranges.
- Use `getRange("A1:D20")` for fixed layout ranges.

## Required object guards

Office Scripts APIs often return `undefined` for missing named workbook objects. Guard before use and make failures specific.

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

For blank-sheet logic:

```ts
const used = sheet.getUsedRange(true);
if (!used) {
  console.log("No values were found on this worksheet.");
  return;
}
```

## Range values and formulas

Range values are two-dimensional arrays.

```ts
type CellValue = string | number | boolean;

const values = sheet.getRange("A2:D20").getValues() as CellValue[][];
const firstCell = values[0][0];

sheet.getRangeByIndexes(1, 0, values.length, values[0].length).setValues(values);
```

Rules:
- The array passed to `setValues` must match the target range shape exactly.
- A single row is still nested: `[["A", "B", "C"]]`.
- A single column is still nested: `[["A"], ["B"], ["C"]]`.
- Formulas use `setFormulas` with the same 2D shape rules.

## Header-driven table work

Prefer header names over hard-coded column numbers when the workbook may change.

```ts
const table = requireTable(workbook, "Orders");
const statusColumn = table.getColumnByName("Status");
const statusValues = statusColumn.getRangeBetweenHeaderAndTotal().getValues();

const body = table.getRangeBetweenHeaderAndTotal().getValues();
const headers = table.getHeaderRowRange().getValues()[0] as string[];
const amountIndex = headers.indexOf("Amount");
if (amountIndex < 0) {
  throw new Error('Required column "Amount" was not found.');
}
```

## Charts and PivotTables

Use charts for visualization tasks and PivotTables for summarization tasks. Prefer source tables over loose ranges when data may grow.

```ts
const table = requireTable(workbook, "Sales");
const sheet = requireWorksheet(workbook, "Report");
const chart = sheet.addChart(ExcelScript.ChartType.columnClustered, table.getRange());
chart.setTop(80);
chart.setLeft(20);
```

For PivotTables, create from a table or explicit source range and place on a report sheet. Verify source field names before adding row/data hierarchies.

## When to use Action Recorder output

Action Recorder output is useful for discovering exact API calls for formatting, UI actions, and rarely used Excel features. Do not keep recorder output unchanged when it hard-codes active selections, absolute ranges, or repeated formatting calls that should be parameterized.


## Cloud-safe workbook manipulation patterns

When the workbook is in OneDrive/SharePoint, design updates as targeted object-model mutations.

Prefer:
- `workbook.getTable("Name")` plus `addRows`, `deleteRowsAt`, `getRangeBetweenHeaderAndTotal`, and header-based indexing.
- `worksheet.getRangeByIndexes(...)` for generated output ranges.
- `worksheet.addTable(...)` for new structured regions.
- `range.setValues(...)` with exact 2D shape.
- `range.clear(...)` on a bounded output area or report sheet, not broad unknown regions.
- `workbook.addWorksheet(...)` only after checking whether the sheet already exists.

Avoid:
- full-workbook replacement
- deleting and recreating worksheets that contain hidden dependencies
- hard-coded active sheet or selected range assumptions in automation
- raw XML/package edits for formulas, pivots, slicers, charts, or query-backed workbooks

For table row replacement:
- Capture headers first.
- Delete body rows only when replacement is intended.
- Add rows with `table.addRows(-1, rows)`.
- For large deletes, batch them; deleting more than 1000 table rows at once can risk Power Automate timeout.
