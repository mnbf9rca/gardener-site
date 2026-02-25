#!/usr/bin/env python3
"""
Day 21 automation - Sessions 6-7
Session 6: 11:32-13:32 UTC (120 min)
Session 7: 14:02-15:32 UTC (90 min)
"""
import requests
from datetime import datetime, timezone
import time

BASE_URL = "http://localhost:3000"

def turn_on_light(minutes):
    """Turn on grow light for specified duration."""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error turning on light: {e}")
        return False

def wait_until(target_time):
    """Wait until the target UTC time."""
    while True:
        now = datetime.now(timezone.utc)
        if now >= target_time:
            break
        sleep_seconds = (target_time - now).total_seconds()
        if sleep_seconds > 60:
            time.sleep(30)  # Check every 30s if more than 1 min away
        else:
            time.sleep(max(1, sleep_seconds))  # Check every second when close

def main():
    sessions = [
        {"name": "Session 6", "start": "2025-12-14T11:32:00+00:00", "duration": 120},
        {"name": "Session 7", "start": "2025-12-14T14:02:00+00:00", "duration": 90},
    ]

    for session in sessions:
        start_time = datetime.fromisoformat(session["start"])
        duration = session["duration"]

        print(f"Waiting for {session['name']} at {start_time} UTC...")
        wait_until(start_time)

        print(f"Activating {session['name']} for {duration} minutes...")
        if turn_on_light(duration):
            print(f"{session['name']} activated successfully at {datetime.now(timezone.utc)}")
        else:
            print(f"FAILED to activate {session['name']} at {datetime.now(timezone.utc)}")

    print("All Day 21 sessions (6-7) completed!")

if __name__ == "__main__":
    main()
