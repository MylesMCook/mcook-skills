---
name: office-scripts-workbench
description: "Use this skill when developing, debugging, refactoring, or reviewing Microsoft Excel Office Scripts (`ExcelScript` TypeScript) for workbook automation, Power Automate Run script actions, ranges, tables, charts, PivotTables, JSON, fetch, performance, or platform limits. Also use when a OneDrive/SharePoint/Teams Excel workbook might be corrupted by agents using openpyxl, pandas, xlsxwriter, SheetJS, LibreOffice, raw .xlsx/ZIP/XML edits, or synced local-file overwrites; route to Office Scripts or Graph Excel APIs instead. Do not use for VBA, Office.js add-ins, Google Apps Script, general formulas, or ordinary local xlsx generation unless translating to Office Scripts or preventing unsafe cloud-workbook mutation."
---

# Office Scripts Workbench

Use this skill for serious Microsoft Excel Office Scripts work: authoring, debugging, refactoring, reviewing, and explaining scripts that run from Excel's Automate tab, workbook buttons, or Power Automate's Excel Online connector.

Office Scripts are not VBA, Office Add-ins, Office.js add-in code, or local `.xlsx` package editing. Keep the target runtime explicit.

## Hard cloud-workbook safety rule

If the workbook is stored in OneDrive, SharePoint, Teams, an Office 365 Group drive, or a synced OneDrive/SharePoint local folder, assume direct `.xlsx` mutation is unsafe for an existing production workbook.

Do not default to `openpyxl`, pandas Excel writers, `xlsxwriter`, SheetJS, LibreOffice conversion, COM automation, or raw ZIP/XML edits for existing cloud workbooks. Default to Office Scripts / `ExcelScript` workbook APIs. If a cloud API workflow is explicitly needed, use Microsoft Graph Excel workbook APIs with workbook sessions and sequential writes.

Only use file-level libraries for new workbook artifacts, offline copies, read-only inspection, or explicitly approved recovery experiments. Never overwrite the source workbook unless the user explicitly accepts that risk.

## Default workflow

1. Classify the workbook location and mutation risk:
   - local throwaway file
   - existing local production file
   - OneDrive/SharePoint/Teams/cloud workbook
   - synced local OneDrive/SharePoint path
2. If cloud-hosted or corruption/locking/coauthoring is mentioned, read `references/sharepoint-onedrive-safety.md` before proposing tools.
3. Identify run mode: Excel Code Editor, workbook button, Power Automate `Run script`, SharePoint-library script, scheduled/flow-triggered script, or Graph Excel API escape hatch.
4. Identify workbook dependencies: worksheet names, table names, range addresses, headers, shapes/charts/PivotTables, selected range assumptions, protection/read-only state, and idempotency needs.
5. Inspect Office Script code against runtime constraints. When a `.ts` file is available, run:
   ```bash
   python3 scripts/scan_office_script.py path/to/script.ts --json
   ```
6. Inspect agent plans or non-Office-Scripts code for unsafe workbook mutation. When a plan, Python script, JS script, or README proposes Excel file edits, run:
   ```bash
   python3 scripts/scan_excel_mutation_plan.py path/to/file --json
   ```
   Add `--cloud` when the workbook is or might be in OneDrive/SharePoint.
7. Decide whether the task is generation, bug triage, refactor, performance work, Power Automate integration, cloud-workbook safety, or Graph handoff. Load only the matching reference.
8. Produce a focused patch or a complete replacement script. For complete scripts, include `main(workbook: ExcelScript.Workbook, ...)` and all helper types/functions.
9. Validate against the gotchas section. State workbook assumptions that could not be verified.

## Reference routing

- Read `references/sharepoint-onedrive-safety.md` for OneDrive, SharePoint, Teams, coauthoring, locks, sync conflicts, corruption, openpyxl/pandas/xlsxwriter risk, cloud workbooks, or Graph Excel API escape hatches.
- Read `references/api-model.md` when designing or reviewing workbook/worksheet/range/table/chart/PivotTable logic.
- Read `references/typescript-restrictions.md` for compile errors, TypeScript issues, callbacks, `any`, constructors, `eval`, or unsupported language patterns.
- Read `references/performance-and-limits.md` for slow scripts, large datasets, timeout risk, batching, looped workbook reads/writes, connector limits, or API throttling.
- Read `references/power-automate-json-fetch.md` for Power Automate, parameters/return values, JSON, external APIs, `fetch`, credentials, CORS, or connector behavior.
- Read `references/troubleshooting.md` for runtime errors, missing objects, Automate tab availability, button/schedule failures, locks, or hard-to-reproduce failures.
- Read `references/review-refactor.md` for deep code review, maintainability refactors, idempotency, or complex multi-step script redesign.
- Read `assets/script-patterns.md` when a task needs reusable code templates.
- Run `scripts/scan_office_script.py` for TypeScript Office Script review/debug/refactor.
- Run `scripts/scan_excel_mutation_plan.py` for plans or code that may mutate `.xlsx` files outside Excel.

