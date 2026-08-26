"""
NB-R12: Regenerate manuscript Figures 3, 4, 5, 6, 8, 9 from the corrected, leakage-safe pipeline.
Reviewer #4 (R2) found these figures still show pre-correction numbers (e.g. Fig 3: 84.5%/54.8%
with p<0.004 asterisks; Fig 5: "VIX p75 threshold (15.08)"; Fig 7: strategy above buy-and-hold
at every cost; Fig 8: n=58/219; Fig 9: "HV obs: 84.5%"). Figs 7 and 9 already have corrected
replacements in plots/ (R09_trading_simulation.png, R04_statistical_tests.png) -- this script
produces the rest, all traceable to results/*.csv and the NB-R09/NB-R11 simulation logic.
"""
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path

PROJ = Path(r'F:\MLSAPU\PhD-SPPU\India-VIX-Major-Revision')
PROC = PROJ / 'data' / 'processed'
RAW = PROJ / 'data' / 'raw'
RESULTS = PROJ / 'results'
PLOTS = PROJ / 'plots'

RFR_ANNUAL, TRADING_DAYS = 0.065, 252
RFR_DAILY = RFR_ANNUAL / TRADING_DAYS

# ============================================================
# FIG 3: Regime-conditioned directional accuracy by horizon
# ============================================================
tbl7 = pd.DataFrame([
    dict(horizon='1d', hv_n=58, hv_acc=0.500, lv_n=218, lv_acc=0.493),
    dict(horizon='5d', hv_n=57, hv_acc=0.528, lv_n=215, lv_acc=0.511),
    dict(horizon='21d', hv_n=8, hv_acc=1.000, lv_n=248, lv_acc=0.665),
])
fig, ax = plt.subplots(figsize=(7, 4.5))
x = np.arange(len(tbl7))
w = 0.35
ax.bar(x - w/2, tbl7['hv_acc']*100, w, label='High-VIX', color='#D6604D')
ax.bar(x + w/2, tbl7['lv_acc']*100, w, label='Low-VIX', color='#4393C3')
for i, row in tbl7.iterrows():
    ax.text(i - w/2, row['hv_acc']*100 + 1.5, f"{row['hv_acc']*100:.1f}%\n(n={row['hv_n']})", ha='center', fontsize=8)
    ax.text(i + w/2, row['lv_acc']*100 + 1.5, f"{row['lv_acc']*100:.1f}%\n(n={row['lv_n']})", ha='center', fontsize=8)
ax.axhline(50, color='grey', linestyle=':', linewidth=1, label='Coin flip')
ax.set_xticks(x)
ax.set_xticklabels(['1-day', '5-day', '21-day'])
ax.set_ylabel('Directional Accuracy (%)')
ax.set_title('Regime-Conditioned Directional Accuracy by Horizon\n(corrected pre-test threshold = 18.71; only 21-day shows a gap, and it is not significant: Fisher p=1.000)')
ax.set_ylim(0, 115)
ax.legend(fontsize=8, loc='upper left')
plt.tight_layout()
plt.savefig(PLOTS / 'R12_Fig3_regime_accuracy_by_horizon.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved Fig 3')

# ============================================================
# FIG 4: AUC by horizon (unconditioned; regime-conditioned marked N/A where undefined)
# ============================================================
auc_uncond = dict(zip(['1-day', '5-day', '21-day'], [0.5444, 0.5620, 0.5820]))
auc_lowvix_21d = 0.5838  # from statistical_tests.json
auc_highvix_21d = np.nan  # undefined: n=8, single class (all Up)

fig, ax = plt.subplots(figsize=(7, 4))
horizons = ['1-day', '5-day', '21-day']
uncond_vals = [auc_uncond[h] for h in horizons]
lowvix_vals = [np.nan, np.nan, auc_lowvix_21d]
highvix_vals = [np.nan, np.nan, np.nan]  # High-VIX AUC undefined at all horizons we can verify (21d confirmed single-class; 1d/5d not separately modeled here)

