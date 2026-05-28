# Troubleshooting Office Scripts

## Contents

- Triage order
- Compile-time failures
- Runtime failures
- Error line numbers
- Automate tab unavailable
- Button and schedule issues
- Power Automate-specific failures
- Cloud workbook corruption or sync conflict triage

Load this for runtime errors, compile errors, missing workbook objects, Automate tab availability, button/schedule failures, or problems that only occur in Power Automate.

## Triage order

1. Capture the exact error text and line number.
2. Identify run mode: Excel Code Editor, button, Power Automate, SharePoint-library script, or scheduled flow.
3. Run `scripts/scan_office_script.py` if code is available.
4. Classify the failure: compile-time, runtime, platform/limit, permissions/admin, or data-shape mismatch.
5. Verify workbook assumptions: sheet/table names, headers, used range, active sheet, selected range, blank sheet, protected workbook, read-only state.
6. Create a minimal reproduction branch of the script that logs object presence and range dimensions.
7. Patch the narrow cause first; only refactor broadly after the script runs.

## Compile-time failures

Typical causes:
- explicit or implicit `any`
- missing `main` function or wrong workbook parameter
- unsupported callback/function syntax
- Office Add-ins APIs mixed into Office Scripts
- unsupported browser/DOM APIs
- class constructors calling workbook APIs or `console`
- user-defined unions mixed with ExcelScript object types

Use `references/typescript-restrictions.md`.

## Runtime failures

Common causes:
- worksheet, table, slicer, style, named item, chart, or PivotTable missing
- `getUsedRange()` returned `undefined` on a blank worksheet
- `setValues` array shape does not match target range
- table header was renamed
- active worksheet or selected range is not what the script expects
- protected/read-only workbook state
- operation too large for one call
- Power Automate timeout or connector limit

Preferred diagnostic logs:

```ts
console.log(`Worksheets: ${workbook.getWorksheets().map((s) => s.getName()).join(", ")}`);

const sheet = workbook.getWorksheet("Data");
console.log(`Data sheet found: ${Boolean(sheet)}`);

if (sheet) {
  const used = sheet.getUsedRange(true);
  console.log(`Used range: ${used ? used.getAddress() : "none"}`);
}
```

Keep logs short. Logs do not change workbook state.

## Error line numbers

Line numbers identify where the runtime noticed the error, not always the root cause. If line 50 fails on `table.getRange()`, the real bug may be that `table` was never found because the name changed earlier.

## Automate tab unavailable

Check these before changing code:
- Microsoft 365 license supports Office Scripts.
- Third-party cookies are enabled for Excel on the web when relevant.
- Tenant admin has not disabled Office Scripts.
- Group policy has not blocked Office Scripts on Windows.
- WebView2 is installed on Windows where required.
- User is not an external/guest tenant user.
- Teams desktop/mobile is not the target host; Office Scripts support in Teams is web-specific.

## Button and schedule issues

For script buttons:
- Confirm the script still exists and is shared/associated as expected.
- Confirm the workbook is not opened in an unsupported host.
- Run the same script in the Code Editor to separate button host problems from code problems.

For schedules:
- Scheduling is backed by Power Automate behavior; diagnose in Power Automate when the schedule/flow fails.
- If scheduling is unavailable in the current product state, use Power Automate directly.

## Power Automate-specific failures

Use `references/power-automate-json-fetch.md` when:
- the script works in Excel but fails in a flow
- `fetch is not defined`
- parameters arrive as objects or arrays with unexpected shapes
- the flow times out
- the flow user lacks access to workbook/script
- the script is stored in OneDrive vs SharePoint library


## Cloud workbook corruption or sync conflict triage

When the user reports corruption, repaired records, missing charts/pivots, sync conflicts, locks, or inconsistent data in a OneDrive/SharePoint workbook:

1. Stop any automation that writes to the workbook.
2. Identify every writer: user sessions, Power Automate, Logic Apps, Power Apps, Graph clients, local synced-folder jobs, Python scripts, and agent jobs.
3. Check whether any writer used file-level libraries such as `openpyxl`, pandas, `xlsxwriter`, SheetJS, LibreOffice, or raw ZIP/XML edits.
4. Preserve the original: use SharePoint version history or a copied workbook before testing repairs.
5. Reproduce on a copy, not the live workbook.
6. Replace package-level mutation with Office Scripts or Graph Excel API calls.
7. If the problem only appears in Power Automate, check connector locks, selected-range assumptions, refresh limitations, timeout, parameter size, and unsupported APIs.

Do not suggest "just save it again with openpyxl" as a repair for a cloud production workbook.