## Output standards

For cloud workbook safety:
- Start by blocking the unsafe path if the user or prior agent proposed file-level mutation of an existing OneDrive/SharePoint workbook.
- Replace `download -> openpyxl/pandas/xlsxwriter -> overwrite` with an Office Script plan when workbook mutation is the goal.
- Do not present full-file upload-back, sync replacement, or save-over-source as a normal safe path for live OneDrive/SharePoint workbook mutation. Discuss it only for explicitly approved recovery or replacement work.
- Use Graph Excel APIs only when the user needs a service/app/API workflow outside Excel or Power Automate. Do not turn this skill into a full Graph auth/app-registration guide.
- Preserve the original workbook by default. Prefer table/range updates over full-file replacement.

For bug fixes:
- Start with the likely root cause.
- Show the minimal code change first.
- Then give the full corrected function/script if the surrounding context is ambiguous.

For new scripts:
- Use named constants for sheet/table/header names.
- Guard required workbook objects before calling methods on them.
- Prefer tables and header names over hard-coded column indexes when the workbook is expected to evolve.
- Use explicit interfaces for JSON and Power Automate payloads.
- Keep workbook reads/writes batched rather than interleaved inside loops.

For reviews:
- Separate unsafe workbook-access strategy, compile-time blockers, runtime risks, performance risks, Power Automate/runtime mismatch, and maintainability changes.
- Do not invent workbook structure. Infer it from code or sample data and label assumptions.

## Most-used snippets

Cloud-safe default response:

```text
I would not use openpyxl/pandas/xlsxwriter to overwrite the live OneDrive/SharePoint workbook. I would write an Office Script that updates the needed worksheets/tables/ranges through ExcelScript, and run it from Excel or Power Automate. If this must be driven by an external service, use Graph Excel APIs with a workbook session and sequential writes.
```

Required worksheet guard:

```ts
const sheet = workbook.getWorksheet("Data");
if (!sheet) {
  throw new Error('Required worksheet "Data" was not found.');
}
```

Typed range read:

```ts
type CellValue = string | number | boolean;
const values = sheet.getRange("A1:D20").getValues() as CellValue[][];
```

Power Automate-friendly entry point:

```ts
interface InputRow {
  id: string;
  amount: number;
}

interface ScriptResult {
  rowsProcessed: number;
  message: string;
}

function main(workbook: ExcelScript.Workbook, rows: InputRow[]): ScriptResult {
  return { rowsProcessed: rows.length, message: "Completed" };
}
```

## Gotchas

- A synced OneDrive/SharePoint path is not just a normal local file when the source workbook is production data.
- Every Office Script needs a `main` function; the first parameter is always `ExcelScript.Workbook`.
- Code outside functions does not run except declarations. Put work inside `main` or helpers called by `main`.
- `workbook.getWorksheet(name)`, `workbook.getTable(name)`, and many named objects can return `undefined`; guard them before use.
- `worksheet.getUsedRange()` can be `undefined` on a blank worksheet.
- Office Scripts does not support explicit or implicit `any`. Type JSON, parameters, and range values.
- Office Scripts code looks synchronous but syncs with the workbook behind the scenes. Avoid workbook reads/writes inside tight loops.
- `fetch` requires `async main`; it does not work when the script runs through Power Automate and is not supported for scripts stored on a SharePoint site.
- Power Automate may run with no active user selection. Avoid `getSelectedRange`, `getActiveCell`, and UI-relative assumptions in flow scripts.
- Do not use `Excel.run`, `context.sync`, `Office.context`, DOM APIs, `localStorage`, or `sessionStorage`; those belong to other runtimes or are unsupported.
- Treat external calls and workbook data as sensitive. Do not hardcode secrets unless the user explicitly accepts that risk.
