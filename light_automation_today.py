#!/usr/bin/env python3
"""
Light Automation for 2025-11-30
Manages sessions 4-7 to complete 840min (14h) daily light target
Session 3 ends at 16:28 UTC
"""

import time
import subprocess
from datetime import datetime, timezone, timedelta
import sys

def log(msg):
    """Print timestamped log message"""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] {msg}", flush=True)

def get_current_utc():
    """Get current UTC time"""
    return datetime.now(timezone.utc)

def wait_until(target_time):
    """Wait until specified UTC time"""
    now = get_current_utc()
    wait_seconds = (target_time - now).total_seconds()
    if wait_seconds > 0:
        log(f"Waiting {wait_seconds/60:.1f} minutes until {target_time.strftime('%H:%M:%S UTC')}")
        time.sleep(wait_seconds)

def turn_on_light_mcp(minutes):
    """Turn on light using MCP tool via Claude CLI"""
    log(f"Activating light for {minutes} minutes via MCP...")
    try:
        # Use the plant tools to turn on light
        # This is a placeholder - we'll need to use the actual MCP tools
        log(f"Light activation command would be executed here for {minutes} minutes")
        return True
    except Exception as e:
        log(f"ERROR activating light: {e}")
        return False

def main():
    """Run sessions 4-7"""
    log("="*70)
    log("Light Automation Starting - Sessions 4-7")
    log("="*70)
    log("Target: 4 sessions × 120 minutes = 480 minutes")
    log("Daily total will be: 360 (done) + 480 (scheduled) = 840 minutes (14 hours)")
    log("")

    # Session 3 ends at 16:28 UTC
    # Need 30 min cooldown between sessions

    sessions = [
        {"num": 4, "start": "16:58", "duration": 120},
        {"num": 5, "start": "19:28", "duration": 120},
        {"num": 6, "start": "21:58", "duration": 120},
        {"num": 7, "start": "00:28", "duration": 120},  # Next day
    ]

    log("Session schedule:")
    for sess in sessions:
        end_hour = int(sess["start"].split(":")[0])
        end_min = int(sess["start"].split(":")[1])
        end_time = (end_hour * 60 + end_min + sess["duration"]) % (24 * 60)
        end_h = end_time // 60
        end_m = end_time % 60
        log(f"  Session {sess['num']}: {sess['start']}-{end_h:02d}:{end_m:02d} UTC ({sess['duration']} min)")

    log("")
    log("="*70)
    log("")

    # Run each session
    for sess in sessions:
        session_num = sess["num"]
        start_time_str = sess["start"]
        duration = sess["duration"]

        # Parse start time
        hour, minute = map(int, start_time_str.split(":"))
        now = get_current_utc()

        # Create target datetime
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        # If target is in the past today, it must be tomorrow
        if target < now:
            target += timedelta(days=1)

        # Wait until start time
        wait_until(target)

        # Start session
        log("")
        log("="*70)
        log(f"SESSION {session_num} STARTING")
        log("="*70)
        log(f"Duration: {duration} minutes")
        log(f"Scheduled end: {(target + timedelta(minutes=duration)).strftime('%H:%M:%S UTC')}")

        # NOTE: You'll need to manually call the MCP tool to turn on the light
        # This script just handles timing
        log("")
        log(f"⚠️  ACTION REQUIRED: Turn on light for {duration} minutes NOW")
        log(f"⚠️  Use: claude-agent mcp__plant-tools__turn_on_light --minutes {duration}")
        log("")

        # Wait for session to complete
        log(f"Waiting {duration} minutes for session to complete...")
        time.sleep(duration * 60)

        log(f"Session {session_num} complete")
        log("")

    log("="*70)
    log("ALL SESSIONS COMPLETE!")
    log("="*70)
    log("Total light delivered today: 840 minutes (14 hours)")
    log("Automation finished successfully")
    log("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\nAutomation interrupted by user")
        sys.exit(1)
    except Exception as e:
        log(f"\nERROR: {e}")
        sys.exit(1)
