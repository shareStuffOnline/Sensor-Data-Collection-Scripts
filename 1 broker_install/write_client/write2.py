import serial
import time

port = '/dev/ttyACM0'  # Replace with the correct port
baudrate = 115200

with serial.Serial(port, baudrate, timeout=1) as ser:
    while True:
        ser.write(b'255\n')  # Turn LED on
        time.sleep(2)
        ser.write(b'56\n')  # Turn LED off
        time.sleep(2)
        ser.write(b'0\n')  # Flash LED
        time.sleep(2)
