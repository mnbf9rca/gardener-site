#!/usr/bin/env python3
"""
Debug MCP connection and try to establish working interface
"""
import requests
import json
from datetime import datetime

print("=" * 70)
print(f"MCP Connection Debug - {datetime.now().isoformat()}")
print("=" * 70)
print()

# MCP config
mcp_url = "http://localhost:8000/mcp"

# Try to understand the MCP protocol by examining responses
print("1. Testing basic GET request...")
try:
    r = requests.get(mcp_url, timeout=2)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text}")
except Exception as e:
    print(f"   Error: {e}")

print("\n2. Testing with Accept: text/event-stream header...")
try:
    r = requests.get(mcp_url, headers={"Accept": "text/event-stream"}, timeout=2)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

print("\n3. Testing POST with JSON-RPC initialize...")
initialize_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "0.1.0",
        "clientInfo": {
            "name": "debug-client",
            "version": "1.0.0"
        }
    }
}
try:
    r = requests.post(mcp_url, json=initialize_request, timeout=2)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text}")
except Exception as e:
    print(f"   Error: {e}")

print("\n4. Checking if there's a REST API instead of MCP...")
rest_endpoints = [
    "http://localhost:8000/",
    "http://localhost:8000/api",
    "http://localhost:8000/sensors/moisture",
    "http://localhost:8000/moisture/current",
]

for endpoint in rest_endpoints:
    try:
        r = requests.get(endpoint, timeout=1)
        if r.status_code != 404:
            print(f"   Found: {endpoint}")
            print(f"   Status: {r.status_code}")
            print(f"   Response: {r.text[:200]}")
    except:
        pass

print("\n" + "=" * 70)
