import streamlit as st
import pandas as pd
from farm_rotation.services import analyze_farm, explain_crop
from farm_rotation.adapters.nasa_power import get_climate

st.set_page_config(page_title="Farm Rotation", layout="wide")
st.title("Farm Rotation Decision Support")

# Session state
if "data" not in st.session_state:
    st.session_state.data = None
if "filtered" not in st.session_state:
    st.session_state.filtered = []
if "explanation" not in st.session_state:
    st.session_state.explanation = None
if "explain_crop_name" not in st.session_state:
    st.session_state.explain_crop_name = None

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

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching data and scoring crops..."):
        data = analyze_farm(lat, lon, soil_manual, weights)

    if not data.get("success"):
        st.error(f"Error: {data.get('error', 'Unknown error')}")
        st.stop()

    st.session_state.data = data
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
    st.session_state.explanation = None  # clear old explanation

# Show results
if st.session_state.data and st.session_state.filtered:
    data = st.session_state.data
    filtered = st.session_state.filtered
    landscape = data["landscape"]
    rotations = data["rotations"]

    st.success(f"Terrain: {landscape['terrain']} ({landscape['elevation_m']} m)")

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

        if st.button(f"Why {r['crop']}?", key=f"why_{i}_{r['crop']}"):
            try:
                climate = get_climate(lat, lon)
                explanation = explain_crop(r["crop_data"], r["score"], climate)
                st.session_state.explanation = explanation
                st.session_state.explain_crop_name = r["crop"]
            except Exception as e:
                st.session_state.explanation = f"Could not generate explanation: {e}"
                st.session_state.explain_crop_name = r["crop"]

    # Show the explanation if one was requested
    if st.session_state.explanation:
        st.info(f"**Why {st.session_state.explain_crop_name}?**\n\n{st.session_state.explanation}")

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
