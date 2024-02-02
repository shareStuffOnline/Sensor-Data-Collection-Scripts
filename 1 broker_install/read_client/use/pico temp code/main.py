from picozero import RGBLED
from bme680 import *
from machine import I2C, Pin
import time

# Initialize RGB LED
rgb = RGBLED(red=13, green=14, blue=15)

# Initialize I2C for BME680
i2c = I2C(0, scl=Pin(17), sda=Pin(16))

# Initialize BME680 sensor
bme = BME680_I2C(i2c)

# Function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

# Function to change LED color based on temperature
def set_led_color(temp_f):
    if temp_f < 78:
        rgb.color = (0, 0, 255)  # Blue
    elif temp_f < 81:
        rgb.color = (0, 255, 0)  # Green
    else:
        rgb.color = (255, 0, 0)  # Red

# Main loop
while True:
    temperature_c = bme.temperature
    temperature_f = celsius_to_fahrenheit(temperature_c)
    set_led_color(temperature_f)  # Set LED color based on temperature

    print("Temperature:", temperature_f, "°F")
    print("Humidity:", bme.humidity, "%")
    print("Pressure:", bme.pressure, "hPa")
    print("Gas_Resistance:", bme.gas, "Ohms")

    time.sleep(1)

