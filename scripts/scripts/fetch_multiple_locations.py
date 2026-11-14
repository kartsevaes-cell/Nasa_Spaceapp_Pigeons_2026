import requests
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

locations = {
    "ames_iowa": {"lat": 41.6, "lon": -93.6},
    "chicago": {"lat": 41.88, "lon": -87.63},
    "des_moines": {"lat": 41.59, "lon": -93.62},
}

url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
base_params = {
    "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "format": "JSON"
}

for name, coords in locations.items():
    params = {**base_params, "latitude": coords["lat"], "longitude": coords["lon"]}
    r = requests.get(url, params=params)
    r.raise_for_status()
    out = DATA_DIR / f"nasa_power_{name}.json"
    out.write_text(json.dumps(r.json(), indent=2), encoding="utf-8")
   
