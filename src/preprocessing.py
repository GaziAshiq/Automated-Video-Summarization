"""
This module handles video preprocessing by extracting frames from input videos
at specified intervals. It is part of the Automated Video Summarization project.
"""

# pylint: disable=E1101

import os
import cv2


def extract_frames(video_path, output_dir, frame_rate=1):
    """
    Extracts frames from a video at the specified frame rate.

    Parameters:
        video_path (str): Path to the input video.
        output_dir (str): Directory to save the extracted frames.
        frame_rate (int): Extract one frame every 'frame_rate' seconds.

    Returns:
        None
    """
    # Check if output directory exists, create if not
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return

    # Get video properties
    video_fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = video_fps * frame_rate
    frame_count = 0
    saved_frame_count = 0

    print(f"Extracting frames from {video_path}...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Save frame if it matches the interval
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(
                output_dir, f"frame_{saved_frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1

        frame_count += 1

    cap.release()
    print(f"Frames saved in {output_dir}. Total frames: {saved_frame_count}")


# Main execution
if __name__ == "__main__":
    INPUT_VIDEO = "data/input_videos/sample.mp4"  # Replace with your video path
    OUTPUT_DIR = "data/frames/"
    extract_frames(INPUT_VIDEO, OUTPUT_DIR, frame_rate=1)
