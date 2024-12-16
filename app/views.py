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

import folium
from folium.plugins import HeatMap
from django.shortcuts import render
from .utils import get_climate_data

def heatmap(request):
    # List of cities you want to monitor for climate data
    cities = [
        'Delhi', 'UttarPradesh', 'Rajasthan', 'Maharashtra', 'Gujarat', 'Goa',
       
    ]

    # Fetch climate data for each city
    heat_data = []
    for city in cities:
        climate_info = get_climate_data(city)
        if climate_info:
            # Add latitude, longitude, and temperature to the heatmap data
            heat_data.append([climate_info['latitude'], climate_info['longitude'], climate_info['temperature']])

    # Create the map centered around India
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    # Add the heatmap layer
    HeatMap(heat_data).add_to(m)

    # Add CircleMarkers with tooltips showing temperature at each location
    for city in cities:
        climate_info = get_climate_data(city)
        if climate_info:
            folium.CircleMarker(
                location=[climate_info['latitude'], climate_info['longitude']],
                radius=10,  # Size of the circle marker
                color='blue',  # Color of the marker
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                tooltip=f"State: {city}<br>Temperature: {climate_info['temperature']}°C"
            ).add_to(m)

    # Generate HTML representation of the map
    map_html = m._repr_html_()

    return render(request, 'heatmap.html', {'map_html': map_html})




import geopandas as gpd
import pandas as pd
import pydeck as pdk
from django.shortcuts import render
import geopandas as gpd
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go
from plotly.offline import plot
from django.shortcuts import render

import geopandas as gpd
import pandas as pd
import plotly.express as px
from django.shortcuts import render

def bussiness(request):
    geojson_path = 'V:/Geospatial/static/data/simplified_geojson.geojson'
    districts = gpd.read_file(geojson_path)

    csv_path = 'V:/Geospatial/static/data/Dmart.csv'
    sales_data = pd.read_csv(csv_path)

    # Merge data
    districts = districts.merge(sales_data, left_on='NAME_1', right_on='state', how='inner')
    districts['centroid'] = districts.geometry.centroid
    districts['lon'] = districts.centroid.x
    districts['lat'] = districts.centroid.y
    data = districts[['state', 'sales', 'lon', 'lat', 'trending']]

    # Pydeck for 3D map
    layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="sales",
        elevation_scale=0.00001,
        radius=30000,
        get_fill_color="[255, 140, 0, 200]",
        pickable=True,
    )
    view_state = pdk.ViewState(
        latitude=20.5937, longitude=78.9629, zoom=4, pitch=45
    )
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{state}: ₹{sales}\\nTrending: {trending}"}
    )
    map_html = deck.to_html(as_string=True)

    context = {
        'map_html': map_html,
        'states': sales_data['state'].unique(),  # Provide state names for dropdowns
    }

    # Handle comparison request
    if request.method == "POST":
        state1 = request.POST.get('state1')
        state2 = request.POST.get('state2')

        if state1 and state2:
            comparison_data = sales_data[sales_data['state'].isin([state1, state2])]
            # Generate a comparison chart using Plotly
            fig = px.bar(
                comparison_data,
                x='state',
                y='sales',
                color='state',
                text='sales',
                title=f"Comparison of Sales: {state1} vs {state2}",
                labels={'sales': 'Sales (₹)', 'state': 'State'},
            )
            fig.update_traces(texttemplate='₹%{text}', textposition='outside')
            fig.update_layout(yaxis_title='Sales (₹)', xaxis_title='State')

            # Render Plotly chart as HTML
            context['plot_div'] = fig.to_html(full_html=False)

    return render(request, 'Bussiness.html', context)


from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
import folium
from folium.plugins import HeatMap
import json
import os

