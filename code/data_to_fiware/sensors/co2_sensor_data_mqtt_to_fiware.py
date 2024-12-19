import paho.mqtt.client as mqtt
import requests
import json
from datetime import datetime, timezone

# MQTT broker and topics
broker = '150.140.186.118'
port = 1883
topic = "json/Room monitoring/mclimate-co2-sensor:1"

# FIWARE Context Broker
fiware_host = "http://150.140.186.118:1026/v2/entities"
fiware_service_path = "/microclimateandtraffic"
entity_id = "CO2SensorDataUni"
entity_type = "omada08_WeatherData"

def check_and_create_entity(attributes):
    """
    Checks if the entity exists in FIWARE. If not, it creates the entity.
    """
    url = f"{fiware_host}/{entity_id}"
    headers = {
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 404:  # Entity doesn't exist
        print(f"Entity {entity_id} not found. Creating entity...")
        # Create entity
        payload = {
            "id": entity_id,
            "type": entity_type
        }
        payload.update(attributes)

        create_response = requests.post(fiware_host, headers=headers, json=payload)
        if create_response.status_code not in (201, 204):
            print(f"Failed to create entity {entity_id}: {create_response.status_code} - {create_response.text}")
        elif response.status_code == 200:
            print("Entity exists in FIWARE.")
        else:
            print(f"Error checking entity existence: {response.status_code} - {response.text}")

def send_to_fiware(attributes):
    """
    Sends data to the FIWARE context broker to update the entity.
    """
    url = f"{fiware_host}/{entity_id}/attrs"
    headers = {
        'Content-Type': 'application/json',
        "Fiware-ServicePath": fiware_service_path
    }
    response = requests.patch(url, headers=headers, json=attributes, timeout=10)
    if response.status_code not in (201, 204):
        print(f"Failed to update entity {entity_id}: {response.status_code} - {response.text}")
        print(f"Payload: {json.dumps(attributes, indent=2)}")
    else:
        print(f"Entity {entity_id} updated successfully.")

def process_func(sensor4_data):
    """
    Processes sensor data, assigns a unified timestamp, and sends it to FIWARE.
    """
    # Create a unified timestamp
    unified_timestamp = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()

    # Combine sensor data into one entity
    unified_data = {
        "timestamp": {"value": unified_timestamp, "type": "DateTime"},
        "co2_level": {"value": sensor4_data.get('co2_level'), "type": "Number"},
        "coordinates": {"value": {"latitude": sensor4_data.get('latitude'), "longitude": sensor4_data.get('longitude')}, "type": "Point"}
    }

    try:
        # Log unified data for debugging
        print("Unified Data to send:", json.dumps(unified_data, indent=2))

        # Check and create entity if it doesn't exist
        check_and_create_entity(unified_data)

        # Send the processed data to FIWARE
        send_to_fiware(unified_data)
    except Exception as e:
        print(f"Error processing data: {e}")

def on_message(client, userdata, message):
    """
    Callback function to handle incoming MQTT messages.
    """
    try:
        data = json.loads(message.payload.decode())
        timestamp = datetime.now(tz=timezone.utc).isoformat()

        # Extract sensor 4 data
        sensor4_meas_obj = data.get('object', {})
        sensor4_meas_rxinfo = data.get('rxInfo', [])

        if sensor4_meas_obj:
            sensor4_data = {
            "co2_level": sensor4_meas_obj.get("CO2"),
            "timestamp": timestamp,
            "latitude": None,
            "longitude": None
        }
        if sensor4_meas_rxinfo and isinstance(sensor4_meas_rxinfo[0], dict):
            location = sensor4_meas_rxinfo[0].get('location', {})
            sensor4_data.update({
                "latitude": location.get('latitude', None),
                "longitude": location.get('longitude', None)
            })

        print("Sensor 4 data received:", sensor4_data)

        # Process and send to FIWARE
        process_func(sensor4_data)

    except json.JSONDecodeError:
        print("Invalid JSON received:", message.payload.decode())
    except Exception as e:
        print(f"Error handling message: {e}")

def connect_mqtt():
    """
    Connects to the MQTT broker and subscribes to topics.
    """
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(topic)
    return client

def run():
    """
    Runs the MQTT client loop.
    """
    client = connect_mqtt()
    client.loop_forever()

if __name__ == "__main__":
    run()