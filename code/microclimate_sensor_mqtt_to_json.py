import paho.mqtt.client as mqtt_client
import random
import json
import os

broker = '150.140.186.118'
port = 1883
client_id = 'rand_id' + str(random.random())  # Something like a username
topic = 'json/Environmental/barani-meteohelix-iot-pro:1'  # Specify the topic you'd like to subscribe to
OUTPUT_DIR = "C:/Users/ariad/OneDrive/Desktop/IoT_Project/data/sensor_weather_data"  # Directory to save the JSON files

# Connect to the MQTT broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Process the incoming message and extract temperature, humidity and rain
def process_func(message):
    """Process the incoming message to extract temperature, humidity and rain."""
    try:
        # Load the JSON message
        data = json.loads(message)

        # Extract temperature, humidity and rain from the `object` field
        measurements = data.get('object', {})
        if measurements:
            temperature = measurements.get('Temperature')
            humidity = measurements.get('Humidity')
            rain = measurements.get('Rain')
            if temperature is not None and humidity is not None and rain is not None:
                # Return rounded temperature, humidity and rain
                return round(float(temperature), 2), round(float(humidity), 2), round(float(rain), 2)
    except json.JSONDecodeError:
        print("Received message is not valid JSON.")
    except (IndexError, ValueError):
        print("Error extracting data from measurements.")
    return None, None, None  # Return None if data extraction fails

# Save temperature, humidity and rain to a JSON file
def save_to_json_file(data, output_dir):
    """Save extracted data to a JSON file."""
    #filename = "environmental_data.json"
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the file path (e.g., weather_patras.json)
    file_path = os.path.join(output_dir, f"environmental_data.json")
    
    try:
        # Append to the JSON file if it exists, else create it
        with open(file_path, 'a') as file:
            json.dump(data, file)
            file.write("\n")  # Newline for each message
        print(f"Data saved to file")
    except IOError as e:
        print(f"Error saving data to file: {e}")

# Subscribe to the MQTT topic and handle incoming messages
def subscribe(client):
    def on_message(client, userdata, msg):
        # Decode the message payload
        message = msg.payload.decode()

        # Process the message to extract temperature, humidity and rain
        temperature, humidity, rain = process_func(message)
        if temperature is not None and humidity is not None and rain is not None:
            print(f"Extracted Data -> Temperature: {temperature}°C, Humidity: {humidity}%, Rain: {rain}mm")

            # Save the data to a JSON file
            save_to_json_file({
                "Temperature": temperature,
                "Humidity": humidity,
                "Rain": rain
            }, OUTPUT_DIR)
        else:
            print("Unable to extract temperature, humidity and rain from the message.")

    client.subscribe(topic)
    client.on_message = on_message

# Run the MQTT client
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()  # Keep the client connected and listening for messages

if __name__ == '__main__':
    run()
