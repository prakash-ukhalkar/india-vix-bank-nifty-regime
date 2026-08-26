# COMMENTS FOR THE AUTHOR

## Reviewer #1

In this study, the authors propose a two-level stacking ensemble model based on XGBoost, LightGBM, Random Forest, CatBoost, and BiLSTM to predict the direction of the Bank Nifty index and to examine the extent to which the model's outputs become reliable under the India VIX regime. The main claim of the study is that, despite the limited overall test performance of the model, it produces significantly higher accuracy in the High-VIX regime over a 21-day trading horizon, and that this finding, when translated to a selective long-only trading strategy, offers a more advantageous decision support filter in terms of Sharpe ratio and maximum decline. The article is current in its subject matter, interesting from a decision-support system perspective, and has the potential to contribute to the literature by focusing not only on raw prediction success but also on the market conditions under which the model can be used. However, in its current form, some methodological and reporting points directly affect the strength of the results and require revision.

1. Calculating the High-VIX threshold (15.08) directly from the distribution of the test itself is a methodological error (p75). A real-time (live deployment) system cannot access the previously unknown distribution of test data. This threshold should be calibrated using rolling or expanding window methods based on historical training/validation data.
2. Due to the 21-day forecast horizon, consecutive daily observations overlap significantly. This leads to strong serial correlation in the data, artificially inflating the p-values from Fisher's exact test, bootstrap confidence intervals, and accuracy differences. The authors should use non-overlapping sampling, block bootstraps, or Newey-West/HAC correction.
3. As acknowledged in the report, all 58 High-VIX days are clustered during the budget and US tariff shock period in the first half of 2025. This makes it unclear whether the model's success stems from a general regime-based phenomenon or from this specific market event. Cross-validation or walk-forward tests covering independent High-VIX periods from different years should be added to ensure the reliability of the results.
4. Table 9 in Section 6.1 clearly shows that the Sharpe ratio of the High-VIX + Up strategy drops to 1.936 under a 50-bps round-trip transaction cost, falling below the buy-and-hold benchmark (1.963). However, the text claims the strategy remains above the benchmark at every cost level. This factual error should be corrected, and it should be stated that the Sharpe advantage disappears at a 50-bps cost.
5. The decision support model states that the India VIX and Bank Nifty closing prices are traded simultaneously. Generating a trading signal before the closing prices are finalized creates look-ahead bias. The exact minute the signal is generated, whether execution is based on the next day's opening or the same day's closing, and how overlapping signals are managed in the portfolio should be clarified.
6. In the test set, the unconditioned model's success (61.01%) is significantly lower than the naive majority baseline (68.95%) due to the strong bullish trend. To assess the quality of the high success rate of 84.5% in the high-VIX regime, the majority rate in this subset, along with the model's precision and recall values, should be presented as class-stratified metrics. Otherwise, it is unclear whether the success is due to directional predictive power or a local class imbalance.
7. The final parameter sets, time series cross-validation fold structures, and chronological details of out-of-fold probability generation for Optuna-based hyperparameter optimization are missing. Furthermore, the reference list contains completely incorrect or irrelevant DOI addresses for critical sources such as Hamilton (1989) and Lundberg & Lee (2017). These academic shortcomings should be addressed.

## Reviewer #2

Comment 1: Contemporaneous Regime Threshold Creates Look-Ahead Bias. The regime definition uses the 75th percentile of the test-period India VIX distribution to partition predictions, creating a subtle look-ahead bias. The threshold is calibrated using information from the entire test window (including future observations) before evaluating performance on that same window. In real deployment, the threshold would need to be known in advance.

Comment 2: Temporal Concentration of High-VIX Events Limits Generalizability. The 58 High-VIX test days are concentrated within a single sustained elevated-volatility episode spanning 2025 Q1-Q2. The bootstrap confidence interval assumes independence of observations, which is violated when High-VIX days cluster temporally. A single stress episode may have unique characteristics that do not replicate across other high-volatility periods.

Comment 3: Missing Comparative Benchmark Against Simpler Models. The paper reports 84.5% accuracy in High-VIX for the stacking ensemble but does not compare against simpler baseline models under the same regime filter. It is unclear whether the ensemble's complexity is justified, or whether a simple directional persistence rule or logistic regression would achieve similar performance.

Comment 4: Inconsistent Sharpe Ratio Calculation Details. The risk-free rate assumption and annualization method for Sharpe ratio calculations are not stated. This makes it difficult to verify whether the Sharpe comparison across strategies (buy-and-hold vs. selective strategy) is consistent and appropriate.

Comment 5: Absence of Feature Importance Analysis for Regime-Specific Prediction. The paper claims that volatility-sensitive features (Bollinger width, ATR-14, MACD dispersion) drive the regime effect, but provides no direct feature importance evidence. SHAP analysis is described qualitatively, but actual SHAP values or feature rankings are not presented.

Comment 6: Insufficient Feature Engineering Details Compromise Reproducibility. The paper emphasizes features are "leakage-safe," but several technical details needed for reproducibility are missing:

- MACD parameterization (12-26-9 standard?) and whether EMAs use data only up to t
- Log-return lag calculation convention: log(P_t / P_{t-k}) or log(P_{t-k+1} / P_{t-k})
- Bollinger Band window length and MA type (simple or exponential)
- Stochastic oscillator lookback period (%K and %D typically 14 days)
- BiLSTM sequence overlap and potential leakage between training/validation/test sequences

I recommend you strengthen the literature such as GATE-GNN, EATSA-GNN, PIMPC-GNN

## Reviewer #3

The manuscript addresses a relevant financial forecasting problem. The use of real market data and several robustness checks are important strengths. However, the below needs to be considered to improve the paper:

- The model predicts whether the price will rise 21 trading days later. Therefore, an observation near the end of the training period may use a future price that falls inside the validation period to create its label. The same issue may occur between the validation and test periods, which means information from the next dataset could influence the earlier dataset. You should remove the final 21 trading days before each data split and rerun the analysis to prevent possible data leakage.
- You have calculated the High-VIX threshold from the full test period, which would not be available during real-time deployment. This needs to be addressed to ensure this work has practical use.
- Moreover, your statistical analysis needs to adequately account for the overlapping 21-day outcomes, especially as the High-VIX observations are concentrated within one volatility episode.
- I feel the approach in this paper has combined different things to achieve a complex model just to tick the box of a scientifically rigorous work. To ensure this is not the case, ablation studies are needed to show the contributions of all the components of the stacked ensemble, including the self-attention of the BiLSTM. Also, it is not clear how the parameters of each component model were decided - there should be table to make this transparent to support reproducibility.
- Several references are old. The literature review should be updated with more recent studies on volatility-regime forecasting. And references were used sparingly, in some cases, to support statements that should be evidenced by authoritative sources.
- Also, you should report regime-specific baselines and metrics and clarify the final target-realisation date.
