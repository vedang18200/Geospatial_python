import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the simplified GeoJSON file
geojson_path = 'V:\Geospatial\simplified_geojson.geojson'  # Path to your simplified GeoJSON
districts = gpd.read_file(geojson_path)

# Example Rainfall Data (Replace with actual data)
rainfall_data = pd.DataFrame({
    'district': ['Bihar', 'Haryana', 'Assam', 'Maharashtra'],  # Replace with actual district names
    'rainfall': [200, 300, 150, 250]  # Rainfall in mm
})

# Merge the GeoJSON data with the rainfall data
districts = districts.merge(rainfall_data, left_on='NAME_1', right_on='district', how='left')

# Plotting
fig, ax = plt.subplots(figsize=(15, 15))
districts.boundary.plot(ax=ax, linewidth=1)  # Plot boundaries
districts.plot(column='rainfall', ax=ax, cmap='YlGnBu', legend=True, legend_kwds={'label': "Rainfall (mm)"})

# Adding Title and Axis Labels
plt.title('Rainfall Heatmap of India by District', fontsize=18)
plt.axis('off')  # Hide axis
plt.show()
