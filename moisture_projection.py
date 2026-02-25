#!/usr/bin/env python3
"""
Calculate current moisture projection based on historical data
"""
from datetime import datetime, timedelta

# Last known data
last_reading = 2201
last_time_str = "2025-11-03 07:48:00 UTC"
last_time = datetime.fromisoformat(last_time_str.replace(" UTC", "+00:00"))

# Current time
current_time = datetime.now().astimezone()
print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"Last reading: {last_reading} at {last_time_str}")

# Calculate elapsed time
elapsed = current_time - last_time
elapsed_hours = elapsed.total_seconds() / 3600
elapsed_minutes = elapsed.total_seconds() / 60

print(f"Time elapsed: {elapsed_minutes:.0f} minutes ({elapsed_hours:.2f} hours)")

# Historical descent rates from notes
# Fastest observed: -33 pts/hr during recent descent phase
# Typical rates are slower and decelerate over time
descent_rate_fast = -33  # pts/hr
descent_rate_moderate = -20  # pts/hr
descent_rate_slow = -10  # pts/hr

print("\n=== Moisture Projections ===")
print(f"Using descent rate scenarios:")

# Scenario 1: Fast descent continues
projected_fast = last_reading + (descent_rate_fast * elapsed_hours)
print(f"\n1. Fast descent ({descent_rate_fast} pts/hr):")
print(f"   Projected moisture: {projected_fast:.0f}")
print(f"   Margin to threshold (2400): {2400 - projected_fast:.0f} points")

# Scenario 2: Moderate descent (more realistic)
projected_mod = last_reading + (descent_rate_moderate * elapsed_hours)
print(f"\n2. Moderate descent ({descent_rate_moderate} pts/hr):")
print(f"   Projected moisture: {projected_mod:.0f}")
print(f"   Margin to threshold (2400): {2400 - projected_mod:.0f} points")

# Scenario 3: Slow descent (decelerated)
projected_slow = last_reading + (descent_rate_slow * elapsed_hours)
print(f"\n3. Slow descent ({descent_rate_slow} pts/hr):")
print(f"   Projected moisture: {projected_slow:.0f}")
print(f"   Margin to threshold (2400): {2400 - projected_slow:.0f} points")

# Best estimate (moderate scenario)
best_estimate = projected_mod
print(f"\n=== Best Estimate ===")
print(f"Current moisture (estimated): ~{best_estimate:.0f}")
print(f"Safety margin: {2400 - best_estimate:.0f} points")

# Calculate time to threshold
hours_to_threshold = (2400 - best_estimate) / abs(descent_rate_moderate)
print(f"Hours to threshold: {hours_to_threshold:.1f}")

# Determine recommendation
print(f"\n=== Recommendation ===")
if best_estimate > 2400:
    print("⚠️  WATER NOW - Above threshold")
elif best_estimate > 2300:
    print("⚠️  WATER SOON - Approaching threshold")
elif best_estimate > 2200:
    print("✓ MONITOR CLOSELY - At threshold range")
else:
    print("✓ DO NOT WATER - Well within safe range")

print(f"\nReasoning:")
print(f"- Estimated moisture {best_estimate:.0f} is {'ABOVE' if best_estimate > 2400 else 'within' if best_estimate > 2200 else 'below'} threshold (2400)")
print(f"- Safety buffer: {2400 - best_estimate:.0f} points")
print(f"- Time available: ~{hours_to_threshold:.1f} hours")
print(f"- Plant demonstrated resilience: 12+ days without water")
print(f"- Previous cycles showed oscillation behavior")
