from machine import ADC, Pin, PWM
import time

# Create an ADC object on pin GP26
adc = ADC(Pin(26))

# Initialize the LED on pin GP15 as a PWM object
led = PWM(Pin(15))

# Set the frequency of the PWM signal
led.freq(1000)  # 1000 Hz is a common frequency for LEDs

# Initialize an empty list to store measurements
led_intensities = []

# Function to map the ADC value from one range to another
def map_value(value, in_min, in_max, out_min, out_max):
    # Ensure value does not exceed bounds
    value = max(min(value, in_max), in_min)
    # Map the value
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Function to add a new measurement and calculate the average
def add_measurement(new_measurement):
    # Add the new measurement to the list
    led_intensities.append(new_measurement)

    # If the list has more than 10 measurements, remove the oldest one
    if len(led_intensities) > 10:
        led_intensities.pop(0)

    # Calculate the average of the measurements
    average_intensity = sum(led_intensities) / len(led_intensities)

    # Print the average value
    print("Average LED_intensity:", average_intensity)

    return average_intensity

# Function to read ADC value and set LED brightness
def adjust_led_brightness():
    raw_value = adc.read_u16()  # Read a value between 0-65535
    mapped_value = map_value(raw_value, 61600, 65535, 0, 255)
    print("raw_pot_measurement:", raw_value)
    #print("Mapped LED_intensity:", mapped_value)

    # Add the mapped value to the list and get the average
    average_intensity = add_measurement(mapped_value)

    # Set the LED brightness based on the average intensity
    led.duty_u16(int(average_intensity) * 257)  # Scale 0-255 to 0-65535 for PWM

# Main loop
while True:
    adjust_led_brightness()
    time.sleep(0.1)  # Adjust the sleep time as needed

