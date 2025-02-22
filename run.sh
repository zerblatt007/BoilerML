#!/bin/bash
export HASS_TOKEN=$(bashio::config 'hass_token')
python3 /app/boiler_ml.py

