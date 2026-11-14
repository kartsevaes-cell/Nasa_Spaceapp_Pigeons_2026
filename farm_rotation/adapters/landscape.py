import requests

def get_landscape(lat: float, lon: float) -> dict:
    """
    Get elevation and simple terrain classification.
    Uses the free Open-Elevation API.
    """
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        elevation = r.json()["results"][0]["elevation"]
    except Exception:
        elevation = 200  # fallback

    # Simple classification
    if elevation < 300:
        terrain = "Flat"
        slope = "Low"
    elif elevation < 800:
        terrain = "Rolling"
        slope = "Moderate"
    else:
        terrain = "Mountainous"
        slope = "High"

    return {
        "elevation_m": round(elevation),
        "terrain": terrain,
        "slope": slope,
    }
