import json
from collections import Counter
from itertools import combinations

forbidden = {'id', 'geometry', 'coordinates','at','version','source'}

def analyze_geojson(file_path, output_file):
    # Read the GeoJSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    if "features" not in data:
        raise ValueError("Invalid GeoJSON format: Missing 'features' key.")
    
    features = data["features"]
    total_entries = len(features)

    # Open the output file for writing
    with open(output_file, 'w') as out:
        out.write(f"Total entries: {total_entries}\n\n")

        # Organize data by 'type'
        type_data = {}
        for feature in features:
            feature_type = feature.get("type", "Unknown")
            type_data.setdefault(feature_type, []).append(feature)
        
        # Analyze attributes
        for feature_type, features_of_type in type_data.items():
            out.write(f"--- Analysis for type: {feature_type} ---\n")
            total_features = len(features_of_type)
            out.write(f"Total features of this type: {total_features}\n\n")
            
            attributes = set()
            for feature in features_of_type:
                properties = feature.get("properties", {})
                attributes.update(properties.keys())
            
            # Analyze each attribute
            attribute_values = {attr: [] for attr in attributes}
            for feature in features_of_type:
                properties = feature.get("properties", {})
                for attr in attributes:
                    attribute_values[attr].append(properties.get(attr))
            
            # Individual attribute analysis
            for attribute in attributes:
                if attribute in forbidden:
                    continue
                values = attribute_values[attribute]
                missing_or_null = sum(1 for value in values if value is None)
                percentage = 100 - (missing_or_null / total_features) * 100
                value_counts = Counter(values)

                out.write(f"Attribute: {attribute}\n")
                out.write(f"  Missing or null: {missing_or_null} entries\n")
                out.write(f"  Percentage: {percentage:.2f}%\n")
                out.write(f"  All values (including counts):\n")
                for value, count in value_counts.items():
                    value_display = "null" if value is None else repr(value)
                    out.write(f"    {value_display}: {count} entries\n")
                out.write("\n")
            
            # Analyze combinations of attributes
            if attributes:
                all_non_null = sum(
                    1 for feature in features_of_type
                    if all(feature.get("properties", {}).get(attr) is not None for attr in attributes)
                )
                out.write(f"Features with all attributes non-null: {all_non_null} entries\n")
                out.write(f"Percentage: {100 - (all_non_null / total_features) * 100:.2f}%\n\n")
                
                # Check combinations of attributes
                out.write(f"--- Combination Analysis ---\n")
                for r in range(1, len(attributes) + 1):
                    for combo in combinations(attributes, r):
                        combo_non_null = sum(
                            1 for feature in features_of_type
                            if all(feature.get("properties", {}).get(attr) is not None for attr in combo)
                        )
                        percentage = (combo_non_null / total_features) * 100
                        out.write(f"Combination: {', '.join(combo)}\n")
                        out.write(f"  Non-null count: {combo_non_null}\n")
                        out.write(f"  Percentage: {percentage:.2f}%\n")
                out.write("\n")
            else:
                out.write("No attributes found for this type.\n\n")
        
        out.write("\nAnalysis complete.")

# Example usage with your GeoJSON file path and desired output file
analyze_geojson("./data/Providence/filtered_providence_segments.geojson", "analysis_output.txt")
