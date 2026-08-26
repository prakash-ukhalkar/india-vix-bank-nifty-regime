"""
Utility script (run once, then can be deleted): rewrites ONLY markdown cell source
in NB-R01..NB-R10 to give each notebook a professional, self-contained, GitHub-ready
front matter, section documentation, and footer. No code cell is modified, added,
removed, or reordered, and no code is executed -- existing outputs are left untouched.
"""
import nbformat as nbf
from pathlib import Path

NB_DIR = Path(__file__).parent

PIPELINE = [
    ("NB-R01_clean_data_splits.ipynb", "01", "Clean Data Splits (Leakage-Safe Train/Val/Test Construction)"),
    ("NB-R02_vix_threshold_recalibration.ipynb", "02", "India VIX Regime Threshold Recalibration"),
    ("NB-R03_model_retraining.ipynb", "03", "Stacking Ensemble Training (21-Day Horizon)"),
    ("NB-R04_block_bootstrap_stats.ipynb", "04", "Dependence-Aware Statistical Testing"),
    ("NB-R05_walkforward_generalizability.ipynb", "05", "Walk-Forward Generalizability Check"),
    ("NB-R06_baseline_comparison.ipynb", "06", "Regime-Stratified Baseline Comparison"),
    ("NB-R07_shap_regime_analysis.ipynb", "07", "SHAP Regime-Specific Feature Importance"),
    ("NB-R08_ablation_studies.ipynb", "08", "Ensemble Ablation Studies"),
    ("NB-R09_corrected_trading_simulation.ipynb", "09", "Deployable Trading Simulation"),
    ("NB-R10_results_compilation.ipynb", "10", "Results Compilation for Manuscript"),
]

def footer(stage_idx, produced, next_nb):
    nxt = f"**Next notebook:** `{next_nb}`" if next_nb else "**Next notebook:** none -- this is the final notebook in the pipeline."
    return (
        "---\n"
        "## Summary\n\n"
        f"**Pipeline stage:** {stage_idx} of 13 (see `notebooks/README.md` for the full pipeline map).\n\n"
        "**Artifacts produced by this notebook:**\n\n"
        + "\n".join(f"- `{p}`" for p in produced) + "\n\n"
        + nxt + "\n"
    )

# ---------------------------------------------------------------------------
# NB-R01
# ---------------------------------------------------------------------------
def update_r01(nb):
    nb.cells[0].source = (
        "# NB-R01 — Clean Data Splits (Leakage-Safe Train/Val/Test Construction)\n\n"
        "**Pipeline stage:** 1 of 13\n\n"
        "**Purpose.** Build the feature set and chronological train/validation/test splits used by every "
        "downstream notebook in this pipeline. This is the foundation notebook: every later result "
        "(model training, statistical tests, trading simulation) depends on the splits produced here "
        "being free of label leakage.\n\n"
        "**Why this matters.** The prediction target is a 21-trading-day-ahead direction label. "
        "A naive chronological split can leak information across split boundaries: an observation near "
        "the end of the training window can have its label computed from a price that falls inside the "
        "validation window, and likewise between validation and test. This notebook removes that leakage "
        "by trimming the last 21 trading days before each split boundary before computing labels, so no "
        "label in any split depends on a price observed in a later split.\n\n"
        "**Inputs:** `data/raw/market_data.csv` (Bank Nifty OHLCV), `data/raw/india_vix.csv` (India VIX).\n\n"
        "**Outputs:** `data/processed/train.csv`, `val.csv`, `test.csv`, `scaler.joblib`, "
        "`feature_cols.json`, `split_summary.csv`.\n\n"
        "**Method summary:**\n"
        "- 16 leakage-safe technical indicators computed causally (each value at date *t* uses only data "
        "up to and including *t*): MACD (12-26-9), EMA-20, RSI-14 (Wilder), Stochastic %K/%D, ROC-10, "
        "Bollinger Bands (20, 2σ), ATR-14 (Wilder), and 1/2/3/5-day log-return lags.\n"
        "- Forward direction labels at 1, 5, and 21 trading days.\n"
        "- Chronological split with the last 21 rows of each pre-boundary period trimmed to prevent "
        "label leakage across the split.\n"
        "- Feature scaling (`StandardScaler`) fit on the training split only, then applied to validation "
        "and test without refitting.\n"
    )
    nb.cells[11].source = (
        "## 4. Chronological Splits — Trimming Boundary Rows to Prevent Label Leakage\n\n"
        "The 21-day-ahead label for a row at date *t* is only well-defined once `close[t+21]` is known. "
        "For rows within the last 21 trading days of the training window, `close[t+21]` falls inside the "
        "validation window; the same issue occurs between validation and test. To keep every split's "
        "labels fully self-contained, the last `HORIZON=21` rows of the training and validation splits "
        "are dropped before saving.\n"
    )
    footer_produced = ["data/processed/train.csv", "data/processed/val.csv", "data/processed/test.csv",
                        "data/processed/scaler.joblib", "data/processed/feature_cols.json", "data/processed/split_summary.csv"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(1, footer_produced, "NB-R02_vix_threshold_recalibration.ipynb")))
    return nb

