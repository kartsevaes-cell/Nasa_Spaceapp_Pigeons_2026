def score_crop(crop, climate, priorities=None):
    """
    Very simple scoring example.
    Later you can make this smarter.
    """
    score = 50  # base score
    
    # Temperature fit (rough example)
    if crop["temp_min_c"] <= climate["temperature_c"] <= crop["temp_max_c"]:
        score += 30
    
    # Rainfall fit
    if crop["rainfall_min_mm"] <= climate["precipitation_mm"] <= crop["rainfall_max_mm"]:
        score += 20
    
    return min(score, 100)
