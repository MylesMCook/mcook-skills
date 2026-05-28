# TypeScript restrictions and compile-time issues

Load this for compile errors, TypeScript issues, unsupported language features, callbacks, `any`, constructors, or code that looks valid TypeScript but fails in Office Scripts.

## Language baseline

Office Scripts uses TypeScript, but not every TypeScript/JavaScript pattern is accepted. Treat Office Scripts as a constrained TypeScript runtime connected to Excel.

## No `any`

Both explicit and implicit `any` are compile-time errors.

Bad:

```ts
let row;
let payload: any;
const parsed = JSON.parse(text);
```

Better:

```ts
type CellValue = string | number | boolean;

interface Payload {
  id: string;
  amount: number;
}

let row: CellValue[];
const payload = JSON.parse(text) as Payload;
```

For JSON from Power Automate or `fetch`, define interfaces. For unpredictable JSON, use `object[]` at the boundary, then validate and cast the parts you need.

## Main function signatures

Basic:

```ts
function main(workbook: ExcelScript.Workbook) {}
```

Power Automate parameters and return value:

```ts
interface Result {
  rowsProcessed: number;
}

function main(workbook: ExcelScript.Workbook, tableName: string): Result {
  return { rowsProcessed: 0 };
}
```

External `fetch`:

```ts
async function main(workbook: ExcelScript.Workbook): Promise<void> {
  const response = await fetch("https://example.com/data.json");
  const rows: object[] = await response.json();
  console.log(rows.length);
}
```

## Unsupported or fragile patterns

Avoid or replace these:

| Pattern | Problem | Replacement |
|---|---|---|
| `let x;` | implicit `any` | initialize or type it |
| `: any`, `as any` | explicit `any` | use interfaces, unions, or `object` |
| `eval(...)` | unsupported | parse data explicitly |
| `function*` / generators | unsupported with Office Scripts APIs | normal functions/loops |
| `Excel.run`, `context.sync` | Office Add-ins, not Office Scripts | direct ExcelScript calls |
| `Office.context`, `OfficeRuntime` | Office Add-ins/runtime APIs | ExcelScript/OfficeScript APIs |
| DOM, `document`, `window`, `localStorage`, `sessionStorage` | unsupported | pass data via parameters, workbook cells, or fetch |
| class extending `ExcelScript.*` | cannot inherit Office Script classes/interfaces | use wrappers/composition |
| `Array.sort` around workbook API objects | incompatible pattern risk | copy primitive values first, sort local data |
| function callbacks in array methods | Office Scripts requires arrow callbacks | `(x) => ...` |

## Array callbacks

Use arrow functions for callbacks.

```ts
const activeRows = rows.filter((row) => row.status === "Active");
```

Do not pass a named function or traditional function expression as an array callback.

## Constructors

Do not call ExcelScript APIs or `console.log` inside class constructors. Constructors cannot contain the hidden synchronization Office Scripts needs for workbook calls. Use a factory function or `init` method called from `main`.

## ExcelScript union caution

Avoid unions that mix ExcelScript object types with custom object types.

Bad:

```ts
type Source = ExcelScript.Table | MyTable;
```

Better: keep ExcelScript objects in one branch and plain data interfaces in another. Convert workbook objects into plain values before passing into business-logic helpers.
