import json

def calculate_non_null_percentage(geojson_path, attribute_name):
    """
    Calculate the percentage of entries in a GeoJSON file where a specified attribute is not null or an empty string.
    
    Args:
        geojson_path (str): Path to the GeoJSON file.
        attribute_name (str): The attribute to check.

    Returns:
        float: The percentage of entries with the attribute not null or empty.
    """
    try:
        # Load the GeoJSON file
        with open(geojson_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Ensure the file has 'features'
        if 'features' not in data or not isinstance(data['features'], list):
            raise ValueError("Invalid GeoJSON file: 'features' key missing or invalid.")
        
        features = data['features']
        total_entries = len(features)
        if total_entries == 0:
            raise ValueError("The GeoJSON file contains no features.")
        
        # Count entries where the attribute is not null or empty
        non_null_count = sum(
            1 for feature in features
            if feature.get('properties', {}).get(attribute_name) not in [None, ""]
        )
        
        # Calculate percentage
        percentage = (non_null_count / total_entries) * 100
        return percentage
    
    except FileNotFoundError:
        print(f"Error: File not found at path {geojson_path}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
geojson_file = './data/Providence/raw_providence_segments.geojson'
attribute = 'connector_id'

percentage = calculate_non_null_percentage(geojson_file, attribute)
if percentage is not None:
    print(f"The percentage of entries where '{attribute}' is not null or empty is {percentage:.2f}%.")
