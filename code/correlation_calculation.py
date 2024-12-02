import os
import json
from scipy.stats import pearsonr

# Define paths to directories
RAIN_DATA_PATH = r"C:/Users/ariad/OneDrive/Desktop/IoT_Project/data/weather_data"
TRAFFIC_DATA_PATH = r"C:/Users/ariad/OneDrive/Desktop/IoT_Project/data/traffic_data"

# Function to extract a value from a single JSON file
def extract_rain_value(json_file_path):
    """Extract 'rain_mm' from a single JSON file, or return 0 if 'rain' is missing."""
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data.get("rain", {}).get("1h", 0)  # Return 0 if 'rain' or '1h' is missing

def extract_traffic_value(json_file_path):
    """Extract 'traffic_pct' from a single JSON file."""
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data["flowSegmentData"]["trafficPercentage"]  # Adjust key path if necessary

# Function to process all JSON files in a directory
def process_directory(directory_path, extract_function):
    values = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_path.endswith(".json"):
            try:
                value = extract_function(file_path)
                values.append(value)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
    return values

# Function to calculate correlation
def calculate_correlation(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Lists must have the same length for correlation calculation.")
    correlation, p_value = pearsonr(list1, list2)
    return correlation, p_value

# Main workflow
try:
    # Generate lists of values
    rain_values = process_directory(RAIN_DATA_PATH, extract_rain_value)
    traffic_values = process_directory(TRAFFIC_DATA_PATH, extract_traffic_value)

    # Display results
    print("Rain Data (mm):", rain_values)
    print("Traffic Data (%):", traffic_values)

    # Calculate and display correlation
    if len(rain_values) > 1 and len(traffic_values) > 1:
        correlation, p_value = calculate_correlation(rain_values, traffic_values)
        print(f"\nCorrelation between rain and traffic: {correlation:.2f}")
        print(f"P-value: {p_value:.2e}")
    else:
        print("\nInsufficient data for correlation calculation. Both lists must have at least 2 values.")
except Exception as e:
    print(f"An error occurred: {e}")
