from farm_rotation.adapters.nasa_power import get_climate
from farm_rotation.adapters.crops import load_crops
from farm_rotation.rotation.scoring import score_crop

def analyze_farm(lat, lon):
    climate = get_climate(lat, lon)
    crops = load_crops()
    
    results = []
    for _, crop in crops.iterrows():
        score = score_crop(crop, climate)
        results.append({
            "crop": crop["crop_name"],
            "score": score,
            "nitrogen_fixing": crop["nitrogen_fixing"],
            "crop_data": crop.to_dict()
        })
    
    return sorted(results, key=lambda x: x["score"], reverse=True)

def explain_crop(crop: dict, score: int, climate: dict) -> str:
    """
    Detailed rule-based explanation using multiple crop and climate variables.
    """
    name = crop.get("crop_name", "This crop")
    temp = climate["temperature_c"]
    rain = climate["precipitation_mm"]
    
    reasons = []
    
    if score >= 85:
        reasons.append(f"{name} is an excellent match for this location.")
    elif score >= 70:
        reasons.append(f"{name} is a good option with minor limitations.")
    elif score >= 50:
        reasons.append(f"{name} is possible but not ideal.")
    else:
        reasons.append(f"{name} is not well suited to this location.")
    
    tmin = crop.get("temp_min_c")
    tmax = crop.get("temp_max_c")
    if tmin is not None and tmax is not None:
        if tmin <= temp <= tmax:
            reasons.append(f"Temperature ({temp}°C) is within the ideal range ({tmin}–{tmax}°C).")
        elif temp < tmin:
            reasons.append
