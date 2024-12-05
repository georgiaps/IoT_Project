import os
import json
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np

# Define paths to directories
RAIN_DATA_PATH = r"C:/Users/ariad/OneDrive/Desktop/IoT_Project/data/weather_data_rainy"
TRAFFIC_DATA_RAINY_PATH = r"C:/Users/ariad/OneDrive/Desktop/IoT_Project/data/traffic_data_rainy"
TRAFFIC_DATA_SUNNY_PATH = r"C:/Users/ariad/OneDrive/Desktop/IoT_Project/data/traffic_data"

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

def extract_time_value(json_file_path):
    """Extract 'time' from a single JSON file."""
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data["flowSegmentData"]["time"][:5]  # Adjust key path if necessary

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

# Correlation calculation
def calculate_correlation(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Lists must have the same length for correlation calculation.")
    correlation, p_value = pearsonr(list1, list2)
    return correlation, p_value

# Main workflow
try:
    # Generate lists of values
    rain_values = process_directory(RAIN_DATA_PATH, extract_rain_value)
    rainy_traffic_values = process_directory(TRAFFIC_DATA_RAINY_PATH, extract_traffic_value)
    sunny_traffic_values = process_directory(TRAFFIC_DATA_SUNNY_PATH, extract_traffic_value)
    time_values = process_directory(TRAFFIC_DATA_RAINY_PATH, extract_time_value)
    traffic_difference = np.subtract(rainy_traffic_values, sunny_traffic_values)

    # Display results
    print("Rain Data (mm):", rain_values)
    print("Rainy Traffic Data (%):", rainy_traffic_values)
    print("Sunny Traffic Data (%):", sunny_traffic_values)
    print("Traffic Difference (%):", traffic_difference)
    print("Time Data :", time_values)

    # Calculate and display correlation
    if len(rain_values) > 1 and len(rainy_traffic_values) > 1:
        correlation, p_value = calculate_correlation(rain_values, traffic_difference)
        print(f"\nCorrelation index between rain and traffic: {correlation:.2f}")
        print(f"P-value: {p_value:.2e}")
    else:
        print("\nInsufficient data for correlation calculation. Both lists must have at least 2 values.")

    # Plot diagrams
    plt.figure(figsize=(12, 6))

    # First diagram
    plt.plot(time_values, rainy_traffic_values, label="Rainy Traffic", marker="o")
    plt.plot(time_values, sunny_traffic_values, label="Sunny Traffic", marker="o")
    plt.xlabel("Time")
    plt.ylabel("Traffic Percentage")
    plt.title("Traffic Comparison (Sunny day vs Rainy day)")
    plt.legend()
    plt.grid()

    # Second diagram
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    ax1.plot(time_values, rain_values, "b-", label="Rain Amount (mm)", marker="o")
    ax2.plot(time_values, traffic_difference, "r-", label="Traffic Difference (%)", marker="o")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Rain Amount (mm)", color="b")
    ax2.set_ylabel("Traffic Difference (%)", color="r")
    plt.title("Traffic and Rain Amount Correlation")
    ax1.grid()

    fig.tight_layout()
    plt.show()

except Exception as e:
    print(f"An error occurred: {e}")