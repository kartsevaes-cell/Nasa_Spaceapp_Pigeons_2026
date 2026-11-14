import streamlit as st
from farm_rotation.services import analyze_farm, explain_crop
from farm_rotation.adapters.nasa_power import get_climate

st.set_page_config(page_title="Farm Rotation", layout="wide")
st.title("Farm Rotation Decision Support")

st.sidebar.header("Location")
lat = st.sidebar.number_input("Latitude", value=41.6, format="%.4f")
lon = st.sidebar.number_input("Longitude", value=-93.6, format="%.4f")

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching NASA data and scoring crops..."):
        results = analyze_farm(lat, lon)
    
    st.subheader("Top Recommendations")
    
    for i, r in enumerate(results[:10], 1):
        # Green intensity based on score
        green = int(200 * (r["score"] / 100)) + 55
        color = f"rgb(0, {green}, 0)"
        
        st.markdown(
            f"""
            <div style="padding:12px; margin:6px 0; background-color:{color}22; 
                        border-left:6px solid {color}; border-radius:4px;">
                <b>{i}. {r['crop']}</b> 
                <span style="float:right;">{r['score']}/100</span><br>
                {"Nitrogen-fixing" if r.get("nitrogen_fixing") else ""}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Why button for this crop
        if st.button(f"Why {r['crop']}?", key=r['crop']):
            climate = get_climate(lat, lon)
            explanation = explain_crop(r["crop_data"], r["score"], climate)
            st.info(explanation)

else:
    st.info("Enter a location and click Analyze.")
