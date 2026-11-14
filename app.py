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

# Map with CartoDB tiles (avoids OpenStreetMap blocking)
m = folium.Map(
    location=[lat, lon],
    zoom_start=6,
    tiles="CartoDB positron",
    attr="© OpenStreetMap contributors © CARTO"
)

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching data and scoring crops..."):
        data = analyze_farm(lat, lon, soil_manual, weights)

    # Error handling
    if not data.get("success"):
        st.error(f"Error: {data.get('error', 'Unknown error')}")
        st.stop()

    results = data["crops"]
    landscape = data["landscape"]
    rotations = data["rotations"]

    st.sidebar.success(f"Terrain: {landscape['terrain']} ({landscape['elevation_m']} m)")

    # Apply filters
    filtered = []
    for r in results:
        if r["score"] < min_score:
            continue
        if only_nfix and not r.get("nitrogen_fixing"):
            continue
        crop_cat = str(r["crop_data"].get("category", "")).lower()
        if category != "All" and category.lower() not in crop_cat:
            continue
        filtered.append(r)

    if not filtered:
        st.warning("No crops match the filters.")
    else:
        # Colored marker
        top = filtered[0]
        score = top["score"]
        green = int(200 * (score / 100)) + 55
        color = f"#{0:02x}{green:02x}{0:02x}"

        folium.CircleMarker(
            location=[lat, lon],
            radius=15,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"Best: {top['crop']} ({score}/100)"
        ).add_to(m)

        st.info(f"Location terrain: **{landscape['terrain']}** — Elevation: {landscape['elevation_m']} m")

        # Results
        st.subheader(f"Top Recommendations ({len(filtered)} crops)")
        for i, r in enumerate(filtered[:10], 1):
            green = int(200 * (r["score"] / 100)) + 55
            color = f"rgb(0, {green}, 0)"
            st.markdown(
                f"""
                <div style="padding:12px; margin:6px 0; background-color:{color}22; 
                            border-left:6px solid {color}; border-radius:4px;">
                    <b>{i}. {r['crop']}</b> 
                    <span style="float:right;">{r['score']}/100</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Why {r['crop']}?", key=r['crop']):
                climate = get_climate(lat, lon)
                explanation = explain_crop(r["crop_data"], r["score"], climate)
                st.info(explanation)

        # Rotations
        st.subheader("Suggested Rotations (3 years)")
        for idx, rot in enumerate(rotations[:3], 1):
            names = " → ".join([c["crop"] for c in rot])
            avg_score = sum(c["score"] for c in rot) / len(rot)
            st.markdown(f"**Rotation {idx}:** {names}  \nAverage score: {avg_score:.0f}/100")

        # Export
        export_df = pd.DataFrame([
            {"crop": r["crop"], "score": r["score"], "nitrogen_fixing": r["nitrogen_fixing"]}
            for r in filtered
        ])
        csv = export_df.to_csv(index=False)
        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name="crop_recommendations.csv",
            mime="text/csv",
        )
else:
    folium.Marker([lat, lon], popup="Selected location").add_to(m)

st_folium(m, width=700, height=450)
