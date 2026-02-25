#!/usr/bin/env python3
"""
Day 21 Session 6-7 Automation v3
Handles remaining sessions for Dec 13-14 (Day 21)

Session 6: 11:32-13:32 UTC (120 min)
Session 7: 14:02-15:32 UTC (90 min) - FINAL SESSION

Total remaining: 210 minutes (Sessions 6-7)
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://plant-server.cynexia.net:8000"

def turn_on_light(minutes):
    """Turn on the grow light for specified duration"""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        response.raise_for_status()
        print(f"✅ Light ON for {minutes} min at {datetime.now(timezone.utc).isoformat()}")
        return True
    except Exception as e:
        print(f"❌ Error turning on light: {e}")
        return False

def wait_until(target_time_str):
    """Wait until target time (HH:MM UTC format)"""
    while True:
        now = datetime.now(timezone.utc)
        target_hour, target_min = map(int, target_time_str.split(':'))

        target = now.replace(hour=target_hour, minute=target_min, second=0, microsecond=0)
        if target < now:
            target = target.replace(day=target.day + 1)

        wait_seconds = (target - now).total_seconds()

        if wait_seconds <= 0:
            return

        if wait_seconds > 60:
            print(f"⏳ Waiting {wait_seconds/60:.1f} min until {target_time_str} UTC...")
            time.sleep(60)
        else:
            print(f"⏳ Final wait: {wait_seconds:.0f} seconds until {target_time_str} UTC")
            time.sleep(wait_seconds)
            return

def main():
    print("=" * 60)
    print("Day 21 Session 6-7 Automation v3 STARTED")
    print(f"Start time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    # Session 6: 11:32-13:32 UTC (120 min)
    print("\n📅 SESSION 6: 11:32-13:32 UTC (120 min)")
    wait_until("11:32")
    if not turn_on_light(120):
        print("❌ Session 6 failed to start")
    else:
        print("✅ Session 6 started successfully")

    # Session 7: 14:02-15:32 UTC (90 min) - FINAL SESSION
    print("\n📅 SESSION 7: 14:02-15:32 UTC (90 min) - FINAL SESSION")
    wait_until("14:02")
    if not turn_on_light(90):
        print("❌ Session 7 failed to start")
    else:
        print("✅ Session 7 started successfully")
        print("🎉 Day 21 automation complete (840 minutes total)")

    print("\n" + "=" * 60)
    print("Day 21 automation finished")
    print(f"End time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
