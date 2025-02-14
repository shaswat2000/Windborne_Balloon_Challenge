# File: backend/app.py

import requests
import json
import sys
import logging
from flask import Flask, jsonify
from flask_cors import CORS  # To allow cross-origin requests from React dev server
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = "7352488c1be55ffced8fa8388d87bf5a"
WINDBORNE_URL = "https://a.windbornesystems.com/treasure"

hours_data = 22

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app)  # Enables cross-origin requests for all routes. 
           # (In production, configure allowed origins more carefully.)

def fetch_balloon_data(hour):
    url = f"{WINDBORNE_URL}/{hour:02d}.json"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return None

def fetch_weather(lat, lon):
    try:
        owm_url = (
            "http://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={API_KEY}"
        )
        r = requests.get(owm_url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[!] Weather fetch error at lat={lat}, lon={lon}: {e}")
        return None

@app.route("/data")
def get_data():
    """Fetch the last 24 hours of balloon data + weather and return as JSON."""
    # data = {'message': 'Hello from Flask!', 'count': 42}
    # return jsonify(data)
    result = []
    balloons = fetch_balloon_data(0)
    np.array(balloons)

    try:
        for hour in range(hours_data):
            balloons = fetch_balloon_data(hour)
            if balloons == None:
                continue

            balloons2 = (np.nan_to_num(balloons, nan = -181)).tolist()

            result.append(balloons2)

        # weather = fetch_weather(lat, lon)
        return jsonify(result)
    except Exception as e:
        print("Error in get_data:", e)
        return jsonify({"error": "Something went wrong"}), 500  #Return JSON even for errors

if __name__ == "__main__":
    print("Flask app starting up...")
    app.run(debug=True, port=5000)
