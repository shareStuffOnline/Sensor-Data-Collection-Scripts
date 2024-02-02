# Sensor-Data-Collection-Scripts
### under construction
This repository contains scripts for collecting sensor data from microcontrollers, reading the data from a serial port, and generating udev rules for the sensors.

## Usage

1. Run `main.py` on your microcontroller supporting micropython to read sensor data and print it out at regular intervals.


2. Run `read.py` on a computer or embedded device with network capabilities to read the sensor data from a serial port, format it, and publish it to an MQTT broker.

python3 read.py --port ttyACM0 --location "/topic/location"

3. Run `generate_udev_rules.py` to generate udev rules for your sensors. This will create symbolic links to your devices that don't change even if the devices are plugged into different USB ports.

sudo python3 generate_udev_rules.py


The MQTT (Message Queuing Telemetry Transport) protocol is a lightweight, publish-subscribe network protocol that transports messages between devices. It is designed for constrained devices and low-bandwidth, high-latency, or unreliable networks, making it ideal for Internet of Things (IoT) applications.

Here are some reasons why it's worth trying the MQTT message broker and interfacing with old devices that otherwise don't support IP:

1. **Efficient and Lightweight**: MQTT is designed to minimize network bandwidth and device resource requirements. It is based on an efficient binary protocol that has a small code footprint and minimizes network traffic. This makes it suitable for "machine-to-machine" (M2M) or IoT contexts where a small code footprint is required and/or network bandwidth is at a premium.

2. **Quality of Service Levels**: MQTT supports three Quality of Service (QoS) levels, allowing you to choose the right level of message delivery assurance for each of your applications.

3. **Last Will and Testament**: If an MQTT client unexpectedly disconnects, the broker can automatically notify other clients using the Last Will and Testament feature.

4. **Secure**: MQTT supports secure communication using Transport Layer Security (TLS) to encrypt the communication between clients and the broker.

5. **Scalable**: MQTT can support a large number of clients, making it suitable for IoT applications where many devices need to be controlled and monitored.

6. **Interoperability**: MQTT is an open standard that is supported by a large number of hardware and software vendors. This ensures that your IoT solution is not locked into a single vendor or platform.

When it comes to interfacing with old devices that don't support IP, using a microcontroller as an intermediary can be a practical solution. The microcontroller can read data from the device using the device's native communication protocol (e.g., RS-232, TTL, etc.), and then transmit the data over IP using MQTT. This approach can breathe new life into old devices, allowing them to be integrated into modern IoT systems.

In addition, using a standardized data representation like the NIST Open Control Systems (OCS) standard can further enhance interoperability. By converting the device data into a standard format, it can be easily understood and processed by a wide range of systems and applications.

In conclusion, using MQTT and a standardized data representation can provide a flexible and extensible solution for integrating old devices into modern IoT systems. It allows you to leverage the capabilities of these devices while benefiting from the advantages of IP-based communication and standardized data formats.
