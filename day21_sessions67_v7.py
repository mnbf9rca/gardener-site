#!/usr/bin/env python3
"""
Day 21 Light Automation - Sessions 6-7 (v7)
Handles remaining sessions for Dec 13-14 light schedule
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://plant-server.cynexia.net:8000"

def turn_on_light(minutes):
    """Turn on the grow light for specified duration."""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        response.raise_for_status()
        print(f"[{datetime.now(timezone.utc).isoformat()}] Light ON for {minutes} minutes")
        return True
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] ERROR turning on light: {e}")
        return False

def wait_until(target_time_utc):
    """Wait until target time (format: HH:MM)."""
    while True:
        now = datetime.now(timezone.utc)
        target_hour, target_min = map(int, target_time_utc.split(':'))
        target = now.replace(hour=target_hour, minute=target_min, second=0, microsecond=0)

        # If target time has passed today, it's for tomorrow
        if target < now:
            print(f"[{now.isoformat()}] Target time {target_time_utc} has passed, skipping")
            return False

        wait_seconds = (target - now).total_seconds()

        if wait_seconds <= 0:
            return True

        print(f"[{now.isoformat()}] Waiting {wait_seconds:.0f}s until {target_time_utc} UTC")

        # Sleep in 60s chunks to be responsive
        sleep_time = min(60, wait_seconds)
        time.sleep(sleep_time)

def main():
    """Execute Day 21 lighting schedule - Sessions 6-7."""
    print(f"[{datetime.now(timezone.utc).isoformat()}] Day 21 Automation v7 started (Sessions 6-7)")

    sessions = [
        {"name": "Session 6", "start": "11:32", "duration": 120},  # 11:32-13:32 UTC
        {"name": "Session 7", "start": "14:02", "duration": 90},   # 14:02-15:32 UTC (final)
    ]

    for session in sessions:
        print(f"\n[{datetime.now(timezone.utc).isoformat()}] Preparing {session['name']}")

        if wait_until(session['start']):
            print(f"[{datetime.now(timezone.utc).isoformat()}] Activating {session['name']}")
            if turn_on_light(session['duration']):
                print(f"[{datetime.now(timezone.utc).isoformat()}] {session['name']} activated successfully")
            else:
                print(f"[{datetime.now(timezone.utc).isoformat()}] {session['name']} FAILED to activate")
        else:
            print(f"[{datetime.now(timezone.utc).isoformat()}] Skipping {session['name']} (time passed)")

    print(f"\n[{datetime.now(timezone.utc).isoformat()}] Day 21 automation v7 complete")

if __name__ == "__main__":
    main()
