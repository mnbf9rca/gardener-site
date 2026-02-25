#!/usr/bin/env python3
"""
Autonomous Plant Care - Data Analysis & Monitoring
Provides tools for analyzing plant sensor data and making care decisions
"""

from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional
import json

class MoistureTrendAnalyzer:
    """Analyze moisture sensor trends and predict watering needs"""
    
    def __init__(self, wet_reference=1100, dry_reference=3400):
        self.wet_ref = wet_reference
        self.dry_ref = dry_reference
        self.watering_threshold = 2200
        
    def to_percentage(self, value: int) -> float:
        """Convert raw sensor to moisture percentage (100% = wet, 0% = dry)"""
        if value <= self.wet_ref:
            return 100.0
        if value >= self.dry_ref:
            return 0.0
        # Invert: higher sensor value = drier soil
        pct = 100 * (1 - (value - self.wet_ref) / (self.dry_ref - self.wet_ref))
        return round(pct, 1)
    
    def analyze_trend(self, readings: List[Tuple[str, int]]) -> Dict:
        """
        Analyze moisture trend from time-series readings
        
        Args:
            readings: List of (timestamp, value) pairs
            
        Returns:
            Dictionary with trend analysis
        """
        if len(readings) < 2:
            return {"status": "insufficient_data", "readings_count": len(readings)}
        
        # Extract values and calculate statistics
        values = [r[1] for r in readings]
        timestamps = [r[0] for r in readings]
        
        first_val = values[0]
        last_val = values[-1]
        total_change = last_val - first_val
        avg_value = sum(values) / len(values)
        
        # Calculate variance to detect stability
        variance = sum((v - avg_value) ** 2 for v in values) / len(values)
        std_dev = variance ** 0.5
        
        # Determine trend
        if std_dev < 10 and abs(total_change) < 20:
            trend_type = "stable"
        elif total_change > 20:
            trend_type = "drying"
        elif total_change < -20:
            trend_type = "moistening"
        else:
            trend_type = "fluctuating"
        
        # Calculate rate (points per hour)
        try:
            time_diff = self._time_diff_hours(timestamps[0], timestamps[-1])
            rate_per_hour = total_change / time_diff if time_diff > 0 else 0
        except:
            rate_per_hour = 0
        
        # Predict watering time
        prediction = None
        if trend_type == "drying" and rate_per_hour > 0 and last_val < self.watering_threshold:
            hours_until_threshold = (self.watering_threshold - last_val) / rate_per_hour
            prediction = {
                "hours_until_watering": round(hours_until_threshold, 1),
                "projected_threshold_reach": self._add_hours(timestamps[-1], hours_until_threshold)
            }
        
        return {
            "status": "analyzed",
            "trend_type": trend_type,
            "readings_count": len(readings),
            "first_value": first_val,
            "last_value": last_val,
            "total_change": total_change,
            "average": round(avg_value, 1),
            "std_deviation": round(std_dev, 1),
            "rate_per_hour": round(rate_per_hour, 2),
            "current_moisture_pct": self.to_percentage(last_val),
            "stability_score": "high" if std_dev < 10 else "medium" if std_dev < 30 else "low",
            "prediction": prediction
        }
    
    def watering_recommendation(self, current_value: int, trend_rate: float) -> Dict:
        """Generate watering recommendation"""
        pct = self.to_percentage(current_value)
        
        if current_value >= 2400:
            action = "WATER_NOW"
            reason = "Soil is dry"
            urgency = "high"
        elif current_value >= 2200:
            action = "WATER_SOON"
            reason = "Soil getting dry"
            urgency = "medium"
        elif current_value >= 1900:
            if trend_rate > 40:
                action = "MONITOR_CLOSELY"
                reason = "Drying quickly"
                urgency = "low"
            else:
                action = "NO_ACTION"
                reason = "Moisture optimal"
                urgency = "none"
        elif current_value >= 1500:
            action = "NO_ACTION"
            reason = "Well hydrated"
            urgency = "none"
        else:
            action = "CHECK_DRAINAGE"
            reason = "May be too wet"
            urgency = "medium"
        
        return {
            "action": action,
            "reason": reason,
            "urgency": urgency,
            "moisture_percentage": pct,
            "raw_value": current_value,
            "suggested_amount_ml": 10 if action == "WATER_NOW" else 15 if action == "WATER_SOON" else 0
        }
    
    def _time_diff_hours(self, ts1: str, ts2: str) -> float:
        """Calculate time difference in hours between two ISO timestamps"""
        try:
            t1 = datetime.fromisoformat(ts1.replace('Z', '+00:00'))
            t2 = datetime.fromisoformat(ts2.replace('Z', '+00:00'))
            return abs((t2 - t1).total_seconds() / 3600)
        except:
            return 0
    
    def _add_hours(self, timestamp: str, hours: float) -> str:
        """Add hours to timestamp"""
        try:
            t = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            new_t = t + timedelta(hours=hours)
            return new_t.isoformat()
        except:
            return timestamp


