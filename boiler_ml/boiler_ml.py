import requests
import json
import os
import pytz
from datetime import datetime, timedelta
import joblib  # Ensure this is installed
import numpy as np

# Fetch HA URL from environment or add-on config (default if not specified)
HA_URL = os.getenv('HA_URL', 'https://hassio.local:8123/')  # Default value if not configured
HASS_TOKEN = os.getenv("HASS_TOKEN")  # Should be set by run.sh

print(f"Using HA_URL: {HA_URL}")  # Debugging output
print(f"HASS_TOKEN: {HASS_TOKEN[:6]}... (truncated)")  # Debugging output (DO NOT print full token!)

HEADERS = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "Content-Type": "application/json"
}

MODEL_PATH = "/app/models/boiler_ml_model_f4.pkl"  # Adjust if needed

# Fetch sensor data from Home Assistant
ENTITY_INPUT_ID = "sensor.custom_nordpool_today"

# Push sensor data to Home Assistant
ENTITY_OUTPUT_ID = "sensor.boiler_off_time"

def get_sensor_data():
    """Fetch sensor data from Home Assistant and return today's prices."""
    response = requests.get(f"{HA_URL}/api/states/{ENTITY_INPUT_ID}", headers=HEADERS, verify=False)
    
    if response.status_code == 200:
        data = response.json()
        today_prices = data.get("attributes", {}).get("today", None)  # Safely extract "today"
        
        if today_prices is not None:
            return today_prices  # Return the list of today's prices
        else:
            print("Error: 'today' data not found in response.")
            return None
    else:
        print(f"Failed to get sensor data: {response.text}")
        return None

def post_result(result):
    """Post ML result (spikeList and spikeHours) to a new sensor in HA."""
    payload = {
        "state": "updated",  # Just a placeholder state
        "attributes": {
            "spikeList": result["spikeList"],
            "spikeHours": result["spikeHours"],
            "unit_of_measurement": "off_time"
        }
    }
    response = requests.post(f"{HA_URL}/api/states/{ENTITY_OUTPUT_ID}", headers=HEADERS, data=json.dumps(payload), verify=False)
    print(f"Post response: {response.status_code} {response.text}")

def predict_off_time(today_state):
    """Use ML model to determine optimal boiler off time for each hour."""
    model = joblib.load(MODEL_PATH)
    spikeList = [0] * 24  # Initialize list with zeros
    spikeHours = []  # List to store timestamps for each hour

    # Set timezone to Europe/Oslo
    oslo_tz = pytz.timezone('Europe/Oslo')

    # Get today's date at 00:00 in Oslo timezone
    today_midnight = datetime.now(oslo_tz).replace(hour=0, minute=0, second=0, microsecond=0)

    # Predict shutdown hours
    for hour in range(24):
        features = [hour, today_state[hour]]

        # Include past and future prices
        if hour > 0:
            features.append(today_state[hour - 1])  # Previous hour price
        else:
            features.append(today_state[hour])  # Use current hour if no previous hour

        if hour < 23:
            features.append(today_state[hour + 1])  # Next hour price
        else:
            features.append(today_state[hour])  # Use current hour if no next hour

        features = np.array([features])  # Reshape for model input
        prediction = model.predict(features)[0]  # Predict shutdown (1) or not (0)
        spikeList[hour] = today_state[hour] if prediction == 1 else 0

        # Generate timestamp for each hour
        spike_time = today_midnight + timedelta(hours=hour)
        spikeHours.append(spike_time.strftime('%Y-%m-%dT%H:%M:%S%z'))

    return {"spikeList": spikeList, "spikeHours": spikeHours}

if __name__ == "__main__":
    price = get_sensor_data()
    if price is not None:
        off_time = predict_off_time(price)
        post_result(off_time)