# ---------------------------------------------------------------------------
# NB-R02
# ---------------------------------------------------------------------------
def update_r02(nb):
    nb.cells[0].source = (
        "# NB-R02 — India VIX Regime Threshold Recalibration\n\n"
        "**Pipeline stage:** 2 of 13\n\n"
        "**Purpose.** Define the India VIX threshold that separates \"High-VIX\" from \"Low-VIX\" test days, "
        "using only information available before the test period begins, so the regime label could in "
        "principle be computed in real time.\n\n"
        "**Why this matters.** A regime threshold computed from the test period's own VIX distribution is "
        "not something a live deployment could know in advance -- it requires having already observed the "
        "full test window. This notebook instead calibrates the threshold from the train+validation VIX "
        "distribution only (a **pre-test-fixed** threshold), and reports two alternative, also pre-test, "
        "calibration methods (expanding window, rolling 252-day window) as sensitivity checks.\n\n"
        "**Inputs:** `data/processed/train.csv`, `val.csv`, `test.csv` (from NB-R01).\n\n"
        "**Outputs:** `data/processed/test_with_regimes.csv`, `results/vix_threshold_config.json`, "
        "`results/threshold_comparison.csv`, `plots/R02_vix_threshold_comparison.png`.\n\n"
        "**Result:** the primary fixed threshold is the 75th percentile of the train+validation India VIX "
        "distribution (18.71), which classifies 8 of the 256 aligned test days as High-VIX.\n"
    )
    footer_produced = ["data/processed/test_with_regimes.csv", "results/vix_threshold_config.json",
                        "results/threshold_comparison.csv", "plots/R02_vix_threshold_comparison.png"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(2, footer_produced, "NB-R03_model_retraining.ipynb")))
    return nb

