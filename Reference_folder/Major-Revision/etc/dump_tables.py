"""
Dump current cell values from the tables that need correction.
Tables: TABLE[1]=T2, TABLE[5]=T6, TABLE[6]=T7, TABLE[7]=T8, TABLE[8]=T9, TABLE[9]=T10
"""
import docx
import json
from pathlib import Path

PATH = r"f:\MLSAPU\PhD-SPPU\India-VIX-Major-Revision\Major-Revision\Latest_Main-Manuscript_UPDATED_2026-07-24.docx"
OUTF = r"f:\MLSAPU\PhD-SPPU\India-VIX-Major-Revision\Major-Revision\etc\table_audit.txt"

d = docx.Document(PATH)

# indices of tables needing update
TARGETS = {1: "T2-Splits", 5: "T6-Overall", 6: "T7-Regime", 7: "T8-Trading", 8: "T9-Costs", 9: "T10-GARCH"}

with open(OUTF, "w", encoding="utf-8") as f:
    for tidx, tname in TARGETS.items():
        tbl = d.tables[tidx]
        f.write(f"\n=== {tname} (table index {tidx}) rows={len(tbl.rows)} cols={len(tbl.columns)} ===\n")
        for ridx, row in enumerate(tbl.rows):
            cells = [c.text.strip() for c in row.cells]
            f.write(f"  Row[{ridx}]: {cells}\n")

print("Done - written to table_audit.txt")
