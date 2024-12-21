#!/bin/bash

# Define the target directory
TARGET_DIR="/home/pi/RPi5_MQTT_GPIO_control"

# Create the target directory if it doesn't exist
mkdir -p $TARGET_DIR

# Copy all files from the current directory to the target directory
cp -r * $TARGET_DIR

# Navigate to the target directory
cd $TARGET_DIR

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

echo "Setup complete. Files copied to $TARGET_DIR, virtual environment created, and requirements installed."