def hmap(request):
    map_html = None
    if request.method == 'POST' and request.FILES['csv_file']:
        # Get the uploaded CSV file
        csv_file = request.FILES['csv_file']
        
        # Save it temporarily to the filesystem under the 'media/' folder
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(csv_file.name, csv_file)
        file_url = fs.url(filename)

        # Read the CSV file
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        data = pd.read_csv(file_path)  # Load CSV from media folder

        # Load the GeoJSON file (assuming it's stored in the 'static' folder)
        with open('V:/Geospatial/static/data/simplified_geojson.geojson', 'r') as f:
            geojson_data = json.load(f)

        # Process the CSV and GeoJSON data...
        state_coords = {}
        for feature in geojson_data['features']:
            state_name = feature['properties']['NAME_1']
            
            # Handle polygon geometry and get the centroid
            if feature['geometry']['type'] == 'Polygon':
                centroid = feature['geometry']['coordinates'][0]
            elif feature['geometry']['type'] == 'MultiPolygon':
                centroid = feature['geometry']['coordinates'][0][0]
            else:
                continue  # Skip non-polygon types
            
            # Calculate the average latitude and longitude
            latitude = sum([point[1] for point in centroid]) / len(centroid)
            longitude = sum([point[0] for point in centroid]) / len(centroid)
            
            # Store the coordinates in the dictionary
            state_coords[state_name] = [latitude, longitude]

        # Prepare heatmap data
        heat_data = []
        for index, row in data.iterrows():
            if row['states'] in state_coords:
                lat, lon = state_coords[row['states']]
                heat_data.append([lat, lon, row['temperature']])

        # Create the base map
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        HeatMap(heat_data).add_to(m)
        map_html = m._repr_html_()

    return render(request, 'hmap.html', {'map_html': map_html})



import plotly.express as px
from django.shortcuts import render, redirect
def compare_states(request):
    if request.method == "POST":
        state1 = request.POST.get('state1')
        state2 = request.POST.get('state2')

        csv_path = 'V:/Geospatial/static/data/Dmart.csv'
        sales_data = pd.read_csv(csv_path)

        if state1 and state2:
            comparison_data = sales_data[sales_data['state'].isin([state1, state2])]
            # Generate a comparison chart
            fig = px.bar(
                comparison_data,
                x='state',
                y='sales',
                color='state',
                text='sales',
                title=f"Comparison of Sales: {state1} vs {state2}",
                labels={'sales': 'Sales (₹)', 'state': 'State'},
            )
            fig.update_traces(texttemplate='₹%{text}', textposition='outside')
            fig.update_layout(yaxis_title='Sales (₹)', xaxis_title='State')

            # Render Plotly chart as HTML
            plot_div = fig.to_html(full_html=False)
            return render(request, 'compare.html', {'plot_div': plot_div, 'state1': state1, 'state2': state2})
    return redirect('bussiness')  # Redirect to main page if accessed without POST data



import geopandas as gpd
import pandas as pd
import pydeck as pdk
from django.shortcuts import render, redirect

def realestate_map(request):
    # Load GeoJSON and CSV data
    geojson_path = 'V:/Geospatial/static/data/simplified_geojson.geojson'
    districts = gpd.read_file(geojson_path)

    csv_path = 'V:/Geospatial/static/data/estate.csv'
    realestate_data = pd.read_csv(csv_path)

    # Merge GeoJSON with real estate data
    districts = districts.merge(realestate_data, left_on='NAME_1', right_on='state', how='inner')
    districts['centroid'] = districts.geometry.centroid
    districts['lon'] = districts.centroid.x
    districts['lat'] = districts.centroid.y
    data = districts[['state', 'price', 'rent', 'lon', 'lat']]

    # Create Pydeck layers for house prices and rent prices
    house_price_layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="price",
        elevation_scale=0.001,
        radius=30000,
        get_fill_color="[0, 128, 255, 200]",
        pickable=True,
    )

    rent_price_layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="rent",
        elevation_scale=0.001,
        radius=30000,
        get_fill_color="[255, 99, 71, 200]",
        pickable=True,
    )

    # Configure the map view
    view_state = pdk.ViewState(
        latitude=20.5937, longitude=78.9629, zoom=4, pitch=45
    )
    deck = pdk.Deck(
        layers=[house_price_layer, rent_price_layer],
        initial_view_state=view_state,
        tooltip={"html": "State: {state}<br>House Price: ₹{price}<br>Rent Price: ₹{rent}"}
    )
    map_html = deck.to_html(as_string=True)

    # Pass data to template
    return render(request, 'Realestate.html', {
        'map_html': map_html,
        'states': realestate_data['state'].unique(),  # State names for dropdowns
    })


