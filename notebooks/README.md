# Notebooks — India VIX Regime Filter for Bank Nifty Directional Prediction

This directory contains the full, reproducible analysis pipeline behind the paper
*"India VIX as a Regime Filter for Bank Nifty Directional Prediction: A Leakage-Safe
Reliability Assessment"* (Neural Computing and Applications, manuscript
NCAA-D-26-02775). The notebooks are numbered in the order they must be run — each
depends on artifacts (`data/processed/`, `models/`, `results/`) produced by the ones
before it.

## Pipeline map

| # | Notebook | Purpose |
|---|---|---|
| 01 | `NB-R01_clean_data_splits.ipynb` | Feature engineering (16 leakage-safe technical indicators) and leakage-safe chronological train/validation/test splits |
| 02 | `NB-R02_vix_threshold_recalibration.ipynb` | Pre-test-fixed India VIX regime threshold (no look-ahead bias) |
| 03 | `NB-R03_model_retraining.ipynb` | Train the 21-day stacking ensemble (XGBoost, LightGBM, Random Forest, CatBoost, BiLSTM+self-attention, ridge meta-learner) |
| 04 | `NB-R04_block_bootstrap_stats.ipynb` | Dependence-aware significance testing (non-overlapping Fisher, block bootstrap, block permutation) |
| 05 | `NB-R05_walkforward_generalizability.ipynb` | Annual walk-forward validation across independent years |
| 06 | `NB-R06_baseline_comparison.ipynb` | Regime-stratified comparison against simple baselines |
| 07 | `NB-R07_shap_regime_analysis.ipynb` | SHAP feature importance, computed separately per regime |
| 08 | `NB-R08_ablation_studies.ipynb` | Per-component ablation of the stacking ensemble |
| 09 | `NB-R09_corrected_trading_simulation.ipynb` | Deployable trading-rule simulation with explicit execution and Sharpe conventions |
| 10 | `NB-R10_results_compilation.ipynb` | Compile all outputs into manuscript-ready tables |
| 11 | `NB-R11_garch_and_threshold_extras.ipynb` | GARCH(1,1) regime comparison; extended threshold sensitivity |
| 12 | `NB-R12_regenerate_figures.ipynb` | Regenerate manuscript figures directly from corrected result files |
| 13 | `NB-R13_train_1d_5d_models.ipynb` | Train real 1-day and 5-day stacking ensembles (same methodology as NB-R03) |

Notebooks 01–10 correspond to the first major-revision round; 11–13 were added in the
second round in direct response to reviewer comments (see `Manuscript/` for the full
review correspondence).

## Reproducing the pipeline

1. Install dependencies from `requirements.txt`, plus `arch`, `optuna`, `catboost`,
   `torch`, and `statsmodels` (used by NB-R11 and NB-R13; not all are needed for
   every notebook — see each notebook's header for its specific requirements).
2. Run the notebooks in numeric order. Each notebook's header states its exact
   inputs and outputs, and its footer states which notebook to run next.
3. All raw data (`data/raw/india_vix.csv`, `data/raw/market_data.csv`) is derived
   from NSE's public historical data downloads (see the manuscript's Data
   Availability statement for URLs).

## `imported_reference/`

This subdirectory contains **read-only reference copies** of notebooks from a
related sibling project, consulted while verifying a claimed cross-pipeline
replication result during the second revision round. They are not part of this
paper's pipeline, are not run by anything here, and are kept only for audit-trail
transparency (see NB-R11's markdown for context on why that replication claim was
ultimately not used).

## Notes on reproducibility

- Every notebook's markdown documents its exact inputs, outputs, and (where
  relevant) the specific reviewer concern it addresses.
- NB-R12 has one known, explicitly documented limitation: two of its figures use
  placeholder 1-day/5-day values that predate NB-R13's retraining. See NB-R12's
  markdown for the exact fix needed if you rerun it after NB-R13.
- Optuna trial counts differ between the 21-day model (NB-R03: 100 trials/model)
  and the 1-day/5-day models (NB-R13: 25 trials/model) for compute-time reasons;
  this is stated in both notebooks and in the manuscript.
