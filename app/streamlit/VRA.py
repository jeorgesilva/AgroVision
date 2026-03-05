# app/streamlit/VRA.py
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="VRA Map", page_icon="🗺️")

st.title("🗺️ Variable-Rate Application (VRA) Map")

st.write("This page displays the generated VRA map.")

# Path to the GeoJSON file
vra_map_path = "outputs/vra/vra.geojson"

try:
    # Read the GeoJSON file
    vra_gdf = gpd.read_file(vra_map_path)

    # Create a Folium map centered on the VRA data
    m = folium.Map(location=[vra_gdf.centroid.y.mean(), vra_gdf.centroid.x.mean()], zoom_start=15)

    # Add the VRA polygons to the map
    folium.GeoJson(
        vra_gdf,
        style_function=lambda feature: {
            "fillColor": "red",
            "color": "red",
            "weight": 2,
            "fillOpacity": 0.5,
        },
        tooltip=folium.GeoJsonTooltip(fields=["weed_density"], aliases=["Weed Density:"]),
    ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=725)

except FileNotFoundError:
    st.error(f"VRA map not found at {vra_map_path}. Please run the VRA mapping pipeline first.")
except Exception as e:
    st.error(f"An error occurred: {e}")
