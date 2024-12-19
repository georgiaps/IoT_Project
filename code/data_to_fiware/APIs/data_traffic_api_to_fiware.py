import requests
import json
from datetime import datetime, timezone

# Configuration
API_KEY = "R51mEIGhkA1ITAySjGZbD5OlRSaJjFHV"
BASE_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

# Points Dictionary
POINTS = {
    "diastaurwsh_ethnikh": {"coordinates": "38.262128,21.750417", "name": "diastaurwsh sthn ethnikh odo"},
    "plaz": {"coordinates": "38.277013,21.745342", "name": "plaz"},
    "notio_parko": {"coordinates": "38.237902,21.725841", "name": "notio parko"},
    "diastaurwsh_panepisthmio": {"coordinates": "38.283701,21.770201", "name": "diastaurwsh panepisthmio"},
    "gounarh": {"coordinates": "38.245566,21.730981", "name": "odos gounarh"}
}

# FIWARE Context Broker
fiware_host = "http://150.140.186.118:1026/v2/entities"
fiware_service_path = "/microclimateandtraffic"
entity_type = "omada08_TrafficData"

def fetch_traffic_flow(coordinates):
    try:
        # Make the API call for Traffic Flow
        response = requests.get(f"{BASE_URL}?point={coordinates}&key={API_KEY}")
        response.raise_for_status()
        print(f"Successful fetching of traffic data for {coordinates}")

        # Parse the JSON data
        traffic_flow_data = response.json()

        # Calculate traffic percentage
        flow_segment_data = traffic_flow_data.get("flowSegmentData", {})
        if "currentSpeed" in flow_segment_data and "freeFlowSpeed" in flow_segment_data:
            current_speed = flow_segment_data["currentSpeed"]
            free_flow_speed = flow_segment_data["freeFlowSpeed"]
            traffic_percentage = round(((free_flow_speed - current_speed) / free_flow_speed), 2)

            # Add the calculated percentage to the data
            flow_segment_data["trafficPercentage"] = traffic_percentage

        return traffic_flow_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Traffic Flow data: {e}")


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

def transform_traffic_data(traffic_data, point):
    """
    Transform raw traffic data into FIWARE-compatible attributes.
    """
    flow_data = traffic_data.get("flowSegmentData", {})
    
    attributes = {
        "current_speed": {"value": flow_data.get("currentSpeed"), "type": "Integer"},
        "free_flow_speed": {"value": flow_data.get("freeFlowSpeed"), "type": "Integer"},
        "traffic_percentage": {"value": flow_data.get("trafficPercentage"), "type": "Float"},
        "coordinates": {"value": point["coordinates"], "type": "Text"},
        "traffic_point": {"value": point["name"], "type": "Text"},
        "timestamp": {"value": datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat(), "type": "DateTime"}
    }
    return attributes

def run():
    for key, point in POINTS.items():
        entity_id = f"TrafficAPIData_{key}"
        print(f"Fetching traffic data for {point['name']}...")

        # Fetch the traffic data
        traffic_data = fetch_traffic_flow(point["coordinates"])

        if traffic_data:
            # Transform the traffic data
            attributes = transform_traffic_data(traffic_data, point)
            print(f"Traffic Data to send for {point['name']}:", json.dumps(attributes, indent=2))

            # Check and create entity if necessary
            check_and_create_entity(entity_id, attributes)

            # Update the FIWARE context broker
            send_to_fiware(entity_id, attributes)

if __name__ == "__main__":
    run()