# MCP Tools Troubleshooting - Cycle 4

## Problem Summary
The MCP plant-tools functions listed in the Claude preamble are not available when invoked, despite:
- MCP server running (PID 3014)
- Configuration file present at `~/.mcp.json`
- Claude started with `--mcp-config /home/gardener/.mcp.json` flag
- Server responding to HTTP requests (returning proper error codes)

## Expected Tools (from preamble)
All of these should be available but return "No such tool available":
- `mcp__plant-tools__read_moisture`
- `mcp__plant-tools__get_current_time`
- `mcp__plant-tools__get_light_status`
- `mcp__plant-tools__get_light_history`
- `mcp__plant-tools__turn_on_light`
- `mcp__plant-tools__turn_off_light`
- `mcp__plant-tools__dispense_water`
- `mcp__plant-tools__capture_photo`
- `mcp__plant-tools__list_messages_from_human`
- `mcp__plant-tools__log_thought`
- `mcp__plant-tools__log_action`
- ...and more

## MCP Configuration
```json
{
  "mcpServers": {
    "plant-tools": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## MCP Server Status
- **Running:** Yes (PID 3014)
- **Endpoint:** http://localhost:8000/mcp
- **Protocol:** SSE (Server-Sent Events) with JSON-RPC
- **Requirements:**
  - Accept headers: `application/json` AND `text/event-stream`
  - Session ID required for requests
  - Proper SSE handshake needed

## Debug Findings

### HTTP Tests
1. **GET /mcp** → 406: Requires SSE headers
2. **GET /mcp (with SSE header)** → 400: Missing session ID
3. **POST /mcp (JSON-RPC initialize)** → 406: Requires both content types
4. **Other endpoints** → 404: No REST API available

### Conclusion
The MCP server is working correctly but requires proper SSE protocol handling. The Claude client should handle this automatically via the `--mcp-config` flag, but the tools are not being exposed in this session.

## Hypotheses

### 1. Session Initialization Failure
The Claude client may have failed to establish an MCP session during startup, causing tools to not be registered.

### 2. Tool Discovery Issue
The tools may have been discovered but not properly registered in the available tools list.

### 3. Naming Convention Mismatch
The expected tool names (`mcp__plant-tools__*`) may not match the actual names exposed by the server.

### 4. Previous Session Issue
This same problem occurred in the previous session (Cycle 3, ~08:31 UTC), suggesting it may be systemic rather than transient.

## Workarounds Used

Since MCP tools are unavailable, I'm operating with:
1. **Historical data analysis** - Using last known sensor readings
2. **Mathematical projections** - Calculating expected current state
3. **Conservative decision-making** - Large safety margins
4. **Existing Python tools** - Analysis scripts for pattern recognition

## Impact on Plant Care

### Limited but Manageable
- ✅ Can still make informed decisions using projections
- ✅ Plant has large safety margins (7+ hours to threshold)
- ✅ Historical patterns well-documented
- ❌ Cannot verify actual current state
- ❌ Cannot take action (water/light) even if needed
- ❌ Cannot capture photos for visual assessment

### Current Safety Status
Based on mathematical projection:
- **Projected moisture:** ~2167 (at 08:49 UTC)
- **Threshold:** 2400 (water needed)
- **Safety margin:** 233 points
- **Time to threshold:** 7+ hours
- **Risk level:** LOW ✅

## Recommendations for Next Session

### Immediate Checks
1. Verify if tools become available in fresh session
2. Check Claude startup logs for MCP connection errors
3. Validate session was established successfully

### If Issue Persists
1. Check MCP server logs at `/home/mcpserver/plant-care-app/`
2. Verify network connectivity to localhost:8000
3. Test MCP connection with minimal client
4. Consider restarting MCP server
5. May require human intervention

### Alternative Approaches
1. **Direct sensor access** - If GPIO permissions allow
2. **Database read access** - If SQLite file permissions can be adjusted
3. **Log file monitoring** - If MCP server logs sensor data
4. **REST API** - If server can be configured to expose one

## Files Generated
- `check_plant_status.py` - HTTP endpoint testing
- `get_sensor_data.py` - Direct Python module import attempts
- `mcp_debug.py` - MCP protocol debugging
- `MCP_TROUBLESHOOTING.md` - This document

## Status
**Plant is SAFE** despite tool unavailability. The robust monitoring in previous cycles and mathematical modeling allows for continued safe operation for several hours. However, **tool access should be restored** to enable:
- Real-time verification
- Active intervention if needed
- Photo-based health assessment
- Long-term reliable care

---
*Created: 08:51 UTC, Nov 3, 2025*
*Impact: Medium (can operate short-term, needs resolution)*
*Priority: High (restore before intervention needed)*
