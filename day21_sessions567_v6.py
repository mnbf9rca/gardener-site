#!/usr/bin/env python3
"""
Day 21 Sessions 5-7 Automation (v6)
Handles remaining 3 sessions for 14-hour light day
Total: 330 minutes across Sessions 5-7
"""

import time
import requests
from datetime import datetime, timezone

BASE_URL = "http://localhost:8000"

def log(msg):
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}", flush=True)

def turn_on_light(minutes):
    """Activate grow light for specified duration"""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        response.raise_for_status()
        log(f"✅ Light ON for {minutes} minutes")
        return True
    except Exception as e:
        log(f"❌ Failed to turn on light: {e}")
        return False

def wait_until(target_time_str):
    """Wait until specified UTC time (HH:MM format)"""
    while True:
        now = datetime.now(timezone.utc)
        target = datetime.strptime(f"{now.date()} {target_time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

        # If target time has passed today, it must be for tomorrow
        if target < now:
            log(f"Target time {target_time_str} has passed, skipping")
            return

        wait_seconds = (target - now).total_seconds()

        if wait_seconds <= 0:
            return

        if wait_seconds > 60:
            log(f"Waiting {wait_seconds/60:.1f} minutes until {target_time_str} UTC...")
            time.sleep(60)  # Check every minute
        else:
            log(f"Waiting {wait_seconds:.0f} seconds until {target_time_str} UTC...")
            time.sleep(wait_seconds)
            return

def main():
    log("=== Day 21 Sessions 5-7 Automation Started (v6) ===")
    log("Schedule: Session 5 (09:02, 120min), Session 6 (11:32, 120min), Session 7 (14:02, 90min)")

    # Session 5: 09:02 UTC, 120 minutes
    log("\n--- Session 5: 09:02 UTC, 120 minutes ---")
    wait_until("09:02")
    if turn_on_light(120):
        log("Session 5 activated successfully")
    else:
        log("Session 5 activation failed - manual intervention needed")

    # Session 6: 11:32 UTC, 120 minutes
    log("\n--- Session 6: 11:32 UTC, 120 minutes ---")
    wait_until("11:32")
    if turn_on_light(120):
        log("Session 6 activated successfully")
    else:
        log("Session 6 activation failed - manual intervention needed")

    # Session 7: 14:02 UTC, 90 minutes
    log("\n--- Session 7: 14:02 UTC, 90 minutes ---")
    wait_until("14:02")
    if turn_on_light(90):
        log("Session 7 activated successfully - Day 21 complete!")
    else:
        log("Session 7 activation failed - manual intervention needed")

    log("\n=== Day 21 Sessions 5-7 Automation Complete ===")
    log("Day 21 total: 840 minutes delivered across 7 sessions")

if __name__ == "__main__":
    main()
