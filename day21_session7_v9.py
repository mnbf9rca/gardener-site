#!/usr/bin/env python3
"""
Day 21 Session 7 (FINAL SESSION) - Automated Start
Starts at: 14:02 UTC
Duration: 90 minutes
Expected end: 15:32 UTC (auto-shutoff)
Completes Day 21: 840 minutes total
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
    print(f"[{datetime.now(timezone.utc).isoformat()}] Day 21 Session 7 Automation Started")
    print(f"[{datetime.now(timezone.utc).isoformat()}] FINAL SESSION of Day 21")
    print(f"[{datetime.now(timezone.utc).isoformat()}] Target start: 14:02:00 UTC")

    # Wait until 14:02:00 UTC
    target_time = datetime(2025, 12, 14, 14, 2, 0, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    if now < target_time:
        wait_seconds = (target_time - now).total_seconds()
        print(f"[{now.isoformat()}] Waiting {wait_seconds:.1f} seconds until {target_time.isoformat()}")
        time.sleep(wait_seconds)

    # Activate Session 7 (90 minutes)
    print(f"[{datetime.now(timezone.utc).isoformat()}] Activating Session 7 (90 minutes)...")
    if turn_on_light(90):
        print(f"[{datetime.now(timezone.utc).isoformat()}] Session 7 activated successfully")
        print(f"[{datetime.now(timezone.utc).isoformat()}] Expected end: 15:32 UTC (auto-shutoff)")
        print(f"[{datetime.now(timezone.utc).isoformat()}] DAY 21 WILL BE COMPLETE: 840 minutes total")
        print(f"[{datetime.now(timezone.utc).isoformat()}] AGENT: Take verification photo immediately!")
    else:
        print(f"[{datetime.now(timezone.utc).isoformat()}] FAILED to activate Session 7")

    print(f"[{datetime.now(timezone.utc).isoformat()}] Automation complete - exiting")

if __name__ == "__main__":
    main()
