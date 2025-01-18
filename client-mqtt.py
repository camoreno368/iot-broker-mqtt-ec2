import paho.mqtt.client as mqtt
import csv
from datetime import datetime
import json

# MQTT Configuration
MQTT_BROKER = "54.87.187.153"  # broker address
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/pub"  # Change to your ESP32 topic

# CSV Configuration
CSV_FILENAME = "esp32_data.csv"

# Initialize CSV file with headers
def init_csv():
    with open(CSV_FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature", "Humidity"])  # headers

# Callback when connecting to MQTT broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# Callback when receiving a message
def on_message(client, userdata, msg):
    try:
        # Assuming ESP32 sends JSON data
        data = json.loads(msg.payload.decode())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write to CSV
        with open(CSV_FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                data.get('temperature', ''),
                data.get('humidity', '')
            ])
        print(f"Data saved: {data}")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    # Initialize CSV file
    init_csv()

    # Set up MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to MQTT broker
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        print(f"Error connecting to broker: {e}")

if __name__ == "__main__":
    main()