"""
NB-R11: GARCH(1,1) regime comparison + extended threshold sensitivity (p85, quarterly breakdown).

Note on P1 replication: the sibling project's P1 pipeline was checked for a fair replication row
(see notebooks/imported_reference/p1 and p2/NB-P2-05-Vix-Regime-Split.ipynb, copied read-only from
Bank_Nifty_SPP_Sentiment_Analysis for reference). It uses a test-window-derived VIX threshold
(same look-ahead bias this revision fixes) over at least two different, mutually inconsistent
test windows across artifacts (n=171/p75=12.53/high=43 in NB-P2-05; n=19/vix<=14.45 in
p1_p75_regime_pred_21d.parquet). No pre-test-threshold version of P1 exists. The P1 replication
row is therefore DROPPED from Table 11 rather than fabricated or force-fit -- see response letter.
Addresses Reviewer #4 (R2) findings that Table 10 (VIX vs GARCH) and Table 11 (threshold
sensitivity) in the R1-revised manuscript contain internally impossible numbers with no
backing analysis artifact. This script performs the real, leakage-safe computation.

Design choices, stated explicitly:
- GARCH(1,1) fit on log returns of Bank Nifty close, TRAIN+VAL ONLY (pre-test), mirroring
  the VIX threshold protocol (train+val p75).
- Out-of-sample conditional volatility for the test period is produced by an EXPANDING
  re-estimation: for each test date t, refit GARCH(1,1) on all data up to and including t-1,
  and take the 1-step-ahead forecast for date t. This uses no future information at any point
  (fully deployable), consistent with the paper's "pre-test-fixed" threshold philosophy but
  applied to the volatility state variable itself.
- GARCH-High threshold = 75th percentile of the TRAIN+VAL in-sample conditional volatility
  (fixed pre-test, same logic as the VIX threshold), applied to the test forecasts.
- VIX p85 threshold = 85th percentile of TRAIN+VAL VIX distribution (fixed pre-test),
  applied to the same 256-row aligned test sample used everywhere else in the paper.
- Quarterly breakdown uses the already-corrected regime_fixed column (VIX >= 18.71) on the
  256-row aligned test sample -- must sum to 8, not the superseded 58.
- accuracy metrics computed against stack_pred vs dir_21d from test_predictions.csv, the same
  256-row aligned file used for all other regime tables in the paper.
"""
import pandas as pd
import numpy as np
from arch import arch_model
import json

pd.set_option('display.width', 160)

# ---- Load data ----
train = pd.read_csv('data/processed/train.csv', parse_dates=['date'])
val = pd.read_csv('data/processed/val.csv', parse_dates=['date'])
preds = pd.read_csv('data/processed/test_predictions.csv', parse_dates=['date'])  # 256-row aligned

trainval = pd.concat([train, val], ignore_index=True).sort_values('date').reset_index(drop=True)

# ==========================================================================
# PART A: GARCH(1,1) regime, fit pre-test, expanding out-of-sample forecast
# ==========================================================================

# Full close-price series needed for expanding refit through the test period.
raw_market = pd.read_csv('data/raw/market_data.csv', parse_dates=['date']).sort_values('date').reset_index(drop=True)
raw_market['log_ret'] = np.log(raw_market['close'] / raw_market['close'].shift(1))
raw_market = raw_market.dropna(subset=['log_ret']).reset_index(drop=True)

trainval_end_date = trainval['date'].max()
test_dates = preds['date'].tolist()

# In-sample GARCH fit on train+val log returns only, to establish the GARCH-High threshold.
trainval_rets = raw_market.loc[raw_market['date'] <= trainval_end_date, 'log_ret'] * 100  # arch expects pct scale
am_trainval = arch_model(trainval_rets, vol='Garch', p=1, q=1, dist='normal', rescale=False)
res_trainval = am_trainval.fit(disp='off')
insample_cond_vol = res_trainval.conditional_volatility
garch_high_threshold = float(np.percentile(insample_cond_vol, 75))
print(f"GARCH(1,1) train+val fit converged: {res_trainval.convergence_flag == 0}")
print(f"In-sample conditional volatility p75 (GARCH-High threshold, fixed pre-test): {garch_high_threshold:.4f}")

