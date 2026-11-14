import streamlit as st
import folium
from streamlit_folium import st_folium
from farm_rotation.services import analyze_farm, explain_crop
from farm_rotation.adapters.nasa_power import get_climate
import pandas as pd

st.set_page_config(page_title="Farm Rotation", layout="wide")
st.title("Farm Rotation Decision Support")

# Sidebar
st.sidebar.header("Location")
lat = st.sidebar.number_input("Latitude", value=41.6, format="%.4f")
lon = st.sidebar.number_input("Longitude", value=-93.6, format="%.4f")

st.sidebar.header("Soil (optional)")
soil_type = st.sidebar.selectbox("Soil type", ["Loam", "Clay", "Sandy", "Silt", "Unknown"])
drainage = st.sidebar.selectbox("Drainage", ["Good", "Moderate", "Poor"])
ph = st.sidebar.slider("Soil pH", 4.0, 8.5, 6.5)

soil_manual = {
    "soil_type": soil_type,
    "drainage": drainage,
    "ph": ph,
}

st.sidebar.header("Priorities")
w_climate = st.sidebar.slider("Climate fit", 0.0, 1.0, 0.6)
w_soil = st.sidebar.slider("Soil health", 0.0, 1.0, 0.25)
w_water = st.sidebar.slider("Water conservation", 0.0, 1.0, 0.15)

weights = {
    "climate": w_climate,
    "soil_health": w_soil,
    "water": w_water,
}

st.sidebar.header("Filters")
min_score = st.sidebar.slider("Minimum score", 0, 100, 50)
only_nfix = st.sidebar.checkbox("Nitrogen-fixing only", value=False)
category = st.sidebar.selectbox(
    "Category",
    ["All", "Cereal", "Legume", "Oilseed", "Root/Tuber", "Cover Crop", "Forage/Legume"]
)

m = folium.Map(location=[lat, lon], zoom_start=6)

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching data and scoring crops..."):
        data = analyze_farm(lat, lon, soil_manual, weights)

    # Error handling
    if not data.get("success"):
        st.error(f"Error: {data.get('error', 'Unknown error')}")
        st.stop()

    results = data["crops"]
