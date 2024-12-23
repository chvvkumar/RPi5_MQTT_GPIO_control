# Control Pi5 GPIO from MQTT

This project allows you to control the GPIO pins on a Raspberry Pi 5 using MQTT messages. The service subscribes to a specified MQTT topic and processes JSON payloads to control the GPIO pins.

## Installation

1. Clone the repository to your Raspberry Pi:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create venv and Install the required dependencies (or run the install script. Please read what it does before running it):
    ```sh
    pip install -r requirements.txt
    ```

3. Configure the service:
    - Edit the `config.txt` file to set your MQTT broker details:
        ```
        [MQTT]
        broker = <your_mqtt_broker>
        port = <your_mqtt_port>
        topic = <your_mqtt_topic>
        username = <your_mqtt_username>
        password = <your_mqtt_password>
        ```

4. Install and start the systemd service:
    ```sh
    sudo ./install.sh
    ```

## Usage

Send a JSON payload to the configured MQTT topic to control the GPIO pins. Below is an example of a JSON payload:

```json
{
    "name": "GPIO Name",
    "gpio": 21,
    "properties": {
        "direction": "out",
        "state": "on"
    }
}
