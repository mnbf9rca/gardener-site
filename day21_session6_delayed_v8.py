#!/usr/bin/env python3
"""
Day 21 Session 6 - Delayed Start Due to Cooldown
Activates Session 6 at 11:43 UTC (10 min late - earliest possible after 30-min cooldown)
Session 5 ended: 11:12:51 UTC
Cooldown expires: 11:42:51 UTC
Target start: 11:43:00 UTC (safety margin)
Duration: 120 minutes -> ends 13:43 UTC
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://localhost:3000"

def turn_on_light(minutes):
    """Activate grow light"""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        response.raise_for_status()
        print(f"[{datetime.now(timezone.utc).isoformat()}] Light activated for {minutes} minutes")
        return True
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] ERROR activating light: {e}")
        return False

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Day 21 Session 6 Delayed Automation Started")
    print(f"[{datetime.now(timezone.utc).isoformat()}] Automation failure #23 - v7 script terminated")
    print(f"[{datetime.now(timezone.utc).isoformat()}] Session 6 scheduled: 11:32 UTC")
    print(f"[{datetime.now(timezone.utc).isoformat()}] Cooldown expires: 11:42:51 UTC")
    print(f"[{datetime.now(timezone.utc).isoformat()}] Target start: 11:43:00 UTC (10 min late)")

    # Wait until 11:43:00 UTC
    target_time = datetime(2025, 12, 14, 11, 43, 0, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    if now < target_time:
        wait_seconds = (target_time - now).total_seconds()
        print(f"[{now.isoformat()}] Waiting {wait_seconds:.1f} seconds until {target_time.isoformat()}")
        time.sleep(wait_seconds)

    # Activate Session 6 (120 minutes)
    print(f"[{datetime.now(timezone.utc).isoformat()}] Activating Session 6 (120 minutes)...")
    if turn_on_light(120):
        print(f"[{datetime.now(timezone.utc).isoformat()}] Session 6 activated successfully")
        print(f"[{datetime.now(timezone.utc).isoformat()}] Expected end: 13:43 UTC (auto-shutoff)")
        print(f"[{datetime.now(timezone.utc).isoformat()}] AGENT: Take verification photo immediately!")
    else:
        print(f"[{datetime.now(timezone.utc).isoformat()}] FAILED to activate Session 6")

    print(f"[{datetime.now(timezone.utc).isoformat()}] Automation complete - exiting")

if __name__ == "__main__":
    main()
