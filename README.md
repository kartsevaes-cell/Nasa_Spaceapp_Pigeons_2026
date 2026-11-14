
# Farm Rotation

Decision-support tool for crop rotations using NASA data, soil information, and farmer priorities.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py




**`farm_rotation/config.py`**
```python
# NASA POWER API base URL
POWER_BASE_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"

# Default scoring weights
DEFAULT_WEIGHTS = {
    "climate": 0.5,
    "soil_health": 0.3,
    "priority": 0.2,
}