xw = np.arange(len(horizons))
ax.plot(xw, uncond_vals, 'o-', label='Unconditioned (overall)', color='grey')
ax.plot(xw, lowvix_vals, 's-', label='Low-VIX', color='#4393C3')
ax.scatter([2], [np.nan], marker='x')  # placeholder to keep legend consistent
ax.axhline(0.5, color='black', linestyle=':', linewidth=1, label='AUC = 0.5 (no ranking skill)')
ax.set_xticks(xw)
ax.set_xticklabels(horizons)
ax.set_ylabel('AUC')
ax.set_ylim(0.45, 0.65)
ax.set_title('Threshold-Free Ranking Quality (AUC) by Horizon\nHigh-VIX AUC is undefined at 21-day: n=8, single class (all outcomes Up)')
ax.legend(fontsize=8)
ax.text(2, 0.47, 'High-VIX\nAUC: N/A\n(single class)', ha='center', fontsize=8, color='#D6604D')
plt.tight_layout()
plt.savefig(PLOTS / 'R12_Fig4_auc_by_horizon.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved Fig 4')

# ============================================================
# FIG 5 & 6: Equity curves and drawdown (reconstructed exactly as in NB-R09)
# ============================================================
test = pd.read_csv(PROC / 'test_predictions.csv', parse_dates=['date'])
mkt = pd.read_csv(RAW / 'market_data.csv', parse_dates=['date'])
mkt.columns = [c.strip().lower().replace(' ', '_') for c in mkt.columns]
close_col = [c for c in mkt.columns if 'close' in c and 'india' not in c][0]
open_col = [c for c in mkt.columns if 'open' in c][0]
mkt = mkt[['date', close_col, open_col]].rename(columns={close_col: 'close', open_col: 'open'})

test = test.drop(columns=[c for c in ['close', 'open'] if c in test.columns], errors='ignore')
test = test.merge(mkt, on='date', how='left').sort_values('date').reset_index(drop=True)
test['close_fwd21'] = test['close'].shift(-21)
test['ret_21d'] = np.log(test['close_fwd21'] / test['close'])
test['bh_ret_daily'] = np.log(test['close'] / test['close'].shift(1)).fillna(0)

signal = (test['regime_fixed'] == 'High-VIX') & (test['stack_pred'] == 1) & test['ret_21d'].notna() & test['open'].notna()
strat_daily = np.zeros(len(test))
in_position = np.zeros(len(test), dtype=int)
trade_windows = []
last_exit = -1
for i in range(len(test)):
    if not signal.iloc[i] or i <= last_exit:
        continue
    entry, exit_ = i + 1, i + 21
    if entry >= len(test) or exit_ >= len(test):
        continue
    if pd.isna(test.loc[entry, 'open']) or pd.isna(test.loc[exit_, 'close']):
        continue
    day1_ret = np.log(test.loc[entry, 'close'] / test.loc[entry, 'open'])
    strat_daily[entry] += day1_ret
    if exit_ > entry:
        strat_daily[entry + 1: exit_ + 1] += test.loc[entry + 1: exit_, 'bh_ret_daily'].values
    in_position[entry: exit_ + 1] = 1
    trade_windows.append((test.loc[entry, 'date'], test.loc[exit_, 'date']))
    last_exit = exit_

test['strat_ret_daily'] = strat_daily
test['in_position'] = in_position
test['strat_cum'] = test['strat_ret_daily'].cumsum()
test['bh_cum'] = test['bh_ret_daily'].cumsum()
test['strat_equity'] = np.exp(test['strat_cum'])
test['bh_equity'] = np.exp(test['bh_cum'])
test['strat_dd'] = test['strat_equity'] / test['strat_equity'].cummax() - 1
test['bh_dd'] = test['bh_equity'] / test['bh_equity'].cummax() - 1

