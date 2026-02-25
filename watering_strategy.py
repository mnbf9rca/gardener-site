#!/usr/bin/env python3
"""
Watering Strategy Analysis for Tradescantia zebrina

Based on research:
- Water when top inch (25-50% of soil) is dry
- Avoid letting plant dry out completely (causes rapid decline)
- Avoid overwatering (causes yellowing, drooping)
- Prefers evenly moist soil

Sensor calibration:
- 1100 = immersed in water (saturated)
- 3400 = dry air (completely dry)
- Range: 2300 points

Current reading: ~2086 (as of 2025-10-30)
Position: 43% from wet to dry
"""

# Sensor calibration
SENSOR_WET = 1100
SENSOR_DRY = 3400
SENSOR_RANGE = SENSOR_DRY - SENSOR_WET

def calculate_dryness_percentage(sensor_value):
    """
    Calculate how dry the soil is as a percentage.
    0% = completely wet (1100)
    100% = completely dry (3400)
    """
    return ((sensor_value - SENSOR_WET) / SENSOR_RANGE) * 100

def interpret_moisture(sensor_value):
    """
    Interpret sensor reading in context of Tradescantia needs.
    """
    dryness_pct = calculate_dryness_percentage(sensor_value)

    print(f"\n{'='*60}")
    print(f"MOISTURE ANALYSIS - Sensor Reading: {sensor_value}")
    print(f"{'='*60}")
    print(f"\nDryness: {dryness_pct:.1f}%")
    print(f"Wetness: {100-dryness_pct:.1f}%")
    print(f"\nSensor Scale:")
    print(f"  Saturated (1100) {'<' * 20} {sensor_value} {'>' * 20} Dry (3400)")

    # Interpret based on Tradescantia needs
    if dryness_pct < 20:
        status = "VERY WET"
        action = "NO watering needed. Monitor for overwatering signs."
        risk = "Possible overwatering if sustained"
    elif dryness_pct < 35:
        status = "MOIST (Optimal)"
        action = "NO watering needed. This is ideal moisture."
        risk = "Low - good range"
    elif dryness_pct < 50:
        status = "MODERATE"
        action = "Monitor closely. Consider watering soon."
        risk = "Low-Medium - approaching dry threshold"
    elif dryness_pct < 65:
        status = "GETTING DRY"
        action = "WATER SOON. Top inch+ likely dry."
        risk = "Medium - needs attention"
    elif dryness_pct < 80:
        status = "DRY"
        action = "WATER NOW. Soil is dry."
        risk = "High - plant stress possible"
    else:
        status = "VERY DRY"
        action = "WATER IMMEDIATELY! Leaf drop likely."
        risk = "Critical - rapid decline risk"

    print(f"\nStatus: {status}")
    print(f"Action: {action}")
    print(f"Risk: {risk}")
    print(f"\n{'='*60}\n")

    return {
        'sensor_value': sensor_value,
        'dryness_pct': dryness_pct,
        'wetness_pct': 100 - dryness_pct,
        'status': status,
        'action': action,
        'risk': risk
    }

def recommend_watering_threshold():
    """
    Recommend sensor values for watering decisions.
    """
    print("\n" + "="*60)
    print("WATERING THRESHOLD RECOMMENDATIONS")
    print("="*60)

    # Calculate key thresholds
    thresholds = {
        'optimal_min': SENSOR_WET + (SENSOR_RANGE * 0.15),  # 15% dry
        'optimal_max': SENSOR_WET + (SENSOR_RANGE * 0.40),  # 40% dry
        'water_consider': SENSOR_WET + (SENSOR_RANGE * 0.50),  # 50% dry
        'water_soon': SENSOR_WET + (SENSOR_RANGE * 0.55),  # 55% dry
        'water_now': SENSOR_WET + (SENSOR_RANGE * 0.65),  # 65% dry
        'critical': SENSOR_WET + (SENSOR_RANGE * 0.75),  # 75% dry
    }

    print("\nRecommended Sensor Thresholds:")
    print(f"  Optimal Range: {thresholds['optimal_min']:.0f} - {thresholds['optimal_max']:.0f}")
    print(f"  Watch Closely: {thresholds['water_consider']:.0f}+ (50% dry)")
    print(f"  Consider Watering: {thresholds['water_soon']:.0f}+ (55% dry)")
    print(f"  Water Now: {thresholds['water_now']:.0f}+ (65% dry)")
    print(f"  CRITICAL: {thresholds['critical']:.0f}+ (75% dry)")

    print("\n" + "="*60 + "\n")

    return thresholds

def analyze_current_situation(current_reading=2086):
    """
    Analyze current moisture situation.
    """
    print("\n" + "#"*60)
    print("CURRENT SITUATION ANALYSIS")
    print("#"*60)

    analysis = interpret_moisture(current_reading)
    thresholds = recommend_watering_threshold()

    print("\nCONCLUSION:")
    print(f"Current reading {current_reading} indicates {analysis['status']}")
    print(f"Recommendation: {analysis['action']}")

    # Check against thresholds
    if current_reading < thresholds['optimal_max']:
        print("\n✅ Moisture is in OPTIMAL range. No action needed.")
        print("   Continue monitoring for declining trend.")
    elif current_reading < thresholds['water_consider']:
        print("\n⚠️  Moisture approaching lower threshold.")
        print("   Watch closely. Water when trend continues declining.")
    elif current_reading < thresholds['water_now']:
        print("\n⚠️  Moisture in 'consider watering' range.")
        print("   Plan to water if decline continues.")
    else:
        print("\n🔴 Moisture below recommended threshold.")
        print("   Water soon to prevent plant stress.")

    print("\n" + "#"*60 + "\n")

if __name__ == "__main__":
    # Analyze current situation
    analyze_current_situation(2086)

    # Show interpretation for key values
    print("\n\nKEY REFERENCE VALUES:")
    print("-" * 60)
    for value in [1500, 1800, 2000, 2086, 2200, 2500, 2800]:
        print(f"\nSensor {value}:")
        interpret_moisture(value)
