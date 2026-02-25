#!/usr/bin/env python3
"""
Day 21 Sessions 6-7 Automation - Version 2
Handles remaining sessions for Dec 13-14, 2025
Auto-activated after automation v1 terminated
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://plant-server.cynexia.net:8000"

def turn_on_light(minutes):
    """Turn on grow light for specified duration"""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        response.raise_for_status()
        print(f"[{datetime.now(timezone.utc).isoformat()}] Light turned ON for {minutes} minutes")
        return True
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] ERROR turning on light: {e}")
        return False

def wait_until(target_time_utc):
    """Wait until target time (format: HH:MM)"""
    while True:
        now = datetime.now(timezone.utc)
        target_hour, target_min = map(int, target_time_utc.split(':'))
        target = now.replace(hour=target_hour, minute=target_min, second=0, microsecond=0)

        # If target time has passed today, it must be tomorrow
        if target <= now:
            break

        wait_seconds = (target - now).total_seconds()
        if wait_seconds <= 0:
            break

        print(f"[{now.isoformat()}] Waiting {wait_seconds:.0f}s until {target_time_utc} UTC...")
        time.sleep(min(wait_seconds, 60))  # Check every minute

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Day 21 Sessions 6-7 Automation v2 Started")
    print("Session 6: 11:32-13:32 UTC (120 min)")
    print("Session 7: 14:02-15:32 UTC (90 min)")

    # Session 6: 11:32 UTC, 120 minutes
    wait_until("11:32")
    turn_on_light(120)
    print(f"[{datetime.now(timezone.utc).isoformat()}] Session 6 activated")

    # Session 7: 14:02 UTC, 90 minutes
    wait_until("14:02")
    turn_on_light(90)
    print(f"[{datetime.now(timezone.utc).isoformat()}] Session 7 activated (FINAL SESSION)")

    print(f"[{datetime.now(timezone.utc).isoformat()}] Day 21 automation complete - all sessions scheduled")

if __name__ == "__main__":
    main()
