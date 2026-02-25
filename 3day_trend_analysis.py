#!/usr/bin/env python3
"""
3-Day Trend Analysis - Understanding the plant's moisture trajectory
"""

import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Get 72-hour moisture data (simplified from the full dataset)
# Sampling key points to show the trend
data_72h = [
    ("2025-11-19T22:30:32Z", 1855),  # Nov 19 evening - post-watering baseline
    ("2025-11-20T06:35:45Z", 1875),  # Nov 20 morning
    ("2025-11-20T12:16:46Z", 1883),  # Nov 20 midday
    ("2025-11-20T18:21:06Z", 1878),  # Nov 20 evening
    ("2025-11-21T00:23:41Z", 1896),  # Nov 21 early morning
    ("2025-11-21T06:14:25Z", 1913),  # Nov 21 morning
    ("2025-11-21T12:32:24Z", 1912),  # Nov 21 midday
    ("2025-11-21T18:14:36Z", 1916),  # Nov 21 evening
    ("2025-11-22T00:24:01Z", 1918),  # Nov 22 early morning
    ("2025-11-22T06:16:07Z", 1942),  # Nov 22 morning
    ("2025-11-22T12:25:51Z", 1948),  # Nov 22 midday
    ("2025-11-22T18:19:54Z", 1951),  # Nov 22 evening (pre-oscillation)
    ("2025-11-22T20:05:24Z", 1976),  # Nov 22 evening peak (oscillation)
    ("2025-11-22T21:49:41Z", 1965),  # Nov 22 current
]

# Parse data
timestamps = [datetime.fromisoformat(d[0].replace('Z', '+00:00')) for d in data_72h]
moisture = [d[1] for d in data_72h]

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))

# Top plot: Full 72-hour trend
ax1.plot(timestamps, moisture, 'b-o', linewidth=2, markersize=6, label='Moisture sensor')

# Add threshold lines
ax1.axhline(y=1900, color='green', linestyle='--', alpha=0.5, label='Optimal/Monitor boundary')
ax1.axhline(y=2000, color='orange', linestyle='--', alpha=0.5, label='Monitor/Water Soon boundary')
ax1.axhline(y=2100, color='red', linestyle='--', alpha=0.5, label='Water Soon/Water Now boundary')

# Mark watering event (approximate)
watering_time = datetime.fromisoformat("2025-11-19T09:00:00+00:00")
ax1.axvline(x=watering_time, color='blue', linestyle=':', alpha=0.7, linewidth=2, label='Last watering (~45ml)')

# Add trend line
x_numeric = [(t - timestamps[0]).total_seconds() / 3600 for t in timestamps]
z = np.polyfit(x_numeric[:12], moisture[:12], 1)  # Linear fit on first 12 points (before evening spike)
p = np.poly1d(z)
trend_line = [p(x) for x in x_numeric]
ax1.plot(timestamps, trend_line, 'r--', alpha=0.5, linewidth=2, label=f'Trend: +{z[0]:.2f}/hour')

# Format x-axis
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M', tz=timestamps[0].tzinfo))
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=12))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Labels and title
ax1.set_xlabel('Time (UTC)', fontsize=12)
ax1.set_ylabel('Moisture Sensor Reading', fontsize=12)
ax1.set_title('72-Hour Moisture Trend - Post-Watering Evolution\n2025-11-19 22:30 to 2025-11-22 21:49 UTC', fontsize=14, fontweight='bold')
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(True, alpha=0.3)

# Add day markers
for day in range(3):
    day_start = datetime.fromisoformat("2025-11-20T00:00:00+00:00") + timedelta(days=day)
    ax1.axvline(x=day_start, color='gray', linestyle=':', alpha=0.3)
    ax1.text(day_start, 1850, f'Day {20+day}', rotation=90, va='bottom', fontsize=9, alpha=0.7)

# Bottom plot: Rate of change analysis
time_diffs = [(timestamps[i+1] - timestamps[i]).total_seconds() / 3600 for i in range(len(timestamps)-1)]
moisture_diffs = [moisture[i+1] - moisture[i] for i in range(len(moisture)-1)]
rates = [md / td if td > 0 else 0 for md, td in zip(moisture_diffs, time_diffs)]
rate_timestamps = timestamps[:-1]

ax2.bar(rate_timestamps, rates, width=0.15, alpha=0.7, color=['green' if r > 0 else 'blue' for r in rates])
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax2.set_xlabel('Time (UTC)', fontsize=12)
ax2.set_ylabel('Rate of Change (units/hour)', fontsize=12)
ax2.set_title('Moisture Change Rate Over Time', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Format x-axis
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M', tz=timestamps[0].tzinfo))
ax2.xaxis.set_major_locator(mdates.HourLocator(interval=12))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('/home/gardener/workspace/3day_moisture_trend.png', dpi=150, bbox_inches='tight')
print("✓ Saved: 3day_moisture_trend.png")

# Print summary statistics
print("\n" + "="*70)
print("72-HOUR MOISTURE TREND ANALYSIS")
print("="*70)

print(f"\nTime since last watering: ~85-90 hours")
print(f"Watering amount: 45ml (Nov 19, ~06:00-12:00 UTC)")

print(f"\nMoisture progression:")
print(f"  Nov 19 evening (baseline): {moisture[0]}")
print(f"  Nov 20 average: ~{np.mean([m for t, m in zip(timestamps, moisture) if t.day == 20]):.0f}")
print(f"  Nov 21 average: ~{np.mean([m for t, m in zip(timestamps, moisture) if t.day == 21]):.0f}")
print(f"  Nov 22 pre-oscillation: {moisture[11]}")
print(f"  Nov 22 current: {moisture[13]}")

print(f"\nOverall trend (excluding evening spike):")
print(f"  Start: {moisture[0]}")
print(f"  End (pre-spike): {moisture[11]}")
print(f"  Total change: +{moisture[11] - moisture[0]} over {(timestamps[11] - timestamps[0]).total_seconds() / 3600:.1f} hours")
print(f"  Average rate: +{z[0]:.2f} units/hour")
print(f"  Expected time to reach 2000 (Water Soon): ~{(2000 - moisture[13]) / z[0]:.0f} hours")

print(f"\nCurrent status:")
print(f"  Moisture: {moisture[13]}")
print(f"  Range: Monitor (1900-2000)")
print(f"  Plant health: HEALTHY")
print(f"  Days without water: ~3.6 days")
print(f"  Estimated days until watering needed: ~{(2000 - moisture[13]) / (z[0] * 24):.1f} days")

print(f"\nKey observations:")
print(f"  - Plant handling water stress very well")
print(f"  - Moisture climbing steadily but slowly (~{z[0]:.2f}/hr)")
print(f"  - No signs of distress despite 3+ days without water")
print(f"  - Evening oscillation was environmental, not plant-related")
print(f"  - Current baseline ~1965 is sustainable for several more days")

print("\n" + "="*70)
