#!/usr/bin/env python3
"""
Light detection script - determines if grow light is ON or OFF from photo.

Key insight from human feedback:
- Light ON: Plant is visible, bright, clear image, larger file size (150-230KB)
- Light OFF: Pitch black, cannot see plant, small file size (<50KB)

This addresses the recurring issue where the agent forgets how to distinguish
light states every 5-10 days.
"""

import sys
import os
import requests
from pathlib import Path

def detect_light_state(photo_url_or_path):
    """
    Detect if grow light is ON or OFF from a photo.

    Args:
        photo_url_or_path: URL or file path to photo

    Returns:
        tuple: (state, confidence, file_size, reasoning)
        state: "ON" or "OFF"
        confidence: 0-100
        file_size: size in bytes
        reasoning: explanation
    """
    # Get file size
    if photo_url_or_path.startswith('http'):
        # Download to get size
        response = requests.get(photo_url_or_path)
        file_size = len(response.content)
        photo_path = '/tmp/temp_photo.jpg'
        with open(photo_path, 'wb') as f:
            f.write(response.content)
    else:
        photo_path = photo_url_or_path
        file_size = os.path.getsize(photo_path)

    # Size-based detection (primary heuristic)
    # Based on observations:
    # - Light ON: 150-230KB (high detail, visible plant)
    # - Light OFF: <50KB (mostly black pixels compress well)

    if file_size < 50000:  # Less than 50KB
        return ("OFF", 95, file_size,
                f"File size {file_size/1024:.1f}KB indicates dark image (light OFF)")
    elif file_size > 100000:  # Greater than 100KB
        return ("ON", 95, file_size,
                f"File size {file_size/1024:.1f}KB indicates illuminated image (light ON)")
    else:  # 50-100KB - ambiguous
        return ("UNKNOWN", 50, file_size,
                f"File size {file_size/1024:.1f}KB is ambiguous - needs visual inspection")


def main():
    if len(sys.argv) < 2:
        print("Usage: light_detector.py <photo_url_or_path>")
        sys.exit(1)

    photo = sys.argv[1]
    state, confidence, size, reasoning = detect_light_state(photo)

    print(f"Light State: {state}")
    print(f"Confidence: {confidence}%")
    print(f"File Size: {size/1024:.1f}KB")
    print(f"Reasoning: {reasoning}")

    # Return exit code: 0 for ON, 1 for OFF, 2 for unknown
    if state == "ON":
        sys.exit(0)
    elif state == "OFF":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
