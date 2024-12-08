import folium
import geopandas as gpd
import pandas as pd

# Load GeoJSON file
geojson_path = 'V:/Geospatial/static/data/simplified_geojson.geojson'
districts = gpd.read_file(geojson_path)

# Example Temperature Data for Last Year and This Year
temperature_data = pd.DataFrame({
    'district': ['Bihar', 'Haryana', 'Assam', 'Maharashtra', 'AndamanandNicobar', 'AndhraPradesh'],
    'last_year_temp': [30, 32, 29, 34, 28, 31],  # Example temperatures for last year
    'this_year_temp': [31, 33, 30, 35, 29, 32]   # Example temperatures for this year
})

# Merge temperature data with districts GeoJSON
districts = districts.merge(temperature_data, left_on='NAME_1', right_on='district')

# Create maps for last year and this year
m_last_year = folium.Map(location=[20.5937, 78.9629], zoom_start=5, control_scale=True, tiles='cartodb positron')
m_this_year = folium.Map(location=[20.5937, 78.9629], zoom_start=5, control_scale=True, tiles='cartodb positron')

# Add choropleth layers or markers for temperature comparison
# For simplicity, we'll add circle markers that represent the temperature of each district
for _, row in districts.iterrows():
    lat = row.geometry.centroid.y
    lon = row.geometry.centroid.x
    district_name = row['district']
    last_year_temp = row['last_year_temp']
    this_year_temp = row['this_year_temp']
    
    # Adding markers for last year's temperature
    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"{district_name} (Last Year): {last_year_temp}°C"
    ).add_to(m_last_year)

    # Adding markers for this year's temperature
    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=f"{district_name} (This Year): {this_year_temp}°C"
    ).add_to(m_this_year)

# Save the two maps as HTML files
m_last_year.save('last_year_map.html')
m_this_year.save('this_year_map.html')
