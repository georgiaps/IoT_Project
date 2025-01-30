import requests
import json
import time
from datetime import datetime, timezone, timedelta

# Configuration
API_KEY = "9bb20a8d36e77bd9d405689a1c985d28"
CITY = "patras"  # City name for which weather data will be fetched
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# FIWARE Context Broker
fiware_host = "http://150.140.186.118:1026/v2/entities"
fiware_service_path = "/microclimateandtraffic"
entity_id = "WeatherForecastAPIDataPatras"
entity_type = "omada08_WeatherData"

def fetch_weather_data(city, api_key):
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def filter_weather_data(weather_data):
    tomorrow = datetime.now() + timedelta(days=1)
    three_days_later = datetime.now() + timedelta(days=3)
    filtered_data = []
    valid_hours = {"09:00:00", "15:00:00", "21:00:00"}
    
    for entry in weather_data.get("list", []):
        dt_txt = entry.get("dt_txt")
        dt_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
        
        if tomorrow.date() <= dt_obj.date() <= three_days_later.date() and dt_txt.split()[1] in valid_hours:
            weather = entry.get("weather", [])
            filtered_data.append({
                "dt": entry.get("dt"),
                "dt_txt": dt_txt,
                "temp": entry["main"].get("temp"),
                "humidity": entry["main"].get("humidity"),
                "pressure": entry["main"].get("pressure"),
                "wind_speed": entry["wind"].get("speed"),
                "wind_deg": entry["wind"].get("deg"),
                "rain_1h": entry.get("rain", {}).get("1h", 0),
                "description": weather[0].get("description")
            })

    return filtered_data

def check_and_create_entity():
    url = f"{fiware_host}/{entity_id}"
    headers = {
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        print(f"Entity {entity_id} not found. Creating entity...")
        payload = {
            "id": entity_id,
            "type": entity_type,
            "forecast": {"value": [], "type": "StructuredValue"}  # Initialize forecast attribute
        }
        create_response = requests.post(fiware_host, headers=headers, json=payload)
        if create_response.status_code not in (201, 204):
            print(f"Failed to create entity {entity_id}: {create_response.status_code} - {create_response.text}")
            return False
        else:
            print(f"Entity {entity_id} created successfully.")
            time.sleep(2)  # Allow FIWARE time to register entity
            return True
    return True

def send_to_fiware(filtered_data):
    if not check_and_create_entity():
        print("Skipping update due to entity creation failure.")
        return
    
    url = f"{fiware_host}/{entity_id}/attrs"
    headers = {
        "Content-Type": "application/json",
        "Fiware-ServicePath": fiware_service_path
    }
    attributes = {"forecast": {"value": filtered_data, "type": "StructuredValue"}}
    response = requests.patch(url, headers=headers, json=attributes)
    if response.status_code not in (201, 204):
        print(f"Failed to update entity {entity_id}: {response.status_code} - {response.text}")
    else:
        print(f"Entity {entity_id} updated successfully.")

def run():
    print(f"Fetching weather data for {CITY}...")
    weather_data = fetch_weather_data(CITY, API_KEY)
    
    if weather_data:
        filtered_data = filter_weather_data(weather_data)
        print("Filtered Weather Data:", json.dumps(filtered_data, indent=2))
        send_to_fiware(filtered_data)

if __name__ == "__main__":
    run()