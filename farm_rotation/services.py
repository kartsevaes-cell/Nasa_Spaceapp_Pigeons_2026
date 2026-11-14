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
            "nitrogen_fixing": crop["nitrogen_fixing"]
        })
    
    return sorted(results, key=lambda x: x["score"], reverse=True)
