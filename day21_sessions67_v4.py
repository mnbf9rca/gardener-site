#!/usr/bin/env python3
"""
Day 21 Sessions 6-7 Automation v4
Handles remaining light sessions for Dec 13-14, 2025

Session 6: 11:32-13:32 UTC (120 min)
Session 7: 14:02-15:32 UTC (90 min) - FINAL SESSION

Total: 210 minutes
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://localhost:3000"

def turn_on_light(minutes):
    """Activate grow light for specified duration."""
    try:
        response = requests.post(
            f"{BASE_URL}/light/on",
            json={"minutes": minutes},
            timeout=30
        )
        response.raise_for_status()
        print(f"✓ Light ON for {minutes} minutes at {datetime.now(timezone.utc).isoformat()}")
        return True
    except Exception as e:
        print(f"✗ Error turning on light: {e}")
        return False

def wait_until(target_time_str):
    """Wait until target UTC time."""
    target = datetime.fromisoformat(target_time_str.replace('Z', '+00:00'))
    while True:
        now = datetime.now(timezone.utc)
        if now >= target:
            break
        sleep_time = min((target - now).total_seconds(), 60)
        if sleep_time > 0:
            time.sleep(sleep_time)

print(f"Day 21 Sessions 6-7 Automation v4 started at {datetime.now(timezone.utc).isoformat()}")

# Session 6: 11:32 UTC, 120 minutes
print("Waiting for Session 6 (11:32 UTC)...")
wait_until("2025-12-14T11:32:00Z")
turn_on_light(120)

# Session 7: 14:02 UTC, 90 minutes
print("Waiting for Session 7 (14:02 UTC)...")
wait_until("2025-12-14T14:02:00Z")
turn_on_light(90)

print(f"Day 21 complete! All sessions automated at {datetime.now(timezone.utc).isoformat()}")
