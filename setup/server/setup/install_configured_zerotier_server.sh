#!/bin/bash

echo "Updating and installing zerotier"  
sudo apt update
sudo apt upgrade
sudo apt-get install jq -y
sudo apt-get install python3-tk -y
sudo apt-get install curl -y

curl https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/zerotierone-archive-keyring.gpg >/dev/null

RELEASE=$(lsb_release -cs)

echo "deb [signed-by=/usr/share/keyrings/zerotierone-archive-keyring.gpg] http://download.zerotier.com/debian/$RELEASE $RELEASE main" | sudo tee /etc/apt/sources.list.d/zerotier.list

sudo apt update
sudo apt install -y zerotier-one

# Read Network ID from zerotier_keys.json
NETWORKID=$(jq -r '.network_key' zerotier_keys.json)

# Check if the Network ID is valid

if [ -z "$NETWORKID" ] || [ ${#NETWORKID} -ne 16 ]; then
    echo "Invalid or missing Network ID in zerotier_keys.json"
    exit 1
fi


# Join the ZeroTier network
sudo zerotier-cli join $NETWORKID

# Get the ZeroTier Node ID
NODE_ID=$(sudo zerotier-cli info | awk '{print $3}' | grep -oE '[0-9a-f]{10}')

echo "ZeroTier Node ID: $NODE_ID"





# Extract API key and Network ID
API_KEY=$(jq -r '.api_key' zerotier_keys.json)
NETWORK_ID=$(jq -r '.network_key' zerotier_keys.json)

# API Endpoint
API_ENDPOINT="https://my.zerotier.com/api/v1/network/${NETWORK_ID}/member/${NODE_ID}"


UUID=$(uuidgen)
NODE_NAME="Node_${UUID}"

curl -X POST -H "Authorization: Bearer ${API_KEY}" -H "Content-Type: application/json" -d '{
    "config": {
	"ipAssignments": ["172.17.17.17"],
        "authorized": true
    },
    
    "name": "Broker '"$NODE_NAME"'",
    "description": "Set IP 172.17.17.17"
}' "$API_ENDPOINT"
sleep 1
clear
echo "change the managed route to 172.16.0.0/12"
echo " and the auto-assign pool to 172.16.0.0	172.31.255.255"

