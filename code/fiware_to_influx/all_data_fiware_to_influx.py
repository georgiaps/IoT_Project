import time
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
import requests
import paho.mqtt.client as mqtt_client
import random 

# MQTT broker
broker = '150.140.186.118'
port = 1883
client_id = 'rand_id_' + str(random.random())
topic = 'omada08'

# Define connection details for InfluxDB
influxdb_url = "http://150.140.186.118:8086"
bucket = "MicroclimateTraffic-team08"
org = "students"
token = "tV_gUZfCKmObZaYxUNYD6DxK3mCQ93REKC-84WaBlASk0-X43U4BST9FyeEzEN1VOnd9rIwQ2SyUeFS_1xhsUQ=="

# FIWARE Context Broker details
fiware_url = "http://150.140.186.118:1026/v2/entities"

# Create InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client):
    def on_message(client, userdata, msg):
        """Handle MQTT messages and process the data."""
        try:
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            notification = json.loads(msg.payload.decode())
            if 'data' in notification:
                for entity in notification['data']:
                    entity_id = entity['id']
                    process_entity_data(entity_id)
        except Exception as e:
            print(f"Error processing MQTT message: {e}")

    client.subscribe(topic)
    client.on_message = on_message

def fetch_data_from_fiware(entity_id):
    """Fetch data from FIWARE Context Broker."""
    try:
        response = requests.get(f"{fiware_url}/{entity_id}", params={"options": "keyValues"})
        response.raise_for_status()
        print(f"Successfully fetched data for entity {entity_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for entity {entity_id}: {e}")
        return None

def process_fiware_data(data):
    """Process the FIWARE data to extract all fields with consistent types."""
    try:
        fields = {}
        timestamp = None

        for key, value in data.items():
            if key == "timestamp":
                timestamp = datetime.fromisoformat(value[:-1])  # Remove 'Z' for parsing
            elif isinstance(value, dict):  # Handle coordinates or nested data
                for sub_key, sub_value in value.items():
                    fields[f"{key}_{sub_key}"] = enforce_numeric_type(sub_value)
            else:
                fields[key] = enforce_numeric_type(value)

        return fields, timestamp
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error processing FIWARE data: {e}")
    return None, None

def enforce_numeric_type(value):
    """Ensure all numeric fields are consistently written as float."""
    try:
        # Convert integers to float to avoid conflicts in InfluxDB
        if isinstance(value, (int, float)):
            return float(value)
        return value
    except Exception as e:
        print(f"Type enforcement error: {e}, value: {value}")
        return value

def write_to_influx(entity_id, fields, timestamp):
    """Write the processed data to InfluxDB."""
    try:
        point = Point(entity_id).time(timestamp.isoformat(), WritePrecision.NS)

        for field, value in fields.items():
            if isinstance(value, (int, float)):
                point = point.field(field, value)
            else:
                try:
                    point = point.field(field, float(value))
                except:
                    point = point.tag(field, str(value))

        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Written data: {point} at {timestamp}")
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")

def process_entity_data(entity_id):
    """Fetch and process data for a given entity ID."""
    fiware_data = fetch_data_from_fiware(entity_id)
    if fiware_data:
        fields, timestamp = process_fiware_data(fiware_data)
        if fields and timestamp:
            write_to_influx(entity_id, fields, timestamp)

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == "__main__":
    run()