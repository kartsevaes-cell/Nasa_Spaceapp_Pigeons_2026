import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent if "__file__" in dir() else Path(".")
DATA_DIR = PROJECT_ROOT / "data"

JSON_FILE = DATA_DIR / "nasa_power_climatology.json"
CSV_FILE = DATA_DIR / "nasa_power_climatology.csv"

data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
params = data["properties"]["parameter"]

df = pd.DataFrame(params).T
df.to_csv(CSV_FILE)
print(f"CSV saved to: {CSV_FILE}")
print(df)
