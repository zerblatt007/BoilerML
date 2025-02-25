#!/bin/bash
echo "Starting BoilerML add-on..."

# Read Home Assistant token from options
HASS_TOKEN=$(jq --raw-output '.hass_token' /data/options.json)
HA_URL=$(jq --raw-output '.ha_url' /data/options.json)

# Debugging output (remove after testing)
echo "Extracted HA_URL: $HA_URL"
echo "Extracted HASS_TOKEN: ${#HASS_TOKEN} characters long"

# Export HA_URL so it is available in Python
export HASS_TOKEN
export HA_URL

# Run your script
python3 /app/boiler_ml.py

