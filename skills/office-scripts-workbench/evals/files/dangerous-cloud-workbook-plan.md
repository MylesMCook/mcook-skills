# Dangerous cloud workbook plan

Target: SharePoint document library workbook `Monthly Ops.xlsx`.

Proposed agent steps:
1. Download the live workbook from SharePoint.
2. Use openpyxl.load_workbook(input_path) to edit cells and tables.
3. Use pandas to append a DataFrame and call to_excel(input_path).
4. Save over the original file and upload back to SharePoint.
5. Run this in parallel for each department.
