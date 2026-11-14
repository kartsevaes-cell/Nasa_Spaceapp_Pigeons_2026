def generate_rotations(results, years=3, max_rotations=5):
    """
    Create simple rotation plans from scored crops.
    Prefers mixing nitrogen-fixing and non-fixing crops.
    """
    if not results:
        return []

    # Separate N-fixing and others
    nfix = [r for r in results if r.get("nitrogen_fixing")]
    others = [r for r in results if not r.get("nitrogen_fixing")]

    rotations = []

    # Generate a few combinations
    for i in range(min(max_rotations, len(results))):
        rotation = []
        for year in range(years):
            if year % 2 == 0 and others:
                rotation.append(others[i % len(others)])
            elif nfix:
                rotation.append(nfix[i % len(nfix)])
            else:
                rotation.append(results[i % len(results)])
        rotations.append(rotation)

    return rotations
