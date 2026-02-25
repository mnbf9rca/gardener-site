#!/usr/bin/env python3
"""
Direct access to plant sensors via MCP Python client
"""
import sys
import os

# Add the MCP server path to try importing the tools directly
sys.path.insert(0, '/home/mcpserver/plant-care-app')

try:
    # Try importing the plant care tools directly
    from plant_care.sensors import read_moisture_sensor
    from plant_care.database import get_latest_moisture, get_latest_light_status
    from datetime import datetime

    print("=" * 70)
    print(f"Direct Sensor Access - {datetime.now().isoformat()}")
    print("=" * 70)
    print()

    # Read current moisture
    moisture = read_moisture_sensor()
    print(f"Current Moisture: {moisture}")

    # Get latest from database
    latest_moisture = get_latest_moisture()
    print(f"Latest DB Moisture: {latest_moisture}")

    latest_light = get_latest_light_status()
    print(f"Latest Light Status: {latest_light}")

except ImportError as e:
    print(f"Could not import plant_care modules: {e}")
    print("\nTrying alternative SQLite access...")

    try:
        import sqlite3
        db_path = '/home/mcpserver/plant-care-app/plant_data.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get latest moisture
        cursor.execute("SELECT timestamp, value FROM moisture_readings ORDER BY timestamp DESC LIMIT 1")
        moisture_row = cursor.fetchone()
        print(f"Latest Moisture: {moisture_row}")

        # Get latest light
        cursor.execute("SELECT timestamp, status FROM light_status ORDER BY timestamp DESC LIMIT 1")
        light_row = cursor.fetchone()
        print(f"Latest Light: {light_row}")

        conn.close()

    except Exception as e2:
        print(f"SQLite access failed: {e2}")
        print("\nAll direct access methods exhausted.")
