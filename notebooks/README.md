# Notebooks — India VIX Regime Filter for Bank Nifty Directional Prediction

This directory contains the full, reproducible analysis pipeline behind a study of
whether India VIX conditions the directional predictability of Bank Nifty, using a
stacking ensemble and a leakage-safe, dependence-aware evaluation protocol. The
notebooks are numbered in the order they must be run — each depends on artifacts
(`data/processed/`, `models/`, `results/`) produced by the ones before it.

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
| 09 | `NB-R09_trading_simulation.ipynb` | Deployable trading-rule simulation with explicit execution and Sharpe conventions |
| 10 | `NB-R10_results_compilation.ipynb` | Compile all outputs into summary tables |
| 11 | `NB-R11_garch_and_threshold_extras.ipynb` | GARCH(1,1) regime comparison; extended threshold sensitivity |
| 12 | `NB-R12_train_1d_5d_models.ipynb` | Train real 1-day and 5-day stacking ensembles (same methodology as NB-R03) |
| 13 | `NB-R13_regenerate_figures.ipynb` | Regenerate figures directly from pipeline result files (depends on NB-R12's output) |

## Reproducing the pipeline

1. Install dependencies from `requirements.txt`, plus `arch`, `optuna`, `catboost`,
   `torch`, and `statsmodels` (used by NB-R11 and NB-R12; not all are needed for
   every notebook — see each notebook's header for its specific requirements).
2. Run the notebooks in numeric order from within the `notebooks/` directory (each
   notebook resolves the repository root as `Path('..').resolve()`, so the working
   directory must be `notebooks/` when you run them — this is the default when you
   open a notebook file located there). Each notebook's header states its exact
   inputs and outputs, and its footer states which notebook to run next.
3. All raw data (`data/raw/india_vix.csv`, `data/raw/market_data.csv`) is derived
   from NSE's public historical data downloads (India VIX and NIFTY BANK OHLCV,
   both freely available for direct CSV download without registration).

## `imported_reference/`

This subdirectory contains **read-only reference copies** of notebooks from a
related project, consulted while checking a candidate independent-replication
comparison (see NB-R11's markdown for context on why that comparison was not
included). They are not part of this pipeline and are not run by anything here —
kept only for audit-trail transparency.

## Notes on reproducibility

- Every notebook's markdown documents its exact inputs, outputs, and the specific
  methodological issue it addresses, where relevant.
- NB-R13 depends on NB-R12's output: its regime-accuracy and AUC figures load the
  1-day/5-day results directly from `results/horizon_1d_5d_results.csv`
  and `data/processed/test_predictions_{1d,5d}.csv` rather than using hardcoded
  values, so run NB-R12 before NB-R13 (or before rerunning NB-R13) if those files
  don't yet exist.
- Optuna trial counts differ between the 21-day model (NB-R03: 100 trials/model)
  and the 1-day/5-day models (NB-R12: 25 trials/model) for compute-time reasons;
  this is stated explicitly in both notebooks.
- NB-R01 through NB-R10 are saved with cleared outputs (unexecuted) so the
  repository does not carry stale printed results or machine-specific paths from
  prior runs; re-run them to reproduce all numbers locally.
