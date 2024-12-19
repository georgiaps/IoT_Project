import paho.mqtt.client as mqtt
import requests
import json
from datetime import datetime, timezone

# MQTT broker and topics
broker = '150.140.186.118'
port = 1883

# Topics for the sensors
topics = {
    "sensor1": "json/Environmental/barani-meteohelix-iot-pro:1",
    "sensor2": "json/Environmental/barani-meteowind-iot-pro:1"
}

# FIWARE Context Broker
fiware_host = "http://150.140.186.118:1026/v2/entities"
fiware_service_path = "/microclimateandtraffic"
entity_id = "UnifiedWeatherSensorDataUni"
entity_type = "omada08_WeatherData"

# Sensor data dictionary
sensor_data = {
    "sensor1": None,
    "sensor2": None
}

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

def process_func():
    """
    Processes sensor data, assigns a unified timestamp, and sends it to FIWARE.
    """
    # Create a unified timestamp
    #unified_timestamp = datetime.now(tz=timezone.utc).isoformat()
    unified_timestamp = datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()

    # Combine sensor data into one entity
    unified_data = {
        "timestamp": {"value": unified_timestamp, "type": "DateTime"}
    }
    if sensor_data["sensor1"]:
        unified_data.update({
            "humidity": {"value": sensor_data["sensor1"].get('humidity'), "type": "Number"},
            "rain": {"value": sensor_data["sensor1"].get('rain'), "type": "Number"},
            "temperature": {"value": sensor_data["sensor1"].get('temperature'), "type": "Number"},
            "pressure": {"value": (sensor_data["sensor1"].get('pressure'))/100, "type": "Number"},
            "irradiation": {"value": sensor_data["sensor1"].get('irradiation'), "type": "Number"}
    })
    if sensor_data["sensor2"]:
        unified_data.update({
            "wind_direction": {"value": sensor_data["sensor2"].get('wind_direction'), "type": "Number"},
            "wind_speed": {"value": sensor_data["sensor2"].get('wind_speed'), "type": "Number"},
            "coordinates": {"value": {"latitude": sensor_data["sensor2"].get('latitude'), "longitude": sensor_data["sensor2"].get('longitude')}, "type": "Point"}
    })

    if not any(sensor_data.values()):  # Ensure there's at least some data to send
        print("No sensor data available to process.")
        return

    try:
        # Log unified data for debugging
        print("Unified Data to send:", json.dumps(unified_data, indent=2))

        # Check and create entity if it doesn't exist
        check_and_create_entity(unified_data)

        # Send the processed data to FIWARE
        send_to_fiware(unified_data)
    except:
        print("ERROR")

    # Clear the sensor_data dictionary for the next cycle
    for key in sensor_data.keys():
        sensor_data[key] = None
    
def on_message(client, userdata, message):
    """
    Callback function to handle incoming MQTT messages.
    """
    #print(f"Message received on topic {message.topic}: {message.payload.decode()}")
    sensor_topic = message.topic
    try:
        data = json.loads(message.payload.decode())
        #print("Parsed JSON data:", json.dumps(data, indent=2))
        timestamp = datetime.now(tz=timezone.utc).isoformat()

        # Match sensor topic to store data
        if sensor_topic == topics["sensor1"]:
            sensor1_meas = data.get('object', {})
            sensor_data["sensor1"] = {
                "humidity": sensor1_meas.get('Humidity'),
                "rain": sensor1_meas.get('Rain'),
                "temperature": sensor1_meas.get('Temperature'),
                "pressure": sensor1_meas.get('Pressure'),
                "irradiation": sensor1_meas.get('Irradiation'),
                "timestamp": timestamp
            }
            print("Sensor 1 data updated:", sensor_data["sensor1"])
        elif sensor_topic == topics["sensor2"]:
            sensor2_meas_obj = data.get('object', {})
            sensor2_meas_rxinfo = data.get('rxInfo', [])

            if sensor2_meas_obj:
                sensor_data["sensor2"] = {
                "wind_direction": sensor2_meas_obj.get('6_Dir_ave10'),
                "wind_speed": sensor2_meas_obj.get('3_Wind_ave10'),
                "timestamp": timestamp,
                "latitude": None,
                "longitude": None
            }
            if sensor2_meas_rxinfo and isinstance(sensor2_meas_rxinfo[0], dict):
                location = sensor2_meas_rxinfo[0].get('location', {})
                sensor_data["sensor2"].update({
                    "latitude": location.get('latitude', None),
                    "longitude": location.get('longitude', None)
                })

            print("Sensor 2 data updated:", sensor_data["sensor2"])

        # Check if all sensor data is available
        if all(sensor_data.values()):
            process_func()  # Process and send to FIWARE

    except json.JSONDecodeError:
        print("Invalid JSON received:", message.payload.decode())
        return

def connect_mqtt():
    """
    Connects to the MQTT broker and subscribes to topics.
    """
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker, port)
    for topic in topics.values():
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