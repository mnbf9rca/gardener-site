#!/usr/bin/env python3
"""
Moisture trend analysis for plant care monitoring.
Helps detect when self-watering pot reservoir needs refilling.
"""

import sys
import json
from datetime import datetime, timedelta

def analyze_moisture_trend(history_data):
    """
    Analyze moisture sensor readings to detect trends.

    Args:
        history_data: List of [timestamp, value] pairs

    Returns:
        dict with trend analysis
    """
    if not history_data or len(history_data) < 2:
        return {"error": "Insufficient data for trend analysis"}

    # Convert to list if needed
    readings = []
    for item in history_data:
        timestamp_str = item[0]
        value = item[1]
        # Parse timestamp
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        readings.append((dt, value))

    # Sort by timestamp
    readings.sort(key=lambda x: x[0])

    # Calculate basic statistics
    values = [v for _, v in readings]
    min_val = min(values)
    max_val = max(values)
    avg_val = sum(values) / len(values)
    current_val = values[-1]

    # Calculate trend over last N readings
    def calculate_trend(data_points):
        """Simple linear trend calculation"""
        if len(data_points) < 2:
            return 0

        n = len(data_points)
        x = list(range(n))
        y = data_points

        # Linear regression: y = mx + b
        x_mean = sum(x) / n
        y_mean = sum(y) / n

        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0

        slope = numerator / denominator
        return slope

    # Trend over all data
    overall_trend = calculate_trend(values)

    # Trend over last 24 hours (if we have that much data)
    now = readings[-1][0]
    day_ago = now - timedelta(hours=24)
    recent_readings = [(dt, v) for dt, v in readings if dt >= day_ago]
    recent_values = [v for _, v in recent_readings]
    recent_trend = calculate_trend(recent_values) if len(recent_values) >= 2 else overall_trend

    # Determine trend direction
    def trend_direction(slope, threshold=1.0):
        if abs(slope) < threshold:
            return "stable"
        elif slope > 0:
            return "rising"
        else:
            return "declining"

    overall_direction = trend_direction(overall_trend)
    recent_direction = trend_direction(recent_trend)

    # Assess reservoir status
    CRITICAL_THRESHOLD = 1800
    WARNING_THRESHOLD = 1900
    OPTIMAL_THRESHOLD = 2000

    if current_val < CRITICAL_THRESHOLD:
        reservoir_status = "critical - refill now"
        action_needed = True
    elif current_val < WARNING_THRESHOLD and recent_direction == "declining":
        reservoir_status = "warning - declining toward critical"
        action_needed = True
    elif current_val < OPTIMAL_THRESHOLD and recent_direction == "declining":
        reservoir_status = "low - monitor closely"
        action_needed = False
    else:
        reservoir_status = "good - no action needed"
        action_needed = False

    return {
        "current_moisture": current_val,
        "min_moisture": min_val,
        "max_moisture": max_val,
        "avg_moisture": round(avg_val, 1),
        "overall_trend_slope": round(overall_trend, 2),
        "overall_trend_direction": overall_direction,
        "recent_trend_slope": round(recent_trend, 2),
        "recent_trend_direction": recent_direction,
        "reservoir_status": reservoir_status,
        "action_needed": action_needed,
        "data_points": len(readings),
        "time_span_hours": (readings[-1][0] - readings[0][0]).total_seconds() / 3600
    }


if __name__ == "__main__":
    # Read JSON data from stdin
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        # Read from stdin
        data = json.load(sys.stdin)

    # Analyze the data
    result = analyze_moisture_trend(data)

    # Pretty print results
    print(json.dumps(result, indent=2))
