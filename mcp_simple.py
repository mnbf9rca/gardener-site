#!/usr/bin/env python3
"""
Simplified MCP client with proper session handling
"""
import requests
import json
import uuid
from datetime import datetime

print(f"=== Simple MCP Client - {datetime.now().isoformat()} ===\n")

BASE_URL = "http://localhost:8000"
session_id = str(uuid.uuid4())

def call_mcp(method, params=None):
    """Call MCP with proper session management"""
    url = f"{BASE_URL}/mcp"

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }

    # Add session ID as query param for subsequent requests
    if method != "initialize":
        url = f"{url}?session_id={session_id}"

    request_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }

    try:
        resp = requests.post(url, json=request_data, headers=headers, timeout=5, stream=True)

        # Parse SSE response
        for line in resp.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = json.loads(line[6:])
                    return data
        return None
    except Exception as e:
        print(f"Error calling {method}: {e}")
        return None

# Initialize
print("1. Initialize...")
init_resp = call_mcp("initialize", {
    "protocolVersion": "2024-11-05",
    "clientInfo": {"name": "simple-client", "version": "1.0"},
    "capabilities": {}
})
if init_resp:
    print(f"✓ Server: {init_resp.get('result', {}).get('serverInfo', {}).get('name')}")
    print(f"✓ Version: {init_resp.get('result', {}).get('serverInfo', {}).get('version')}\n")

# List tools
print("2. List tools...")
tools_resp = call_mcp("tools/list")
if tools_resp and 'result' in tools_resp:
    tools = tools_resp['result'].get('tools', [])
    print(f"✓ Found {len(tools)} tools:")
    for tool in tools[:10]:
        print(f"  - {tool['name']}")
    if len(tools) > 10:
        print(f"  ... and {len(tools) - 10} more\n")
else:
    print(f"✗ Failed: {tools_resp}\n")

# Get moisture
print("3. Read moisture sensor...")
moisture_resp = call_mcp("tools/call", {
    "name": "read_moisture",
    "arguments": {}
})
if moisture_resp and 'result' in moisture_resp:
    content = moisture_resp['result'].get('content', [])
    if content:
        print(f"✓ Moisture: {content[0].get('text', 'N/A')}\n")
else:
    print(f"✗ Failed: {moisture_resp}\n")

# Get current time
print("4. Get current time...")
time_resp = call_mcp("tools/call", {
    "name": "get_current_time",
    "arguments": {}
})
if time_resp and 'result' in time_resp:
    content = time_resp['result'].get('content', [])
    if content:
        print(f"✓ Time: {content[0].get('text', 'N/A')}\n")
else:
    print(f"✗ Failed: {time_resp}\n")

# Get light status
print("5. Get light status...")
light_resp = call_mcp("tools/call", {
    "name": "get_light_status",
    "arguments": {}
})
if light_resp and 'result' in light_resp:
    content = light_resp['result'].get('content', [])
    if content:
        print(f"✓ Light: {content[0].get('text', 'N/A')}\n")
else:
    print(f"✗ Failed: {light_resp}\n")

print("=== Done ===")
