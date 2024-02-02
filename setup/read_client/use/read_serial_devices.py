# python3 read.py --port ttyACM0 --location "loc2"


# pip install pyserial
import serial
import threading
import time

def read_serial(device_name):
    try:
        with serial.Serial(f'/dev/{device_name}', 9600, timeout=1) as ser:
            while True:
                line = ser.readline()
                if line:
                    print(f"{device_name}: {line.decode().strip()}")
                time.sleep(0.1)  # Small delay to prevent CPU overuse
    except serial.SerialException as e:
        print(f"Error with device {device_name}: {e}")

def main():
    # Start threads for each device
    devices = ["frank", "frank1"]
    for device in devices:
        thread = threading.Thread(target=read_serial, args=(device,))
        thread.daemon = True
        thread.start()

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
