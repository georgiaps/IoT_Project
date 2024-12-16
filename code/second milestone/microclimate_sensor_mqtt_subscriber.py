import paho.mqtt.client as mqtt_client
import random 
import json

broker = '150.140.186.118'  # ip tou ergasthriou
port = 1883
client_id = 'rand_id' +str(random.random())  # kati san to username
topic = 'json/Environmental/barani-meteohelix-iot-pro:1'  # Specify the topic you'd like to subscribe to, an valw "#" tha lambanw mhnumata apola ta topics 
# username = 'your_username'  # Optional: Use if your broker requires a username
# password = 'your_password'  # Optional: Use if your broker requires a password

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)  # Uncomment if username/password is required
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client):
    def on_message(client, userdata, msg):
        # Decode the message payload
        message = msg.payload.decode()
        
        # Process the message to extract temperature
        temperature = process_func(message)
        if temperature is not None:
            print(f"Extracted Temperature: {temperature}°C")
        else:
            print("Unable to extract temperature from the message.")

        #print(f"Received {msg.payload.decode()} from {msg.topic} topic")

    client.subscribe(topic)
    client.on_message = on_message


def process_func(message):
    """Process the incoming message and extract temperature data."""
    try:
        # Load the JSON message
        data = json.loads(message)
        
        # Extract temperature from measurements
        measurements = data.get('object', {})
        if measurements:
            # Assuming we are interested in the first measurement's LAeq as the temperature value
            temperature = measurements.get('Temperature')  # Modify if you need a different value
            if temperature is not None:
                return round(float(temperature), 2)
    except json.JSONDecodeError:
        print("Received message is not valid JSON.")
    except (IndexError, ValueError):
        print("Error extracting temperature from measurements.")  


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()  # Keep the client connected and listening for messages


if __name__ == '__main__':
    run()
