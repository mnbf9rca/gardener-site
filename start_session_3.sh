#!/bin/bash
# Wait until 01:58 UTC to start light session 3

echo "Waiting until 01:58 UTC to start session 3..."
current_time=$(date -u +%s)
target_time=$(date -u -d "2025-11-06 01:58:00" +%s)
wait_seconds=$((target_time - current_time))

if [ $wait_seconds -gt 0 ]; then
    echo "Sleeping for ${wait_seconds} seconds..."
    sleep $wait_seconds
fi

echo "Starting session 3 now at $(date -u)"
# The actual turn_on_light command will be executed from the main script
