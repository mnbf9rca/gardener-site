#!/usr/bin/env python3
"""
Day 21 Sessions 5-7 Automation (v2)
Handles remaining sessions to complete 840 minutes
"""

import requests
import time
from datetime import datetime, timezone, timedelta

BASE_URL = "http://localhost:8000"

def log(msg):
    """Print timestamped log message"""
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}", flush=True)

def turn_on_light(minutes):
    """Activate grow light"""
    try:
        response = requests.post(f"{BASE_URL}/light/on", json={"minutes": minutes}, timeout=10)
        response.raise_for_status()
        log(f"✅ Light activated for {minutes} minutes")
        return True
    except Exception as e:
        log(f"❌ Error activating light: {e}")
        return False

def get_light_status():
    """Get current light status"""
    try:
        response = requests.get(f"{BASE_URL}/light/status", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log(f"❌ Error getting light status: {e}")
        return None

def wait_until(target_time, session_name):
    """Wait until target time, logging countdown"""
    while True:
        now = datetime.now(timezone.utc)
        remaining = (target_time - now).total_seconds()

        if remaining <= 0:
            break

        if remaining > 60:
            log(f"⏳ {session_name}: {remaining/60:.1f} minutes until start")
            time.sleep(min(60, remaining))
        else:
            log(f"⏳ {session_name}: {remaining:.0f} seconds until start")
            time.sleep(min(10, remaining))

def run_session(session_num, start_time, duration_minutes):
    """Run a single light session"""
    session_name = f"Session {session_num}"
    log(f"📅 {session_name} scheduled: {start_time.isoformat()} for {duration_minutes} min")

    # Wait until start time
    wait_until(start_time, session_name)

    # Activate light
    log(f"🚀 Starting {session_name}")
    success = turn_on_light(duration_minutes)

    if success:
        log(f"✅ {session_name} activated successfully")
        end_time = start_time + timedelta(minutes=duration_minutes)
        log(f"📍 {session_name} will end at {end_time.isoformat()}")
    else:
        log(f"❌ {session_name} FAILED to activate")

    return success

def main():
    """Main automation loop for Sessions 5-7"""
    log("=" * 60)
    log("Day 21 Sessions 5-7 Automation Started (v2)")
    log("=" * 60)

    # Check current light status
    status = get_light_status()
    if status:
        log(f"Current light status: {status.get('status', 'unknown')}")
        if status.get('status') == 'on':
            last_on = status.get('last_on', 'unknown')
            log(f"Light is currently ON (started: {last_on})")

    # Session 4 ends at 08:32 UTC (from notes)
    session4_end = datetime(2025, 12, 14, 8, 32, 0, tzinfo=timezone.utc)
    cooldown = timedelta(minutes=30)

    # Define session schedule
    sessions = [
        {
            'num': 5,
            'start': session4_end + cooldown,  # 09:02 UTC
            'duration': 120
        },
        {
            'num': 6,
            'start': session4_end + cooldown + timedelta(minutes=120) + cooldown,  # 11:32 UTC
            'duration': 120
        },
        {
            'num': 7,
            'start': session4_end + cooldown + timedelta(minutes=120) + cooldown + timedelta(minutes=120) + cooldown,  # 14:02 UTC
            'duration': 90
        }
    ]

    # Log schedule
    log("\n📋 Session Schedule:")
    for session in sessions:
        log(f"  Session {session['num']}: {session['start'].isoformat()} ({session['duration']} min)")

    total_minutes = sum(s['duration'] for s in sessions)
    log(f"\n📊 Total: {total_minutes} minutes across {len(sessions)} sessions")
    log("")

    # Run each session
    for session in sessions:
        success = run_session(session['num'], session['start'], session['duration'])

        if not success:
            log(f"⚠️ Session {session['num']} failed - will retry in next cycle")

        # Brief pause between sessions
        time.sleep(5)

    log("=" * 60)
    log("Day 21 Sessions 5-7 Automation Complete")
    log("All sessions scheduled/executed")
    log("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n⚠️ Automation interrupted by user")
    except Exception as e:
        log(f"\n❌ Fatal error: {e}")
        raise
