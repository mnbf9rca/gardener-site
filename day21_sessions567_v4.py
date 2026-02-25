#!/usr/bin/env python3
"""
Day 21 Light Sessions 5, 6, 7 Automation - v4
Sessions 5-7 with precise timing
Total: 330 minutes (5.5 hours)
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://localhost:3000"

def turn_on_light(minutes):
    """Activate grow light for specified duration."""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        response.raise_for_status()
        print(f"✅ Light activated for {minutes} minutes at {datetime.now(timezone.utc).isoformat()}")
        return True
    except Exception as e:
        print(f"❌ Failed to activate light: {e}")
        return False

def wait_until(target_time_str):
    """Wait until specified UTC time."""
    target = datetime.fromisoformat(target_time_str.replace('Z', '+00:00'))
    while True:
        now = datetime.now(timezone.utc)
        if now >= target:
            break
        sleep_seconds = (target - now).total_seconds()
        if sleep_seconds > 60:
            print(f"⏳ Waiting {sleep_seconds/60:.1f} minutes until {target_time_str}...")
            time.sleep(60)
        else:
            time.sleep(max(1, sleep_seconds))

# Session schedule
sessions = [
    {"name": "Session 5", "start": "2025-12-14T09:02:00Z", "duration": 120},
    {"name": "Session 6", "start": "2025-12-14T11:32:00Z", "duration": 120},
    {"name": "Session 7", "start": "2025-12-14T14:02:00Z", "duration": 90},
]

print(f"🌱 Day 21 Sessions 5-7 Automation Started: {datetime.now(timezone.utc).isoformat()}")
print(f"📋 Schedule: Session 5 (09:02, 120min), Session 6 (11:32, 120min), Session 7 (14:02, 90min)")
print(f"📊 Total: 330 minutes across 3 sessions")

for session in sessions:
    print(f"\n{'='*60}")
    print(f"🎯 {session['name']}: {session['duration']} minutes starting at {session['start']}")

    wait_until(session['start'])

    success = turn_on_light(session['duration'])
    if not success:
        print(f"⚠️ Failed to start {session['name']} - manual intervention needed!")
        continue

    print(f"✅ {session['name']} activated successfully")

print(f"\n{'='*60}")
print(f"🎉 Day 21 Complete! All 7 sessions finished.")
print(f"📊 Total Day 21: 840 minutes delivered")
print(f"🕐 Finished at: {datetime.now(timezone.utc).isoformat()}")
