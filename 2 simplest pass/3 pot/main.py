from machine import ADC, Pin, PWM
import time

# Create an ADC object on pin GP26
adc = ADC(Pin(26))

# Initialize the LED on pin GP15 as a PWM object
led = PWM(Pin(15))

# Set the frequency of the PWM signal
led.freq(1000)  # 1000 Hz is a common frequency for LEDs

# Function to map the ADC value from one range to another
def map_value(value, in_min, in_max, out_min, out_max):
    # Ensure value does not exceed bounds
    value = max(min(value, in_max), in_min)
    # Map the value
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Function to read ADC value and set LED brightness
def adjust_led_brightness():
    raw_value = adc.read_u16()  # Read a value between 0-65535
    mapped_value = map_value(raw_value, 62000, 65535, 0, 255)
    print("raw_pot_measurement", raw_value)
    print("LED_intensity:", mapped_value)
    led.duty_u16(mapped_value * 257)  # Scale 0-255 to 0-65535 for PWM

# Main loop
while True:
    adjust_led_brightness()
    time.sleep(0.5)  # Wait for 0.5 seconds
