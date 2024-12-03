from django.shortcuts import render
import json
import pydeck as pdk
import pandas as pd
import geopandas as gpd
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def map(request):
    return render(request, 'Indian_map.html')


def rainfall_analysis(request):
    # Load GeoJSON file
    geojson_path = 'V:\Geospatial\static\data\simplified_geojson.geojson'
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
        get_elevation="rainfall",
        elevation_scale=10,
        radius=30000,
        get_fill_color=[255, 165, 0],
        pickable=True,
    )

    # View
    view_state = pdk.ViewState(
        latitude=20.5937, longitude=78.9629, zoom=4, pitch=45
    )

    # Render Pydeck map as HTML
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{district}: {rainfall} mm"}
    )
    map_html = deck.to_html(as_string=True)  # Generate HTML as a string

    # Pass the HTML to the template
    return render(request, 'Rainfall_analysis.html', {'map_html': map_html})