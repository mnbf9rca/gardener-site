#!/usr/bin/env python3
"""
Day 21 Light Automation - Sessions 5, 6, 7
Created: 2025-12-14 07:13 UTC
Handles remaining 3 sessions for Day 21
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://plant-server.cynexia.net:8000"

def log(message):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] {message}", flush=True)

def turn_on_light(minutes):
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        log(f"Light ON for {minutes} min - Status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        log(f"ERROR turning light on: {e}")
        return False

def main():
    log("=== Day 21 Sessions 5-7 Automation Started ===")

    # Session 5: 09:02-11:02 (120 min)
    session5_start = datetime(2025, 12, 14, 9, 2, 0, tzinfo=timezone.utc)
    session5_duration = 120

    # Session 6: 11:32-13:32 (120 min)
    session6_start = datetime(2025, 12, 14, 11, 32, 0, tzinfo=timezone.utc)
    session6_duration = 120

    # Session 7: 14:02-15:32 (90 min)
    session7_start = datetime(2025, 12, 14, 14, 2, 0, tzinfo=timezone.utc)
    session7_duration = 90

    sessions = [
        ("Session 5", session5_start, session5_duration),
        ("Session 6", session6_start, session6_duration),
        ("Session 7", session7_start, session7_duration)
    ]

    for session_name, start_time, duration in sessions:
        now = datetime.now(timezone.utc)

        if now < start_time:
            wait_seconds = (start_time - now).total_seconds()
            log(f"Waiting {wait_seconds:.1f}s for {session_name} at {start_time.strftime('%H:%M:%S UTC')}")
            time.sleep(wait_seconds)

        log(f"=== Starting {session_name} ({duration} min) ===")
        success = turn_on_light(duration)

        if success:
            log(f"{session_name} activated successfully")
        else:
            log(f"ERROR: {session_name} activation failed")

        # Small delay between sessions
        time.sleep(5)

    log("=== Day 21 Sessions 5-7 Complete ===")

if __name__ == "__main__":
    main()
