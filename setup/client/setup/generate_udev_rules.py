# sudo python3 generate_udev_rules.py


import os
import subprocess

def list_ttyACM_devices():
    return [dev for dev in os.listdir('/dev') if dev.startswith('ttyACM')]

def get_device_attributes(device):
    output = subprocess.check_output(f'udevadm info --query=property --name=/dev/{device}', shell=True)
    properties = output.decode().split('\n')
    attributes = {prop.split('=')[0]: prop.split('=')[1] for prop in properties if '=' in prop}
    return attributes

def write_udev_rule(device, attributes, sensor_name):
    id_vendor = attributes.get('ID_VENDOR_ID')
    id_product = attributes.get('ID_MODEL_ID')
    id_serial = attributes.get('ID_SERIAL_SHORT')

    rule = f'SUBSYSTEM=="tty", ATTRS{{idVendor}}=="{id_vendor}", ATTRS{{idProduct}}=="{id_product}", ATTRS{{serial}}=="{id_serial}", SYMLINK+="{sensor_name}"\n'
    with open('/etc/udev/rules.d/99-sensor.rules', 'a') as file:
        file.write(rule)
    print(f"Udev rule written for {device} as {sensor_name}")

def reload_udev_rules():
    subprocess.run(['pkexec', 'udevadm', 'control', '--reload-rules'], check=True)
    subprocess.run(['pkexec', 'udevadm', 'trigger'], check=True)
    print("Udev rules reloaded and applied.")

def main():
    initial_devices = set(list_ttyACM_devices())
    print("Initial devices detected:", initial_devices)

    input("\nPlease plug in your sensors and press Enter when finished...\n")

    current_devices = set(list_ttyACM_devices())
    new_devices = current_devices - initial_devices

    for device in new_devices:
        attributes = get_device_attributes(device)
        print(f"New device detected: {device}")
        sensor_name = input(f"Enter a name for {device}: ").strip()
        write_udev_rule(device, attributes, sensor_name)

    reload_udev_rules()
    print("Sensor addition complete.")

if __name__ == "__main__":
    main()
