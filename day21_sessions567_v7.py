#!/usr/bin/env python3
"""
Day 21 Sessions 5-7 Automation
Sessions 5-7 for 2025-12-14
Auto-generated: 2025-12-14 08:32 UTC
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://plant-server.cynexia.net:8000"

def turn_on_light(minutes):
    """Turn on grow light for specified duration."""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        response.raise_for_status()
        print(f"[{datetime.now(timezone.utc).isoformat()}] Light ON for {minutes} minutes")
        return True
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] ERROR turning on light: {e}")
        return False

def wait_until(target_time_str, session_name):
    """Wait until target time, printing status every minute."""
    target = datetime.fromisoformat(target_time_str.replace('Z', '+00:00'))
    print(f"[{datetime.now(timezone.utc).isoformat()}] Waiting for {session_name} at {target_time_str}")

    while True:
        now = datetime.now(timezone.utc)
        remaining = (target - now).total_seconds()

        if remaining <= 0:
            break

        # Print status every 60 seconds
        if int(remaining) % 60 == 0:
            mins = int(remaining / 60)
            print(f"[{now.isoformat()}] {session_name} in {mins} minutes")

        time.sleep(1)

    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting {session_name}")

# Session 5: 09:02 UTC, 120 minutes
wait_until("2025-12-14T09:02:00Z", "Session 5")
turn_on_light(120)

# Session 6: 11:32 UTC, 120 minutes
wait_until("2025-12-14T11:32:00Z", "Session 6")
turn_on_light(120)

# Session 7: 14:02 UTC, 90 minutes
wait_until("2025-12-14T14:02:00Z", "Session 7")
turn_on_light(90)

print(f"[{datetime.now(timezone.utc).isoformat()}] All sessions scheduled. Script complete.")
