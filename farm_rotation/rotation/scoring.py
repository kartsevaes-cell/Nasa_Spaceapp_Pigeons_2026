def score_crop(crop, climate, priorities=None):
    """
    Score a crop from 0-100 based on climate fit.
    """
    score = 40  # base score

    temp = climate["temperature_c"]
    rain = climate["precipitation_mm"]

    # Temperature suitability
    if crop["temp_min_c"] <= temp <= crop["temp_max_c"]:
        score += 35
    elif abs(temp - crop["temp_min_c"]) <= 5 or abs(temp - crop["temp_max_c"]) <= 5:
        score += 15

    # Rainfall suitability
    if crop["rainfall_min_mm"] <= rain <= crop["rainfall_max_mm"]:
        score += 25
    elif abs(rain - crop["rainfall_min_mm"]) <= 150 or abs(rain - crop["rainfall_max_mm"]) <= 150:
        score += 10

    # Bonus for nitrogen-fixing crops (soil health)
    if crop.get("nitrogen_fixing") is True or str(crop.get("nitrogen_fixing")).lower() == "true":
        score += 10

    return min(max(score, 0), 100)
