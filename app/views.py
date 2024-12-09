from django.shortcuts import render
import json
import pydeck as pdk
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from .utils import get_climate_data



def index(request):
    return render(request, 'index.html')

def map(request):
    return render(request, 'Indian_map.html')

def rainfall_analysis(request):
    # Load GeoJSON file
    geojson_path = 'V:/Geospatial/static/data/simplified_geojson.geojson'
    districts = gpd.read_file(geojson_path)

    csv_path = 'V:\Geospatial\static\data\Rain_data.csv'
    rainfall_data = pd.read_csv(csv_path)

    # Merge data
    districts = districts.merge(rainfall_data, left_on='NAME_1', right_on='states', how='inner')

    # Prepare data for Pydeck
    districts['centroid'] = districts.geometry.centroid
    districts['lon'] = districts.centroid.x
    districts['lat'] = districts.centroid.y
    data = districts[['states', 'rainfall', 'lon', 'lat']]

    # Create Pydeck layer for 3D bar
    layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="rainfall",
        elevation_scale=10,
        radius=30000,
        get_fill_color=[0, 0, 255],  # Blue color
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
        tooltip={"text": "{states}: {rainfall} mm"}
    )
    map_html = deck.to_html(as_string=True)  # Generate HTML as a string

    # Pass the HTML to the template
    return render(request, 'Rainfall_analysis.html', {'map_html': map_html})


import folium
from folium.plugins import HeatMap
from django.shortcuts import render
from .utils import get_climate_data  

def heatmap(request):
    # List of cities you want to monitor for climate data
    cities = ['maharashtra']

    # Fetch climate data for each city
    heat_data = []
    for city in cities:
        climate_info = get_climate_data(city)
        if climate_info:
           
            heat_data.append([climate_info['latitude'], climate_info['longitude'], climate_info['temperature']])

    
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  

    
    HeatMap(heat_data).add_to(m)

    map_html = m._repr_html_()

    return render(request, 'heatmap.html', {'map_html': map_html})



def bussiness(request):
     # Load GeoJSON file
    geojson_path = 'V:/Geospatial/static/data/simplified_geojson.geojson'
    districts = gpd.read_file(geojson_path)

    csv_path = 'V:/Geospatial/static/data/bussiness.csv'
    rainfall_data = pd.read_csv(csv_path)

    # Merge data
    districts = districts.merge(rainfall_data, left_on='NAME_1', right_on='state', how='inner')

    # Prepare data for Pydeck
    districts['centroid'] = districts.geometry.centroid
    districts['lon'] = districts.centroid.x
    districts['lat'] = districts.centroid.y
    data = districts[['state', 'sales', 'lon', 'lat']]

    # Create Pydeck layer for 3D bar
    layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="sales",
        elevation_scale=0.0001,
        radius=30000,
        get_fill_color="[255, 140, 0, 200]",  
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
       tooltip={"text": "{state}: ₹{sales}"}
    )
    map_html = deck.to_html(as_string=True) 

    # Pass the HTML to the template
    return render(request, 'Bussiness.html', {'map_html': map_html})
