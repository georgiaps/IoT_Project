openweather_API_key = "9bb20a8d36e77bd9d405689a1c985d28"
tomtom_API_key = "R51mEIGhkA1ITAySjGZbD5OlRSaJjFHV"

microclimate_sensor_topic = 'Environmental/barani-meteohelix-iot-pro:1' #air temperature, humidity, sun intensity
wind_sensor_topic = 'json/Environmental/barani-meteowind-iot-pro:1' #wind speed and direction
noise_sensor_topic = 'json/Environmental/dutch-sensor-systems-ranos-db-2:1'
co2_sensor_topic = 'json/Room monitoring/mclimate-co2-sensor:1'

fiware_host = "http://150.140.186.118:1026/v2/entities"
fiware_service_path = "/microclimateandtraffic"
fiware_weather_data = 'http://150.140.186.118:1026/v2/entities?type=WeatherData'
fiware_traffic_data = 'http://150.140.186.118:1026/v2/entities?type=TrafficData'

influxdb_url = "http://150.140.186.118:8086"
bucket = "MicroclimateTraffic"
org = "students"
token = "N5EVklgWe-dWwE0YxgvWXIsi_mifEjPm-kNZy7U-MmLgUSLbsa43-gOSKYkEu1UHyg3EeihC8pB_oUU_IssaFw=="