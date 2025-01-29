from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app) 

# Mapping between backend location names and FIWARE entity names
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

    "Patras": "WeatherAPIDataPatras"
}

forecast_entity = "WeatherForecastAPIDataPatras"

# Initialize data store
city_data = {
    "University Crossroad": {},
    "Agyias Beach": {},
    "National Road Interchange": {},
    "Patras Centre": {},
    "Gounarh Road": {},
    "South Park": {},
    "Dasyllio": {},
    "Rio-Antirrio Bridge": {},
    "Leuka": {},
    "Paralia": {},
    "Kato Sychaina": {},
    "Demenika": {},
    "Kastelokampos": {},
    "Patras": {},
    "University of Patras": {}
}

# FIWARE API endpoint
FIWARE_BASE_URL = "http://150.140.186.118:1026/v2/entities"

def fetch_fiware_data():
    """Fetch updated data from FIWARE and update city_data."""
    for backend_name, fiware_entity in location_mapping.items():
        #print(f"Fetching weather data for: {fiware_entity}")

        # Fetch weather data
        weather_response = requests.get(f"{FIWARE_BASE_URL}/{fiware_entity}")

        if (weather_response.status_code == 200) & (backend_name != "Patras"):
            try:
                weather_data = weather_response.json()
                city_data[backend_name]["weather"] = {
                    "Temperature": weather_data.get("temperature", {}).get("value", "N/A"),
                    "Humidity": weather_data.get("humidity", {}).get("value", "N/A"),
                    "Wind Speed": weather_data.get("wind_speed", {}).get("value", "N/A"),
                    "Wind Direction": weather_data.get("wind_deg", {}).get("value", "N/A"),
                    "Rain": weather_data.get("rain_1h", {}).get("value", "N/A"),
                    "Pressure": weather_data.get("pressure", {}).get("value", "N/A")
                }
            except Exception as e:
                print(f"Error processing weather data for {fiware_entity}: {e}")

        elif (weather_response.status_code == 200) & (backend_name == "Patras"):
            try:
                weather_data = weather_response.json()
                city_data[backend_name]["weather"] = {
                    "Description": weather_data.get("description", {}).get("value", "N/A"),
                    "Temperature": weather_data.get("temperature", {}).get("value", "N/A"),
                    "Humidity": weather_data.get("humidity", {}).get("value", "N/A"),
                    "Wind Speed": weather_data.get("wind_speed", {}).get("value", "N/A"),
                    "Wind Direction": weather_data.get("wind_deg", {}).get("value", "N/A"),
                    "Rain": weather_data.get("rain_1h", {}).get("value", "N/A"),
                    "Pressure": weather_data.get("pressure", {}).get("value", "N/A")
                }
            except Exception as e:
                print(f"Error processing weather data for {fiware_entity}: {e}")

        # Traffic data mapping (optional)
        traffic_entity = fiware_entity.replace("WeatherAPIData_", "TrafficAPIData_")
        #print(f"Fetching traffic data for: {traffic_entity}")

        # Fetch traffic data
        traffic_response = requests.get(f"{FIWARE_BASE_URL}/{traffic_entity}")

        if (traffic_response.status_code == 200) & (backend_name != "Patras"):
            try:
                traffic_data = traffic_response.json()
                city_data[backend_name]["traffic"] = {
                    "Current Speed": traffic_data.get("current_speed", {}).get("value", "N/A"),
                    "Free Flow Speed": traffic_data.get("free_flow_speed", {}).get("value", "N/A"),
                    "Traffic Percentage": traffic_data.get("traffic_percentage", {}).get("value", "N/A")
                }
            except Exception as e:
                print(f"Error processing traffic data for {traffic_entity}: {e}")
    print("Completed fetching traffic data for all the locations")

def fetch_fiware_uni_data():
    """Fetch updated data from FIWARE and update city_data."""

    # Fetch weather data
    weather_response = requests.get(f"{FIWARE_BASE_URL}/UnifiedWeatherSensorDataUni")

    if (weather_response.status_code == 200):
        try:
            weather_data = weather_response.json()
            city_data["University of Patras"]["weather"] = {
                "Temperature": weather_data.get("temperature", {}).get("value", "N/A"),
                "Humidity": weather_data.get("humidity", {}).get("value", "N/A"),
                "Wind Speed": weather_data.get("wind_speed", {}).get("value", "N/A"),
                "Wind Direction": weather_data.get("wind_direction", {}).get("value", "N/A"),
                "Rain": weather_data.get("rain", {}).get("value", "N/A"),
                "Pressure": weather_data.get("pressure", {}).get("value", "N/A")
            }
        except Exception as e:
            print(f"Error processing weather data for university of patras: {e}")

    # Fetch traffic data
    traffic_response = requests.get(f"{FIWARE_BASE_URL}/TrafficAPIData_university_patras")

    if (traffic_response.status_code == 200):
        try:
            traffic_data = traffic_response.json()
            city_data["University of Patras"]["traffic"] = {
                "Current Speed": traffic_data.get("current_speed", {}).get("value", "N/A"),
                "Free Flow Speed": traffic_data.get("free_flow_speed", {}).get("value", "N/A"),
                "Traffic Percentage": traffic_data.get("traffic_percentage", {}).get("value", "N/A")
            }
        except Exception as e:
            print(f"Error processing traffic data for university of patras: {e}")

def fetch_fiware_forecast_data():
    """Fetch updated forecast data from FIWARE and update city_data."""
    
    forecast_response = requests.get(f"{FIWARE_BASE_URL}/{forecast_entity}")

    if forecast_response.status_code == 200:
        try:
            forecast_data = forecast_response.json()
            forecast_values = forecast_data.get("forecast", {}).get("value", [])

            # Update forecast data for all locations
            for backend_name, _ in location_mapping.items():
                if backend_name != "Patras":
                    city_data[backend_name]["forecast"] = forecast_values

            # Manually update "University of Patras"
            city_data["University of Patras"]["forecast"] = forecast_values

            print(f"Updated forecast data for all locations, including University of Patras.")
        
        except Exception as e:
            print(f"Error processing forecast data: {e}")
    else:
        print(f"Failed to fetch forecast data: {forecast_response.status_code} - {forecast_response.text}")
    
# Schedule FIWARE data updates every 10 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_fiware_data, 'interval', minutes=10)
scheduler.add_job(fetch_fiware_uni_data, 'interval', minutes=10)
scheduler.add_job(fetch_fiware_forecast_data, 'interval', minutes=10)
scheduler.start()

@app.route('/api/city-data', methods=['GET'])
def get_city_data():
    """Endpoint to retrieve updated city data."""
    return jsonify(city_data)

# Run Flask app
if __name__ == '__main__':
    # Fetch initial data on startup
    fetch_fiware_data()
    fetch_fiware_uni_data()
    fetch_fiware_forecast_data()
    app.run(host='0.0.0.0', port=8080, debug=True)