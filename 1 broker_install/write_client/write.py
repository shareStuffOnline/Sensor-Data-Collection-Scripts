import serial
import time
import paho.mqtt.client as mqtt

# MQTT settings
MQTT_BROKER = "172.17.17.17"
MQTT_TOPIC = "control/LED"

# Serial settings
port = '/dev/ttyACM2'
baudrate = 115200   

# Callback function for when a message is received
def on_message(client, userdata, message):
    value = message.payload.decode()
    ser.write((value + '\n').encode())
    print(value)

# MQTT client setup
client = mqtt.Client()
client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC)
client.on_message = on_message

# Open serial connection
ser = serial.Serial(port, baudrate, timeout=1)

# Start the MQTT client
client.loop_start()

try:
    while True:
        time.sleep(1)  # Main loop does nothing, MQTT client handles messages
except KeyboardInterrupt:
    client.loop_stop()
    ser.close()
