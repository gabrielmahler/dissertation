import osmnx as ox
import geopandas as gpd
import duckdb

# Step 1: Get the boundaries for Providence, RI
def get_city_boundary(city_name, state_name, country_name, output_file):
    # Query OpenStreetMap for the city's boundary
    query = f"{city_name}, {state_name}, {country_name}"
    city_boundary = ox.geocode_to_gdf(query)
    
    # Save the boundary to a GeoJSON file
    city_boundary.to_file(output_file, driver="GeoJSON")
    print(f"Saved city boundaries to {output_file}")

# Step 2: Load the boundary into DuckDB and query
def query_city_boundary(boundary_file):
    # Load the GeoJSON into a GeoPandas DataFrame
    gdf = gpd.read_file(boundary_file)
    
    # Ensure the DataFrame is loaded into DuckDB for querying
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    con.register("city_boundary", gdf)
    
    # Perform a sample spatial query in DuckDB
    result = con.execute("""
        SELECT * 
        FROM city_boundary
        WHERE ST_Area(geometry) > 0
    """).fetchdf()
    
    print("Query result:")
    print(result)

# Run the script
# output_file = "cambridge_boundaries.geojson"
# city = "Cambridge"
# state = "Cambridgeshire"
# country = "UK"
output_file = "prague_boundaries.geojson"
city = "Prague"
state = "Prague"
country = "Czech Republic"

get_city_boundary(city, state, country, output_file)
