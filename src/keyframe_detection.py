"""
Module for detecting keyframes in a video using histogram differences.
"""

import cv2
import os
import numpy as np


def detect_keyframes(frame_dir, threshold=0.5):
    """
    Detects keyframes in a sequence of frames based on histogram differences.

    Args:
        frame_dir (str): Directory containing the extracted frames.
        threshold (float): Threshold for histogram difference to detect keyframes.

    Returns:
        list: List of keyframe filenames.
    """
    frame_files = sorted(
        [os.path.join(frame_dir, f) for f in os.listdir(frame_dir) if f.endswith(".jpg")]
    )
    keyframes = []

    if len(frame_files) < 2:
        print("Not enough frames to detect keyframes.")
        return keyframes

    prev_hist = None

    for i, frame_file in enumerate(frame_files):
        # Read the frame
        frame = cv2.imread(frame_file, cv2.IMREAD_GRAYSCALE)

        # Calculate histogram
        hist = cv2.calcHist([frame], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        if prev_hist is not None:
            # Calculate histogram difference
            diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
            if diff < threshold:
                keyframes.append(frame_file)

        # Update previous histogram
        prev_hist = hist

    print(f"Detected {len(keyframes)} keyframes.")
    return keyframes


if __name__ == "__main__":
    FRAME_DIR = "data/frames/"  # Directory where frames are stored
    KEYFRAME_THRESHOLD = 0.5  # Adjust the threshold as needed
    keyframes = detect_keyframes(FRAME_DIR, KEYFRAME_THRESHOLD)
    print(f"Keyframes: {keyframes}")
