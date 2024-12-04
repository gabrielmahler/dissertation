import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np

# Paths
parquet_folder = './2024-11-19/places/'  # Folder containing Parquet files
# city_geojson_path = './data/Providence/providence_boundaries.geojson'  # GeoJSON file with city boundaries
# output_geojson_path = 'providence_foursquare.geojson'  # Output GeoJSON file
city_geojson_path = './data/cambridge/cambridge_boundaries.geojson'  # GeoJSON file with city boundaries
output_geojson_path = 'cambridge_foursquare.geojson'  # Output GeoJSON file

# Load city boundaries
city_boundary = gpd.read_file(city_geojson_path)

# Ensure the boundary is in a single geometry (in case it's a MultiPolygon)
city_boundary = city_boundary.unary_union

# Process Parquet files
filtered_entries = []
for parquet_file in os.listdir(parquet_folder):
    if parquet_file.endswith('.parquet'):
        # Load parquet file into a DataFrame
        df = pd.read_parquet(os.path.join(parquet_folder, parquet_file))
        
        # Check if latitude and longitude columns exist
        if 'latitude' in df.columns and 'longitude' in df.columns:
            # Create a GeoDataFrame with geometries
            gdf = gpd.GeoDataFrame(
                df,
                geometry=[Point(xy) for xy in zip(df['longitude'], df['latitude'])],
                crs="EPSG:4326"  # Ensure CRS is WGS84
            )
            
            # Filter points within the city boundary
            filtered = gdf[gdf.geometry.within(city_boundary)]
            
            # Collect filtered entries
            if not filtered.empty:
                filtered_entries.append(filtered)
        print(f"Processed {parquet_file}")

# Combine all filtered entries into a single GeoDataFrame
if filtered_entries:
    result_gdf = gpd.GeoDataFrame(pd.concat(filtered_entries, ignore_index=True))
    for col in result_gdf.columns:
        if result_gdf[col].apply(lambda x: isinstance(x, np.ndarray)).any():
            # Convert ndarray to list
            result_gdf[col] = result_gdf[col].apply(
                lambda x: x.tolist() if isinstance(x, np.ndarray) else x
            )
    for col in result_gdf.columns:
        if result_gdf[col].apply(lambda x: isinstance(x, list)).any():
            # Convert lists to strings (or apply another strategy)
            result_gdf[col] = result_gdf[col].apply(
                lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x
            )
    # Save to GeoJSON
    result_gdf.to_file(output_geojson_path, driver='GeoJSON')
    print(f"Filtered entries saved to {output_geojson_path}")
else:
    print("No entries found within the city boundaries.")