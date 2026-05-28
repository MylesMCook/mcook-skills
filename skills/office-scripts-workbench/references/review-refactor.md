# Review and refactor guide

## Contents

- Review categories
- Workbook contract
- Refactor principles
- Idempotency checklist
- Refactor shape
- Security/privacy review
- Cloud workbook access strategy

Load this for deep code review, maintainability refactors, idempotency, complex scripts, or cases where the user says the Office Script is large, fragile, slow, or hard to reason about.

## Review categories

Always group findings into:

1. Compile-time blockers
2. Runtime/data-shape risks
3. Performance risks
4. Power Automate/runtime mismatch
5. Maintainability/refactor opportunities
6. Security/privacy risks

Do not bury blockers under style comments.

## Workbook contract

Extract a workbook contract before refactoring:

```text
Inputs:
- required worksheets:
- required tables:
- required headers:
- selected range required:
- active sheet required:
- expected Power Automate parameters:
- expected return value:

Writes:
- worksheets created/deleted:
- ranges edited:
- tables appended/cleared:
- charts/PivotTables/shapes changed:

Failure behavior:
- throws:
- returns status:
- logs only:
```

State which parts are inferred rather than verified.

## Refactor principles

- Separate workbook I/O from business logic. Read once into arrays/objects, transform locally, write once.
- Keep helper functions small and typed.
- Use interfaces for row-shaped data and flow payloads.
- Replace magic sheet/table/header strings with constants.
- Preserve workbook side effects unless the user asks for behavioral changes.
- Make destructive operations explicit and idempotent.
- Prefer `throw new Error(...)` for required missing inputs in automated flows.
- Prefer status returns for expected no-op conditions.

## Idempotency checklist

A script should be safe to rerun when possible:
- It does not create duplicate report sheets without checking/removing/updating.
- It does not append duplicate rows unless that is intended.
- It clears only the target output region, not whole worksheets by accident.
- It recreates charts/PivotTables predictably or updates existing named objects.
- It uses stable object names for generated artifacts.

## Refactor shape

For complex scripts, aim for this shape:

```ts
const SOURCE_TABLE = "Orders";
const REPORT_SHEET = "Report";

interface OrderRow {
  orderId: string;
  amount: number;
  status: string;
}

interface Result {
  processed: number;
  message: string;
}

function main(workbook: ExcelScript.Workbook): Result {
  const source = readOrders(workbook);
  const summary = summarizeOrders(source);
  writeReport(workbook, summary);
  return { processed: source.length, message: "Report updated" };
}
```

Keep ExcelScript objects near the boundary. Plain arrays and interfaces should drive the core logic.

## Security/privacy review

Flag:
- hardcoded API keys or bearer tokens
- external URLs receiving workbook data
- logs containing sensitive worksheet values
- code that reads entire sheets when only a small range is needed
- Power Automate flows that expose workbook data to broad connectors


## Cloud workbook access strategy

Add this as the first review category whenever the workbook is or might be stored in OneDrive/SharePoint:

```text
Workbook access strategy:
- Is this an existing production workbook?
- Is the proposed tool mutating the .xlsx package directly?
- Is the workbook stored in OneDrive/SharePoint/Teams or a synced folder?
- Are there concurrent writers?
- Can the task be done through Office Scripts tables/ranges?
- If not, is Graph Excel API with a workbook session the right escape hatch?
```

Block this refactor direction by default:

```text
Use Python/openpyxl to load the live workbook, edit it, and save over the same SharePoint/OneDrive file.
```

Prefer this refactor direction:

```text
Create an Office Script with explicit workbook object guards, table/range-level writes, batched operations, and a typed result for the flow or agent.
```

When a local file library is unavoidable, require a copied input and a new output path. The review should call out unsupported workbook features and original-file preservation.
