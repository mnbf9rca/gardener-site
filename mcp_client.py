#!/usr/bin/env python3
"""
Direct MCP client to get sensor data via SSE protocol
"""
import requests
import json
import uuid
from datetime import datetime

print(f"=== MCP Direct Client - {datetime.now().isoformat()} ===\n")

mcp_url = "http://localhost:8000/mcp"
session_id = str(uuid.uuid4())

# Headers required for SSE + JSON-RPC
headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream, application/json",
    "X-Session-ID": session_id
}

def parse_sse_response(text):
    """Parse SSE formatted response"""
    lines = text.strip().split('\n')
    data_lines = [l.replace('data: ', '') for l in lines if l.startswith('data: ')]
    if data_lines:
        return json.loads(data_lines[0])
    return None

def send_request(method, params=None):
    """Send JSON-RPC request to MCP server"""
    request = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": method,
        "params": params or {}
    }

    try:
        response = requests.post(
            mcp_url,
            json=request,
            headers=headers,
            timeout=5
        )
        print(f"Method: {method}")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            parsed = parse_sse_response(response.text)
            if parsed:
                print(f"Parsed response: {json.dumps(parsed, indent=2)[:300]}\n")
                return parsed
            else:
                print(f"Raw response: {response.text[:500]}\n")
        else:
            print(f"Response: {response.text[:300]}\n")
        return None
    except Exception as e:
        print(f"Error: {e}\n")
        return None

# Try to initialize session
print("1. Initializing MCP session...")
result = send_request("initialize", {
    "protocolVersion": "2024-11-05",
    "clientInfo": {
        "name": "direct-python-client",
        "version": "1.0"
    },
    "capabilities": {}
})

# Try to list available tools
print("2. Listing available tools...")
result = send_request("tools/list")

# Try to call read_moisture directly
print("3. Attempting to read moisture sensor...")
result = send_request("tools/call", {
    "name": "read_moisture",
    "arguments": {}
})

print("=== End ===")
