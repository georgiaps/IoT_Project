import time
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
import requests

# Define connection details for InfluxDB
influxdb_url = "http://150.140.186.118:8086"
bucket = "MicroclimateTraffic"
org = "students"
token = "N5EVklgWe-dWwE0YxgvWXIsi_mifEjPm-kNZy7U-MmLgUSLbsa43-gOSKYkEu1UHyg3EeihC8pB_oUU_IssaFw=="
measurement = "weather_sensor_data"

# FIWARE Context Broker details
fiware_url = "http://150.140.186.118:1026/v2/entities"
entity_id = "UnifiedSensorData"
headers = {
    "Content-Type": "application/json"
}

# Create InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api()

def fetch_data_from_fiware():
    """Fetch data from FIWARE Context Broker."""
    try:
        response = requests.get(f"{fiware_url}/{entity_id}", headers=headers)
        response.raise_for_status()
        print("Successful fetching of data from the fiware context broker")
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from FIWARE: {e}")
        return None

def process_fiware_data(data):
    """Process the FIWARE data to extract all fields."""
    try:
        fields = {}
        timestamp = None

        for key, attribute in data.items():
            if key == "timestamp":
                timestamp = datetime.fromisoformat(attribute["value"][:-1])  # Remove 'Z' for parsing
            elif "value" in attribute:
                value = attribute["value"]
                if isinstance(value, dict):  # Handle coordinates as separate fields
                    for sub_key, sub_value in value.items():
                        fields[f"{key}_{sub_key}"] = sub_value
                else:
                    fields[key] = value

        return fields, timestamp
    except (KeyError, ValueError) as e:
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
        time.sleep(600)

if __name__ == "__main__":
    main()