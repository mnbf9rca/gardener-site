#!/usr/bin/env python3
"""
Automation for Day 21 Sessions 5-7
Session 5: 09:02-11:02 UTC (120 min)
Session 6: 11:32-13:32 UTC (120 min)
Session 7: 14:02-15:32 UTC (90 min)
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://localhost:3000"

def turn_on_light(minutes):
    """Turn on light for specified minutes"""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=30)
        print(f"[{datetime.now(timezone.utc).isoformat()}] Light ON for {minutes} min: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] Error turning on light: {e}")
        return False

def wait_until(target_time_str):
    """Wait until specified UTC time (HH:MM format)"""
    while True:
        now = datetime.now(timezone.utc)
        target_hour, target_min = map(int, target_time_str.split(':'))
        target = now.replace(hour=target_hour, minute=target_min, second=0, microsecond=0)

        # If target time has passed today, schedule for tomorrow
        if target <= now:
            print(f"[{now.isoformat()}] Target {target_time_str} already passed, skipping")
            return False

        wait_seconds = (target - now).total_seconds()
        print(f"[{now.isoformat()}] Waiting {wait_seconds:.0f}s until {target_time_str} UTC")

        if wait_seconds <= 0:
            return True

        time.sleep(min(wait_seconds, 60))  # Check every minute

        # Recheck if we've reached target
        if datetime.now(timezone.utc) >= target:
            return True

print(f"[{datetime.now(timezone.utc).isoformat()}] Day 21 Sessions 5-7 automation starting")

# Session 5: 09:02-11:02 UTC (120 min)
if wait_until("09:02"):
    turn_on_light(120)
    print(f"[{datetime.now(timezone.utc).isoformat()}] Session 5 started, will auto-shutoff at 11:02")
    time.sleep(30 * 60)  # Wait 30 min before next session

# Session 6: 11:32-13:32 UTC (120 min)
if wait_until("11:32"):
    turn_on_light(120)
    print(f"[{datetime.now(timezone.utc).isoformat()}] Session 6 started, will auto-shutoff at 13:32")
    time.sleep(30 * 60)  # Wait 30 min before next session

# Session 7: 14:02-15:32 UTC (90 min)
if wait_until("14:02"):
    turn_on_light(90)
    print(f"[{datetime.now(timezone.utc).isoformat()}] Session 7 started, will auto-shutoff at 15:32")
    print(f"[{datetime.now(timezone.utc).isoformat()}] Day 21 complete! All 7 sessions done.")

print(f"[{datetime.now(timezone.utc).isoformat()}] Automation script complete")
