#!/bin/bash
echo "Installing and Configuring Mosquitto MQTT Broker"

# Update package list
sudo apt-get update

# Install Mosquitto broker
sudo apt-get install -y mosquitto mosquitto-clients

# Enable Mosquitto broker to start on boot
sudo systemctl enable mosquitto.service

# Basic configuration setup
# Create a configuration file (modify as needed)
MOSQUITTO_CONF="/etc/mosquitto/conf.d/default.conf"
echo "Creating a basic configuration file for Mosquitto at $MOSQUITTO_CONF"

# You can add your configuration lines here. For example:
#echo "listener 1883" | sudo tee $MOSQUITTO_CONF
echo "listener 1883 172.17.17.17" | sudo tee $MOSQUITTO_CONF
echo "allow_anonymous true" | sudo tee -a $MOSQUITTO_CONF

# Restart Mosquitto service to apply changes
sudo systemctl restart mosquitto

echo "Mosquitto MQTT Broker installation and basic configuration complete."

