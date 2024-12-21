#!/bin/bash
SERVICE_NAME="gpiocontrol.service"
LOG_FILE="/var/log/gpiocontrol.log"

echo "Stopping the service..."
sudo systemctl stop $SERVICE_NAME

echo "Disabling the service..."
sudo systemctl disable $SERVICE_NAME

echo "Removing the service file..."
sudo rm /etc/systemd/system/$SERVICE_NAME

echo "Reloading the systemd manager configuration..."
sudo systemctl daemon-reload

echo "Checking if the log file exists..."
if [ -f $LOG_FILE ]; then
    echo "Removing the log file..."
    sudo rm $LOG_FILE
fi

echo "Uninstallation script completed."