# ---------------------------------------------------------------------------
# NB-R03
# ---------------------------------------------------------------------------
def update_r03(nb):
    nb.cells[0].source = (
        "# NB-R03 — Stacking Ensemble Training (21-Day Horizon)\n\n"
        "**Pipeline stage:** 3 of 13\n\n"
        "**Purpose.** Train the full two-level stacking ensemble on the clean, leakage-safe splits from "
        "NB-R01: four tree-based base learners (XGBoost, LightGBM, Random Forest, CatBoost) plus a BiLSTM "
        "with self-attention, combined by a ridge logistic-regression meta-learner trained on out-of-fold "
        "base-learner probabilities.\n\n"
        "**Inputs:** `data/processed/train.csv`, `val.csv`, `test_with_regimes.csv`, `feature_cols.json`.\n\n"
        "**Outputs:** `models/xgb_model.joblib`, `lgb_model.joblib`, `rf_model.joblib`, `cb_model.joblib`, "
        "`bilstm_best.pt`, `meta_learner.joblib`, `results/hyperparameter_table.csv`, "
        "`results/all_best_params.json`, `data/processed/test_predictions.csv`.\n\n"
        "**Method summary:**\n"
        "- Each tree-based learner is tuned with Optuna (TPE sampler, 100 trials) against 5-fold "
        "`TimeSeriesSplit` cross-validated log-loss -- never against random shuffles, which would break "
        "temporal ordering.\n"
        "- The BiLSTM (hidden size 64, dropout 0.2) is trained on rolling 20-day sequences with early "
        "stopping on validation log-loss.\n"
        "- Base-learner out-of-fold probabilities (never the in-sample-fit probabilities) are stacked as "
        "input features to the ridge meta-learner, preventing the meta-learner from learning off overfit "
        "predictions.\n\n"
        "**Note on later horizons:** this notebook covers only the 21-day target. The equivalent 1-day and "
        "5-day models (added in the second major-revision round) are trained in NB-R13.\n"
    )
    footer_produced = ["models/xgb_model.joblib", "models/lgb_model.joblib", "models/rf_model.joblib",
                        "models/cb_model.joblib", "models/bilstm_best.pt", "models/meta_learner.joblib",
                        "results/hyperparameter_table.csv", "results/all_best_params.json",
                        "data/processed/test_predictions.csv"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(3, footer_produced, "NB-R04_block_bootstrap_stats.ipynb")))
    return nb

# ---------------------------------------------------------------------------
# NB-R04
# ---------------------------------------------------------------------------
def update_r04(nb):
    nb.cells[0].source = (
        "# NB-R04 — Dependence-Aware Statistical Testing\n\n"
        "**Pipeline stage:** 4 of 13\n\n"
        "**Purpose.** Test whether the High-VIX vs Low-VIX accuracy difference is statistically "
        "distinguishable from chance, using inference procedures that account for the serial correlation "
        "induced by the 21-day-ahead forecast horizon.\n\n"
        "**Why this matters.** Because the target is a 21-day-ahead label, consecutive daily observations "
        "share up to 20 overlapping future days, which violates the independence assumption behind a "
        "standard Fisher's exact test and inflates apparent significance. This notebook instead reports: "
        "(a) Fisher's exact test on a non-overlapping subsample (every 21st observation), (b) a circular "
        "block-bootstrap confidence interval for the accuracy difference (block length 21), and (c) a "
        "block-permutation test, all with Bonferroni correction across the three forecast horizons tested "
        "in this study.\n\n"
        "**Inputs:** `data/processed/test_predictions.csv` (from NB-R03).\n\n"
        "**Outputs:** `results/table4_regime_metrics.csv`, `results/table5_statistical_tests.csv`, "
        "`results/statistical_tests.json`, `plots/R04_statistical_tests.png`.\n\n"
        "**Result:** a 33.5-percentage-point observed accuracy gap (100.0% High-VIX vs 66.5% Low-VIX), "
        "but neither the non-overlapping Fisher test nor the block-permutation test rejects the null "
        "hypothesis after Bonferroni correction (both p = 1.000).\n"
    )
    footer_produced = ["results/table4_regime_metrics.csv", "results/table5_statistical_tests.csv",
                        "results/statistical_tests.json", "plots/R04_statistical_tests.png"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(4, footer_produced, "NB-R05_walkforward_generalizability.ipynb")))
    return nb

