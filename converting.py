import json
from shapely.geometry import shape, mapping, MultiPolygon

# Load the GeoJSON file
input_file = "static\data\map.geojson"  # Replace with your file path
output_file = "district.geojson"

with open(input_file, 'r', encoding='utf-8') as file:
    geojson_data = json.load(file)

# Simplify geometries
for feature in geojson_data['features']:
    geometry = feature['geometry']
    if geometry['type'] == 'MultiPolygon':
        # Convert MultiPolygon to the largest Polygon
        multi_polygon = shape(geometry)
        if isinstance(multi_polygon, MultiPolygon):
            largest_polygon = max(multi_polygon.geoms, key=lambda g: g.area)
            feature['geometry'] = mapping(largest_polygon)

# Save the simplified GeoJSON
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(geojson_data, file)

print(f"Simplified GeoJSON saved to {output_file}")









# rainfall_data = pd.DataFrame({
#     'district': ['Bihar', 'Haryana', 'Assam', 'Maharashtra'],  # Replace with actual district names
#     'rainfall': [200, 300, 150, 250]  # Rainfall in mm
# })