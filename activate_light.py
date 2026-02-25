#!/usr/bin/env python3
"""Wait for light cooldown and activate session 5"""

import time
import requests
import json
from datetime import datetime

def check_light_status():
    """Check if light can be activated"""
    # This would normally call the MCP tool, but we'll use a simple time-based approach
    return True

def activate_light(duration_minutes):
    """Activate the grow light"""
    print(f"{datetime.utcnow().strftime('%H:%M:%S UTC')}: Attempting to activate light for {duration_minutes} minutes...")
    # This would normally call the MCP tool
    return True

def main():
    target_time = "08:35:00"
    duration = 100

    print(f"Current time: {datetime.utcnow().strftime('%H:%M:%S UTC')}")
    print(f"Waiting until {target_time} UTC to activate light for {duration} minutes...")

    while True:
        current_time = datetime.utcnow().strftime('%H:%M:%S')
        if current_time >= target_time:
            print(f"\nTime reached: {current_time} UTC")
            print(f"Activating light session 5 for {duration} minutes...")
            break
        time.sleep(30)  # Check every 30 seconds

    print("\nReady to activate!")

if __name__ == "__main__":
    main()
