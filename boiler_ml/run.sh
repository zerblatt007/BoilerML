#!/bin/bash
echo "Starting BoilerML add-on..."

# Read Home Assistant token from options
TOKEN=$(jq --raw-output '.hass_token' /data/options.json)

# Run your script
python3 /app/boiler_ml.py "$TOKEN"

