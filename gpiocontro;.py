import json
import logging
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import configparser
import os
from threading import Timer

# Load configuration from config.txt
config = configparser.ConfigParser()
config.read('config.txt')

MQTT_BROKER = config['MQTT']['broker']
MQTT_PORT = int(config['MQTT']['port'])
MQTT_TOPIC = config['MQTT']['topic']
MQTT_USERNAME = config['MQTT'].get('username')
MQTT_PASSWORD = config['MQTT'].get('password')


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Define the timer
disconnect_timer = None

# Define the on_disconnect callback function
def on_disconnect(client, userdata, rc):
    global disconnect_timer
    if rc != 0:
        logging.warning("Unexpected disconnection.")
    # Start a timer to turn off GPIO pins after 15 minutes
    disconnect_timer = Timer(900, turn_off_gpio_pins)
    disconnect_timer.start()

def on_connect(client, userdata, flags, rc):
    global disconnect_timer
    if rc == 0:
        logging.info("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
        # Cancel the disconnect timer if it exists
        if disconnect_timer:
            disconnect_timer.cancel()
            disconnect_timer = None
    else:
        logging.error("Failed to connect, return code %d\n", rc)

def turn_off_gpio_pins():
    GPIO.cleanup()
    logging.info("All GPIO pins have been turned off due to prolonged disconnection.")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        
        # Validate JSON structure
        if "gpio" not in data or "properties" not in data or "direction" not in data["properties"] or "state" not in data["properties"]:
            logging.error("Invalid JSON structure")
            return
        
        gpio_pin = data["gpio"]
        direction = data["properties"]["direction"]
        state = data["properties"]["state"]
        name = data["name"]

        if direction == "out":
            GPIO.setup(gpio_pin, GPIO.OUT)
            logging.info(f"GPIO {name} - {gpio_pin} set to OUT")
            if state == "on":
                GPIO.output(gpio_pin, GPIO.HIGH)
                logging.info(f"GPIO {name} - {gpio_pin} set to HIGH")
            elif state == "off":
                GPIO.output(gpio_pin, GPIO.LOW)
                logging.info(f"GPIO {name} - {gpio_pin} set to LOW")
            else:
                logging.error("Unknown state: %s", state)
        elif direction == "in":
            GPIO.setup(gpio_pin, GPIO.IN)
            logging.info(f"GPIO {name} - {gpio_pin} set to IN")
        else:
            logging.error("Unknown direction: %s", direction)
    except json.JSONDecodeError:
        logging.error("Error decoding JSON")
    except Exception as e:
        logging.error("Error processing message: %s", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Set MQTT login credentials if provided
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()