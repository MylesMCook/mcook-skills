# Performance and platform limits

Load this for slow scripts, large datasets, timeouts, batching, looped workbook reads/writes, Power Automate limits, or scripts that work on small data but fail in production.

## Core performance rule

The common slow-script cause is excessive communication with the workbook. Office Scripts code looks synchronous, but workbook reads and writes synchronize with Excel behind the scenes. Minimize workbook API calls inside loops.

Bad:

```ts
for (let i = 0; i < rowCount; i++) {
  const value = sheet.getRange(`A${i + 1}`).getValue();
  sheet.getRange(`B${i + 1}`).setValue(String(value).trim());
}
```

Better:

```ts
const source = sheet.getRangeByIndexes(0, 0, rowCount, 1).getValues();
const output = source.map((row) => [String(row[0]).trim()]);
sheet.getRangeByIndexes(0, 1, output.length, 1).setValues(output);
```

## Read once, compute locally, write once

Use this plan for most data transformations:

1. Get one range/table body.
2. Convert values into typed local arrays.
3. Compute everything in local TypeScript.
4. Write the final 2D array back in one `setValues`, or in deliberate batches.

## Batch large writes

For large writes, split by rows or cells so a single `setValues` call is not too large.

```ts
function writeInBatches(
  sheet: ExcelScript.Worksheet,
  startRow: number,
  startCol: number,
  values: (string | number | boolean)[][],
  rowsPerBatch: number
) {
  for (let row = 0; row < values.length; row += rowsPerBatch) {
    const chunk = values.slice(row, row + rowsPerBatch);
    sheet
      .getRangeByIndexes(startRow + row, startCol, chunk.length, chunk[0].length)
      .setValues(chunk);
  }
}
```

Use smaller batches when the data is wide, formula-heavy, or the workbook has volatile calculations.

## Loop rules

- Do not call `getValues`, `getValue`, `getRange`, `getUsedRange`, `getWorksheet`, `getTable`, `setValues`, or `setValue` repeatedly inside tight loops unless the loop count is tiny.
- Do not use `try...catch` inside hot loops. Catch around the batch operation or around a small number of expected failure points.
- Do not log every row in production. Summarize counts and sample rows.

## Power Automate limits to design around

When the script is called by Power Automate:
- Treat 120 seconds as a hard synchronous timeout target.
- Split long work into multiple script calls or move orchestration to the flow.
- Keep Run script parameters comfortably below the documented parameter size limit.
- Design return values as compact summaries or JSON chunks, not whole workbooks.

## Practical optimization checklist

- Replace per-cell operations with range operations.
- Use tables for growing data and `addRows` for append operations.
- Store workbook object references once.
- Use `getUsedRange(true)` if formatting-only cells should not expand the range.
- Filter and map local arrays rather than the workbook object model.
- Return early when required inputs are missing.
- Avoid formatting huge ranges unless necessary.
- Separate data updates from chart/PivotTable/report formatting when possible.


## Cloud workbook and connector concurrency

When the workbook is in OneDrive/SharePoint, performance work is also safety work.

- Do not run parallel write jobs against the same workbook.
- For Power Automate/Excel Online connector workflows, assume the file can remain temporarily locked after connector use.
- Avoid multiple clients writing the same workbook at the same time: Excel desktop/web, Power Automate, Logic Apps, Power Apps, Graph clients, and agent scripts.
- Prefer one serialized writer that updates explicit ranges/tables and returns a small status object.
- For Graph Excel API workflows, create a workbook session for multi-call work, pass the session ID on every request, and keep writes sequential.
- If a script risks the 120-second Power Automate timeout, split work by table, worksheet, date window, or batch of rows rather than retrying blindly.
