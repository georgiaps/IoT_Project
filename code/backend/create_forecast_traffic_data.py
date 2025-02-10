from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime, timedelta
from influxdb_client.client.write_api import WriteOptions

# InfluxDB connection details
influxdb_url = "http://150.140.186.118:8086"
bucket = "MicroclimateTraffic-team08-Final"
org = "students"
token = "sJcp3CYIFhde06U1V9LMu1Qcsl0KVo4die707OYtsM9XNzTg-w5-tUlbwtzQtm3rS30xIL5N9jT92h6K05cpiw=="

# Location mapping
location_mapping = {
    "University Crossroad": "TrafficAPIData_diastaurwsh_panepisthmio",
    "Agyias Beach": "TrafficAPIData_plaz",
    "National Road Interchange": "TrafficAPIData_diastaurwsh_ethnikh",
    "Patras Centre": "TrafficAPIData_ermou",
    "Gounarh Road": "TrafficAPIData_gounarh",
    "South Park": "TrafficAPIData_notio_parko",
    "Dasyllio": "TrafficAPIData_dasyllio",
    "Rio-Antirrio Bridge": "TrafficAPIData_gefyra_rio_antirrio",
    "Leuka": "TrafficAPIData_leuka",
    "Paralia": "TrafficAPIData_paralia",
    "Kato Sychaina": "TrafficAPIData_kato_sychaina",
    "Demenika": "TrafficAPIData_demenika",
    "Kastelokampos": "TrafficAPIData_kastelokampos",
    "University of Patras": "TrafficAPIData_university_patras"
}

# Initialize InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=token, org=org)
query_api = client.query_api()
with client.write_api(write_options=WriteOptions(batch_size=500)) as write_api:
    for location, measurement in location_mapping.items():
        forecast_measurement = f"Forecast_{measurement}"
        
        # Query the latest timestamps in the forecast measurement to avoid duplicates
        latest_query = f'''from(bucket: "{bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r._measurement == "{forecast_measurement}")
            |> keep(columns: ["_time"])
            |> sort(columns: ["_time"], desc: true)
            |> limit(n:1)'''
        latest_result = query_api.query(latest_query)
        latest_time = None
        if latest_result and latest_result[0].records:
            latest_time = latest_result[0].records[0].get_time()
        
        # Query traffic_percentage from the past 7 days
        query = f'''
            from(bucket: "{bucket}")
            |> range(start: -7d, stop: now())
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) => r["_field"] == "traffic_percentage")
        '''

        result = query_api.query(query)
        
        points = []
        for table in result:
            for record in table.records:
                new_time = record.get_time() + timedelta(days=7)
                if latest_time and new_time <= latest_time:
                    continue  # Skip duplicates
                
                point = Point(forecast_measurement)
                point.time(new_time, WritePrecision.NS)
                point.field("traffic_percentage", record.get_value())
                points.append(point)
        
        if points:
            write_api.write(bucket=bucket, org=org, record=points)

client.close()  # Close the client after the `with` block