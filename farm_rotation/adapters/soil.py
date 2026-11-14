def get_soil(lat: float, lon: float, manual: dict = None) -> dict:
    """
    Returns soil information.
    For now uses manual input. Later can call SoilGrids.
    """
    if manual:
        return {
            "soil_type": manual.get("soil_type", "Unknown"),
            "ph": manual.get("ph", 6.5),
            "organic_matter": manual.get("organic_matter", 2.0),
            "drainage": manual.get("drainage", "Moderate"),
        }
    
    # Placeholder defaults (replace with SoilGrids later)
    return {
        "soil_type": "Loam",
        "ph": 6.5,
        "organic_matter": 2.5,
        "drainage": "Moderate",
    }
