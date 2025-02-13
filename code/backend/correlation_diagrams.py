import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuration for InfluxDB
INFLUXDB_URL = "http://150.140.186.118:8086"  
INFLUXDB_TOKEN = "sJcp3CYIFhde06U1V9LMu1Qcsl0KVo4die707OYtsM9XNzTg-w5-tUlbwtzQtm3rS30xIL5N9jT92h6K05cpiw=="  
INFLUXDB_ORG = "students"  
INFLUXDB_BUCKET = "MicroclimateTraffic-team08-Final" 

# Points configuration with units
POINTS = {
    "University Crossroad": ["diastaurwsh_panepisthmio", "rain_1h", "mm"],
    "Agyias Beach": ["plaz", "temperature", "°C"],
    "National Road Interchange": ["diastaurwsh_ethnikh", "rain_1h", "mm"],
    "Patras Centre": ["ermou", "temperature", "°C"],
    "South Park": ["notio_parko", "temperature", "°C"],
    "Dasyllio": ["dasyllio", "humidity", "%"],
    "Rio-Antirrio Bridge": ["gefyra_rio_antirrio", "wind_speed", "m/sec"]
}

def query_influxdb(client, bucket, point, measurement_type, field, start, stop):
    try:
        query = f'''
        from(bucket: "{bucket}")
        |> range(start: {start.isoformat()}Z, stop: {stop.isoformat()}Z)
        |> filter(fn: (r) => r["_measurement"] == "{measurement_type}_{point}")
        |> filter(fn: (r) => r["_field"] == "{field}")
        |> aggregateWindow(every: 15m, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''
        
        tables = client.query_api().query(query, org=INFLUXDB_ORG)
        data = [(record.get_time(), record.get_value()) for table in tables for record in table.records]
        return data
    except Exception as exc:
        print(f"Error querying data for {point}: {exc}")
        return []
            

def plot_daily_diagrams(client, bucket, point, point_code, weather_field, weather_unit, date): 
    point_folder = os.path.join("code/backend/static/correlation_diagrams", point)
    os.makedirs(point_folder, exist_ok=True)
    
    for day_offset in range(3):
        current_date = (date - timedelta(days=day_offset)).date()
        start = datetime.combine(current_date, datetime.min.time())
        stop = datetime.combine(current_date, datetime.max.time())
        
        filename = os.path.join(point_folder, f"{current_date}.png")
        
        # If the file exists, it will be replaced with a new diagram
        if os.path.exists(filename):
            print(f"Diagram for {current_date} already exists, replacing it.")

        traffic_data = query_influxdb(
            client, bucket, point_code, "TrafficAPIData", "traffic_percentage", start, stop
        )

        weather_data = query_influxdb(
            client, bucket, point_code, "WeatherAPIData", weather_field, start, stop
        )

        if traffic_data or weather_data:
            fig, ax1 = plt.subplots(figsize=(12, 7))
            ax2 = ax1.twinx()

            if traffic_data:
                traffic_times, traffic_values = zip(*traffic_data)
                # Add +2 hours to the traffic times
                traffic_times = [t + timedelta(hours=2) for t in traffic_times]
                traffic_values = [val * 100 for val in traffic_values]
                ax1.plot(traffic_times, traffic_values, label='Traffic Percentage', color='#75283d', linestyle='-')
                ax1.set_ylabel('Traffic Percentage (%)', color='#75283d', fontsize=18, labelpad=16)
                ax1.tick_params(axis='y', labelcolor='#75283d')

            if weather_data:
                weather_times, weather_values = zip(*weather_data)
                # Add +2 hours to the weather times
                weather_times = [t + timedelta(hours=2) for t in weather_times]
                ax2.plot(weather_times, weather_values, label=f'{weather_field.capitalize()}', color='#2b6cb0', linestyle='--')
                ax2.set_ylabel(f'{weather_field.capitalize()} ({weather_unit})', color='#2b6cb0', fontsize=18, labelpad=16)
                ax2.tick_params(axis='y', labelcolor='#2b6cb0')

            plt.title(f"{point} - {current_date}", fontsize=20)
            ax1.set_xlabel("Time", fontsize=16, labelpad=15)
            ax1.grid(True)

            # Format x-axis to show only time
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

            # Save the diagram, overwriting if the file exists
            plt.savefig(filename, bbox_inches='tight')
            plt.close()
            print(f"Saved or replaced diagram: {filename}")
        else:
            plt.close()
            print(f"No data found for {point} on {current_date}")


def main():
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    today = datetime.now()

    for location, (point_code, weather_field, weather_unit) in POINTS.items():
        plot_daily_diagrams(client, INFLUXDB_BUCKET, location, point_code, weather_field, weather_unit, today)

    client.close()

if __name__ == "__main__":
    main()