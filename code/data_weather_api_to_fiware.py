import requests
import json
from datetime import datetime, timezone

# Configuration
API_KEY = "9bb20a8d36e77bd9d405689a1c985d28"
CITY = "patras"  # City name for which weather data will be fetched
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# FIWARE Context Broker
fiware_host = "http://150.140.186.118:1026/v2/entities"  # Replace with your FIWARE context broker URL
fiware_service_path = "/microclimateandtraffic"
entity_id = "UnifiedWeatherAPIData"
entity_type = "WeatherData"

def fetch_weather_data(city, api_key):
    """
    Fetch current weather data for a specific city from the OpenWeather API.
    """
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Fetch data in Celsius
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        print("Successful fetching of weather data")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def check_and_create_entity(attributes):
    """
    Checks if the entity exists in FIWARE. If not, creates the entity.
    """
    url = f"{fiware_host}/{entity_id}"
    headers = {
        "Fiware-ServicePath": fiware_service_path
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 404:  # Entity doesn't exist
        print(f"Entity {entity_id} not found. Creating entity...")
        payload = {
            "id": entity_id,
            "type": entity_type
        }
        payload.update(attributes)

        create_response = requests.post(fiware_host, headers=headers, json=payload)
        if create_response.status_code not in (201, 204):
            print(f"Failed to create entity {entity_id}: {create_response.status_code} - {create_response.text}")
        else:
            print(f"Entity {entity_id} created successfully.")
    elif response.status_code == 200:
        print(f"Entity {entity_id} exists in FIWARE.")
    else:
        print(f"Error checking entity existence: {response.status_code} - {response.text}")

def send_to_fiware(attributes):
    """
    Sends data to the FIWARE context broker to update the entity.
    """
    url = f"{fiware_host}/{entity_id}/attrs"
    headers = {
        "Content-Type": "application/json",
        "Fiware-ServicePath": fiware_service_path
    }

    response = requests.patch(url, headers=headers, json=attributes)
    if response.status_code not in (201, 204):
        print(f"Failed to update entity {entity_id}: {response.status_code} - {response.text}")
    else:
        print(f"Entity {entity_id} updated successfully.")

def transform_weather_data(weather_data):
    """
    Transform raw weather data into FIWARE-compatible attributes.
    """
    main = weather_data.get("main", {})
    wind = weather_data.get("wind", {})
    rain = weather_data.get("rain", {}).get("1h", 0)  # Default to 0 if rain is missing

    attributes = {
        "temperature": {"value": main.get("temp"), "type": "Float"},
        "pressure": {"value": main.get("pressure"), "type": "Integer"},
        "humidity": {"value": main.get("humidity"), "type": "Integer"},
        "visibility": {"value": weather_data.get("visibility", 0), "type": "Integer"},
        "wind_speed": {"value": wind.get("speed", 0), "type": "Float"},
        "wind_deg": {"value": wind.get("deg", 0), "type": "Integer"},
        "rain_1h": {"value": rain, "type": "Float"},
        "timestamp": {"value": datetime.now(tz=timezone.utc).isoformat(), "type": "Text"}
    }
    return attributes

def run():
    # Fetch the weather data
    print(f"Fetching weather data for {CITY}...")
    weather_data = fetch_weather_data(CITY, API_KEY)

    if weather_data:
        # Transform the weather data
        attributes = transform_weather_data(weather_data)
        print("Weather Data to send:", json.dumps(attributes, indent=2))

        # Check and create entity if necessary
        check_and_create_entity(attributes)

        # Update the FIWARE context broker
        send_to_fiware(attributes)

if __name__ == "__main__":
    run()
