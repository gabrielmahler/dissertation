import geopandas as gpd

city = "cambridge"
props = ['addresses', 'buildingparts', 'buildings', 'connectors', 'places', 'segments']

# Load the GeoJSON files
boundary_data = gpd.read_file(f"./data/{city}/{city}_boundaries.geojson")

for prop in props:
    region_data = gpd.read_file(f"./data/{city}/raw_{city}_{prop}.geojson")
    if region_data.crs != boundary_data.crs:
        region_data = region_data.to_crs(boundary_data.crs)
    filtered_data = region_data[region_data.geometry.within(boundary_data.unary_union)]
    if not filtered_data.empty:
        filtered_data.to_file(f"./data/{city}/filtered_{city}_{prop}.geojson", driver="GeoJSON")
    else:
        print(f"No data found for {prop}")
print("done")

# region_data = gpd.read_file("./data/Providence/raw_providence_connectors.geojson")  # Your specific data
# boundary_data = gpd.read_file("./data/Providence/providence_boundaries.geojson")  # The boundaries

# # Ensure both datasets use the same CRS
# if region_data.crs != boundary_data.crs:
#     region_data = region_data.to_crs(boundary_data.crs)

# # Perform spatial filtering
# # Option 1: Points or polygons entirely within the boundary
# filtered_data = region_data[region_data.geometry.within(boundary_data.unary_union)]

# # Option 2: Intersecting (for partial overlaps)
# # filtered_data = region_data[region_data.geometry.intersects(boundary_data.unary_union)]

# # Save the filtered data to a new GeoJSON file
# filtered_data.to_file("./data/Providence/filtered_cambridge_connectors.geojson", driver="GeoJSON")

# print("Filtered data saved to 'filtered_data.geojson'")