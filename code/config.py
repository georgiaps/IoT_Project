openweather_API_key = "9bb20a8d36e77bd9d405689a1c985d28"
tomtom_API_key = "R51mEIGhkA1ITAySjGZbD5OlRSaJjFHV"
googlemaps_API_key = "AIzaSyCRKU-OL54ZavlAUgYhxeDjdv9_rx4jLGM"

openweather_API_city_link = "https://api.openweathermap.org/data/2.5/weather?q={patras}&appid={9bb20a8d36e77bd9d405689a1c985d28}&units={metric}"
openweather_API_points_link = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={9bb20a8d36e77bd9d405689a1c985d28}&units={metric}"
openweather_API_forecast_link = "https://api.openweathermap.org/data/2.5/forecast?q={patras}&appid={9bb20a8d36e77bd9d405689a1c985d28}&units={metric}"
tomtom_API_link = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={coordinates}&key={R51mEIGhkA1ITAySjGZbD5OlRSaJjFHV}"

microclimate_sensor_topic = 'Environmental/barani-meteohelix-iot-pro:1' #air temperature, humidity, sun intensity
wind_sensor_topic = 'json/Environmental/barani-meteowind-iot-pro:1' #wind speed and direction
noise_sensor_topic = 'json/Environmental/dutch-sensor-systems-ranos-db-2:1'
co2_sensor_topic = 'json/Room monitoring/mclimate-co2-sensor:1'


broker = '150.140.186.118'
port = 1883


fiware_host = "http://150.140.186.118:1026/v2/entities"
fiware_service_path = "/microclimateandtraffic"
fiware_weather_data = 'http://150.140.186.118:1026/v2/entities?type=omada08_WeatherData'
fiware_traffic_data = 'http://150.140.186.118:1026/v2/entities?type=omada08_TrafficData'


influxdb_url = "http://150.140.186.118:8086"
bucket = "MicroclimateTraffic-team08"
org = "students"
token = "N5EVklgWe-dWwE0YxgvWXIsi_mifEjPm-kNZy7U-MmLgUSLbsa43-gOSKYkEu1UHyg3EeihC8pB_oUU_IssaFw=="

bucket = "MicroclimateTraffic-team08-Final"
org = "students"
token = "sJcp3CYIFhde06U1V9LMu1Qcsl0KVo4die707OYtsM9XNzTg-w5-tUlbwtzQtm3rS30xIL5N9jT92h6K05cpiw=="