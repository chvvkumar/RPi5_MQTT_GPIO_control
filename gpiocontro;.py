import json
import logging
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from threading import Timer

# Define the timer
disconnect_timer = None

# Define the on_disconnect callback function
def on_disconnect(client, userdata, rc):
    global disconnect_timer
    if rc != 0:
        logging.warning("Unexpected disconnection. Starting a timer to turn off GPIO pins.")
    # Start a timer to turn off GPIO pins after 15 minutes
    disconnect_timer = Timer(900, turn_off_gpio_pins)
    disconnect_timer.start()

def on_connect(client, userdata, flags, rc):
    global disconnect_timer
    if rc == 0:
        logging.info("Connected to MQTT broker")
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