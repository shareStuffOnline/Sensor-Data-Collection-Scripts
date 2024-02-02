import paho.mqtt.client as mqtt

# Callback when connected to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")

# Callback when a message is received
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("local.werx.broker", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks
client.loop_forever()
