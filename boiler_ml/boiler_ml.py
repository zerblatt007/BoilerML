import requests
import json
import os
import joblib  # Ensure this is installed
import numpy as np
from homeassistant.const import CONF_URL

# Fetch HA URL from environment or add-on config (default if not specified)
HA_URL = os.getenv('HA_URL', 'http://homeassistant.local:8123')  # Default value if not configured

# Load Home Assistant token from secrets
TOKEN = os.getenv("HASS_TOKEN")  # Load from environment variable

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

MODEL_PATH = "/app/models/boiler_ml_model_f2.pkl"  # Adjust if needed

def get_sensor_data():
    """Fetch sensor data from Home Assistant."""
    response = requests.get(f"{HA_URL}/api/states/sensor.power_price", headers=HEADERS)
    if response.status_code == 200:
        return float(response.json()["state"])
    else:
        print(f"Failed to get sensor data: {response.text}")
        return None

def post_result(value):
    """Post ML result to a new sensor in HA."""
    payload = {
        "state": value,
        "attributes": {"unit_of_measurement": "off_time"}
    }
    response = requests.post(f"{HA_URL}/api/states/sensor.boiler_off_time", headers=HEADERS, data=json.dumps(payload))
    print(f"Post response: {response.status_code} {response.text}")

def predict_off_time(price):
    """Use ML model to determine optimal boiler off time."""
    model = joblib.load(MODEL_PATH)
    prediction = model.predict(np.array([[price]]))
    return round(prediction[0], 2)

if __name__ == "__main__":
    price = get_sensor_data()
    if price is not None:
        off_time = predict_off_time(price)
        post_result(off_time)