print(f"Reconstructed trade windows: {trade_windows}")
print(f"Final strat equity: {test['strat_equity'].iloc[-1]:.4f}, BH equity: {test['bh_equity'].iloc[-1]:.4f}")
print(f"Strat max DD: {test['strat_dd'].min()*100:.2f}%, BH max DD: {test['bh_dd'].min()*100:.2f}%")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={'height_ratios': [2.2, 1]})
ax1.plot(test['date'], test['bh_equity'], '--', color='grey', label='Buy-and-Hold')
ax1.plot(test['date'], test['strat_equity'], color='tomato', linewidth=1.8, label='High-VIX + Up (corrected: 1 trade, 21 active days)')
for (s, e) in trade_windows:
    ax1.axvspan(s, e, color='tomato', alpha=0.15)
ax1.set_ylabel('Portfolio Value (start = 1.0)')
ax1.set_title('Equity Curves — Bank Nifty Test Period (Jan 2025 – Feb 2026)\nCorrected protocol: signal at close[t], entry at open[t+1], exit at close[t+21], single position only')
ax1.legend(fontsize=8, loc='upper left')

ax2b = ax2.twinx()
ax2b.fill_between(test['date'], 0, test['india_vix'], color='salmon', alpha=0.4)
ax2b.axhline(18.71, color='darkred', linestyle='--', linewidth=1.2)
ax2b.text(test['date'].iloc[5], 18.71 + 0.5, 'VIX p75 threshold (18.71, fixed pre-test)', fontsize=8, color='darkred')
ax2b.set_ylabel('India VIX')
ax2.set_yticks([])
ax2.set_xlabel('Date')
plt.tight_layout()
plt.savefig(PLOTS / 'R12_Fig5_equity_curves.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved Fig 5')

fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(test['date'], test['bh_dd']*100, '--', color='grey', label='Buy-and-Hold')
ax.plot(test['date'], test['strat_dd']*100, color='tomato', label='High-VIX + Up')
ax.set_ylabel('Drawdown (%)')
ax.set_xlabel('Date')
ax.set_title(f"Drawdown Profiles (Max DD: Strategy {test['strat_dd'].min()*100:.2f}% vs Buy-and-Hold {test['bh_dd'].min()*100:.2f}%)")
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(PLOTS / 'R12_Fig6_drawdown.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved Fig 6')

# ============================================================
# FIG 8: VIX vs GARCH regime comparison (corrected, from NB-R11 output)
# ============================================================
t10 = pd.read_csv(RESULTS / 'table10_garch_comparison_CORRECTED.csv')
fig, ax = plt.subplots(figsize=(7, 4.5))
labels = t10['Regime'].tolist()
accs = t10['Accuracy_pct'].tolist()
ns = t10['n'].tolist()
colors = ['#D6604D', '#F4A582', '#2166AC', '#92C5DE', '#777777']
bars = ax.bar(range(len(labels)), accs, color=colors)
for i, (a, n) in enumerate(zip(accs, ns)):
    if not pd.isna(a):
        ax.text(i, a + 1.5, f'{a:.1f}%\n(n={n})', ha='center', fontsize=8)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(['VIX\nHigh', 'VIX\nLow', 'GARCH\nHigh', 'GARCH\nLow', 'VIX∩GARCH\nHigh'], fontsize=8)
ax.axhline(50, color='grey', linestyle=':', linewidth=1)
ax.set_ylabel('Directional Accuracy (%)')
ax.set_title('India VIX vs GARCH(1,1) Regime Comparison (corrected, pre-test thresholds)\nNeither regime split is statistically significant (Fisher p=1.000 for both)')
ax.set_ylim(0, 115)
plt.tight_layout()
plt.savefig(PLOTS / 'R12_Fig8_vix_vs_garch.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved Fig 8')

print('\nAll figures regenerated in plots/. Fig 7 and Fig 9 already corrected: '
      'plots/R09_trading_simulation.png, plots/R04_statistical_tests.png')
