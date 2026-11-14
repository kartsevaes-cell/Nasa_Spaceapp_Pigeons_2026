import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
JSON_FILE = PROJECT_ROOT / "data" / "nasa_power_climatology.json"
EXCEL_FILE = PROJECT_ROOT / "data" / "nasa_power_climatology.xlsx"

data = json.loads(JSON_FILE.read_text())
df = pd.DataFrame(data["properties"]["parameter"]).T
df.to_excel(EXCEL_FILE)
print(f"Excel saved to: {EXCEL_FILE}")
