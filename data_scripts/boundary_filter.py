import geopandas as gpd

# Load the GeoJSON files
region_data = gpd.read_file("./data/Providence/raw_providence_places.geojson")  # Your specific data
boundary_data = gpd.read_file("./data/Providence/providence_boundaries.geojson")  # The boundaries

# Ensure both datasets use the same CRS
if region_data.crs != boundary_data.crs:
    region_data = region_data.to_crs(boundary_data.crs)

# Perform spatial filtering
# Option 1: Points or polygons entirely within the boundary
filtered_data = region_data[region_data.geometry.within(boundary_data.unary_union)]

# Option 2: Intersecting (for partial overlaps)
# filtered_data = region_data[region_data.geometry.intersects(boundary_data.unary_union)]

# Save the filtered data to a new GeoJSON file
filtered_data.to_file("./data/Providence/filtered_providence_places.geojson", driver="GeoJSON")

print("Filtered data saved to 'filtered_data.geojson'")