# Major Revision Addressal Audit (2026-07-24)

## Scope Used
- Reviewed only files under [Major-Revision](Major-Revision) for manuscript/comment artifacts.
- Cross-validated notebook implementation and generated evidence from [notebooks](notebooks) and [results](results).

## Key Finding
- Major-revision implementation was not fully reliable before this audit due to two notebook logic issues.
- Both critical issues are now fixed in notebook code and re-run for updated outputs.

## Fixes Applied During This Audit

### 1) Walk-forward episode detection bug fixed
- File patched: [notebooks/NB-R05_walkforward_generalizability.ipynb](notebooks/NB-R05_walkforward_generalizability.ipynb)
- Old behavior incorrectly computed each episode end using all later High-VIX rows, causing repeated same end dates.
- New behavior groups contiguous High-VIX runs and reports true start/end/duration per episode.
- Re-executed and updated output file: [results/walkforward_results.csv](results/walkforward_results.csv)

### 2) Trading simulation protocol/metrics logic fixed
- File patched: [notebooks/NB-R09_corrected_trading_simulation.ipynb](notebooks/NB-R09_corrected_trading_simulation.ipynb)
- Corrected to match stated protocol:
  - signal at day t
  - entry at open[t+1]
  - exit at close[t+21]
  - non-overlapping positions
  - proper bps conversion for costs
  - daily return series based metrics
- Re-executed and updated output file: [results/trading_simulation.csv](results/trading_simulation.csv)

## Current Evidence Snapshot (Post-Fix)
- Threshold method still implies sparse High-VIX in fixed split:
  - [results/vix_threshold_config.json](results/vix_threshold_config.json)
  - [results/threshold_comparison.csv](results/threshold_comparison.csv)
- Walk-forward now shows High-VIX outperformance only 1/6 years:
  - [results/walkforward_results.csv](results/walkforward_results.csv)
- Corrected trading table now shows strategy Sharpe below buy-and-hold at all tested costs:
  - [results/trading_simulation.csv](results/trading_simulation.csv)
- Reviewer tracker still flags one manuscript-only item pending:
  - [results/revision_tracker.csv](results/revision_tracker.csv)

## Major-Revision Folder Check (Requested Scope)
- Present artifacts in [Major-Revision](Major-Revision):
  - [Major-Revision/Latest_Main-Manuscript.docx](Major-Revision/Latest_Main-Manuscript.docx)
  - [Major-Revision/Major_NCAA-D-26-02775_R1.docx](Major-Revision/Major_NCAA-D-26-02775_R1.docx)
  - [Major-Revision/Gmail - NCAA-D-26-02775R1 - Editor Decision.pdf](Major-Revision/Gmail%20-%20NCAA-D-26-02775R1%20-%20Editor%20Decision.pdf)

## Remaining Work To Complete Submission-Ready Addressal
- Update revised manuscript text/tables to match new post-fix outputs (especially walk-forward and trading claims).
- Finalize manuscript-only references/literature update item (R3.5 / R1.7 DOI checks).
- Prepare final point-by-point response letter aligned to the updated output tables.

## Important Note
- Notebook metadata still shows cells as not executed in-session history, but outputs and CSV artifacts were regenerated during this audit for NB-R05 and NB-R09.
