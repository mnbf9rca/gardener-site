#!/usr/bin/env python3
"""Wait for light cooldown to complete and activate next session."""

import time
import sys
from datetime import datetime, timezone

def get_light_status():
    """Check light status using MCP tool."""
    import subprocess
    import json
    # We'll check by calculating time since last_off
    # Last off was at 02:10:31, need to wait 30 minutes
    return None

def main():
    # Light went off at 02:10:31 UTC
    # Need to wait until 02:40:31 UTC (30 minute cooldown)
    # Current time is around 02:13-02:14 UTC
    # So we need to wait about 26-27 minutes

    target_time = "02:40:31"
    print(f"Waiting for cooldown to complete... Target activation time: {target_time} UTC")

    while True:
        now = datetime.now(timezone.utc)
        current_time = now.strftime("%H:%M:%S")

        # Check if we've reached 02:40:31 or later
        if current_time >= target_time:
            print(f"\nCooldown complete at {current_time} UTC!")
            print("Ready to activate Session #2 for 120 minutes")
            break

        # Print progress every minute
        if now.second == 0:
            print(f"Current time: {current_time} UTC - waiting for {target_time} UTC")

        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    main()
