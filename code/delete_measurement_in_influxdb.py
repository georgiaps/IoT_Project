from influxdb_client import InfluxDBClient
from influxdb_client.rest import ApiException
from datetime import datetime, timezone

# InfluxDB connection details
influxdb_url = "http://150.140.186.118:8086"
bucket = "MicroclimateTraffic-team08-Final"
org = "students"
token = "sJcp3CYIFhde06U1V9LMu1Qcsl0KVo4die707OYtsM9XNzTg-w5-tUlbwtzQtm3rS30xIL5N9jT92h6K05cpiw=="

# The measurement to delete
measurement_name = "Forecast_TrafficAPIData_university_patras"  # Replace with your actual measurement name

# Time range for deletion (adjust as needed)
start_time = "1970-01-01T00:00:00Z"  # Start of time range
#end_time = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")  # Proper RFC3339Nano format
end_time = "2025-02-20T00:00:00Z"

try:
    # Initialize the InfluxDB client
    client = InfluxDBClient(url=influxdb_url, token=token, org=org)

    # Delete the measurement
    delete_api = client.delete_api()
    delete_api.delete(
        start=start_time,
        stop=end_time,
        predicate=f'_measurement="{measurement_name}"',
        bucket=bucket,
        org=org,
    )

    print(f"Successfully deleted measurement '{measurement_name}' from bucket '{bucket}'.")
except ApiException as e:
    print(f"An error occurred: {e}")
finally:
    client.close()
