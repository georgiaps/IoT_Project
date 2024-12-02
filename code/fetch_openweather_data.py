import requests
import json
import os
from datetime import datetime

# Configuration
API_KEY = "9bb20a8d36e77bd9d405689a1c985d28"
CITY = "patras"  # City name for which weather data will be fetched
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
OUTPUT_DIR = "C:/Users/ariad/OneDrive/Desktop/IoT_Project/data/weather_data"  # Directory to save the JSON files

def fetch_weather_data(city, api_key):
    """
    Fetch current weather data for a specific city from the OpenWeather API.
    """
    params = {
        "q": city,  # City name
        "appid": api_key,  # API key
    }

    try:
        # Send the HTTP GET request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def save_weather_data(data, city, output_dir):
    """
    Save weather data to a JSON file.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the file path (e.g., weather_patras.json)
    file_path = os.path.join(output_dir, f"weather_{city.lower()}_{int(datetime.now().timestamp())}.json")
    
    # Write the JSON data to the file
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Weather data saved to {file_path}")
    except IOError as e:
        print(f"Error saving weather data: {e}")

def main():
    # Fetch the weather data
    print(f"Fetching weather data for {CITY}...")
    weather_data = fetch_weather_data(CITY, API_KEY)

    if weather_data:
        # Save the data to a JSON file
        save_weather_data(weather_data, CITY, OUTPUT_DIR)

if __name__ == "__main__":
    main()