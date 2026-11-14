import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
JSON_FILE = PROJECT_ROOT / "data" / "nasa_power_climatology.json"

data = json.loads(JSON_FILE.read_text())
t2m = data["properties"]["parameter"]["T2M"]

# Base temperature 10 °C (common for many crops)
base = 10
months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
gdd = {m: max(0, t2m[m] - base) * 30 for m in months}  # approx monthly GDD

print("Approximate monthly Growing Degree Days (base 10°C):")
for m, val in gdd.items():
    print(f"  {m}: {val:.0f}")
print(f"Annual total: {sum(gdd.values()):.0f}")
