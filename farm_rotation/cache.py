import sqlite3
import json
from pathlib import Path

DB_PATH = Path("data/farm.db")

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS climate_cache (
            lat REAL,
            lon REAL,
            data TEXT,
            PRIMARY KEY (lat, lon)
        )
    """)
    conn.commit()
    conn.close()

def get_cached_climate(lat: float, lon: float):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    # Round to 2 decimals to group nearby points
    row = conn.execute(
        "SELECT data FROM climate_cache WHERE lat = ? AND lon = ?",
        (round(lat, 2), round(lon, 2))
    ).fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def save_climate(lat: float, lon: float, data: dict):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO climate_cache (lat, lon, data) VALUES (?, ?, ?)",
        (round(lat, 2), round(lon, 2), json.dumps(data))
    )
    conn.commit()
    conn.close()
