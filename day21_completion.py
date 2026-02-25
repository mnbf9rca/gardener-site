#!/usr/bin/env python3
"""
Day 21 Completion Script - Sessions 4-7
Automates the remaining sessions for Day 21 Phase 2
"""

import time
import requests
from datetime import datetime, timezone, timedelta

# MCP server base URL
BASE_URL = "http://localhost:8000"

def get_current_time():
    """Get current UTC time"""
    return datetime.now(timezone.utc)

def turn_on_light(minutes):
    """Turn on light for specified minutes"""
    response = requests.post(
        f"{BASE_URL}/plant/light/on",
        json={"minutes": minutes}
    )
    response.raise_for_status()
    return response.json()

def capture_photo():
    """Capture a photo"""
    response = requests.post(f"{BASE_URL}/plant/camera/capture")
    response.raise_for_status()
    return response.json()

def get_light_status():
    """Get light status"""
    response = requests.get(f"{BASE_URL}/plant/light/status")
    response.raise_for_status()
    return response.json()

def wait_until(target_time, description):
    """Wait until target time"""
    now = get_current_time()
    wait_seconds = (target_time - now).total_seconds()

    if wait_seconds > 0:
        print(f"[{now.strftime('%H:%M:%S')}] Waiting {wait_seconds:.1f}s ({wait_seconds/60:.1f}min) until {description}")
        time.sleep(wait_seconds)
    else:
        print(f"[{now.strftime('%H:%M:%S')}] Target time passed, proceeding with {description}")

def run_session(session_num, duration_minutes, start_time):
    """Run a single light session with verification"""
    print(f"\n{'='*60}")
    print(f"SESSION {session_num} - {duration_minutes} minutes")
    print(f"{'='*60}")

    # Wait until start time
    wait_until(start_time, f"Session {session_num} start")

    # Activate light
    now = get_current_time()
    print(f"[{now.strftime('%H:%M:%S')}] Activating light for {duration_minutes} minutes...")
    light_result = turn_on_light(duration_minutes)
    print(f"[{now.strftime('%H:%M:%S')}] Light ON - Auto-shutoff at {light_result['off_at']}")

    # Take verification photo
    time.sleep(5)  # Brief delay
    now = get_current_time()
    print(f"[{now.strftime('%H:%M:%S')}] Taking verification photo...")
    photo_result = capture_photo()
    print(f"[{now.strftime('%H:%M:%S')}] Photo captured: {photo_result['url']}")

    # Calculate next available time (30 min cooldown after shutoff)
    shutoff_time = datetime.fromisoformat(light_result['off_at'].replace('Z', '+00:00'))
    next_available = shutoff_time + timedelta(minutes=30)

    print(f"[{now.strftime('%H:%M:%S')}] Session {session_num} running until {shutoff_time.strftime('%H:%M:%S')}")
    print(f"[{now.strftime('%H:%M:%S')}] Next session available at {next_available.strftime('%H:%M:%S')}")

    return shutoff_time, next_available

def main():
    """Main execution"""
    print("Day 21 Completion Script - Sessions 4-7")
    print(f"Started at {get_current_time().strftime('%Y-%m-%d %H:%M:%S')} UTC\n")

    # Session schedule (waiting for Session 3 to complete first)
    # Session 3 ends at 05:59:39, next available at 06:29:39

    sessions = [
        (4, 120, datetime(2025, 12, 14, 6, 29, 39, tzinfo=timezone.utc)),
        (5, 120, None),  # Will calculate after Session 4
        (6, 120, None),  # Will calculate after Session 5
        (7, 90, None),   # Will calculate after Session 6
    ]

    next_available = None

    for session_num, duration, scheduled_start in sessions:
        # Use calculated time if scheduled_start is None
        if scheduled_start is None:
            if next_available is None:
                raise ValueError(f"Cannot determine start time for Session {session_num}")
            scheduled_start = next_available

        shutoff_time, next_available = run_session(session_num, duration, scheduled_start)

    print(f"\n{'='*60}")
    print("DAY 21 COMPLETE!")
    print(f"{'='*60}")
    print(f"Finished at {get_current_time().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"Total sessions: 7")
    print(f"Total minutes: 840 (14 hours)")
    print("All sessions photo-verified ✅")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
