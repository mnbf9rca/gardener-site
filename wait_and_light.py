#!/usr/bin/env python3
import time
import requests

# Wait until light is ready
while True:
    try:
        response = requests.get('http://localhost:8080/light/status')
        data = response.json()
        if data.get('can_activate', False):
            print("Light ready to activate!")
            break
        else:
            mins = data.get('minutes_until_available', 0)
            print(f"Waiting... {mins} minutes until available")
            time.sleep(60)  # Check every minute
    except Exception as e:
        print(f"Error checking status: {e}")
        time.sleep(30)

print("Starting Session 3...")
# Activate the light for 120 minutes
try:
    response = requests.post('http://localhost:8080/light/on', json={'minutes': 120})
    print(f"Light activation response: {response.json()}")
except Exception as e:
    print(f"Error activating light: {e}")
