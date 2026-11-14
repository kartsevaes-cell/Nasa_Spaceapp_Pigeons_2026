def score_crop(crop, climate, soil=None, weights=None):
    if weights is None:
        weights = {"climate": 0.6, "soil_health": 0.25, "water": 0.15}

    score = 0
    temp = climate["temperature_c"]
    rain = climate["precipitation_mm"]

    # Climate fit (0-100)
    climate_score = 40
    if crop["temp_min_c"] <= temp <= crop["temp_max_c"]:
        climate_score += 35
    elif abs(temp - crop["temp_min_c"]) <= 5 or abs(temp - crop["temp_max_c"]) <= 5:
        climate_score += 15
    if crop["rainfall_min_mm"] <= rain <= crop["rainfall_max_mm"]:
        climate_score += 25
    climate_score = min(climate_score, 100)

    # Soil health bonus
    soil_score = 50
    if str(crop.get("nitrogen_fixing", "")).lower() in ("true", "1", "yes"):
        soil_score += 30
    if crop.get("soil_health_score", 0) >= 4:
        soil_score += 20
    soil_score = min(soil_score, 100)

    # Water fit
    water_score = 70
    if crop.get("water_use") == "High" and rain < 500:
        water_score -= 30
    elif crop.get("water_use") == "Low":
        water_score += 15
    water_score = max(0, min(water_score, 100))

    # Weighted total
    total = (
        climate_score * weights["climate"] +
        soil_score * weights["soil_health"] +
        water_score * weights["water"]
    )
    return round(total)
