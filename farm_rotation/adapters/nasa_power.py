import requests
import pandas as pd

POWER_BASE_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"

def get_climate(lat: float, lon: float) -> dict:
    """
    Fetch average climate data from NASA POWER for a given location.
    Returns temperature, precipitation, and solar radiation.
    """
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
    
    # Extract annual averages
    properties = data["properties"]["parameter"]
    return {
        "temperature_c": round(properties["T2M"]["ANN"], 1),
        "precipitation_mm": round(properties["PRECTOTCORR"]["ANN"], 0),
        "solar_radiation": round(properties["ALLSKY_SFC_SW_DWN"]["ANN"], 2),
    }
