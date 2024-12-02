import duckdb
import osmnx as ox
import geopandas as gpd

providence = ["./data/Providence/providence_boundaries.geojson" "providence"] 
cambridge = ["./data/Cambridge/cambridge_boundaries.geojson", "cambridge"]
coordinates = cambridge

gdf = gpd.read_file(coordinates[0])
boundary = gdf.unary_union
boundary_wkt = boundary.wkt
print("Loaded wkt, quering..")

# Buildings
# duckdb.sql(f"""
# LOAD spatial; --noqa
# SET azure_storage_connection_string = 'DefaultEndpointsProtocol=https;AccountName=overturemapswestus2;AccountKey=;EndpointSuffix=core.windows.net';

# COPY(
#   SELECT
#     id,
#     CAST(bbox AS JSON) AS bbox,
#     names.primary AS name,
#     subtype,
#     class,
#     num_floors,
#     height,
#   FROM read_parquet('azure://release/2024-11-13.0/theme=buildings/type=building/*', filename=true, hive_partitioning=1)
#   AND ST_Intersects(geometry, ST_GeomFromText('{boundary_wkt}'))
#   LIMIT 10
# ) TO '{coordinates[1]}_buildings.geojsonseq' WITH (FORMAT GDAL, DRIVER 'GeoJSONSeq');
# """)

# Places
duckdb.sql(f"""
LOAD spatial; 

SET s3_region='eu-west-1';

COPY(                                  
    SELECT
       id,
       CAST(bbox AS JSON) AS bbox,
       names.primary AS name,
       confidence,
       CAST(categories AS JSON) AS categories,
    FROM read_parquet('s3://overturemaps-us-west-2/release/2024-11-13.0/theme=places/type=place/*', filename=true, hive_partitioning=1)
    WHERE ST_Intersects(geometry, ST_GeomFromText('{boundary_wkt}'))

) TO '{coordinates[1]}_places.geojson' WITH (FORMAT GDAL, DRIVER 'GeoJSON');""")