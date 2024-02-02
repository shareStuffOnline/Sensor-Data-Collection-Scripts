#!/bin/bash
echo "Configuring serial access and installing Thonny"



# Updating package list
sudo apt update

# Purging existing Thonny installation
echo "Purging existing Thonny installation"
sudo apt purge -y thonny

# Installing the latest Thonny
echo "Installing the latest version of Thonny"
sudo apt install -y thonny

echo "Script execution completed"

# Adding current user to the dialout group for serial control
echo "Adding current user to the dialout group"
sudo usermod -a -G dialout $USER

# Informing the user about the need to re-login
echo "Please log out and then log in again for group changes to take effect"

# Informing the user about the logout
echo "You will be rebooted out in 5 seconds to apply group changes."
echo "Please save your work before the logout occurs."

# Adding a 5-second pause
sleep 5

# Forcing a logout
sudo reboot
