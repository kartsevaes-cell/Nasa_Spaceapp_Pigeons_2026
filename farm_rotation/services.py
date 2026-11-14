from farm_rotation.adapters.nasa_power import get_climate
from farm_rotation.adapters.crops import load_crops
from farm_rotation.rotation.scoring import score_crop
from farm_rotation.adapters.soil import get_soil
from farm_rotation.rotation.generator import generate_rotations

def analyze_farm(lat, lon, soil_manual=None):
    climate = get_climate(lat, lon)
    soil = get_soil(lat, lon, soil_manual)
    crops = load_crops()
    
    results = []
    for _, crop in crops.iterrows():
        score = score_crop(crop, climate, soil)
        results.append({
            "crop": crop["crop_name"],
            "score": score,
            "nitrogen_fixing": crop["nitrogen_fixing"],
            "crop_data": crop.to_dict()
        })
    
    return sorted(results, key=lambda x: x["score"], reverse=True)

def analyze_farm_with_rotations(lat, lon, soil_manual=None, years=3):
    results = analyze_farm(lat, lon, soil_manual)
    rotations = generate_rotations(results, years=years)
    return {
        "crops": results,
        "rotations": rotations
    }

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
            reasons.append(f"Temperature ({temp}°C) is below the preferred minimum ({tmin}°C).")
        else:
            reasons.append(f"Temperature ({temp}°C) is above the preferred maximum ({tmax}°C).")
    
    rmin = crop.get("rainfall_min_mm")
    rmax = crop.get("rainfall_max_mm")
    if rmin is not None and rmax is not None:
        if rmin <= rain <= rmax:
            reasons.append(f"Rainfall ({rain:.0f} mm) fits the crop’s needs ({rmin}–{rmax} mm).")
        elif rain < rmin:
            reasons.append(f"Rainfall ({rain:.0f} mm) is lower than recommended ({rmin} mm). Irrigation may be needed.")
        else:
            reasons.append(f"Rainfall ({rain:.0f} mm) is higher than typical ({rmax} mm).
