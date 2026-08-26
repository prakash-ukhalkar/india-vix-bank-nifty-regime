import pandas as pd

base = r"f:\MLSAPU\PhD-SPPU\India-VIX-Major-Revision\data"
mkt = pd.read_csv(fr"{base}\raw\market_data.csv")
vix = pd.read_csv(fr"{base}\raw\india_vix.csv")
print("market_data cols:", mkt.columns.tolist())
print("market_data range:", mkt.iloc[:,0].min(), mkt.iloc[:,0].max(), "rows:", len(mkt))
print("vix cols:", vix.columns.tolist())
print("vix range:", vix.iloc[:,0].min(), vix.iloc[:,0].max(), "rows:", len(vix))

test = pd.read_csv(fr"{base}\processed\test.csv")
print("\ntest.csv rows:", len(test), "range:", test['date'].min(), test['date'].max())
print("dir_21d NaN count:", test['dir_21d'].isna().sum())
print("last 5 rows date/dir_21d:\n", test[['date','dir_21d']].tail(25))

twr = pd.read_csv(fr"{base}\processed\test_with_regimes.csv")
print("\ntest_with_regimes shape:", twr.shape)
print(twr.columns.tolist())

tp = pd.read_csv(fr"{base}\processed\test_predictions.csv")
print("\ntest_predictions shape:", tp.shape)
print(tp.columns.tolist())
