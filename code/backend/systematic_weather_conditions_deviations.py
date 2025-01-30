from influxdb_client import InfluxDBClient
import pandas as pd
import json

# InfluxDB connection parameters
influxdb_url = "http://150.140.186.118:8086"
bucket = "MicroclimateTraffic-team08-Final"
org = "students"
token = "sJcp3CYIFhde06U1V9LMu1Qcsl0KVo4die707OYtsM9XNzTg-w5-tUlbwtzQtm3rS30xIL5N9jT92h6K05cpiw=="

# Fields and measurements
fields = ["temperature", "humidity", "pressure", "rain_1h", "wind_deg", "wind_speed"]
location_mapping = {
    "University Crossroad": "WeatherAPIData_diastaurwsh_panepisthmio",
    "Agyias Beach": "WeatherAPIData_plaz",
    "National Road Interchange": "WeatherAPIData_diastaurwsh_ethnikh",
    "Patras Centre": "WeatherAPIData_ermou",
    "Gounarh Road": "WeatherAPIData_gounarh",
    "South Park": "WeatherAPIData_notio_parko",
    "Dasyllio": "WeatherAPIData_dasyllio",
    "Rio-Antirrio Bridge": "WeatherAPIData_gefyra_rio_antirrio",
    "Leuka": "WeatherAPIData_leuka",
    "Paralia": "WeatherAPIData_paralia",
    "Kato Sychaina": "WeatherAPIData_kato_sychaina",
    "Demenika": "WeatherAPIData_demenika",
    "Kastelokampos": "WeatherAPIData_kastelokampos",
    "Patras": "WeatherAPIDataPatras",
    "University of Patras": "UnifiedWeatherSensorDataUni"
}

# Field mapping for University sensor
def map_fields(df, measurement):
    if measurement == "UnifiedWeatherSensorDataUni":
        df = df.rename(columns={"rain": "rain_1h", "wind_direction": "wind_deg"})
    return df

def query_influxdb(measurement):
    """Queries InfluxDB for the last 30 days of data for a given measurement."""
    query_fields = ["rain" if f == "rain_1h" and measurement == "UnifiedWeatherSensorDataUni" else "wind_direction" if f == "wind_deg" and measurement == "UnifiedWeatherSensorDataUni" else f for f in fields]
    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -30d)
      |> filter(fn: (r) => r["_measurement"] == "{measurement}")
      |> filter(fn: (r) => {" or ".join([f'r["_field"] == "{field}"' for field in query_fields])})
      |> aggregateWindow(every: 10m, fn: mean, createEmpty: false)
      |> yield(name: "mean")'''

    with InfluxDBClient(url=influxdb_url, token=token, org=org) as client:
        query_api = client.query_api()
        tables = query_api.query(query, org=org)
        data = []
        for table in tables:
            for record in table.records:
                data.append((record.get_time(), record.get_measurement(), record.get_field(), record.get_value()))
    
    df = pd.DataFrame(data, columns=["time", "measurement", "field", "value"])
    df["time"] = pd.to_datetime(df["time"])
    df = df.pivot_table(index="time", columns="field", values="value")
    df = map_fields(df, measurement)
    return df

# Query Patras as reference
df_patras = query_influxdb("WeatherAPIDataPatras")
df_patras_resampled = df_patras.resample("5min").mean()

# Dictionary to store differences
results = {}

# Loop over other locations
for location, measurement in location_mapping.items():
    if measurement == "WeatherAPIDataPatras":
        continue  # Skip Patras itself
    
    df_other = query_influxdb(measurement)
    df_other_resampled = df_other.resample("5min").mean()
    df_diff = df_other_resampled - df_patras_resampled
    average_diff = df_diff.mean()
    
    results[location] = {
        "humidity": round(average_diff.get("humidity", 0), 2),
        "pressure": round(average_diff.get("pressure", 0), 2),
        "rain_1h": round(average_diff.get("rain_1h", 0), 2),
        "temp": round(average_diff.get("temperature", 2), 2),
        "wind_deg": round(average_diff.get("wind_deg", 0), 2),
        "wind_speed": round(average_diff.get("wind_speed", 0), 2)
    }

# Save to JSON
with open("code/backend/average_differences.json", "w") as json_file:
    json.dump(results, json_file, indent=4)

print("JSON file 'average_differences.json' has been created successfully.")
