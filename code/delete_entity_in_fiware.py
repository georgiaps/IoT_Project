import requests

url = "http://150.140.186.118:1026/v2/entities/WeatherForecastAPIDataPatras"
fiware_service_path = "/microclimateandtraffic"

headers = {
    
    "Fiware-ServicePath": fiware_service_path  # Optional
}

response = requests.delete(url, headers=headers)

if response.status_code == 204:
    print("Entity deleted successfully.")
else:
    print(f"Failed to delete entity. Status code: {response.status_code}, Message: {response.text}")
