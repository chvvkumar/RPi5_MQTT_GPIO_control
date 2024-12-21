#!/bin/bash

REPO_DIR=$(pwd)
INSTALL_DIR="/home/pi/RPi5_MQTT_GPIO_control"
SERVICE_NAME="gpiocontrol.service"
LOG_FILE="/var/log/gpiocontrol.log"

echo "Performing git pull..."
git pull

echo "Creating installation directory..."
mkdir -p $INSTALL_DIR

echo "Copying files to installation directory..."
cp -r $REPO_DIR/* $INSTALL_DIR

echo "Uninstalling existing service..."
sudo systemctl stop $SERVICE_NAME
sudo systemctl disable $SERVICE_NAME
sudo rm /etc/systemd/system/$SERVICE_NAME
sudo systemctl daemon-reload

echo "Cleaning up old log file..."
if [ -f $LOG_FILE ]; then
    sudo rm $LOG_FILE
fi

echo "Installing new service..."
sudo cp $INSTALL_DIR/gpiocontrol.service /etc/systemd/system/$SERVICE_NAME
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
sudo systemctl status $SERVICE_NAME

echo "Installation script completed."