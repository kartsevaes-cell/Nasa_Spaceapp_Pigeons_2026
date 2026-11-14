import streamlit as st
import pandas as pd
from farm_rotation.services import analyze_farm, explain_crop
from farm_rotation.adapters.nasa_power import get_climate

st.set_page_config(page_title="Farm Rotation", layout="wide")
st.title("Farm Rotation Decision Support")

# Session state
if "results_ready" not in st.session_state:
    st.session_state.results_ready = False
if "filtered" not in st.session_state:
    st.session_state.filtered = []
if "landscape" not in st.session_state:
    st.session_state.landscape = {}
if "rotations" not in st.session_state:
    st.session_state.rotations = []

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

st.write(f"**Selected coordinates:** {lat}, {lon}")

# Analyze button
if st.sidebar.button("Analyze"):
    with st.spinner("Fetching data and scoring crops..."):
        data = analyze_farm(lat, lon, soil_manual, weights)

    if not data.get("success"):
        st.error(f"Error: {data.get('error', 'Unknown error')}")
        st.stop()

    results = data["crops"]
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

    st.session_state.filtered = filtered
    st.session_state.landscape = data["landscape"]
    st.session_state.rotations = data["rotations"]
    st.session_state.results_ready = True

# Always show results if we have them
if st.session_state.results_ready and st.session_state.filtered:
    landscape = st.session_state.landscape
    filtered = st.session_state.filtered
    rotations = st.session_state.rotations

    st.success(f"Terrain: {landscape.get('terrain', 'Unknown')} ({landscape.get('elevation_m', '?')} m)")

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

    # Explanation
    st.subheader("Explanation")
    crop_names = [r["crop"] for r in filtered[:10]]
    selected = st.selectbox("Choose a crop", ["-- select --"] + crop_names, key="explain_select")

    if selected != "-- select --":
        selected_crop = next(r for r in filtered if r["crop"] == selected)
        score = selected_crop["score"]
        crop_data = selected_crop.get("crop_data", {})

        lines = [f"{selected} scored {score}/100."]
        if score >= 80:
            lines.append("This is a strong match for the location.")
        elif score >= 60:
            lines.append("This is a reasonable option.")
        else:
            lines.append("This crop is not well suited here.")

        tmin = crop_data.get("temp_min_c")
        tmax = crop_data.get("temp_max_c")
        if tmin is not None and tmax is not None:
            lines.append(f"Preferred temperature: {tmin}–{tmax}°C.")

        rmin = crop_data.get("rainfall_min_mm")
        rmax = crop_data.get("rainfall_max_mm")
        if rmin is not None and rmax is not None:
            lines.append(f"Preferred rainfall: {rmin}–{rmax} mm.")

        if selected_crop.get("nitrogen_fixing"):
            lines.append("It fixes nitrogen and helps soil health.")

        st.info(" ".join(lines))

    st.subheader("Suggested Rotations (3 years)")
    for idx, rot in enumerate(rotations[:3], 1):
        names = " → ".join([c["crop"] for c in rot])
        avg_score = sum(c["score"] for c in rot) / len(rot)
        st.markdown(f"**Rotation {idx}:** {names}  \nAverage score: {avg_score:.0f}/100")

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