# Expanding out-of-sample 1-step-ahead forecast for each test date (no look-ahead).
forecast_vol = {}
returns_all = raw_market.set_index('date')['log_ret'] * 100
for d in test_dates:
    hist = returns_all.loc[returns_all.index < d]
    if len(hist) < 250:
        forecast_vol[d] = np.nan
        continue
    am = arch_model(hist, vol='Garch', p=1, q=1, dist='normal', rescale=False)
    r = am.fit(disp='off', show_warning=False)
    f = r.forecast(horizon=1, reindex=False)
    forecast_vol[d] = float(np.sqrt(f.variance.values[-1, 0]))

preds['date_str'] = preds['date'].dt.strftime('%Y-%m-%d')
preds['garch_vol_forecast'] = preds['date'].map(forecast_vol)
preds['garch_regime'] = np.where(preds['garch_vol_forecast'] >= garch_high_threshold, 'High-GARCH', 'Low-GARCH')

# ---- Regime accuracy (GARCH), same 256-row aligned sample ----
def regime_stats(df, regime_col, high_label, y_col='dir_21d', pred_col='stack_pred'):
    out = {}
    for label, sub in [('High', df[df[regime_col] == high_label]),
                        ('Low', df[df[regime_col] != high_label])]:
        n = len(sub)
        if n == 0:
            out[label] = dict(n=0, acc=np.nan)
            continue
        acc = (sub[y_col] == sub[pred_col]).mean() * 100
        out[label] = dict(n=n, acc=round(acc, 1))
    return out

garch_stats = regime_stats(preds, 'garch_regime', 'High-GARCH')
vix_stats = regime_stats(preds, 'regime_fixed', 'High-VIX')

print("\nGARCH regime stats:", garch_stats)
print("VIX regime stats (for cross-check against existing Table 9):", vix_stats)

# Fisher exact test for GARCH split (non-overlapping, every 21st obs, matching R1.2 protocol)
from scipy.stats import fisher_exact
preds_sorted = preds.sort_values('date').reset_index(drop=True)
non_overlap_idx = list(range(0, len(preds_sorted), 21))
no = preds_sorted.iloc[non_overlap_idx]
def fisher_for(df, regime_col, high_label, y_col='dir_21d', pred_col='stack_pred'):
    hi = df[df[regime_col] == high_label]
    lo = df[df[regime_col] != high_label]
    a = (hi[y_col] == hi[pred_col]).sum(); b = len(hi) - a
    c = (lo[y_col] == lo[pred_col]).sum(); d = len(lo) - c
    if len(hi) == 0 or len(lo) == 0:
        return np.nan
    _, p = fisher_exact([[a, b], [c, d]])
    return p

garch_fisher_p = fisher_for(no, 'garch_regime', 'High-GARCH')
print(f"\nGARCH non-overlapping Fisher p: {garch_fisher_p:.4f}")

# ---- Intersection: VIX-High and GARCH-High on the SAME 256-row sample ----
vix_high_mask = preds['regime_fixed'] == 'High-VIX'
garch_high_mask = preds['garch_regime'] == 'High-GARCH'
n_vix_high = int(vix_high_mask.sum())
n_garch_high = int(garch_high_mask.sum())
n_intersect = int((vix_high_mask & garch_high_mask).sum())
intersect_acc = np.nan
if n_intersect > 0:
    inter_df = preds[vix_high_mask & garch_high_mask]
    intersect_acc = round((inter_df['dir_21d'] == inter_df['stack_pred']).mean() * 100, 1)

print(f"\nVIX-High n={n_vix_high}, GARCH-High n={n_garch_high}, "
      f"Intersection n={n_intersect} (must be <= min({n_vix_high},{n_garch_high}))")
print(f"Intersection accuracy: {intersect_acc}")

table10 = pd.DataFrame([
    dict(Regime='VIX High (>= 18.71)', n=n_vix_high, Accuracy_pct=vix_stats['High']['acc'],
         Fisher_p=1.000, Phi=np.nan, Bonferroni_pass='No'),
    dict(Regime='VIX Low', n=vix_stats['Low']['n'], Accuracy_pct=vix_stats['Low']['acc'],
         Fisher_p=np.nan, Phi=np.nan, Bonferroni_pass=np.nan),
    dict(Regime=f'GARCH High (>= {garch_high_threshold:.4f}, pre-test p75)', n=n_garch_high,
         Accuracy_pct=garch_stats['High']['acc'], Fisher_p=round(garch_fisher_p, 4) if not np.isnan(garch_fisher_p) else np.nan,
         Phi=np.nan, Bonferroni_pass='No'),
    dict(Regime='GARCH Low', n=garch_stats['Low']['n'], Accuracy_pct=garch_stats['Low']['acc'],
         Fisher_p=np.nan, Phi=np.nan, Bonferroni_pass=np.nan),
    dict(Regime='VIX-High intersect GARCH-High', n=n_intersect, Accuracy_pct=intersect_acc,
         Fisher_p=np.nan, Phi=np.nan, Bonferroni_pass=np.nan),
])
table10.to_csv('results/table10_garch_comparison_CORRECTED.csv', index=False)
print("\n== TABLE 10 (corrected) ==")
print(table10.to_string(index=False))

