"""Dump TABLE[10] = Table 11 (threshold sensitivity)"""
import docx

PATH = r"f:\MLSAPU\PhD-SPPU\India-VIX-Major-Revision\Major-Revision\Latest_Main-Manuscript_UPDATED_2026-07-24.docx"
d = docx.Document(PATH)
tbl = d.tables[10]
print(f"TABLE[10] rows={len(tbl.rows)} cols={len(tbl.columns)}")
for ridx, row in enumerate(tbl.rows):
    cells = [c.text.strip() for c in row.cells]
    print(f"  Row[{ridx}]: {cells}")
