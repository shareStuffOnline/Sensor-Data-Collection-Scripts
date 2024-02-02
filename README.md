# Sensor-Data-Collection-Scripts
### under construction
This repository contains scripts for collecting sensor data from microcontrollers, reading the data from a serial port, and generating udev rules for the sensors.

## Usage

1. Run `main.py` on your microcontroller supporting micropython to read sensor data and print it out at regular intervals.


2. Run `read.py` on a computer or embedded device with network capabilities to read the sensor data from a serial port, format it, and publish it to an MQTT broker.

python3 read.py --port ttyACM0 --location "/topic/location"

3. Run `generate_udev_rules.py` to generate udev rules for your sensors. This will create symbolic links to your devices that don't change even if the devices are plugged into different USB ports.

sudo python3 generate_udev_rules.py

