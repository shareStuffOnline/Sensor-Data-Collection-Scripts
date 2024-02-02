import serial
import time
import argparse
import sys
from datetime import datetime
import paho.mqtt.publish as publish

# Setup argument parser
parser = argparse.ArgumentParser(description='Read data from a specified serial port.')
parser.add_argument('--location', type=str, help='Location of the device')
parser.add_argument('--port', type=str, required=True, help='Symlink name of the TTY port (e.g., toggler1)')
args = parser.parse_args()

# Function to connect to the serial port
def connect_to_serial(port_name):
    try:
        return serial.Serial(f'/dev/{port_name}', 115200, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port /dev/{port_name}: {e}")
        return None

# Attempt to connect to the serial port
ser = connect_to_serial(args.port)

# Function to get current time in a short, formatted string
def current_time():
    return datetime.now().strftime('%H:%M:%S')

# Function to format the output message
def format_message(location, sensor_type, reading):
    topic = f"{location}/{sensor_type}"
    message = f" {reading}"
    return topic, message

# Continuously try to read from the serial port
while True:
    if ser:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                sensor_readings = line.split('\n')
                for sensor_reading in sensor_readings:
                    parts = sensor_reading.split(':', 1)
                    if len(parts) == 2:
                        sensor_type, reading = parts
                        reading = reading.strip()
                        topic, formatted_line = format_message(args.location, sensor_type.strip(), reading)
                        # Publish to MQTT broker
                        publish.single(topic, formatted_line, hostname="arpa.net.ai")
                        print(f"{topic} {formatted_line}")
        except (serial.SerialException, OSError) as e:
            print(f"Serial error: {e}")
            ser.close()
            ser = None
    else:
        print(f"Waiting for device /dev/{args.port} at {args.location}...")
        ser = connect_to_serial(args.port)
        time.sleep(5)  # Wait before trying to reconnect

    time.sleep(0.1)

    # Handle KeyboardInterrupt outside the inner try-except to ensure proper termination
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program terminated by user")
        if ser:
            ser.close()
        sys.exit(0)
