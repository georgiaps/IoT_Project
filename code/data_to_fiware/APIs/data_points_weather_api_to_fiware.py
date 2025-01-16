import requests
import json
from datetime import datetime, timezone

# Configuration
API_KEY = "9bb20a8d36e77bd9d405689a1c985d28"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Points Dictionary
POINTS = {
    "diastaurwsh_ethnikh": {"coordinates": "38.262128,21.750417", "name": "diastaurwsh sthn ethnikh odo"},
    "plaz": {"coordinates": "38.277013,21.745342", "name": "plaz"},
    "notio_parko": {"coordinates": "38.237902,21.725841", "name": "notio parko"},
    "diastaurwsh_panepisthmio": {"coordinates": "38.290672,21.780164", "name": "diastaurwsh panepisthmio"},
    "gounarh": {"coordinates": "38.245566,21.730981", "name": "odos gounarh"},
    "ermou": {"coordinates": "38.246877,21.735854", "name": "odos ermou"},
    "dasyllio": {"coordinates": "38.248858,21.745578", "name": "dasyllio"},
    "gefyra_rio_antirrio": {"coordinates": "38.320745,21.773224", "name": "gefyra rio_antirrio"}
}

# FIWARE Context Broker
fiware_host = "http://150.140.186.118:1026/v2/entities"  # Replace with your FIWARE context broker URL
fiware_service_path = "/microclimateandtraffic"
entity_type = "omada08_WeatherData"

def fetch_weather_data(lat, lon):
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

def transform_weather_data(weather_data, point):
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
        "coordinates": {"value": point["coordinates"], "type": "Text"},
        "location_name": {"value": point["name"], "type": "Text"},
        "timestamp": {"value": datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat(), "type": "DateTime"}
    }
    return attributes

def run():
    for key, point in POINTS.items():
        entity_id = f"WeatherAPIData_{key}"
        lat, lon = point["coordinates"].split(",")
        print(f"Fetching weather data for {point['name']}...")

        # Fetch the weather data
        weather_data = fetch_weather_data(lat, lon)

        if weather_data:
            # Transform the weather data
            attributes = transform_weather_data(weather_data, point)
            print(f"Weather Data to send for {point['name']}:", json.dumps(attributes, indent=2))

            # Check and create entity if necessary
            check_and_create_entity(entity_id, attributes)

            # Update the FIWARE context broker
            send_to_fiware(entity_id, attributes)

if __name__ == "__main__":
    run()
