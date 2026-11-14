import requests
import json
from pathlib import Path

# API endpoint and parameters
url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
params = {
    "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "longitude": -93.6,
    "latitude": 41.6,
    "format": "JSON"
}

def fetch_nasa_power():
    """Fetch climatology data from NASA POWER API and save to data/ folder."""
    print("Fetching data from NASA POWER API...")
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error for bad status codes
    
    data = response.json()
    
    # Ensure the data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Save the full response
    output_path = data_dir / "nasa_power_climatology.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    print(f"Data saved to: {output_path}")
    
    # Optional: print a quick summary
    params_data = data["properties"]["parameter"]
    print("\nAnnual averages:")
    for param, values in params_data.items():
        print(f"  {param}: {values.get('ANN')}")

if __name__ == "__main__":
    fetch_nasa_power()
