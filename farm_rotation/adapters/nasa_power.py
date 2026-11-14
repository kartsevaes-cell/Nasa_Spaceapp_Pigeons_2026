import requests
from farm_rotation.cache import get_cached_climate, save_climate

POWER_BASE_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"

def get_climate(lat: float, lon: float) -> dict:
    # Check cache first
    cached = get_cached_climate(lat, lon)
    if cached:
        return cached

    params = {
        "parameters": "T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "format": "JSON",
    }
    
    response = requests.get(POWER_BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    properties = data["properties"]["parameter"]
    result = {
        "temperature_c": round(properties["T2M"]["ANN"], 1),
        "precipitation_mm": round(properties["PRECTOTCORR"]["ANN"], 0),
        "solar_radiation": round(properties["ALLSKY_SFC_SW_DWN"]["ANN"], 2),
    }
    
    # Save to cache
    save_climate(lat, lon, result)
    return result
