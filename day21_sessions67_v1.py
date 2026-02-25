#!/usr/bin/env python3
"""
Day 21 Sessions 6-7 Automation
Handles remaining sessions for Day 21 (Dec 14, 2025)
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
        print(f"✅ Light ON for {minutes} minutes at {datetime.now(timezone.utc).isoformat()}")
        return True
    except Exception as e:
        print(f"❌ Failed to turn on light: {e}")
        return False

def wait_until(target_time_utc):
    """Wait until specified UTC time"""
    while True:
        now = datetime.now(timezone.utc)
        if now >= target_time_utc:
            break
        sleep_seconds = (target_time_utc - now).total_seconds()
        if sleep_seconds > 0:
            print(f"⏳ Waiting {sleep_seconds:.0f}s until {target_time_utc.strftime('%H:%M:%S')} UTC")
            time.sleep(min(sleep_seconds, 60))  # Check every minute

def main():
    print("🌱 Day 21 Sessions 6-7 Automation Starting")
    print(f"⏰ Current time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")

    # Session 6: 11:32-13:32 UTC (120 minutes)
    session6_start = datetime(2025, 12, 14, 11, 32, 0, tzinfo=timezone.utc)
    print(f"\n📅 Session 6: {session6_start.strftime('%H:%M')} UTC (120 min)")
    wait_until(session6_start)
    if not turn_on_light(120):
        print("❌ Session 6 failed to start")
        return

    # Wait for Session 6 to complete
    session6_end = datetime(2025, 12, 14, 13, 32, 0, tzinfo=timezone.utc)
    wait_until(session6_end)

    # Session 7: 14:02-15:32 UTC (90 minutes) - FINAL SESSION
    session7_start = datetime(2025, 12, 14, 14, 2, 0, tzinfo=timezone.utc)
    print(f"\n📅 Session 7: {session7_start.strftime('%H:%M')} UTC (90 min) - FINAL SESSION")
    wait_until(session7_start)
    if not turn_on_light(90):
        print("❌ Session 7 failed to start")
        return

    print("\n✅ All sessions scheduled successfully!")
    print(f"⏰ Day 21 will complete at 15:32 UTC (total: 840 minutes)")

if __name__ == "__main__":
    main()
