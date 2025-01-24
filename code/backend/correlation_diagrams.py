import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuration for InfluxDB
INFLUXDB_URL = "http://150.140.186.118:8086"  
INFLUXDB_TOKEN = "sJcp3CYIFhde06U1V9LMu1Qcsl0KVo4die707OYtsM9XNzTg-w5-tUlbwtzQtm3rS30xIL5N9jT92h6K05cpiw=="  
INFLUXDB_ORG = "students"  
INFLUXDB_BUCKET = "MicroclimateTraffic-team08-Final"  

# Points configuration
POINTS = {
    "University Crossroad": ["diastaurwsh_panepisthmio", "rain_1h"],
    "Agyias Beach": ["plaz", "temperature"],
    "National Road Interchange": ["diastaurwsh_ethnikh", "rain_1h"],
    "Patras Centre": ["ermou", "temperature"],
    "South Park": ["notio_parko", "temperature"],
    "Dasyllio": ["dasyllio", "humidity"],
    "Rio-Antirrio Bridge": ["gefyra_rio_antirrio", "wind_speed"]
}
# Folder to save diagrams
OUTPUT_FOLDER = "correlation_diagrams"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Query templates
WEATHER_QUERY_TEMPLATE = (
    "from(bucket: \"{bucket}\") "
    "|> range(start: v.timeRangeStart, stop: v.timeRangeStop) "
    "|> filter(fn: (r) => r[\"_measurement\"] == \"WeatherAPIData_{point}\") "
    "|> filter(fn: (r) => r[\"_field\"] == \"{field}\") "
    "|> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false) "
    "|>  yield(name: \"mean\") "
)

TRAFFIC_QUERY_TEMPLATE = (
    "from(bucket: \"{bucket}\") "
    "|> range(start: v.timeRangeStart, stop: v.timeRangeStop) "
    "|> filter(fn: (r) => r[\"_measurement\"] == \"WeatherAPIData_{point}\") "
    "|> filter(fn: (r) => r[\"_field\"] == \"traffic_percentage\") "
    "|> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false) "
    "|>  yield(name: \"mean\") "
)

def query_influxdb(client, bucket, query_template, point, field, start, stop):
    try:
        query = query_template.format(
            bucket=bucket,
            start=start.isoformat() + "Z",  # Append 'Z' for UTC
            stop=stop.isoformat() + "Z",  # Append 'Z' for UTC
            field=field,
            point=point
        )
        print(f"Running Query:\n{query}")  # Debugging: Log the query
        tables = client.query_api().query(query, org=INFLUXDB_ORG)
        data = [(record.get_time(), record.get_value()) for table in tables for record in table.records]
        return data
    except Exception as e:
        print(f"Error querying data for {point}: {e}")
        return []


def plot_diagrams_per_day(weather_series, traffic_series, point, date):
    plt.figure(figsize=(10, 6))
    for day, data in weather_series.items():
        timestamps, values = zip(*data) if data else ([], [])
        plt.plot(timestamps, values, label=f"Weather ({day})")

    for day, data in traffic_series.items():
        timestamps, values = zip(*data) if data else ([], [])
        plt.plot(timestamps, values, label=f"Traffic ({day})", linestyle='--')

    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.title(f"Weather and Traffic Correlation ({point}) - {date}")
    plt.legend()
    plt.grid()
    filename = os.path.join(OUTPUT_FOLDER, f"{date}_{point}.png")
    plt.savefig(filename)
    plt.close()
    print(f"Saved diagram: {filename}")


def main():
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    today = datetime.now()

    for location, values in POINTS.items():
        # Ensure point and field are present
        if len(values) < 2:
            print(f"Skipping {location} due to missing field configuration.")
            continue

        point, field = values[0], values[1]
        weather_series, traffic_series = {}, {}

        for day_offset in range(3):
            date = (today - timedelta(days=day_offset)).date()
            start = datetime.combine(date, datetime.min.time())
            stop = datetime.combine(date, datetime.max.time())

            # Query data
            weather_series[date] = query_influxdb(
                client, INFLUXDB_BUCKET, WEATHER_QUERY_TEMPLATE, point, field, start, stop
            )
            traffic_series[date] = query_influxdb(
                client, INFLUXDB_BUCKET, TRAFFIC_QUERY_TEMPLATE, point, "traffic_percentage", start, stop
            )

        # Plot for all days
        plot_diagrams_per_day(weather_series, traffic_series, location, today.date())

    client.close()



if __name__ == "__main__":
    main()