# Submission Package Checklist (2026-07-24)

## 1) Primary Upload Files (In Order)

1. Main revised manuscript:
- [Major-Revision/Latest_Main-Manuscript_UPDATED_2026-07-24.docx](Major-Revision/Latest_Main-Manuscript_UPDATED_2026-07-24.docx)

2. Point-by-point response letter:
- [Major-Revision/Response_to_Reviewers_Comments.docx](Major-Revision/Response_to_Reviewers_Comments.docx)

3. Optional internal readiness note (usually not uploaded unless journal allows/requests):
- [Major-Revision/FINAL_SUBMISSION_READINESS_CHECK_2026-07-24.md](Major-Revision/FINAL_SUBMISSION_READINESS_CHECK_2026-07-24.md)

## 2) Final Pre-Upload Checks

- Confirm you are uploading the UPDATED manuscript, not the old locked version.
- Confirm manuscript metadata exactly matches:
  - Manuscript ID: NCAA-D-26-02775
  - Title: India VIX Regime-Conditional Directional Prediction of Bank Nifty: A Stacking Ensemble Approach
  - Journal: Neural Computing and Applications
- Confirm response letter includes Reviewer 1/2/3 point-by-point items (R1.1-R3.6).
- Confirm no tracked changes/comments remain in the DOCX files.

## 3) Evidence Map (For Quick Editorial Queries)

### Leakage and threshold protocol
- [results/vix_threshold_config.json](results/vix_threshold_config.json)
- [results/threshold_comparison.csv](results/threshold_comparison.csv)
- [data/processed/split_summary.csv](data/processed/split_summary.csv)

### Dependence-aware statistics
- [results/table5_statistical_tests.csv](results/table5_statistical_tests.csv)
- [results/statistical_tests.json](results/statistical_tests.json)

### Generalizability
- [results/walkforward_results.csv](results/walkforward_results.csv)
- [plots/R05_walkforward_regime_accuracy.png](plots/R05_walkforward_regime_accuracy.png)

### Baselines and regime metrics
- [results/baseline_comparison.csv](results/baseline_comparison.csv)
- [results/table4_regime_metrics.csv](results/table4_regime_metrics.csv)
- [plots/R06_baseline_comparison.png](plots/R06_baseline_comparison.png)

### SHAP analysis
- [results/shap_importance_High_VIX.csv](results/shap_importance_High_VIX.csv)
- [results/shap_importance_Low_VIX.csv](results/shap_importance_Low_VIX.csv)
- [results/shap_importance_Overall.csv](results/shap_importance_Overall.csv)
- [plots/R07_shap_regime_comparison.png](plots/R07_shap_regime_comparison.png)

### Ablation and model transparency
- [results/ablation_results.csv](results/ablation_results.csv)
- [plots/R08_ablation_accuracy.png](plots/R08_ablation_accuracy.png)
- [results/hyperparameter_table.csv](results/hyperparameter_table.csv)
- [results/all_best_params.json](results/all_best_params.json)

### Trading simulation and Sharpe conventions
- [results/trading_simulation.csv](results/trading_simulation.csv)
- [plots/R09_trading_simulation.png](plots/R09_trading_simulation.png)

## 4) Figure/Table Source Pointers

- Threshold comparison figure: [plots/R02_vix_threshold_comparison.png](plots/R02_vix_threshold_comparison.png)
- Statistical tests figure: [plots/R04_statistical_tests.png](plots/R04_statistical_tests.png)
- Walk-forward figure: [plots/R05_walkforward_regime_accuracy.png](plots/R05_walkforward_regime_accuracy.png)
- Baseline comparison figure: [plots/R06_baseline_comparison.png](plots/R06_baseline_comparison.png)
- SHAP figures: [plots/R07_shap_beeswarm_high_vix.png](plots/R07_shap_beeswarm_high_vix.png), [plots/R07_shap_regime_comparison.png](plots/R07_shap_regime_comparison.png)
- Ablation figure: [plots/R08_ablation_accuracy.png](plots/R08_ablation_accuracy.png)
- Trading figure: [plots/R09_trading_simulation.png](plots/R09_trading_simulation.png)

## 5) Final Go/No-Go

- GO if both files below are the uploaded pair:
  1. [Major-Revision/Latest_Main-Manuscript_UPDATED_2026-07-24.docx](Major-Revision/Latest_Main-Manuscript_UPDATED_2026-07-24.docx)
  2. [Major-Revision/Response_to_Reviewers_Comments.docx](Major-Revision/Response_to_Reviewers_Comments.docx)

- NO-GO if any old manuscript variant is selected by mistake.
