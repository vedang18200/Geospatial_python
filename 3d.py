import pydeck as pdk
import pandas as pd
import geopandas as gpd

# Load GeoJSON file
geojson_path = 'V:\Geospatial\simplified_geojson.geojson'
districts = gpd.read_file(geojson_path)

# Example Rainfall Data
rainfall_data = pd.DataFrame({
    'district': ['Bihar', 'Haryana', 'Assam', 'Maharashtra'],  # Replace with actual district names
    'rainfall': [20000, 30000, 15000, 25000]  # Rainfall in mm
})
# Merge data
districts = districts.merge(rainfall_data, left_on='NAME_1', right_on='district')

# Prepare data for Pydeck
districts['centroid'] = districts.geometry.centroid
districts['lon'] = districts.centroid.x
districts['lat'] = districts.centroid.y

data = districts[['district', 'rainfall', 'lon', 'lat']]

# Create Pydeck layer for 3D bar
layer = pdk.Layer(
    "ColumnLayer",
    data=data,
    get_position=["lon", "lat"],
    get_elevation="rainfall",  # Elevation based on rainfall
    elevation_scale=10,
    radius=30000,
    get_fill_color=[255, 165, 0],
    pickable=True,
)

# View
view_state = pdk.ViewState(
    latitude=20.5937, longitude=78.9629, zoom=4, pitch=45
)

# Render map
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{district}: {rainfall} mm"}
)
deck.to_html("rainfall_3d_map.html")
