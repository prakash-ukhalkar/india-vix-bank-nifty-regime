import pandas as pd

base = r"f:\MLSAPU\PhD-SPPU\India-VIX-Major-Revision\data\processed"
for name in ["train", "val", "test"]:
    df = pd.read_csv(fr"{base}\{name}.csv")
    print(name, df.shape)
    date_cols = [c for c in df.columns if "date" in c.lower()]
    print("date cols:", date_cols)
    if date_cols:
        c = date_cols[0]
        print("range:", df[c].min(), df[c].max())
    print(df.columns.tolist())
    print("---")
