import requests
import json
from pathlib import Path

# Full path from project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "nasa_power_climatology.json"

url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
params = {
    "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "longitude": -93.6,
    "latitude": 41.6,
    "format": "JSON"
}

def fetch_nasa_power():
    print("Fetching data from NASA POWER API...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved to: {OUTPUT_FILE}")

    # Quick summary
    params_data = data["properties"]["parameter"]
    print("\nAnnual averages:")
    for param, values in params_data.items():
        print(f"  {param}: {values.get('ANN')}")

if __name__ == "__main__":
    fetch_nasa_power()
