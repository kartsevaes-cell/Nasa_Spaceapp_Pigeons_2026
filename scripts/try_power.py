from farm_rotation.adapters.nasa_power import get_climate

# Example: Iowa, USA
result = get_climate(lat=41.6, lon=-93.6)
print(result)
