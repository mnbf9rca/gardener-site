#!/usr/bin/env python3
"""
Quick plant status check - work around MCP access issues
Try multiple methods to get current plant data
"""
import requests
import json
from datetime import datetime

print("=" * 70)
print(f"Plant Status Check - {datetime.now().isoformat()}")
print("=" * 70)
print()

# Try different endpoint patterns
endpoints = [
    "http://localhost:8000/api/moisture",
    "http://localhost:8000/api/status",
    "http://localhost:8000/moisture",
    "http://localhost:8000/status",
    "http://localhost:8000/health",
]

print("Trying to reach MCP server endpoints...")
print("-" * 70)

for endpoint in endpoints:
    try:
        r = requests.get(endpoint, timeout=2)
        print(f"✓ {endpoint}")
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  Data: {json.dumps(data, indent=2)}")
            except:
                print(f"  Response: {r.text[:200]}")
        else:
            print(f"  Response: {r.text[:100]}")
    except Exception as e:
        print(f"✗ {endpoint}")
        print(f"  Error: {e}")
    print()

print("=" * 70)