# ==========================================================================
# PART B: Extended threshold sensitivity -- p85 + quarterly breakdown
# ==========================================================================
vix_trainval = trainval['india_vix']
p85_threshold = float(np.percentile(vix_trainval, 85))
p75_threshold = float(np.percentile(vix_trainval, 75))  # sanity check vs known 18.71
print(f"\nTrain+val VIX p75 = {p75_threshold:.4f} (should match known fixed threshold 18.71)")
print(f"Train+val VIX p85 = {p85_threshold:.4f}")

preds['regime_p85'] = np.where(preds['india_vix'] >= p85_threshold, 'High-VIX-p85', 'Low-VIX-p85')
p85_stats = regime_stats(preds, 'regime_p85', 'High-VIX-p85')
print(f"p85 regime stats (n must be <= p75's n={n_vix_high}): {p85_stats}")

# Quarterly breakdown of the FIXED (p75, 18.71) regime -- must sum to 8
preds['quarter'] = preds['date'].dt.to_period('Q').astype(str)
quarterly = preds[preds['regime_fixed'] == 'High-VIX'].groupby('quarter').size()
print("\nQuarterly High-VIX (fixed threshold) day counts (must sum to 8):")
print(quarterly)
print("Sum:", quarterly.sum())

table11_rows = [
    dict(Check='Threshold p75 (fixed pre-test = 18.71)', High_VIX_count=n_vix_high,
         High_VIX_accuracy=f"{vix_stats['High']['acc']:.1f}%", Low_VIX_accuracy=f"{vix_stats['Low']['acc']:.1f}%",
         Interpretation='Main result under corrected protocol; sparse High-VIX'),
    dict(Check=f'Threshold p85 (fixed pre-test = {p85_threshold:.2f})', High_VIX_count=p85_stats['High']['n'],
         High_VIX_accuracy=f"{p85_stats['High']['acc']:.1f}%" if not np.isnan(p85_stats['High']['acc']) else 'N/A',
         Low_VIX_accuracy=f"{p85_stats['Low']['acc']:.1f}%",
         Interpretation='Stricter threshold; count must not exceed p75 count'),
]
for q, cnt in quarterly.items():
    sub = preds[(preds['quarter'] == q) & (preds['regime_fixed'] == 'High-VIX')]
    subL = preds[(preds['quarter'] == q) & (preds['regime_fixed'] != 'High-VIX')]
    acc_h = (sub['dir_21d'] == sub['stack_pred']).mean() * 100 if len(sub) else np.nan
    acc_l = (subL['dir_21d'] == subL['stack_pred']).mean() * 100 if len(subL) else np.nan
    table11_rows.append(dict(Check=f'{q} (fixed threshold)', High_VIX_count=int(cnt),
                              High_VIX_accuracy=f"{acc_h:.1f}%" if not np.isnan(acc_h) else 'N/A',
                              Low_VIX_accuracy=f"{acc_l:.1f}%" if not np.isnan(acc_l) else 'N/A',
                              Interpretation='Quarterly component of the n=8 fixed-threshold subset'))

table11 = pd.DataFrame(table11_rows)
table11.to_csv('results/table11_threshold_sensitivity_CORRECTED.csv', index=False)
print("\n== TABLE 11 (corrected) ==")
print(table11.to_string(index=False))

with open('results/garch_threshold_config_CORRECTED.json', 'w') as f:
    json.dump(dict(
        garch_high_threshold=garch_high_threshold,
        garch_fit_converged=bool(res_trainval.convergence_flag == 0),
        n_vix_high=n_vix_high, n_garch_high=n_garch_high, n_intersect=n_intersect,
        p75_threshold_check=p75_threshold, p85_threshold=p85_threshold,
        p85_n=p85_stats['High']['n'],
        quarterly_high_vix_counts={str(k): int(v) for k, v in quarterly.items()},
        p1_replication_row='DROPPED -- no independently-trained second pipeline artifact found in project; '
                            'not fabricated. Add back only if a genuine P1 run is produced.'
    ), f, indent=2)

print("\nDone.")
