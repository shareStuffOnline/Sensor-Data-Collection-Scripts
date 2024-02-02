import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import re

def list_ttyACM_devices():
    return [dev for dev in os.listdir('/dev') if dev.startswith('ttyACM')]

def get_device_attributes(device):
    output = subprocess.check_output(f'udevadm info --query=property --name=/dev/{device}', shell=True)
    properties = output.decode().split('\n')
    attributes = {prop.split('=')[0]: prop.split('=')[1] for prop in properties if '=' in prop}
    return attributes

def read_existing_rules():
    rules = {}
    try:
        with open('/etc/udev/rules.d/99-sensor.rules', 'r') as file:
            for line in file:
                match = re.search(r'ATTRS{serial}=="([^"]+)",\s+SYMLINK\+="([^"]+)"', line)
                if match:
                    rules[match.group(1)] = match.group(2)
    except IOError:
        pass  # File doesn't exist or cannot be read
    return rules
def write_udev_rules(device_entries, window):
    try:
        with open('/etc/udev/rules.d/99-sensor.rules', 'w') as file:
            for device, (attributes, entry) in device_entries.items():
                sensor_name = entry.get().strip()
                if sensor_name:
                    id_vendor = attributes.get('ID_VENDOR_ID')
                    id_product = attributes.get('ID_MODEL_ID')
                    id_serial = attributes.get('ID_SERIAL_SHORT')
                    rule = f'SUBSYSTEM=="tty", ATTRS{{idVendor}}=="{id_vendor}", ATTRS{{idProduct}}=="{id_product}", ATTRS{{serial}}=="{id_serial}", SYMLINK+="{sensor_name}"\n'
                    file.write(rule)
        messagebox.showinfo("Info", "Udev rules written and applied.")
        window.destroy()  # Close the Tkinter window and end the program
    except IOError as e:
        messagebox.showerror("Error", f"Failed to write udev rules: {e}")

def reload_udev_rules():
    try:
        subprocess.run(['pkexec', 'udevadm', 'control', '--reload-rules'], check=True)
        subprocess.run(['pkexec', 'udevadm', 'trigger'], check=True)
        messagebox.showinfo("Info", "Udev rules reloaded and applied.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to reload udev rules: {e}")

def update_device_list(window, device_entries, existing_rules):
    for device in list_ttyACM_devices():
        if device not in device_entries:
            attributes = get_device_attributes(device)
            row = tk.Frame(window)
            label = tk.Label(row, text=f"{device}", width=20)
            entry = tk.Entry(row)
            serial = attributes.get('ID_SERIAL_SHORT')
            if serial and serial in existing_rules:
                entry.insert(0, existing_rules[serial])
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            device_entries[device] = (attributes, entry)

def main():
    window = tk.Tk()
    window.title("Sensor Manager")

    device_entries = {}
    existing_rules = read_existing_rules()

    update_device_list(window, device_entries, existing_rules)

    update_button = tk.Button(window, text="Update Device List", command=lambda: update_device_list(window, device_entries, existing_rules))
    update_button.pack(side=tk.TOP, pady=5)

    save_button = tk.Button(window, text="Save Udev Rules", command=lambda: [write_udev_rules(device_entries, window), reload_udev_rules()])
    save_button.pack(side=tk.TOP, pady=5)

    window.mainloop()

if __name__ == "__main__":
    main()