# ---------------------------------------------------------------------------
# NB-R05
# ---------------------------------------------------------------------------
def update_r05(nb):
    nb.cells[0].source = (
        "# NB-R05 — Walk-Forward Generalizability Check\n\n"
        "**Pipeline stage:** 5 of 13\n\n"
        "**Purpose.** Test whether the High-VIX regime effect observed in the primary test window "
        "(2025-2026) generalizes across other years, or whether it is specific to the single stress "
        "episode contained in that window.\n\n"
        "**Why this matters.** Every High-VIX observation in the primary test set falls within one "
        "concentrated volatility episode. A single episode cannot distinguish a genuine, repeatable "
        "regime effect from an artifact of that particular episode's other characteristics. This notebook "
        "runs an annual walk-forward evaluation: for each year *Y*, a model is trained on all data up to "
        "*Y* and evaluated on year *Y*+1, with the regime threshold recalibrated from the corresponding "
        "pre-test window at each step.\n\n"
        "**Inputs:** `data/raw/market_data.csv`, `data/raw/india_vix.csv`.\n\n"
        "**Outputs:** `results/walkforward_results.csv`, `plots/R05_walkforward_regime_accuracy.png`.\n\n"
        "**Result:** across six independently evaluated years (2019, 2020, 2021, 2022, 2024, 2025), the "
        "High-VIX accuracy advantage holds in only one (2021, +12.4 pp) and reverses in the other five "
        "(-11.6 to -39.3 pp). This is the single most important robustness result in the study: it "
        "indicates the primary-sample finding is concentrated in, and likely specific to, the one "
        "evaluated stress episode rather than reflecting a general, repeatable regime effect.\n"
    )
    footer_produced = ["results/walkforward_results.csv", "plots/R05_walkforward_regime_accuracy.png"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(5, footer_produced, "NB-R06_baseline_comparison.ipynb")))
    return nb

# ---------------------------------------------------------------------------
# NB-R06
# ---------------------------------------------------------------------------
def update_r06(nb):
    nb.cells[0].source = (
        "# NB-R06 — Regime-Stratified Baseline Comparison\n\n"
        "**Pipeline stage:** 6 of 13\n\n"
        "**Purpose.** Establish whether the stacking ensemble's complexity is justified by comparing it, "
        "under the identical High-VIX/Low-VIX split, against simple baselines: a majority-class rule, a "
        "naive persistence rule, logistic regression, and a single (untuned-stack) XGBoost model.\n\n"
        "**Why this matters.** A high accuracy number within a small, class-imbalanced subset (the "
        "High-VIX regime has only 8 observations, all realizing the same outcome) can look impressive "
        "without reflecting any real skill above a trivial rule. Reporting the same regime split's "
        "majority-class baseline alongside every model's accuracy makes that distinction explicit.\n\n"
        "**Inputs:** `data/processed/test_with_regimes.csv`, trained base models from NB-R03.\n\n"
        "**Outputs:** `results/baseline_comparison.csv`, `plots/R06_baseline_comparison.png`.\n\n"
        "**Result:** on the High-VIX subset every model that predicts \"Up\" matches the 100% majority "
        "baseline trivially (n=8, single class). On the Low-VIX subset, the stacking ensemble (66.5%) "
        "beats every individual baseline tested but still falls short of that subset's own 70.2% majority "
        "baseline.\n"
    )
    footer_produced = ["results/baseline_comparison.csv", "plots/R06_baseline_comparison.png"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(6, footer_produced, "NB-R07_shap_regime_analysis.ipynb")))
    return nb