class LightScheduler:
    """Calculate optimal lighting schedules"""
    
    def __init__(self, daily_target_hours=7):
        self.daily_target = daily_target_hours
        self.session_min = 30
        self.session_max = 120
        
    def calculate_remaining_light(self, current_minutes: int) -> Dict:
        """Calculate how much more light is needed today"""
        target_minutes = self.daily_target * 60
        remaining = target_minutes - current_minutes
        
        if remaining <= 0:
            return {
                "status": "target_met",
                "remaining_minutes": 0,
                "sessions_needed": 0,
                "suggestion": "Daily target achieved"
            }
        
        # Suggest session schedule
        if remaining <= self.session_max:
            sessions = [remaining]
        else:
            # Split into multiple sessions
            num_sessions = (remaining + self.session_max - 1) // self.session_max
            session_length = remaining // num_sessions
            sessions = [session_length] * num_sessions
        
        return {
            "status": "needs_more_light",
            "remaining_minutes": remaining,
            "sessions_needed": len(sessions),
            "suggested_sessions": sessions,
            "suggestion": f"Provide {len(sessions)} session(s) of {sessions[0]}min each"
        }


class PlantHealthScorer:
    """Score overall plant health based on multiple factors"""
    
    def calculate_health_score(self, 
                               moisture_stable: bool,
                               moisture_in_range: bool,
                               light_adequate: bool,
                               visual_healthy: bool = True) -> Dict:
        """Calculate overall health score"""
        
        score = 0
        factors = []
        
        if moisture_stable:
            score += 25
            factors.append("Stable moisture")
        else:
            factors.append("⚠️ Unstable moisture")
        
        if moisture_in_range:
            score += 25
            factors.append("Optimal moisture level")
        else:
            factors.append("⚠️ Moisture out of range")
        
        if light_adequate:
            score += 25
            factors.append("Adequate light")
        else:
            factors.append("⚠️ Insufficient light")
        
        if visual_healthy:
            score += 25
            factors.append("Healthy appearance")
        else:
            factors.append("⚠️ Visual concerns")
        
        if score >= 90:
            status = "excellent"
        elif score >= 70:
            status = "good"
        elif score >= 50:
            status = "fair"
        else:
            status = "concerning"
        
        return {
            "score": score,
            "status": status,
            "factors": factors
        }


def demo_analysis():
    """Demonstrate analysis capabilities"""
    print("=" * 60)
    print("PLANT MONITORING SYSTEM - Analysis Demo")
    print("=" * 60)
    
    # Sample data from current monitoring
    readings = [
        ["2025-10-22T22:23:51Z", 1829],
        ["2025-10-22T22:36:16Z", 1835],
        ["2025-10-22T22:49:04Z", 1847],
        ["2025-10-22T23:00:49Z", 1844]
    ]
    
    analyzer = MoistureTrendAnalyzer()
    
    print("\n📊 MOISTURE TREND ANALYSIS")
    print("-" * 60)
    result = analyzer.analyze_trend(readings)
    print(f"Status: {result['status']}")
    print(f"Trend: {result['trend_type'].upper()}")
    print(f"Readings: {result['first_value']} → {result['last_value']} ({result['total_change']:+d} points)")
    print(f"Average: {result['average']}")
    print(f"Std Dev: {result['std_deviation']} (Stability: {result['stability_score']})")
    print(f"Rate: {result['rate_per_hour']} points/hour")
    print(f"Current Moisture: {result['current_moisture_pct']}%")
    
    if result['prediction']:
        print(f"\n🔮 Prediction: Watering needed in {result['prediction']['hours_until_watering']} hours")
    
    print("\n💧 WATERING RECOMMENDATION")
    print("-" * 60)
    rec = analyzer.watering_recommendation(readings[-1][1], result['rate_per_hour'])
    print(f"Action: {rec['action']}")
    print(f"Reason: {rec['reason']}")
    print(f"Urgency: {rec['urgency']}")
    print(f"Current: {rec['raw_value']} ({rec['moisture_percentage']}% moisture)")
    if rec['suggested_amount_ml'] > 0:
        print(f"Suggested amount: {rec['suggested_amount_ml']}ml")
    
    print("\n💡 LIGHT SCHEDULE")
    print("-" * 60)
    scheduler = LightScheduler(daily_target_hours=7)
    light_plan = scheduler.calculate_remaining_light(current_minutes=60)
    print(f"Status: {light_plan['status']}")
    print(f"Remaining needed: {light_plan['remaining_minutes']} minutes")
    print(f"Suggestion: {light_plan['suggestion']}")
    
    print("\n🌱 HEALTH SCORE")
    print("-" * 60)
    scorer = PlantHealthScorer()
    health = scorer.calculate_health_score(
        moisture_stable=True,
        moisture_in_range=True,
        light_adequate=False,  # Only 1h of 7h target
        visual_healthy=True
    )
    print(f"Score: {health['score']}/100 ({health['status'].upper()})")
    print("Factors:")
    for factor in health['factors']:
        print(f"  • {factor}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo_analysis()
