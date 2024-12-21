#!/bin/bash

SERVICE_NAME="gpiocontrol.service"
TARGET_DIR="/home/pi/RPi5_MQTT_GPIO_control"
LOG_FILE="/var/log/gpiocontrol.log"

# Pull the latest code from the repository
git pull
#!/bin/bash

SERVICE_NAME="gpiocontrol.service"
TARGET_DIR="/home/pi/RPi5_MQTT_GPIO_control"
LOG_FILE="/var/log/gpiocontrol.log"

echo "Pulling the latest code from the repository..."
git pull

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

echo "Navigating to the target directory..."
cd $TARGET_DIR

echo "Reinstalling the service..."
./install.sh

echo "Copying the service file to the systemd directory..."
sudo cp $SERVICE_NAME /etc/systemd/system/

echo "Installation script completed."
# Stop the service
sudo systemctl stop $SERVICE_NAME

# Disable the service
sudo systemctl disable $SERVICE_NAME

# Remove the service file
sudo rm /etc/systemd/system/$SERVICE_NAME

# Reload the systemd manager configuration
sudo systemctl daemon-reload

# Remove the log file if it exists
if [ -f $LOG_FILE ]; then
    sudo rm $LOG_FILE
fi

# Navigate to the target directory
cd $TARGET_DIR

# Reinstall the service
./install.sh

# Copy the service file to the systemd directory
sudo cp $SERVICE_NAME /etc/systemd/system/

# Reload the systemd manager configuration
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable $SERVICE_NAME

# Start the service
sudo systemctl start $SERVICE_NAME

# Check the status of the service
sudo systemctl status $SERVICE_NAME