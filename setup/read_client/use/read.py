# python3 read.py --port ttyACM0 --location "loc2"


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
def format_message(location, message):
    truncated_location = (location[:12] + '..') if len(location) > 12 else location
    location_format = f"[{truncated_location}]".ljust(14)
    truncated_message = (message[:23] + '...') if len(message) > 26 else message
    message_format = f"{truncated_message:^26}"
    return f"{message_format}{location_format} @{current_time()}"

# Continuously try to read from the serial port
while True:
    if ser:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                formatted_line = format_message(args.location, line)
                print(formatted_line)
                publish.single(args.location, formatted_line, hostname="local.werx.broker")

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

