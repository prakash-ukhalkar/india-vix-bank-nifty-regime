"""Verify the corrected docx tables."""
import docx

PATH = r"f:\MLSAPU\PhD-SPPU\India-VIX-Major-Revision\Major-Revision\Latest_Main-Manuscript_UPDATED_2026-07-24_tables_fixed.docx"
d = docx.Document(PATH)
TARGETS = {1: "T2-Splits", 5: "T6-Overall", 6: "T7-Regime", 7: "T8-Trading", 8: "T9-Costs", 9: "T10-GARCH", 10: "T11-Threshold"}

for tidx, tname in TARGETS.items():
    tbl = d.tables[tidx]
    print(f"\n=== {tname} (TABLE[{tidx}]) ===")
    for ridx, row in enumerate(tbl.rows):
        cells = [c.text.strip() for c in row.cells]
        print(f"  Row[{ridx}]: {cells}")
