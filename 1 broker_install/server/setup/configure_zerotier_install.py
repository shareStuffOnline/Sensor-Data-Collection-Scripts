import webbrowser
import tkinter as tk
import json
import os
import re

# Function to validate a 16-digit hexadecimal code
def is_valid_hexadecimal(code):
    return bool(re.match(r'^[0-9a-fA-F]{16}$', code))

# Function to open a URL
def open_url(url):
    webbrowser.open_new(url)

# Function to create a hyperlink label
def create_hyperlink(parent, text, url):
    link = tk.Label(parent, text=text, fg="blue", cursor="hand2")
    link.bind("<Button-1>", lambda e: open_url(url))
    return link

# Function to add placeholder text to an entry widget
def add_placeholder_to(entry, placeholder, default_text=""):
    def on_focus_in(event, placeholder=placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event, placeholder=placeholder):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    if default_text:
        entry.insert(0, default_text)
        entry.config(fg='black')
    else:
        entry.insert(0, placeholder)
        entry.config(fg='grey')
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Load keys from file if it exists
def load_keys_from_file():
    if os.path.exists("zerotier_keys.json"):
        try:
            with open("zerotier_keys.json", "r") as file:
                keys = json.load(file)
                return keys.get("api_key", ""), keys.get("network_key", "")
        except json.JSONDecodeError:
            return "", ""
    return "", ""

# Create a Tkinter interface with two input fields
def ask_for_keys(api_key_default, network_key_default):
    def on_submit():
        api_key = api_key_entry.get()
        network_key = network_key_entry.get()

        # Validate the Network ID
        if not is_valid_hexadecimal(network_key):
            tk.messagebox.showerror("Invalid Input", "Network ID must be a 16-digit hexadecimal code.")
            return

        # Validate the API Key (check if it's not empty)
        if not api_key:
            tk.messagebox.showerror("Invalid Input", "API Key cannot be empty.")
            return

        # Write the keys to a JSON file
        with open("zerotier_keys.json", "w") as file:
            json.dump({"api_key": api_key, "network_key": network_key}, file, indent=4)
        root.destroy()

    root = tk.Tk()
    root.title("Enter ZeroTier Keys")

    tk.Label(root, text="ZeroTier API Key:").pack()
    api_key_entry = tk.Entry(root, width=50)
    add_placeholder_to(api_key_entry, "Enter API Key here", api_key_default)
    api_key_entry.pack()

    # Hyperlink to API Key page
    api_key_link = create_hyperlink(root, "Get your API Key", "https://my.zerotier.com/account")
    api_key_link.pack()

    tk.Label(root, text="ZeroTier Network ID:").pack()
    network_key_entry = tk.Entry(root, width=50)
    add_placeholder_to(network_key_entry, "Enter Network ID here", network_key_default)
    network_key_entry.pack()

    # Hyperlink to Network ID page
    network_id_link = create_hyperlink(root, "Find your Network ID", "https://my.zerotier.com/network/")
    network_id_link.pack()

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack()

    root.mainloop()

# Load existing keys or use empty strings as defaults
api_key_default, network_key_default = load_keys_from_file()

# Call the function with the loaded or default keys
ask_for_keys(api_key_default, network_key_default)
