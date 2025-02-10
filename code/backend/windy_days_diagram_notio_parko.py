import os
from influxdb_client import InfluxDBClient
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# InfluxDB connection parameters
influxdb_url = "http://150.140.186.118:8086"
bucket = "MicroclimateTraffic-team08-Final"
org = "students"
token = "sJcp3CYIFhde06U1V9LMu1Qcsl0KVo4die707OYtsM9XNzTg-w5-tUlbwtzQtm3rS30xIL5N9jT92h6K05cpiw=="

# Initialize InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=token, org=org)
query_api = client.query_api()

def query_influxdb(query):
    result = query_api.query(org=org, query=query)
    times, values = [], []
    for table in result:
        for record in table.records:
            times.append(record.get_time().strftime('%H:%M'))
            values.append(record.get_value())
    return times, values

# Queries
no_windy_traffic_query = '''
from(bucket: "MicroclimateTraffic-team08-Final")
  |> range(start: time(v: "2025-02-05T06:45:00Z"), stop: time(v: "2025-02-05T23:00:00Z"))
  |> filter(fn: (r) => r["_measurement"] == "TrafficAPIData_notio_parko")
  |> filter(fn: (r) => r["_field"] == "traffic_percentage")
  |> aggregateWindow(every:  15m, fn: mean, createEmpty: false)
  |> yield(name: "mean")
'''

windy_traffic_query = '''
from(bucket: "MicroclimateTraffic-team08-Final")
  |> range(start: time(v: "2025-02-04T06:45:00Z"), stop: time(v: "2025-02-04T23:00:00Z"))
  |> filter(fn: (r) => r["_measurement"] == "TrafficAPIData_notio_parko")
  |> filter(fn: (r) => r["_field"] == "traffic_percentage")
  |> aggregateWindow(every: 15m, fn: mean, createEmpty: false)
  |> yield(name: "mean")
'''

wind_amount_query = '''
from(bucket: "MicroclimateTraffic-team08-Final")
  |> range(start: time(v: "2025-02-04T06:45:00Z"), stop: time(v: "2025-02-04T23:00:00Z"))
  |> filter(fn: (r) => r["_measurement"] == "WeatherAPIData_notio_parko")
  |> filter(fn: (r) => r["_field"] == "wind_speed")
  |> aggregateWindow(every: 15m, fn: mean, createEmpty: false)
  |> yield(name: "mean")
'''

# Fetch data
no_windy_traffic_times, no_windy_traffic_values = query_influxdb(no_windy_traffic_query)
windy_traffic_times, windy_traffic_values = query_influxdb(windy_traffic_query)
wind_times, wind_values = query_influxdb(wind_amount_query)

# Ensure time alignment (assuming equal length data)
if len(windy_traffic_values) != len(no_windy_traffic_values):
    raise ValueError("Mismatch in data length between windy and no_windy traffic.")

traffic_difference = np.subtract(windy_traffic_values, no_windy_traffic_values)

# Calculate correlation
if len(wind_values) > 1:
    correlation, p_value = pearsonr(wind_values, windy_traffic_values)
    print(f"\nCorrelation index between wind and traffic: {correlation:.2f}")
    print(f"P-value: {p_value:.2e}")
else:
    print("Insufficient data for correlation calculation.")

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(windy_traffic_times, windy_traffic_values, label="Windy Day", color='#2b6cb0', marker="o")
plt.plot(no_windy_traffic_times, no_windy_traffic_values, label="No Windy Day", color='#75283d', marker="o")
plt.xlabel("Time", fontsize=14)
plt.xticks(windy_traffic_times[::4], rotation=30)
plt.ylabel("Traffic Percentage", fontsize=14, labelpad=16)
plt.title("Traffic Comparison in South Park (No Windy vs Windy Day)", fontsize=18)
plt.legend()
plt.grid(axis='y')
plt.savefig(f"code/frontend/correlation_diagrams/windy_vs_no_windy_diagram_notio_parko_{correlation:.2f}.png", bbox_inches='tight')
plt.show()

'''
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()
ax1.plot(wind_times, wind_values, "b-", label="wind Amount (mm)", marker="o")
ax2.plot(wind_times, traffic_difference, "r-", label="Traffic Difference (%)", marker="o")
ax1.set_xlabel("Time")
ax1.set_ylabel("wind Amount (mm)", color="b")
ax2.set_ylabel("Traffic Difference (%)", color="r")
plt.title("Traffic and wind Correlation")
ax1.grid()
fig.tight_layout()
plt.show()'''