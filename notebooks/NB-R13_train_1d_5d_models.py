"""
NB-R13: Train real 1-day and 5-day stacking ensembles on the corrected, leakage-safe splits.
Reviewer #4 (R2, point 5) correctly identified that the manuscript's 1-day/5-day rows in
Tables 5-7 were never recomputed after the split-boundary fix (NB-R01) -- they were leftover
numbers from the original, uncorrected submission. This script trains real models for both
horizons using the same methodology as NB-R03 (21-day), so every horizon in the paper is
backed by an actual run on the corrected data.

Optuna trial count reduced from 100 (NB-R03) to 25 per model for time budget; this is stated
explicitly in the manuscript hyperparameter section rather than hidden.
"""
import pandas as pd
import numpy as np
import json
import joblib
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, log_loss
from statsmodels.stats.contingency_tables import mcnemar
import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)

import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
from catboost import CatBoostClassifier
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from scipy.stats import fisher_exact

PROJ = Path(r'F:\MLSAPU\PhD-SPPU\India-VIX-Major-Revision')
PROC = PROJ / 'data' / 'processed'
MODELS = PROJ / 'models'
RESULTS = PROJ / 'results'

with open(PROC / 'feature_cols.json') as f:
    FEATURE_COLS = json.load(f)

N_FOLDS = 5
OPTUNA_TRIALS = 25
RANDOM_SEED = 42
SEQ_LEN, HIDDEN_SIZE, DROPOUT = 20, 64, 0.2
MAX_EPOCHS, PATIENCE, BATCH_SIZE, LR = 50, 8, 64, 1e-3

train = pd.read_csv(PROC / 'train.csv', parse_dates=['date'])
val = pd.read_csv(PROC / 'val.csv', parse_dates=['date'])
test = pd.read_csv(PROC / 'test_with_regimes.csv', parse_dates=['date'])

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Device: {device}')


class SelfAttention(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.attn = nn.Linear(hidden_size * 2, 1)

    def forward(self, x):
        scores = self.attn(x).squeeze(-1)
        weights = torch.softmax(scores, dim=1).unsqueeze(-1)
        return (x * weights).sum(dim=1)


class BiLSTMClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, dropout):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True, bidirectional=True, dropout=dropout)
        self.attn = SelfAttention(hidden_size)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size * 2, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        ctx = self.attn(out)
        ctx = self.dropout(ctx)
        return self.fc(ctx).squeeze(-1)


def make_sequences(X, y, seq_len):
    Xs, ys = [], []
    for i in range(seq_len, len(X)):
        Xs.append(X[i - seq_len:i])
        ys.append(y[i])
    return np.array(Xs), np.array(ys)