# ---------------------------------------------------------------------------
# NB-R07
# ---------------------------------------------------------------------------
def update_r07(nb):
    nb.cells[0].source = (
        "# NB-R07 — SHAP Regime-Specific Feature Importance\n\n"
        "**Pipeline stage:** 7 of 13\n\n"
        "**Purpose.** Quantify which engineered features drive the XGBoost base learner's predictions, "
        "separately within the High-VIX and Low-VIX subsets, using SHAP (SHapley Additive exPlanations) "
        "values rather than a qualitative description.\n\n"
        "**Inputs:** `data/processed/test_with_regimes.csv`, `models/xgb_model.joblib`.\n\n"
        "**Outputs:** `results/shap_importance_High_VIX.csv`, `shap_importance_Low_VIX.csv`, "
        "`shap_importance_Overall.csv`, `shap_regime_shift.csv`, `plots/R07_shap_beeswarm_high_vix.png`, "
        "`plots/R07_shap_regime_comparison.png`.\n\n"
        "**Result:** `bb_upper` (Bollinger upper band) is the dominant feature in both regimes. Beyond "
        "that, the regime shift is feature-specific rather than a uniform amplification of "
        "volatility-sensitive indicators: `macd_signal`, `ema20`, and `macd` become relatively more "
        "important in the High-VIX subset, while `atr14` and `bb_width` -- the two features most directly "
        "built to measure realized dispersion -- become markedly *less* important there than in the "
        "Low-VIX subset. All High-VIX-subset SHAP values are computed on only 8 observations and should "
        "be read with that caveat.\n"
    )
    footer_produced = ["results/shap_importance_High_VIX.csv", "results/shap_importance_Low_VIX.csv",
                        "results/shap_importance_Overall.csv", "results/shap_regime_shift.csv",
                        "plots/R07_shap_beeswarm_high_vix.png", "plots/R07_shap_regime_comparison.png"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(7, footer_produced, "NB-R08_ablation_studies.ipynb")))
    return nb

# ---------------------------------------------------------------------------
# NB-R08
# ---------------------------------------------------------------------------
def update_r08(nb):
    nb.cells[0].source = (
        "# NB-R08 — Ensemble Ablation Studies\n\n"
        "**Pipeline stage:** 8 of 13\n\n"
        "**Purpose.** Isolate the contribution of each ensemble component by evaluating: every base "
        "learner individually (XGBoost, LightGBM, Random Forest, CatBoost, BiLSTM+Attention), a BiLSTM "
        "variant without the self-attention mechanism, a trees-only stack (no BiLSTM), and the full "
        "five-model stack -- all under the identical regime split.\n\n"
        "**Why this matters.** A stacking ensemble is only justified if it outperforms its components; "
        "an ablation table is also the only way to check whether a specific architectural choice (here, "
        "self-attention in the BiLSTM) actually earns its complexity.\n\n"
        "**Inputs:** `data/processed/test_with_regimes.csv`, all trained base models from NB-R03.\n\n"
        "**Outputs:** `results/ablation_results.csv`, `plots/R08_ablation_accuracy.png`.\n\n"
        "**Result:** every individual base learner underperforms the Low-VIX majority baseline, while "
        "both stacked configurations exceed it -- stacking clearly adds value over any single model. "
        "Less expected: the full five-model stack (including the BiLSTM with self-attention) slightly "
        "*underperforms* the trees-only stack on both Low-VIX (64.9% vs 66.7%) and overall accuracy "
        "(66.1% vs 67.8%), which does not support a claim that self-attention adds predictive value in "
        "this sample.\n"
    )
    footer_produced = ["results/ablation_results.csv", "plots/R08_ablation_accuracy.png"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(8, footer_produced, "NB-R09_corrected_trading_simulation.ipynb")))
    return nb

