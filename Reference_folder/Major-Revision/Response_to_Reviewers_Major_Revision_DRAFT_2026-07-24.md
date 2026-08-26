Response to Reviewers
Manuscript ID: NCAA-D-26-02775
Title: India VIX Regime-Conditional Directional Prediction of Bank Nifty: A Stacking Ensemble Approach
Journal: Neural Computing and Applications

Dear Editor and Reviewers,

We sincerely thank the Editor and all Reviewers for the detailed and constructive feedback. We have reworked the analysis pipeline and manuscript to address methodological concerns related to leakage, look-ahead bias, overlapping outcomes, regime concentration, baseline benchmarking, and reporting transparency. Importantly, where corrected analyses no longer support our earlier strength of claim, we now report those results transparently and have revised the manuscript narrative accordingly.

Below we respond point-by-point.

Reviewer 1

R1.1. VIX threshold look-ahead bias (threshold estimated from test distribution)
Reviewer comment:
The High-VIX threshold (15.08) was estimated from the test period distribution, creating look-ahead bias.

Response:
Accepted. We replaced the biased threshold with a pre-test calibration from train+validation only.

Changes made:
1. Primary threshold is now p75 of train+validation VIX, equal to 18.71.
2. We also report two robustness alternatives (expanding p75 and rolling 252-day p75).
3. Regime partition was recomputed under the fixed threshold.

Current evidence:
1. results/vix_threshold_config.json
2. results/threshold_comparison.csv


R1.2. Serial dependence from overlapping 21-day targets invalidates i.i.d. inference
Reviewer comment:
The original Fisher/bootstrapped inference did not adequately address dependence from overlapping forward labels.

Response:
Accepted. We replaced i.i.d. style inference with dependence-aware procedures.

Changes made:
1. Non-overlapping Fisher test (every 21st observation).
2. Circular block bootstrap confidence interval (block length 21).
3. Block permutation test with Bonferroni-adjusted reporting across horizons.

Current evidence:
1. results/table5_statistical_tests.csv
2. results/statistical_tests.json

Current reported values:
1. Non-overlapping Fisher p = 1.000
2. Block permutation p = 0.3566
3. Block bootstrap 95% CI for High-Low accuracy difference = [16.2, 51.4] percentage points

Manuscript narrative revision:
We now avoid strong significance language and present the regime differential as sensitive to dependence-aware testing assumptions.


R1.3. Generalizability risk because High-VIX days cluster in one episode
Reviewer comment:
The original effect may be event-specific.

Response:
Accepted. We added a yearly walk-forward test across multiple historical years using the fixed pre-test threshold.

Changes made:
1. Annual walk-forward evaluation with train-before-test chronology.
2. Regime-specific accuracy tracked by year.

Current evidence:
1. results/walkforward_results.csv
2. plots/R05_walkforward_regime_accuracy.png

Current reported values:
1. High-VIX accuracy exceeds Low-VIX in 1 of 6 evaluated years.
2. In 5 of 6 years, Low-VIX accuracy is higher.

Manuscript narrative revision:
We now explicitly state limited cross-period generalizability and position the regime filter as context-dependent rather than universally superior.


R1.4. Factual inconsistency in transaction cost statement (50 bps Sharpe)
Reviewer comment:
The text claimed strategy Sharpe remained above buy-and-hold at all costs, inconsistent with table values.

Response:
Accepted and corrected. We rewrote the simulation logic and corrected all related text.

Changes made:
1. Simulation now follows protocol-consistent entry/exit timing and non-overlapping positions.
2. Cost handling corrected in basis-point conversion.
3. Cost-sensitivity table regenerated.

Current evidence:
1. results/trading_simulation.csv
2. notebooks/NB-R09_corrected_trading_simulation.ipynb

Current reported values:
At 50 bps, strategy Sharpe = 0.375 and buy-and-hold Sharpe = 1.204 (strategy below benchmark).


R1.5. Signal timing ambiguity
Reviewer comment:
Execution timing relative to close prices and VIX publication was unclear.

Response:
Accepted. We added explicit protocol text and implemented the simulation accordingly.

Protocol now stated:
1. Signal computed after close on day t using Close[t], VIX[t], and features available through t.
2. Entry at open[t+1].
3. Exit at close[t+21].
4. At most one active position (no pyramiding).

Current evidence:
1. notebooks/NB-R09_corrected_trading_simulation.ipynb
2. results/trading_simulation.csv


R1.6. High-VIX subset must include local baseline and class metrics
Reviewer comment:
Need majority baseline, precision, recall, and F1 within High-VIX subset.

Response:
Accepted. We report full class-stratified metrics by regime.

Current evidence:
1. results/table4_regime_metrics.csv
2. results/statistical_tests.json

Current reported values:
1. High-VIX N = 8
2. High-VIX majority baseline = 100.0%
3. High-VIX model accuracy/precision/recall/F1 = 100.0% each

Manuscript narrative revision:
Given class concentration in this small subset, we now caution that these High-VIX metrics do not establish superiority over the local baseline.


R1.7. Missing reproducibility details (hyperparameters, folds, OOF chronology) and DOI corrections
Reviewer comment:
Need complete hyperparameter and CV details; references contained DOI issues.

Response:
Accepted.

Changes made:
1. Final tuned hyperparameters are tabulated.
2. Time-series fold structure and chronological OOF generation are documented in methods and notebook flow.
3. DOI/reference corrections prepared for manuscript revision cycle.

