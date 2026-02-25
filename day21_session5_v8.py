#!/usr/bin/env python3
"""
Day 21 Session 5 automation - v8
Handles only Session 5 (09:02-11:02 UTC, 120 min)
Simplifies automation to single session at a time
Created: 2025-12-14 08:52 UTC
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://localhost:3000"

def turn_on_light(minutes):
    """Activate grow light for specified duration"""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        response.raise_for_status()
        print(f"[{datetime.now(timezone.utc).isoformat()}] Light ON for {minutes} minutes")
        return True
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] ERROR turning light on: {e}")
        return False

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Day 21 Session 5 automation started")
    print(f"[{datetime.now(timezone.utc).isoformat()}] Waiting for Session 5 start time: 09:02 UTC")

    # Session 5: 09:02-11:02 UTC (120 min)
    session5_start = datetime(2025, 12, 14, 9, 2, 0, tzinfo=timezone.utc)

    # Wait for Session 5
    now = datetime.now(timezone.utc)
    if now < session5_start:
        wait_seconds = (session5_start - now).total_seconds()
        print(f"[{datetime.now(timezone.utc).isoformat()}] Waiting {wait_seconds:.1f} seconds until Session 5...")
        time.sleep(wait_seconds)

    # Start Session 5
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting Session 5 (120 min)")
    if turn_on_light(120):
        print(f"[{datetime.now(timezone.utc).isoformat()}] Session 5 started successfully")
        print(f"[{datetime.now(timezone.utc).isoformat()}] Session 5 will auto-shutoff at 11:02 UTC")
    else:
        print(f"[{datetime.now(timezone.utc).isoformat()}] FAILED to start Session 5")

    print(f"[{datetime.now(timezone.utc).isoformat()}] Automation complete")

if __name__ == "__main__":
    main()
