# All 19 Reviewer Comments Status Check (2026-07-24)

## Important scope note
- The file [Major-Revision/Major_NCAA-D-26-02775_R1.docx](Major-Revision/Major_NCAA-D-26-02775_R1.docx) contains only 7 numbered comments (single-reviewer block), not the full 19 comments from 3 reviewers.
- Full 19-comment mapping is taken from the established revision mapping and evidence files.

## Notebook execution snapshot
- Executed now: [notebooks/NB-R05_walkforward_generalizability.ipynb](notebooks/NB-R05_walkforward_generalizability.ipynb), [notebooks/NB-R09_corrected_trading_simulation.ipynb](notebooks/NB-R09_corrected_trading_simulation.ipynb)
- Not executed in current notebook metadata: NB-R01, NB-R02, NB-R03, NB-R04, NB-R06, NB-R07, NB-R08, NB-R10
- Outputs exist in [results](results) for all required artifacts.

## 19-comment status

### Reviewer 1
1. Threshold look-ahead bias: Addressed
Evidence: [results/vix_threshold_config.json](results/vix_threshold_config.json), [results/threshold_comparison.csv](results/threshold_comparison.csv)

2. Overlap/serial-correlation inference issue: Addressed
Evidence: [results/statistical_tests.json](results/statistical_tests.json), [results/table5_statistical_tests.csv](results/table5_statistical_tests.csv)

3. Single-episode generalizability risk: Addressed (with adverse result)
Evidence: [results/walkforward_results.csv](results/walkforward_results.csv), [plots/R05_walkforward_regime_accuracy.png](plots/R05_walkforward_regime_accuracy.png)

4. 50 bps Sharpe factual error: Addressed
Evidence: [results/trading_simulation.csv](results/trading_simulation.csv)

5. Signal timing ambiguity: Addressed
Evidence: [notebooks/NB-R09_corrected_trading_simulation.ipynb](notebooks/NB-R09_corrected_trading_simulation.ipynb)

6. High-VIX class-stratified metrics: Addressed
Evidence: [results/table4_regime_metrics.csv](results/table4_regime_metrics.csv)

7. Hyperparameters/CV/OOF and DOI issues: Partially addressed
Evidence: [results/hyperparameter_table.csv](results/hyperparameter_table.csv), [results/all_best_params.json](results/all_best_params.json)
Gap: DOI and reference-quality cleanup not fully proven complete.

### Reviewer 2
8. Threshold look-ahead bias: Addressed
Evidence: [results/vix_threshold_config.json](results/vix_threshold_config.json)

9. High-VIX clustering concern: Addressed
Evidence: [results/walkforward_results.csv](results/walkforward_results.csv)

10. Missing simple baselines: Addressed
Evidence: [results/baseline_comparison.csv](results/baseline_comparison.csv)

11. Sharpe convention missing: Addressed
Evidence: [notebooks/NB-R09_corrected_trading_simulation.ipynb](notebooks/NB-R09_corrected_trading_simulation.ipynb), [results/trading_simulation.csv](results/trading_simulation.csv)

12. Missing SHAP tables/plots: Addressed
Evidence: [results/shap_importance_High_VIX.csv](results/shap_importance_High_VIX.csv), [results/shap_importance_Low_VIX.csv](results/shap_importance_Low_VIX.csv), [plots/R07_shap_regime_comparison.png](plots/R07_shap_regime_comparison.png)

13. Feature engineering reproducibility details: Addressed
Evidence: [results/feature_specification.csv](results/feature_specification.csv)

### Reviewer 3
14. Split-boundary label leakage: Addressed
Evidence: [data/processed/split_summary.csv](data/processed/split_summary.csv)

15. Threshold look-ahead bias: Addressed
Evidence: [results/vix_threshold_config.json](results/vix_threshold_config.json)

16. Overlap/clustering in stats: Addressed
Evidence: [results/table5_statistical_tests.csv](results/table5_statistical_tests.csv)

17. Ablation studies: Addressed
Evidence: [results/ablation_results.csv](results/ablation_results.csv), [plots/R08_ablation_accuracy.png](plots/R08_ablation_accuracy.png)

18. Older references / recency gap: Not fully addressed
Evidence check against current manuscript indicates missing requested recent literature coverage completeness.

19. Regime-specific baselines + target realization clarity: Addressed
Evidence: [results/baseline_comparison.csv](results/baseline_comparison.csv), [notebooks/NB-R09_corrected_trading_simulation.ipynb](notebooks/NB-R09_corrected_trading_simulation.ipynb)

## Bottom line
- Fully addressed: 17/19
- Partially/Not fully addressed: 2/19 (reference/DOI and literature-recency items)
- Additional process risk: 8 notebooks are currently not executed in metadata, even though output artifacts are present.
