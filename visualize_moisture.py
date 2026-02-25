#!/usr/bin/env python3
"""
Simple text-based visualization of moisture data trends.
"""

import sys
import json
from datetime import datetime

def text_chart(data, height=15, width=60):
    """
    Create a simple ASCII chart of the data.

    Args:
        data: List of [timestamp, value] pairs
        height: Chart height in characters
        width: Chart width in characters
    """
    if not data or len(data) < 2:
        print("Insufficient data for chart")
        return

    # Parse data
    points = []
    for timestamp_str, value in data:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        points.append((dt, value))

    points.sort(key=lambda x: x[0])

    # Get value range
    values = [v for _, v in points]
    min_val = min(values)
    max_val = max(values)
    value_range = max_val - min_val if max_val > min_val else 1

    # Get time range
    start_time = points[0][0]
    end_time = points[-1][0]
    time_range = (end_time - start_time).total_seconds()

    # Print header
    print(f"\nMoisture Trend: {start_time.date()} to {end_time.date()}")
    print(f"Range: {min_val} - {max_val} (span: {max_val - min_val})")
    print(f"Current: {values[-1]}\n")

    # Create chart
    # Y-axis: moisture values
    # X-axis: time

    chart = [[' ' for _ in range(width)] for _ in range(height)]

    # Plot points
    for dt, value in points:
        # Normalize to chart dimensions
        x = int((dt - start_time).total_seconds() / time_range * (width - 1))
        y = height - 1 - int((value - min_val) / value_range * (height - 1))

        if 0 <= x < width and 0 <= y < height:
            chart[y][x] = '*'

    # Print chart
    print(f"{max_val:4.0f} ┤", end='')
    for col in chart[0]:
        print(col, end='')
    print()

    for i in range(1, height - 1):
        print("     │", end='')
        for col in chart[i]:
            print(col, end='')
        print()

    print(f"{min_val:4.0f} ┤", end='')
    for col in chart[-1]:
        print(col, end='')
    print()
    print("     └" + "─" * width)
    print(f"     {start_time.strftime('%m-%d')}{'':>{width-10}}{end_time.strftime('%m-%d')}")

    # Daily summary
    print("\n=== Daily Averages ===")
    current_day = None
    day_values = []
    day_summaries = []

    for dt, value in points:
        day = dt.date()
        if current_day is None:
            current_day = day

        if day != current_day:
            if day_values:
                avg = sum(day_values) / len(day_values)
                day_summaries.append((current_day, avg, min(day_values), max(day_values)))
            current_day = day
            day_values = []

        day_values.append(value)

    # Last day
    if day_values:
        avg = sum(day_values) / len(day_values)
        day_summaries.append((current_day, avg, min(day_values), max(day_values)))

    # Print summaries
    for day, avg, min_v, max_v in day_summaries:
        trend = ""
        if len(day_summaries) > 1:
            idx = day_summaries.index((day, avg, min_v, max_v))
            if idx > 0:
                prev_avg = day_summaries[idx - 1][1]
                diff = avg - prev_avg
                if diff > 5:
                    trend = " ▲"
                elif diff < -5:
                    trend = " ▼"
                else:
                    trend = " →"

        print(f"{day}: avg={avg:5.0f} (range {min_v:4.0f}-{max_v:4.0f}){trend}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    text_chart(data)
