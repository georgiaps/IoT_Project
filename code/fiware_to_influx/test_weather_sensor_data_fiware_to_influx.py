import time
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
import requests

# Define connection details for InfluxDB
influxdb_url = "http://150.140.186.118:8086"
bucket = "test-team08"
org = "students"
token = "DFnEuF2lKPD4isa3nZq3zWvfC-lXuV3DFiD2RBNAazVEdk0oqmvw0W3gIr2W1inoYNoVT7jYAAa-N2QhKpNVTQ=="
measurement = "weather_sensor_data"

# FIWARE Context Broker details
fiware_url = "http://150.140.186.118:1026/v2/entities"
entity_id = "UnifiedWeatherSensorDataUni"
headers = {}

# Create InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api()

def fetch_data_from_fiware():
    """Fetch data from FIWARE Context Broker."""
    try:
        response = requests.get(f"{fiware_url}/{entity_id}", params={"options": "keyValues"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from FIWARE: {e}")
        return None

def process_fiware_data(data):
    """Process the FIWARE data to extract all fields."""
    try:
        fields = {}
        timestamp = None

        for key, value in data.items():
            if key == "timestamp":
                timestamp = datetime.fromisoformat(value[:-1])  # Remove 'Z' for parsing
            elif isinstance(value, dict):  # Handle coordinates or nested data
                for sub_key, sub_value in value.items():
                    fields[f"{key}_{sub_key}"] = sub_value
            else:
                fields[key] = value

        return fields, timestamp
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error processing FIWARE data: {e}")
    return None, None

def write_to_influx(fields, timestamp):
    """Write the processed data to InfluxDB."""
    try:
        point = Point(measurement).time(timestamp.isoformat(), WritePrecision.NS)

        for field, value in fields.items():
            if isinstance(value, (int, float)):
                point = point.field(field, value)
            else:
                try:
                    point = point.field(field, float(value))
                except:
                    point = point.tag(field, str(value))

        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Written data: {fields} at {timestamp}")
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")

def main():
    while True:
        # Fetch data from FIWARE
        fiware_data = fetch_data_from_fiware()
        if fiware_data:
            # Process the FIWARE data
            fields, timestamp = process_fiware_data(fiware_data)
            if fields and timestamp:
                # Write the data to InfluxDB
                write_to_influx(fields, timestamp)

        # Wait before the next fetch (e.g., 10 seconds)
        time.sleep(10)

if __name__ == "__main__":
    main()
