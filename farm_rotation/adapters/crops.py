import pandas as pd

def load_crops(path="data/global_crops_50.csv") -> pd.DataFrame:
    return pd.read_csv(path)
