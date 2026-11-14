import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
JSON_FILE = DATA_DIR / "nasa_power_climatology.json"
PLOT_FILE = DATA_DIR / "climatology_plot.png"

# Load data
data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
params = data["properties"]["parameter"]
df = pd.DataFrame(params).T

# Select months only (drop ANN)
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
df_months = df[months]

# Plot
plt.figure(figsize=(12, 6))
for param in df_months.index:
    plt.plot(months, df_months.loc[param], marker="o", label=param)

plt.title("NASA POWER Monthly Climatology")
plt.xlabel("Month")
plt.ylabel("Value")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save plot
plt.savefig(PLOT_FILE, dpi=150)
print(f"Plot saved to: {PLOT_FILE}")
plt.show()
