#!/usr/bin/env python3
"""
Automate remaining light sessions for Day 30 photoperiod.
Sessions 2-7, each 120 minutes with 30-minute cooldowns.
"""

import time
import requests
import json
from datetime import datetime, timezone

MCP_BASE_URL = "http://localhost:3000"

def get_current_time():
    """Get current UTC time"""
    response = requests.post(f"{MCP_BASE_URL}/mcp/call", json={
        "server": "plant-tools",
        "method": "get_current_time",
        "params": {}
    })
    result = response.json()
    return result['timestamp']

def get_light_status():
    """Check light status"""
    response = requests.post(f"{MCP_BASE_URL}/mcp/call", json={
        "server": "plant-tools",
        "method": "get_light_status",
        "params": {}
    })
    return response.json()

def turn_on_light(minutes):
    """Turn on grow light"""
    response = requests.post(f"{MCP_BASE_URL}/mcp/call", json={
        "server": "plant-tools",
        "method": "turn_on_light",
        "params": {"minutes": minutes}
    })
    return response.json()

def log_action(action_type, details):
    """Log action"""
    response = requests.post(f"{MCP_BASE_URL}/mcp/call", json={
        "server": "plant-tools",
        "method": "log_action",
        "params": {"type": action_type, "details": details}
    })
    return response.json()

def run_remaining_sessions():
    """Run sessions 3-7"""
    sessions = [
        {"number": 3, "name": "3/7"},
        {"number": 4, "name": "4/7"},
        {"number": 5, "name": "5/7"},
        {"number": 6, "name": "6/7"},
        {"number": 7, "name": "7/7"},
    ]

    for session in sessions:
        # Wait until light is available
        while True:
            status = get_light_status()
            if status['can_activate']:
                break
            mins_remaining = status.get('minutes_until_available', 0)
            print(f"[{datetime.now(timezone.utc).isoformat()}] Waiting for cooldown... {mins_remaining} minutes remaining")
            time.sleep(60)  # Check every minute

        # Start the session
        current_time = get_current_time()
        result = turn_on_light(120)
        print(f"[{current_time}] Session {session['name']} started: {result}")

        # Log the action
        log_action("light", {
            "session": session['name'],
            "duration_minutes": 120,
            "started_at": current_time,
            "will_end_at": result.get('off_at'),
            "day": 30,
            "cycle_type": "WATER"
        })

        # Wait for session to complete (120 minutes)
        print(f"[{current_time}] Waiting for Session {session['name']} to complete (120 minutes)...")
        time.sleep(7200)  # 120 minutes

        # Wait for cooldown if not last session
        if session['number'] < 7:
            print(f"[{get_current_time()}] Session {session['name']} complete. Starting 30-minute cooldown...")
            time.sleep(1800)  # 30 minutes cooldown

    print(f"[{get_current_time()}] All sessions complete! Day 30 photoperiod: 840 minutes achieved.")

if __name__ == "__main__":
    print(f"[{get_current_time()}] Starting automated light session manager...")
    print("Session 2/7 is already running (started 02:47 UTC, ends 04:47 UTC)")
    print("This script will run sessions 3-7")
    print()

    # Wait until Session 2 completes (04:47 UTC)
    current = datetime.now(timezone.utc)
    session2_end = datetime(2026, 2, 8, 4, 47, 0, tzinfo=timezone.utc)

    if current < session2_end:
        wait_seconds = (session2_end - current).total_seconds()
        print(f"Waiting {wait_seconds/60:.1f} minutes for Session 2 to complete...")
        time.sleep(wait_seconds + 60)  # Add 1 minute buffer

    run_remaining_sessions()