# ---------------------------------------------------------------------------
# NB-R09
# ---------------------------------------------------------------------------
def update_r09(nb):
    nb.cells[0].source = (
        "# NB-R09 — Deployable Trading Simulation\n\n"
        "**Pipeline stage:** 9 of 13\n\n"
        "**Purpose.** Translate the regime-conditioned prediction into a fully specified, deployable "
        "trading rule (\"go long when the regime is High-VIX and the model predicts Up\"), and evaluate "
        "its risk-adjusted performance against buy-and-hold across a range of transaction-cost "
        "assumptions.\n\n"
        "**Execution protocol (stated explicitly so it is fully reproducible):** signal computed from all "
        "features available after market close on day *t*; entry at the open on day *t*+1; exit at the "
        "close on day *t*+21; at most one open position at a time (no pyramiding, no overlapping trades).\n\n"
        "**Sharpe-ratio convention (stated explicitly):** annual risk-free rate 6.5% (India 91-day T-bill, "
        "RBI FY2025 average), daily RFR = 6.5%/252, annualized Sharpe = (mean daily excess return / std "
        "daily excess return) x sqrt(252), computed identically for the strategy and buy-and-hold series.\n\n"
        "**Inputs:** `data/processed/test_predictions.csv`, `data/raw/market_data.csv`.\n\n"
        "**Outputs:** `results/trading_simulation.csv`, `plots/R09_trading_simulation.png`.\n\n"
        "**Result:** under the corrected protocol, the strategy trades exactly once in the evaluated "
        "window (21 active days of 256). It achieves a lower maximum drawdown than buy-and-hold (-3.69% "
        "vs -6.62%) but does not exceed buy-and-hold Sharpe at any tested transaction-cost level (0.455 "
        "vs 1.204 at 0 bps, declining to 0.375 vs 1.204 at 50 bps round-trip).\n"
    )
    footer_produced = ["results/trading_simulation.csv", "plots/R09_trading_simulation.png"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(9, footer_produced, "NB-R10_results_compilation.ipynb")))
    return nb

# ---------------------------------------------------------------------------
# NB-R10
# ---------------------------------------------------------------------------
def update_r10(nb):
    nb.cells[0].source = (
        "# NB-R10 — Results Compilation for Manuscript\n\n"
        "**Pipeline stage:** 10 of 13\n\n"
        "**Purpose.** Collect the outputs of NB-R01 through NB-R09 into the manuscript-ready tables used "
        "in the paper, and produce a single revision-tracking file cross-referencing each addressed review "
        "comment to the notebook that resolves it.\n\n"
        "**Inputs:** all `results/*.csv` and `results/*.json` files produced by NB-R01 through NB-R09.\n\n"
        "**Outputs:** consolidated manuscript tables (splits, feature specification, hyperparameters, "
        "regime metrics, statistical tests, trading simulation) and `results/revision_tracker.csv`.\n\n"
        "**Note:** this notebook closes out the first major-revision round. The second round's additions "
        "(GARCH comparison, extended threshold sensitivity, 1-day/5-day model retraining, and figure "
        "regeneration) are covered by NB-R11 through NB-R13.\n"
    )
    footer_produced = ["results/revision_tracker.csv", "consolidated manuscript tables (see results/)"]
    nb.cells.append(nbf.v4.new_markdown_cell(footer(10, footer_produced, "NB-R11_garch_and_threshold_extras.ipynb")))
    return nb

UPDATERS = {
    "NB-R01_clean_data_splits.ipynb": update_r01,
    "NB-R02_vix_threshold_recalibration.ipynb": update_r02,
    "NB-R03_model_retraining.ipynb": update_r03,
    "NB-R04_block_bootstrap_stats.ipynb": update_r04,
    "NB-R05_walkforward_generalizability.ipynb": update_r05,
    "NB-R06_baseline_comparison.ipynb": update_r06,
    "NB-R07_shap_regime_analysis.ipynb": update_r07,
    "NB-R08_ablation_studies.ipynb": update_r08,
    "NB-R09_corrected_trading_simulation.ipynb": update_r09,
    "NB-R10_results_compilation.ipynb": update_r10,
}

for fname, fn in UPDATERS.items():
    path = NB_DIR / fname
    nb = nbf.read(path, as_version=4)
    before_code_cells = [c.source for c in nb.cells if c.cell_type == "code"]
    nb = fn(nb)
    after_code_cells = [c.source for c in nb.cells if c.cell_type == "code"]
    assert before_code_cells == after_code_cells, f"CODE CELLS CHANGED in {fname}!"
    nbf.write(nb, path)
    print(f"Updated {fname}")

print("Done.")
