import streamlit as st
import folium
from streamlit_folium import st_folium
from farm_rotation.services import analyze_farm, explain_crop
from farm_rotation.adapters.nasa_power import get_climate

st.set_page_config(page_title="Farm Rotation", layout="wide")
st.title("Farm Rotation Decision Support")

# Sidebar filters
st.sidebar.header("Location")
lat = st.sidebar.number_input("Latitude", value=41.6, format="%.4f")
lon = st.sidebar.number_input("Longitude", value=-93.6, format="%.4f")

st.sidebar.header("Filters")
min_score = st.sidebar.slider("Minimum score", 0, 100, 50)
only_nfix = st.sidebar.checkbox("Nitrogen-fixing only", value=False)
category = st.sidebar.selectbox(
    "Category",
    ["All", "Cereal", "Legume", "Oilseed", "Root/Tuber", "Cover Crop", "Forage/Legume"]
)

# Create map
m = folium.Map(location=[lat, lon], zoom_start=6)

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching NASA data and scoring crops..."):
        results = analyze_farm(lat, lon)
    
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
        # Colored marker for best result
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

        # Results list
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
               