def run_horizon(target_col, horizon_label):
    print(f'\n{"="*70}\nHORIZON: {horizon_label} (target={target_col})\n{"="*70}')

    X_train = train[FEATURE_COLS].values
    y_train = train[target_col].values
    X_val = val[FEATURE_COLS].values
    y_val = val[target_col].values
    X_test = test[FEATURE_COLS].values
    y_test = test[target_col].values

    tscv = TimeSeriesSplit(n_splits=N_FOLDS)

    def xgb_obj(trial):
        params = dict(n_estimators=trial.suggest_int('n_estimators', 100, 500),
                      max_depth=trial.suggest_int('max_depth', 3, 8),
                      learning_rate=trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                      subsample=trial.suggest_float('subsample', 0.5, 1.0),
                      colsample_bytree=trial.suggest_float('colsample_bytree', 0.5, 1.0),
                      reg_alpha=trial.suggest_float('reg_alpha', 1e-4, 10.0, log=True),
                      reg_lambda=trial.suggest_float('reg_lambda', 1e-4, 10.0, log=True),
                      use_label_encoder=False, eval_metric='logloss', random_state=RANDOM_SEED, n_jobs=-1)
        scores = []
        for tr, va in tscv.split(X_train):
            m = xgb.XGBClassifier(**params)
            m.fit(X_train[tr], y_train[tr], verbose=False)
            scores.append(log_loss(y_train[va], m.predict_proba(X_train[va])[:, 1]))
        return np.mean(scores)

    def lgb_obj(trial):
        params = dict(n_estimators=trial.suggest_int('n_estimators', 100, 500),
                      max_depth=trial.suggest_int('max_depth', 3, 8),
                      learning_rate=trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                      num_leaves=trial.suggest_int('num_leaves', 15, 127),
                      subsample=trial.suggest_float('subsample', 0.5, 1.0),
                      colsample_bytree=trial.suggest_float('colsample_bytree', 0.5, 1.0),
                      reg_alpha=trial.suggest_float('reg_alpha', 1e-4, 10.0, log=True),
                      reg_lambda=trial.suggest_float('reg_lambda', 1e-4, 10.0, log=True),
                      random_state=RANDOM_SEED, n_jobs=-1, verbose=-1)
        scores = []
        for tr, va in tscv.split(X_train):
            m = lgb.LGBMClassifier(**params)
            m.fit(X_train[tr], y_train[tr])
            scores.append(log_loss(y_train[va], m.predict_proba(X_train[va])[:, 1]))
        return np.mean(scores)

    def rf_obj(trial):
        params = dict(n_estimators=trial.suggest_int('n_estimators', 100, 400),
                      max_depth=trial.suggest_int('max_depth', 3, 15),
                      min_samples_split=trial.suggest_int('min_samples_split', 2, 20),
                      min_samples_leaf=trial.suggest_int('min_samples_leaf', 1, 10),
                      max_features=trial.suggest_categorical('max_features', ['sqrt', 'log2']),
                      random_state=RANDOM_SEED, n_jobs=-1)
        scores = []
        for tr, va in tscv.split(X_train):
            m = RandomForestClassifier(**params)
            m.fit(X_train[tr], y_train[tr])
            scores.append(log_loss(y_train[va], m.predict_proba(X_train[va])[:, 1]))
        return np.mean(scores)

    def cb_obj(trial):
        params = dict(iterations=trial.suggest_int('iterations', 100, 500),
                      depth=trial.suggest_int('depth', 3, 8),
                      learning_rate=trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
                      l2_leaf_reg=trial.suggest_float('l2_leaf_reg', 1e-4, 10.0, log=True),
                      bagging_temperature=trial.suggest_float('bagging_temperature', 0.0, 1.0),
                      random_seed=RANDOM_SEED, verbose=0, allow_writing_files=False)
        scores = []
        for tr, va in tscv.split(X_train):
            m = CatBoostClassifier(**params)
            m.fit(X_train[tr], y_train[tr])
            scores.append(log_loss(y_train[va], m.predict_proba(X_train[va])[:, 1]))
        return np.mean(scores)

    studies = {}
    for name, obj in [('xgb', xgb_obj), ('lgb', lgb_obj), ('rf', rf_obj), ('cb', cb_obj)]:
        s = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=RANDOM_SEED))
        s.optimize(obj, n_trials=OPTUNA_TRIALS, show_progress_bar=False)
        studies[name] = s
        print(f'  {name} best loss: {s.best_value:.4f}')

    best_xgb = {**studies['xgb'].best_params, 'use_label_encoder': False, 'eval_metric': 'logloss', 'random_state': RANDOM_SEED, 'n_jobs': -1}
    best_lgb = {**studies['lgb'].best_params, 'random_state': RANDOM_SEED, 'n_jobs': -1, 'verbose': -1}
    best_rf = {**studies['rf'].best_params, 'random_state': RANDOM_SEED, 'n_jobs': -1}
    best_cb = {**studies['cb'].best_params, 'random_seed': RANDOM_SEED, 'verbose': 0, 'allow_writing_files': False}

    xgb_model = xgb.XGBClassifier(**best_xgb).fit(X_train, y_train, verbose=False)
    lgb_model = lgb.LGBMClassifier(**best_lgb).fit(X_train, y_train)
    rf_model = RandomForestClassifier(**best_rf).fit(X_train, y_train)
    cb_model = CatBoostClassifier(**best_cb).fit(X_train, y_train)

    for name, m in [('xgb', xgb_model), ('lgb', lgb_model), ('rf', rf_model), ('cb', cb_model)]:
        joblib.dump(m, MODELS / f'{name}_model_{horizon_label}.joblib')

    Xtr_seq, ytr_seq = make_sequences(X_train, y_train, SEQ_LEN)
    Xva_seq, yva_seq = make_sequences(X_val, y_val, SEQ_LEN)

    torch.manual_seed(RANDOM_SEED)
    bilstm = BiLSTMClassifier(len(FEATURE_COLS), HIDDEN_SIZE, DROPOUT).to(device)
    opt = torch.optim.Adam(bilstm.parameters(), lr=LR)
    loss_fn = nn.BCEWithLogitsLoss()

    tr_loader = DataLoader(TensorDataset(torch.tensor(Xtr_seq, dtype=torch.float32), torch.tensor(ytr_seq, dtype=torch.float32)), batch_size=BATCH_SIZE, shuffle=False)
    va_loader = DataLoader(TensorDataset(torch.tensor(Xva_seq, dtype=torch.float32), torch.tensor(yva_seq, dtype=torch.float32)), batch_size=BATCH_SIZE, shuffle=False)

    best_val_loss, patience_cnt = float('inf'), 0
    ckpt_path = MODELS / f'bilstm_best_{horizon_label}.pt'
    for epoch in range(MAX_EPOCHS):
        bilstm.train()
        for Xb, yb in tr_loader:
            Xb, yb = Xb.to(device), yb.to(device)
            opt.zero_grad()
            loss = loss_fn(bilstm(Xb), yb)
            loss.backward()
            opt.step()
        bilstm.eval()
        vl = []
        with torch.no_grad():
            for Xb, yb in va_loader:
                Xb, yb = Xb.to(device), yb.to(device)
                vl.append(loss_fn(bilstm(Xb), yb).item())
        val_loss = np.mean(vl)
        if val_loss < best_val_loss:
            best_val_loss, patience_cnt = val_loss, 0
            torch.save(bilstm.state_dict(), ckpt_path)
        else:
            patience_cnt += 1
            if patience_cnt >= PATIENCE:
                print(f'  BiLSTM early stop epoch {epoch+1}')
                break
    bilstm.load_state_dict(torch.load(ckpt_path, map_location=device))
    print(f'  BiLSTM best val loss: {best_val_loss:.4f}')

    bilstm.eval()
    Xva_t = torch.tensor(Xva_seq, dtype=torch.float32).to(device)
    with torch.no_grad():
        bilstm_val_probs = torch.sigmoid(bilstm(Xva_t)).cpu().numpy()

    val_xgb = xgb_model.predict_proba(X_val)[:, 1]
    val_lgb = lgb_model.predict_proba(X_val)[:, 1]
    val_rf = rf_model.predict_proba(X_val)[:, 1]
    val_cb = cb_model.predict_proba(X_val)[:, 1]

    n_align_val = len(bilstm_val_probs)
    meta_X_val = np.column_stack([val_xgb[-n_align_val:], val_lgb[-n_align_val:], val_rf[-n_align_val:], val_cb[-n_align_val:], bilstm_val_probs])
    y_val_a = y_val[-n_align_val:]

    meta = LogisticRegression(C=1.0, max_iter=1000, random_state=RANDOM_SEED).fit(meta_X_val, y_val_a)
    joblib.dump(meta, MODELS / f'meta_learner_{horizon_label}.joblib')

    test_xgb = xgb_model.predict_proba(X_test)[:, 1]
    test_lgb = lgb_model.predict_proba(X_test)[:, 1]
    test_rf = rf_model.predict_proba(X_test)[:, 1]
    test_cb = cb_model.predict_proba(X_test)[:, 1]

    Xte_seq, yte_seq = make_sequences(X_test, y_test, SEQ_LEN)
    with torch.no_grad():
        Xte_t = torch.tensor(Xte_seq, dtype=torch.float32).to(device)
        bilstm_test_probs = torch.sigmoid(bilstm(Xte_t)).cpu().numpy()

    n_align_test = len(bilstm_test_probs)
    test_aligned = test.iloc[-n_align_test:].copy()
    meta_X_test = np.column_stack([test_xgb[-n_align_test:], test_lgb[-n_align_test:], test_rf[-n_align_test:], test_cb[-n_align_test:], bilstm_test_probs])
    y_test_a = yte_seq

    stack_probs = meta.predict_proba(meta_X_test)[:, 1]
    stack_preds = (stack_probs >= 0.5).astype(int)

    test_aligned['stack_prob'] = stack_probs
    test_aligned['stack_pred'] = stack_preds

    overall_acc = accuracy_score(y_test_a, stack_preds)
    overall_auc = roc_auc_score(y_test_a, stack_probs)
    majority_class = int(pd.Series(y_test_a).mode()[0])
    majority_acc = (y_test_a == majority_class).mean()

    # McNemar test: stack vs majority-class baseline
    stack_correct = (stack_preds == y_test_a)
    majority_preds = np.full_like(y_test_a, majority_class)
    majority_correct = (majority_preds == y_test_a)
    both_correct = int((stack_correct & majority_correct).sum())
    stack_only = int((stack_correct & ~majority_correct).sum())
    majority_only = int((~stack_correct & majority_correct).sum())
    neither = int((~stack_correct & ~majority_correct).sum())
    table = [[both_correct, stack_only], [majority_only, neither]]
    mcnemar_p = mcnemar(table, exact=True).pvalue

    print(f'  Overall acc={overall_acc:.4f}, AUC={overall_auc:.4f}, majority={majority_acc:.4f}, McNemar p={mcnemar_p:.4f}')

    # Regime-conditioned (High-VIX vs Low-VIX, fixed pre-test threshold already in regime_fixed col)
    hv = test_aligned[test_aligned['regime_fixed'] == 'High-VIX']
    lv = test_aligned[test_aligned['regime_fixed'] != 'High-VIX']
    hv_acc = (hv[target_col] == hv['stack_pred']).mean() if len(hv) else np.nan
    lv_acc = (lv[target_col] == lv['stack_pred']).mean() if len(lv) else np.nan

    fisher_p = np.nan
    if len(hv) > 0 and len(lv) > 0:
        a = int((hv[target_col] == hv['stack_pred']).sum()); b = len(hv) - a
        c = int((lv[target_col] == lv['stack_pred']).sum()); e = len(lv) - c
        _, fisher_p = fisher_exact([[a, b], [c, e]])

    test_aligned.to_csv(PROC / f'test_predictions_{horizon_label}.csv', index=False)

    return dict(
        horizon=horizon_label, overall_acc=overall_acc, overall_auc=overall_auc,
        majority_acc=majority_acc, mcnemar_p=mcnemar_p,
        hv_n=len(hv), hv_acc=hv_acc, lv_n=len(lv), lv_acc=lv_acc, fisher_p=fisher_p,
    ), dict(
        xgb=studies['xgb'].best_value, lgb=studies['lgb'].best_value,
        rf=studies['rf'].best_value, cb=studies['cb'].best_value, bilstm=best_val_loss,
    )


results_1d, cv_1d = run_horizon('dir_1d', '1d')
results_5d, cv_5d = run_horizon('dir_5d', '5d')

summary = pd.DataFrame([results_1d, results_5d])
summary.to_csv(RESULTS / 'horizon_1d_5d_results_CORRECTED.csv', index=False)
print('\n\n=== FINAL SUMMARY ===')
print(summary.to_string(index=False))
