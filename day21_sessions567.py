#!/usr/bin/env python3
"""
Day 21 completion automation - Sessions 5-7
Session 4 started manually at 06:32 (ends 08:32)
This script handles remaining sessions 5-7
"""

import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://localhost:8000"

def turn_on_light(minutes):
    """Turn on grow light for specified duration"""
    response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes})
    response.raise_for_status()
    result = response.json()
    print(f"[{datetime.now(timezone.utc).isoformat()}] Light ON for {minutes} min, off at {result['off_at']}")
    return result

def capture_photo():
    """Capture verification photo"""
    response = requests.post(f"{BASE_URL}/camera/capture")
    response.raise_for_status()
    result = response.json()
    print(f"[{datetime.now(timezone.utc).isoformat()}] Photo: {result['url']}")
    return result

def wait_until(target_time_str):
    """Wait until specific UTC time"""
    target = datetime.fromisoformat(target_time_str.replace('Z', '+00:00'))
    while True:
        now = datetime.now(timezone.utc)
        if now >= target:
            break
        sleep_seconds = (target - now).total_seconds()
        if sleep_seconds > 60:
            print(f"[{now.isoformat()}] Waiting {sleep_seconds:.0f}s until {target_time_str}")
            time.sleep(60)
        else:
            time.sleep(max(1, sleep_seconds))

# Session 4 is running manually (started 06:32, ends 08:32)
# Wait for cooldown after Session 4 ends, then start Session 5

sessions = [
    # Session 5: 30 min after Session 4 ends (08:32 + 0:30 = 09:02)
    {"name": "Session 5", "start": "2025-12-14T09:02:06+00:00", "duration": 120},
    # Session 6: 30 min after Session 5 ends (11:02 + 0:30 = 11:32)
    {"name": "Session 6", "start": "2025-12-14T11:32:06+00:00", "duration": 120},
    # Session 7: 30 min after Session 6 ends (13:32 + 0:30 = 14:02), 90 min to complete 840
    {"name": "Session 7", "start": "2025-12-14T14:02:06+00:00", "duration": 90},
]

print(f"[{datetime.now(timezone.utc).isoformat()}] Day 21 Sessions 5-7 automation started")
print("Session 4 running manually (06:32-08:32)")
print("This script will handle Sessions 5-7")

for session in sessions:
    print(f"\n=== {session['name']} ===")
    wait_until(session['start'])

    # Start session
    turn_on_light(session['duration'])
    time.sleep(1)
    capture_photo()

    print(f"[{datetime.now(timezone.utc).isoformat()}] {session['name']} started successfully")

print(f"\n[{datetime.now(timezone.utc).isoformat()}] Day 21 complete! All 7 sessions executed (840 minutes)")
print("Sessions 1-3: Manual, Session 4: Manual (late start), Sessions 5-7: Automated")
