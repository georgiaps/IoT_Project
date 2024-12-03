import requests
import json
import os
from datetime import datetime

# Define the API key and base URLs for TomTom APIs
API_KEY = "R51mEIGhkA1ITAySjGZbD5OlRSaJjFHV"
TRAFFIC_FLOW_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
'''TRAFFIC_INCIDENTS_URL = "https://api.tomtom.com/traffic/services/5/incidentDetails"'''

# Define the coordinates for the area of interest
POINT = "38.255539,21.747222"  # Latitude,Longitude for Traffic Flow ston komvo agias sofias, ethnikh odos
'''BBOX = "38.265478,21.752883,38.256404,21.744566"  # Bounding box (lon1,lat1,lon2,lat2) for Traffic Incidents'''

# Define the directory to save the JSON files
SAVE_DIRECTORY = "C:/Users/ariad/OneDrive/Desktop/IoT_Project/data/traffic_data"

# Ensure the directory exists
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

# Define file paths for saving the JSON data
TRAFFIC_FLOW_FILE = os.path.join(SAVE_DIRECTORY, f"traffic_flow_{int(datetime.now().timestamp())}.json")
'''TRAFFIC_INCIDENTS_FILE = os.path.join(SAVE_DIRECTORY, f"traffic_incidents_{int(datetime.now().timestamp())}.json")'''

# Fetch Traffic Flow Data and Add Traffic Percentage
def fetch_traffic_flow():
    try:
        # Make the API call for Traffic Flow
        response = requests.get(f"{TRAFFIC_FLOW_URL}?point={POINT}&key={API_KEY}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON data
        traffic_flow_data = response.json()

        # Calculate traffic percentage
        flow_segment_data = traffic_flow_data.get("flowSegmentData", {})
        if "currentSpeed" in flow_segment_data and "freeFlowSpeed" in flow_segment_data:
            current_speed = flow_segment_data["currentSpeed"]
            free_flow_speed = flow_segment_data["freeFlowSpeed"]
            traffic_percentage = round(((free_flow_speed - current_speed) / free_flow_speed), 2)

            # Add the calculated percentage to the data
            flow_segment_data["trafficPercentage"] = traffic_percentage

        flow_segment_data["time"] = datetime.now().strftime("%X")

        # Save the updated data to a JSON file
        with open(TRAFFIC_FLOW_FILE, "w") as file:
            json.dump(traffic_flow_data, file, indent=4)
        
        print(f"Traffic Flow data saved to {TRAFFIC_FLOW_FILE}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Traffic Flow data: {e}")

'''# Fetch Traffic Incidents Data
def fetch_traffic_incidents():
    try:
        # Make the API call for Traffic Incidents
        response = requests.get(f"{TRAFFIC_INCIDENTS_URL}?bbox={BBOX}&key={API_KEY}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse and save the JSON data
        traffic_incidents_data = response.json()
        with open(TRAFFIC_INCIDENTS_FILE, "w") as file:
            json.dump(traffic_incidents_data, file, indent=4)
        
        print(f"Traffic Incidents data saved to {TRAFFIC_INCIDENTS_FILE}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Traffic Incidents data: {e}")'''

# Run the functions to fetch and save data
fetch_traffic_flow()
'''fetch_traffic_incidents()'''