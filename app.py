import streamlit as st
from farm_rotation.services import analyze_farm

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
        # Simple green intensity based on score
        green = int(255 * (r["score"] / 100))
        color = f"rgb(0, {green}, 0)"
        
        st.markdown(
            f"""
            <div style="padding:10px; margin:5px 0; background-color:{color}20; border-left:5px solid {color};">
                <b>{i}. {r['crop']}</b> — Score: {r['score']}/100
                {" (N-fixing)" if r.get("nitrogen_fixing") else ""}
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("Enter a location and click Analyze.")
