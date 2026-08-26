# Comments Status Check (Based on Provided Reviewer Text)

Source comments file: [Major-Revision/COMMENTS_FOR_THE_AUTHOR_2026-07-24.md](Major-Revision/COMMENTS_FOR_THE_AUTHOR_2026-07-24.md)

## Summary
- Total tracked comments: 19
- Fully addressed: 16
- Partially addressed: 2
- Not fully addressed: 1

## Reviewer 1

1. High-VIX threshold from test-period p75 (look-ahead bias): Fully addressed.
Evidence: [results/vix_threshold_config.json](results/vix_threshold_config.json), [results/threshold_comparison.csv](results/threshold_comparison.csv)

2. Overlap-induced serial dependence/statistical inflation: Fully addressed.
Evidence: [results/statistical_tests.json](results/statistical_tests.json), [results/table5_statistical_tests.csv](results/table5_statistical_tests.csv)

3. Single-episode High-VIX concentration/generalizability: Fully addressed.
Evidence: [results/walkforward_results.csv](results/walkforward_results.csv), [plots/R05_walkforward_regime_accuracy.png](plots/R05_walkforward_regime_accuracy.png)

4. 50-bps Sharpe textual inconsistency: Fully addressed.
Evidence: [results/trading_simulation.csv](results/trading_simulation.csv)

5. Signal-generation timing/execution and overlap handling: Fully addressed.
Evidence: [notebooks/NB-R09_corrected_trading_simulation.ipynb](notebooks/NB-R09_corrected_trading_simulation.ipynb), [results/trading_simulation.csv](results/trading_simulation.csv)

6. Class-stratified metrics for High-VIX subset: Fully addressed.
Evidence: [results/table4_regime_metrics.csv](results/table4_regime_metrics.csv)

7. Hyperparameters/CV-OOF chronology and incorrect DOI references: Partially addressed.
Evidence for hyperparameters: [results/hyperparameter_table.csv](results/hyperparameter_table.csv), [results/all_best_params.json](results/all_best_params.json)
Gap: DOI/reference correction completeness is not fully evidenced as closed.

## Reviewer 2

1. Threshold look-ahead bias: Fully addressed.
Evidence: [results/vix_threshold_config.json](results/vix_threshold_config.json)

2. Temporal concentration limits generalizability: Fully addressed.
Evidence: [results/walkforward_results.csv](results/walkforward_results.csv)

3. Missing simple baselines: Fully addressed.
Evidence: [results/baseline_comparison.csv](results/baseline_comparison.csv)

4. Sharpe assumptions/annualization not stated: Fully addressed.
Evidence: [notebooks/NB-R09_corrected_trading_simulation.ipynb](notebooks/NB-R09_corrected_trading_simulation.ipynb), [results/trading_simulation.csv](results/trading_simulation.csv)

5. Missing SHAP evidence: Fully addressed.
Evidence: [results/shap_importance_High_VIX.csv](results/shap_importance_High_VIX.csv), [results/shap_importance_Low_VIX.csv](results/shap_importance_Low_VIX.csv), [results/shap_importance_Overall.csv](results/shap_importance_Overall.csv), [plots/R07_shap_regime_comparison.png](plots/R07_shap_regime_comparison.png)

6. Feature engineering reproducibility + recommendation to strengthen literature (GATE-GNN, EATSA-GNN, PIMPC-GNN): Partially addressed.
Evidence for feature engineering: [results/feature_specification.csv](results/feature_specification.csv)
Gap: recommended literature additions are not demonstrably complete in current manuscript state.

## Reviewer 3

1. Split-boundary leakage (remove final 21 days before each split): Fully addressed.
Evidence: [data/processed/split_summary.csv](data/processed/split_summary.csv)

2. Threshold from full test period: Fully addressed.
Evidence: [results/vix_threshold_config.json](results/vix_threshold_config.json)

3. Overlap/clustering-aware statistics: Fully addressed.
Evidence: [results/table5_statistical_tests.csv](results/table5_statistical_tests.csv), [results/statistical_tests.json](results/statistical_tests.json)

4. Need ablation and transparent component parameter table: Fully addressed.
Evidence: [results/ablation_results.csv](results/ablation_results.csv), [plots/R08_ablation_accuracy.png](plots/R08_ablation_accuracy.png), [results/hyperparameter_table.csv](results/hyperparameter_table.csv)

5. References are old; literature update needed: Not fully addressed.
Evidence: manuscript-level literature refresh appears incomplete for requested recent volatility-regime studies.

6. Regime-specific baselines/metrics and final target-realisation date clarity: Fully addressed.
Evidence: [results/baseline_comparison.csv](results/baseline_comparison.csv), [results/table4_regime_metrics.csv](results/table4_regime_metrics.csv), [notebooks/NB-R09_corrected_trading_simulation.ipynb](notebooks/NB-R09_corrected_trading_simulation.ipynb)

## Execution provenance note
- Current notebook metadata shows only [notebooks/NB-R05_walkforward_generalizability.ipynb](notebooks/NB-R05_walkforward_generalizability.ipynb) and [notebooks/NB-R09_corrected_trading_simulation.ipynb](notebooks/NB-R09_corrected_trading_simulation.ipynb) executed recently.
- Other outputs are present in [results](results), but the remaining notebook execution traces are not freshly rerun in current metadata.