def compare_realestate(request):
    if request.method == "POST":
        state1 = request.POST.get('state1')
        state2 = request.POST.get('state2')

        csv_path = 'V:/Geospatial/static/data/estate.csv'
        realestate_data = pd.read_csv(csv_path)

        # Filter data for the selected states
        comparison_data = realestate_data[realestate_data['state'].isin([state1, state2])]

        # Calculate price differences
        house_price_diff = (
            comparison_data.loc[comparison_data['state'] == state1, 'price'].values[0] -
            comparison_data.loc[comparison_data['state'] == state2, 'price'].values[0]
        )
        rent_price_diff = (
            comparison_data.loc[comparison_data['state'] == state1, 'rent'].values[0] -
            comparison_data.loc[comparison_data['state'] == state2, 'rent'].values[0]
        )

        return render(request, 'compare_realestate.html', {
            'state1': state1,
            'state2': state2,
            'house_price_diff': house_price_diff,
            'rent_price_diff': rent_price_diff,
        })

    return redirect('Realestate.html') 





import geopandas as gpd
import pandas as pd
import pydeck as pdk
from django.shortcuts import render

def agriculture_map(request):
    # Load GeoJSON and agriculture data
    geojson_path = 'V:/Geospatial/static/data/simplified_geojson.geojson'
    districts = gpd.read_file(geojson_path)

    csv_path = 'V:/Geospatial/static/data/crops.csv'
    agriculture_data = pd.read_csv(csv_path)

    # Merge GeoJSON with agriculture data
    districts = districts.merge(agriculture_data, left_on='NAME_1', right_on='state', how='inner')
    districts['centroid'] = districts.geometry.centroid
    districts['lon'] = districts.centroid.x
    districts['lat'] = districts.centroid.y

    # Prepare data for Pydeck
    data = districts[['state', 'water_quality', 'soil_quality', 'air_quality', 'recommended_crops', 'lon', 'lat']]

    # Create Pydeck layers for visualization
    layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="soil_quality",  # Use soil quality as elevation
        elevation_scale=5000,
        radius=30000,
        get_fill_color="[255, 223, 0, 200]",
        pickable=True,
    )

    # View state configuration
    view_state = pdk.ViewState(
        latitude=20.5937, longitude=78.9629, zoom=4, pitch=45
    )

    # Pydeck map
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"html": "State: {state}<br>Water Quality: {water_quality}<br>Soil Quality: {soil_quality}<br>Air Quality: {air_quality}<br>Recommended Crops: {recommended_crops}"}
    )
    map_html = deck.to_html(as_string=True)

    # Pass data to template
    return render(request, 'crops.html', {
        'map_html': map_html,
        'states': agriculture_data['state'].unique(),
    })

def state_analysis(request, state_name):
    # Load CSV data
    csv_path = 'V:/Geospatial/static/data/crops.csv'
    agriculture_data = pd.read_csv(csv_path)

    # Filter data for the selected state
    state_data = agriculture_data[agriculture_data['state'] == state_name].iloc[0]

    return render(request, 'analysis.html', {
        'state': state_name,
        'water_quality': state_data['water_quality'],
        'soil_quality': state_data['soil_quality'],
        'air_quality': state_data['air_quality'],
        'recommended_crops': state_data['recommended_crops'].split(','),
    })
