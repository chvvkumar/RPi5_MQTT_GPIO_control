import json
import logging
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import configparser
import os
from threading import Timer
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from config.txt
config = configparser.ConfigParser()
config.read('config.txt')

MQTT_BROKER = config['MQTT']['broker']
MQTT_PORT = int(config['MQTT']['port'])
MQTT_TOPIC = config['MQTT']['receive_topic']
MQTT_USERNAME = config['MQTT'].get('username')
MQTT_PASSWORD = config['MQTT'].get('password')
PUBLISH_TOPIC = config['MQTT']['publish_topic']

logging.info(f"MQTT Topic: {MQTT_TOPIC}")
logging.info(f"MQTT Publish Topic: {PUBLISH_TOPIC}")

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

def check_gpio_status(gpio_pin, name):
    state = GPIO.input(gpio_pin)
    status = "HIGH" if state == GPIO.HIGH else "LOW"
    status_message = json.dumps({"gpio": gpio_pin, "name": name, "status": status})
    client.publish(PUBLISH_TOPIC, status_message)
    logging.info(f"Published GPIO {name} - {gpio_pin} status: {status}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        
        # Validate JSON structure
        if "MQTT_GPIO" not in data:
            logging.error("Invalid JSON structure")
            return
        
        gpio_data = data["MQTT_GPIO"]
        
        for pin_key, pin_data in gpio_data.items():
            gpio_pin = pin_data["pin"]
            direction = pin_data["direction"]
            state = pin_data["state"]
            name = pin_data["name"]

            logging.info(f"Processing GPIO {name} - {gpio_pin} with direction {direction} and state {state}")
            
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
                
                # Check the status after 5 seconds
                threading.Timer(5.0, check_gpio_status, args=(gpio_pin, name)).start()
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
client.loop_start()

#GPIO.cleanup()

logging.info("Sleeping for 30 seconds before restarting")
sleep_time = 30
logging.info(f"Sleeping for {sleep_time} seconds")
time.sleep(sleep_time)