Current evidence:
1. results/hyperparameter_table.csv
2. notebooks/NB-R03_model_retraining.ipynb


Reviewer 2

R2.1. Threshold look-ahead bias
Response:
Addressed identically to R1.1.

Evidence:
1. results/vix_threshold_config.json
2. results/threshold_comparison.csv


R2.2. Temporal concentration and dependence concerns
Response:
Addressed through dependence-aware tests and walk-forward generalizability checks.

Evidence:
1. results/table5_statistical_tests.csv
2. results/walkforward_results.csv

Narrative revision:
We now report these results as constrained and episode-sensitive rather than broadly generalizable.


R2.3. Missing simpler baselines under the same regime filter
Reviewer comment:
Need majority, persistence, and logistic-type baseline comparisons.

Response:
Accepted. We added and reported comparable baselines under identical regime partitions.

Current evidence:
1. results/baseline_comparison.csv
2. plots/R06_baseline_comparison.png

Current highlights:
1. High-VIX subset has N = 8 and local majority baseline = 100.0%.
2. Stacking equals majority in High-VIX under this split.

Manuscript revision:
Claims about complexity advantage are now narrowed and conditioned on sample limitations.


R2.4. Sharpe convention not stated
Reviewer comment:
Risk-free rate and annualization convention must be explicit.

Response:
Accepted.

Changes made:
1. RFR fixed at 6.5% annual.
2. Daily RFR = annual/252.
3. Annualization factor = sqrt(252).

Evidence:
1. notebooks/NB-R09_corrected_trading_simulation.ipynb
2. results/trading_simulation.csv


R2.5. SHAP evidence missing for feature-level claims
Reviewer comment:
Need actual SHAP rankings by regime.

Response:
Accepted. We provide regime-specific SHAP importance tables and plots.

Evidence:
1. results/shap_importance_High_VIX.csv
2. results/shap_importance_Low_VIX.csv
3. results/shap_importance_Overall.csv
4. results/shap_regime_shift.csv
5. plots/R07_shap_regime_comparison.png

Current highlights:
1. High-VIX top features include BB Upper, BB Lower, MACD Signal, EMA20.
2. Low-VIX top features include BB Upper, ATR14, BB Lower, BB Width.


R2.6. Feature engineering reproducibility details insufficient
Reviewer comment:
Need precise formulas/parameters and leakage-safe conventions.

Response:
Accepted. We compiled a full feature specification table and clarified sequence construction assumptions.

Evidence:
1. results/feature_specification.csv
2. notebooks/NB-R01_clean_data_splits.ipynb
3. notebooks/NB-R10_results_compilation.ipynb


Reviewer 3

R3.1. Label leakage at split boundaries
Reviewer comment:
21-day labels near split boundaries can leak future split information.

Response:
Accepted. We trimmed final 21 trading days before split boundaries in upstream data construction.

Evidence:
1. data/processed/split_summary.csv
2. notebooks/NB-R01_clean_data_splits.ipynb

Current split counts:
1. Train: 1794
2. Validation: 273
3. Test: 276


R3.2. Threshold look-ahead bias
Response:
Addressed identically to R1.1/R2.1.

Evidence:
1. results/vix_threshold_config.json


R3.3. Overlapping outcomes and clustered dependence in statistics
Response:
Addressed identically to R1.2/R2.2 with non-overlap Fisher, block bootstrap, and block permutation tests.

Evidence:
1. results/table5_statistical_tests.csv


R3.4. Ablation studies required (components and self-attention contribution)
Reviewer comment:
Need component-level and no-attention ablation.

Response:
Accepted. We added full ablation grid including BiLSTM no-attention and trees-only stacking.

Evidence:
1. results/ablation_results.csv
2. plots/R08_ablation_accuracy.png
3. notebooks/NB-R08_ablation_studies.ipynb

Current highlights:
1. Trees-only stack slightly outperforms full stack on Low-VIX and Overall in this run.
2. BiLSTM with attention does not dominate no-attention in this split.

Narrative revision:
We now describe self-attention contribution as mixed and data-regime dependent.


R3.5. Literature recency and citation support
Reviewer comment:
Need more recent studies and stronger citation grounding.

Response:
Accepted. We are updating the literature section with recent volatility-regime forecasting papers and resolving citation metadata consistency in the final manuscript package.

Status:
Manuscript editorial pass item to finalize before resubmission.


R3.6. Regime-specific baselines and target-realization clarity
Reviewer comment:
Need regime-specific baselines and explicit target realization date.

Response:
Accepted.

Changes made:
1. Regime-specific baseline metrics are reported.
2. Target and execution timeline are explicitly stated in simulation protocol.

Evidence:
1. results/table4_regime_metrics.csv
2. results/baseline_comparison.csv
3. notebooks/NB-R09_corrected_trading_simulation.ipynb


Summary of substantive revision impact

1. Leakage and look-ahead corrections are implemented and documented.
2. Dependence-aware statistics are implemented; significance claims are now appropriately conservative.
3. Walk-forward analysis indicates limited cross-period generalization of High-VIX advantage.
4. Corrected trading simulation no longer supports Sharpe superiority versus buy-and-hold under tested costs.
5. Baselines, SHAP, and ablation outputs are fully reported; model-advantage claims are tempered accordingly.

We thank the Reviewers again for their guidance, which has materially improved the methodological rigor and transparency of the manuscript.

Sincerely,
Authors
