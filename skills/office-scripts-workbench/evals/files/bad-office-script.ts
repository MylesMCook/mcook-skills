function main(workbook) {
  let data;
  const table: any = workbook.getTable("Orders");
  Excel.run(async (context) => {
    await context.sync();
  });
  const response = fetch("https://example.com/api/orders");
  for (let i = 0; i < 1000; i++) {
    sheet.getRange("A" + i).setValue(i);
  }
}
