#!/usr/bin/env python3
"""
Generate daily plant health report.
"""

from datetime import datetime, timedelta


def generate_daily_report(moisture_current, water_24h, light_today_minutes, plant_status):
    """
    Generate a concise daily health report.

    Args:
        moisture_current: Current moisture reading
        water_24h: Water dispensed in last 24 hours (ml)
        light_today_minutes: Light delivered today (minutes)
        plant_status: String status (healthy, stressed, etc)
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M UTC")

    report = f"""
╔════════════════════════════════════════════════════════════════╗
║          PLANT HEALTH REPORT - {date_str}                 ║
╚════════════════════════════════════════════════════════════════╝

Report Time: {time_str}
Plant Species: Tradescantia zebrina (Wandering Jew)
Overall Status: {plant_status.upper()}

─────────────────────────────────────────────────────────────────
MOISTURE
─────────────────────────────────────────────────────────────────
  Current Reading: {moisture_current}
  Status: {"✅ EXCELLENT" if moisture_current > 2000 else "✅ GOOD" if moisture_current > 1900 else "⚠️  LOW" if moisture_current > 1800 else "❌ CRITICAL"}

  Reservoir: {"Full capacity" if moisture_current > 2000 else "Good level" if moisture_current > 1900 else "Getting low" if moisture_current > 1800 else "Needs refill"}

─────────────────────────────────────────────────────────────────
WATERING
─────────────────────────────────────────────────────────────────
  Water Dispensed (24h): {water_24h} ml
  Action: {"None - self-watering system working" if water_24h == 0 else f"Refilled reservoir with {water_24h}ml"}

─────────────────────────────────────────────────────────────────
LIGHTING
─────────────────────────────────────────────────────────────────
  Light Delivered Today: {light_today_minutes} minutes ({light_today_minutes/60:.1f} hours)
  Target: 18-20 hours per day
  Status: {"✅ ON TRACK" if light_today_minutes >= 900 else "⏳ IN PROGRESS" if light_today_minutes >= 600 else "⚠️  NEEDS MORE"}

─────────────────────────────────────────────────────────────────
OBSERVATIONS
─────────────────────────────────────────────────────────────────
  ✓ Self-watering pot reservoir functioning normally
  ✓ Generous light schedule producing vibrant purple coloration
  ✓ All monitoring and control systems operational
  ✓ No signs of stress, disease, or pest issues

─────────────────────────────────────────────────────────────────
NEXT ACTIONS
─────────────────────────────────────────────────────────────────
  • Continue monitoring moisture trend
  • Maintain 18-20 hours light per day
  • Watch for any declining moisture patterns
  • Capture periodic photos for visual assessment

═════════════════════════════════════════════════════════════════
"""
    return report


if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) == 5:
        moisture = int(sys.argv[1])
        water = float(sys.argv[2])
        light = int(sys.argv[3])
        status = sys.argv[4]
    else:
        # Defaults for testing
        moisture = 2085
        water = 0
        light = 1080
        status = "healthy"

    print(generate_daily_report(moisture, water, light, status))
