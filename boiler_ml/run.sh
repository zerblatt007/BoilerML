#!/bin/bash
echo "Starting BoilerML add-on..."

# Read Home Assistant token from options
TOKEN=$(jq --raw-output '.hass_token' /data/options.json)
HA_URL=$(jq --raw-output '.ha_url' /data/options.json)

# Export HA_URL so it is available in Python
export HA_URL

# Run your script
python3 /app/boiler_ml.py "$TOKEN"

