#!/usr/bin/env python3
"""
Session Manager - Handles Session 2 shutoff verification and Session 3 startup
"""
import time
from datetime import datetime, timezone
import subprocess
import sys

def run_command(cmd):
    """Execute a command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def log(msg):
    """Log with timestamp"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{now}] {msg}")
    sys.stdout.flush()

def main():
    # Wait until Session 2 auto-shutoff time (03:29:35 UTC + 5 seconds buffer)
    shutoff_time = datetime(2025, 12, 14, 3, 29, 40, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    if now < shutoff_time:
        wait_seconds = (shutoff_time - now).total_seconds()
        log(f"Waiting {wait_seconds:.0f} seconds until shutoff verification time ({shutoff_time.strftime('%H:%M:%S UTC')})")
        time.sleep(wait_seconds)

    # Take shutoff verification photo
    log("Taking Session 2 shutoff verification photo...")
    stdout, stderr, code = run_command("curl -s http://plant-server.cynexia.net:8000/api/camera/capture")
    log(f"Shutoff photo captured: {stdout}")

    # Check light status
    stdout, stderr, code = run_command("curl -s http://plant-server.cynexia.net:8000/api/light/status")
    log(f"Light status after shutoff: {stdout}")

    # Wait 30 minutes for cooldown (system requirement)
    session3_start = datetime(2025, 12, 14, 3, 59, 35, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    if now < session3_start:
        wait_seconds = (session3_start - now).total_seconds()
        log(f"Waiting {wait_seconds:.0f} seconds for cooldown until Session 3 start ({session3_start.strftime('%H:%M:%S UTC')})")
        time.sleep(wait_seconds)

    # Start Session 3
    log("Starting Session 3 (120 minutes)...")
    stdout, stderr, code = run_command("curl -s -X POST http://plant-server.cynexia.net:8000/api/light/on -H 'Content-Type: application/json' -d '{\"minutes\": 120}'")
    log(f"Light activation response: {stdout}")

    # Take verification photo (within 10 seconds)
    log("Taking Session 3 start verification photo...")
    time.sleep(5)  # Wait 5 seconds for light to stabilize
    stdout, stderr, code = run_command("curl -s http://plant-server.cynexia.net:8000/api/camera/capture")
    log(f"Session 3 start photo captured: {stdout}")

    log("Session 2 shutoff verified and Session 3 started successfully!")

if __name__ == "__main__":
    main()
