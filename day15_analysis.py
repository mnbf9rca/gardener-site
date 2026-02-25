#!/usr/bin/env python3
"""
Day 15 Analysis - Visualizing oscillation patterns and evening event
"""

import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Day 15 moisture data (from the 6-hour history, expanded with recent readings)
data = [
    ("2025-11-22T15:00:00Z", 1949, "Session 8 Start"),
    ("2025-11-22T16:10:32Z", 1939, "During Session 8"),
    ("2025-11-22T17:00:00Z", 1967, "Session 8 End"),
    ("2025-11-22T17:03:40Z", 1967, "Post-light peak"),
    ("2025-11-22T17:11:52Z", 1937, "Phase 1 - Sharp drop"),
    ("2025-11-22T17:27:03Z", 1952, "Phase 2 - Recovery"),
    ("2025-11-22T17:42:13Z", 1959, "Phase 2"),
    ("2025-11-22T18:02:27Z", 1959, "Phase 3 - Damped oscillation"),
    ("2025-11-22T18:19:54Z", 1951, "Phase 3"),
    ("2025-11-22T18:37:43Z", 1957, "Phase 3"),
    ("2025-11-22T18:55:41Z", 1961, "Phase 3"),
    ("2025-11-22T19:12:59Z", 1963, "Phase 3"),
    ("2025-11-22T19:30:09Z", 1963, "Phase 3"),
    ("2025-11-22T19:47:52Z", 1962, "Evening oscillation - Baseline"),
    ("2025-11-22T20:05:24Z", 1976, "Evening oscillation - PEAK"),
    ("2025-11-22T20:22:51Z", 1971, "Evening oscillation - Declining"),
    ("2025-11-22T20:40:13Z", 1964, "Evening oscillation - TROUGH"),
    ("2025-11-22T20:57:14Z", 1973, "Evening oscillation - Recovery"),
    ("2025-11-22T21:14:42Z", 1962, "Evening oscillation - Baseline restored"),
    ("2025-11-22T21:32:14Z", 1964, "Stable"),
    ("2025-11-22T21:49:41Z", 1965, "Current"),
]

# Parse data
timestamps = [datetime.fromisoformat(d[0].replace('Z', '+00:00')) for d in data]
moisture = [d[1] for d in data]
labels = [d[2] for d in data]

# Create figure
fig, ax = plt.subplots(figsize=(16, 8))

# Plot moisture
ax.plot(timestamps, moisture, 'b-o', linewidth=2, markersize=6, label='Moisture sensor')

# Add threshold lines
ax.axhline(y=1900, color='green', linestyle='--', alpha=0.5, label='Optimal/Monitor boundary')
ax.axhline(y=2000, color='orange', linestyle='--', alpha=0.5, label='Monitor/Water Soon boundary')

# Highlight key regions
session8_start = datetime.fromisoformat("2025-11-22T15:00:00+00:00")
session8_end = datetime.fromisoformat("2025-11-22T17:00:00+00:00")
ax.axvspan(session8_start, session8_end, alpha=0.2, color='yellow', label='Session 8 (Light ON)')

evening_start = datetime.fromisoformat("2025-11-22T19:47:52+00:00")
evening_end = datetime.fromisoformat("2025-11-22T21:14:42+00:00")
ax.axvspan(evening_start, evening_end, alpha=0.2, color='purple', label='Evening Oscillation (87min)')

# Mark key events
peak_idx = 14  # 20:05 - Peak at 1976
trough_idx = 16  # 20:40 - Trough at 1964
baseline_restore_idx = 18  # 21:14 - Baseline restored

ax.plot(timestamps[peak_idx], moisture[peak_idx], 'r*', markersize=20, label='Evening Peak (1976)')
ax.plot(timestamps[trough_idx], moisture[trough_idx], 'cv', markersize=12, label='Evening Trough (1964)')
ax.plot(timestamps[baseline_restore_idx], moisture[baseline_restore_idx], 'gs', markersize=12, label='Baseline Restored (1962)')

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M', tz=timestamps[0].tzinfo))
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
plt.xticks(rotation=45, ha='right')

# Labels and title
ax.set_xlabel('Time (UTC)', fontsize=12)
ax.set_ylabel('Moisture Sensor Reading', fontsize=12)
ax.set_title('Day 15 Evening - Post-Light Equilibration & Evening Oscillation Pattern\n2025-11-22 15:00-21:49 UTC', fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)

# Add annotations for phases
ax.annotate('Post-light\nequilibration\n(3 phases)', xy=(datetime.fromisoformat("2025-11-22T18:00:00+00:00"), 1955),
            fontsize=10, ha='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax.annotate('Evening\noscillation\n(5 phases)', xy=(datetime.fromisoformat("2025-11-22T20:30:00+00:00"), 1968),
            fontsize=10, ha='center', bbox=dict(boxstyle='round', facecolor='plum', alpha=0.5))

plt.tight_layout()
plt.savefig('/home/gardener/workspace/day15_evening_analysis.png', dpi=150, bbox_inches='tight')
print("✓ Saved: day15_evening_analysis.png")

# Print summary statistics
print("\n" + "="*70)
print("DAY 15 EVENING ANALYSIS - SUMMARY")
print("="*70)

print(f"\nSession 8 (15:00-17:00 UTC):")
print(f"  Start: {moisture[0]}")
print(f"  End: {moisture[2]} (peak)")

print(f"\nPost-Light Equilibration (17:00-19:47 UTC):")
print(f"  Duration: ~167 minutes")
print(f"  Pattern: 3-phase oscillatory decay")
print(f"  Final baseline: {moisture[13]}")

print(f"\nEvening Oscillation (19:47-21:14 UTC):")
print(f"  Duration: 87 minutes")
print(f"  Baseline start: {moisture[13]}")
print(f"  Peak: {moisture[peak_idx]} (+{moisture[peak_idx] - moisture[13]} from baseline)")
print(f"  Trough: {moisture[trough_idx]} ({moisture[trough_idx] - moisture[peak_idx]} from peak)")
print(f"  Baseline restored: {moisture[baseline_restore_idx]}")
print(f"  Current (21:49): {moisture[-1]} (+{moisture[-1] - moisture[13]} from pre-event baseline)")

print(f"\nPhases:")
print(f"  1. Rise: 1962 → 1976 (+14) in 18min")
print(f"  2. Decline: 1976 → 1971 (-5) in 17min")
print(f"  3. Trough: 1971 → 1964 (-7) in 18min")
print(f"  4. Recovery: 1964 → 1973 (+9) in 17min")
print(f"  5. Restoration: 1973 → 1962 (-11) in 17min")

print(f"\nPlant Status:")
print(f"  Moisture range during event: {min(moisture[13:])} - {max(moisture[13:])}")
print(f"  All readings in Monitor range (1900-2000): ✓")
print(f"  Plant health: HEALTHY")
print(f"  Intervention needed: NONE")

print("\n" + "="*70)
