import threading
import time
import subprocess

def run_script(path):
    """Execute a Python script given its file path."""
    try:
        subprocess.run(["python", path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {path}: {e}")

def weather_sensors():
    while True:
        run_script("code/data_to_fiware/sensors/weather_sensors_data_mqtt_to_fiware.py")
        time.sleep(2)  

def co2_sensor():
    while True:
        run_script("code/data_to_fiware/sensors/co2_sensor_data_mqtt_to_fiware.py")
        time.sleep(2)  

def noise_level_sensor():
    while True:
        run_script("code/data_to_fiware/sensors/10min_noise_level_sensor_data_mqtt_to_fiware.py")
        time.sleep(2)  

def fiware_to_influx():
    while True:
        run_script("code/fiware_to_influx/all_data_fiware_to_influx.py")
        time.sleep(2)  

def weather_api():
    while True:
        run_script("code/data_to_fiware/APIs/data_weather_api_to_fiware.py")
        time.sleep(600) 

def weather_points_api():
    while True:
        run_script("code/data_to_fiware/APIs/data_points_weather_api_to_fiware.py")
        time.sleep(600) 

def weather_stations_points_api():
    while True:
        run_script("code/data_to_fiware/weather_stations/data_weather_stations_to_fiware.py")
        time.sleep(600) 

def traffic_api():
    while True:
        run_script("code/data_to_fiware/APIs/data_traffic_api_to_fiware.py")
        time.sleep(600) 

if __name__ == "__main__":
    # Threads for continuous tasks
    continuous_threads = [
        threading.Thread(target=weather_sensors, daemon=True),
        threading.Thread(target=co2_sensor, daemon=True),
        threading.Thread(target=noise_level_sensor, daemon=True),
        threading.Thread(target=fiware_to_influx, daemon=True),
    ]

    # Threads for periodic tasks
    periodic_threads = [
        threading.Thread(target=weather_api, daemon=True),
        threading.Thread(target=weather_points_api, daemon=True),
        threading.Thread(target=weather_stations_points_api, daemon=True),
        threading.Thread(target=traffic_api, daemon=True),
    ]

    # Start all threads
    for thread in continuous_threads + periodic_threads:
        thread.start()

    # Keep the main program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated.")