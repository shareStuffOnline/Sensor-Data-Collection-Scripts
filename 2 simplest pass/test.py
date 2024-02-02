import serial
import time

def main():
    try:
        # Set up serial connection
        # Replace '/dev/ttyACM0' with your actual serial port
        s = serial.Serial(port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
        s.flush()

        led_state = 0  # Initialize state variable

        while True:
            # Send "0" or "1" to the serial port
            s.write(f"{led_state}\r".encode())
            print(f"Sent: {led_state}")

            # Alternate the state between 0 and 1
            led_state = 1 - led_state

            # Wait for 5 seconds
            time.sleep(5)

    except serial.SerialException as e:
        print("Error:", e)
    finally:
        # Ensure the serial connection is closed on exit
        s.close()

if __name__ == "__main__":
    main()
