import requests
import json
from datetime import datetime, timezone
import time

# Configuration
API_KEY = "9bb20a8d36e77bd9d405689a1c985d28"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
STATIONS_URL = "http://labserver.sense-campus.gr:5047/exmi_patras"
token = "studentpassword"

# Points Dictionary
POINTS = {
    "leuka": {"coordinates": "38.2066,21.7271", "name": "leuka", "sensorid": "101589"},
    "paralia": {"coordinates": "38.1994,21.6992", "name": "paralia", "sensorid": "101609"},
    "kato_sychaina": {"coordinates": "38.2652,21.757", "name": "kato sychaina", "sensorid": "56113"},
    "demenika": {"coordinates": "38.2001,21.7438", "name": "demenika", "sensorid": "14857"},
    "kastelokampos": {"coordinates": "38.2893,21.7739", "name": "kastelokampos", "sensorid": "1672"}
}

# FIWARE Context Broker
fiware_host = "http://150.140.186.118:1026/v2/entities"  # Replace with your FIWARE context broker URL
fiware_service_path = "/microclimateandtraffic"
entity_type = "omada08_WeatherData"

def fetch_weather_data_api(lat, lon):
    """
    Fetch current weather data for specific coordinates from the OpenWeather API.
    """
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"  # Fetch data in Celsius
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        print(f"Successful fetching of weather data for coordinates ({lat}, {lon})")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    
def fetch_weather_data_stations(token, sensorid):
    """
    Fetch current weather data for specific coordinates from the OpenWeather API.
    """
    params = {
        "token": token,
        "sensorid": sensorid
    }

    try:
        response = requests.get(STATIONS_URL, params=params)
        response.raise_for_status()
        print(f"Successful fetching of weather data for {sensorid})")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None    

def check_and_create_entity(entity_id, attributes):
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

def send_to_fiware(entity_id, attributes):
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

def transform_weather_data(weather_data_api, weather_data_stations, point):
    """
    Transform raw weather data into FIWARE-compatible attributes.
    """
    main = weather_data_api.get("main", {})
    wind = weather_data_api.get("wind", {})
    rain = weather_data_api.get("rain", {}).get("1h", 0)  # Default to 0 if rain is missing

    attributes = {
        "temperature": {"value": weather_data_stations["temp"], "type": "Integer"},
        "pressure": {"value": main.get("pressure"), "type": "Integer"},
        "humidity": {"value": weather_data_stations["hum"], "type": "Integer"},
        "visibility": {"value": weather_data_api.get("visibility", 0), "type": "Integer"},
        "wind_speed": {"value": wind.get("speed", 0), "type": "Float"},
        "wind_deg": {"value": wind.get("deg", 0), "type": "Integer"},
        "rain_1h": {"value": rain, "type": "Float"},
        "coordinates": {"value": point["coordinates"], "type": "Text"},
        "location_name": {"value": point["name"], "type": "Text"},
        "timestamp": {"value": datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat(), "type": "DateTime"}
    }
    return attributes

def run():
    for key, point in POINTS.items():
        entity_id = f"WeatherAPIData_{key}"
        lat, lon = point["coordinates"].split(",")
        sensorid = point['sensorid']
        print(f"Fetching weather data for {point['name']}...")

        # Fetch the weather data
        weather_data_api = fetch_weather_data_api(lat, lon)
        weather_data_stations = fetch_weather_data_stations(token, sensorid)

        if weather_data_api:
            # Transform the weather data
            attributes = transform_weather_data(weather_data_api, weather_data_stations, point)
            print(f"Weather Data to send for {point['name']}:", json.dumps(attributes, indent=2))

            # Check and create entity if necessary
            check_and_create_entity(entity_id, attributes)

            # Update the FIWARE context broker
            send_to_fiware(entity_id, attributes)
        time.sleep(0.500)

if __name__ == "__main__":
    run()
