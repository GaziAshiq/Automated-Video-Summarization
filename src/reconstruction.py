"""
Module for reconstructing a summarized video from selected keyframes.
"""

import cv2
import os


def reconstruct_video(keyframe_dir, output_video, fps=1):
    """
    Reconstructs a summarized video from selected keyframes.

    Args:
        keyframe_dir (str): Directory containing the selected keyframes.
        output_video (str): Path to save the output summarized video.
        fps (int): Frames per second for the output video.

    Returns:
        None
    """
    # Get the list of keyframe files
    keyframe_files = sorted(
        [os.path.join(keyframe_dir, f) for f in os.listdir(keyframe_dir) if f.endswith(".jpg")]
    )

    if not keyframe_files:
        print("No keyframes found in the directory.")
        return

    # Read the first frame to get video properties
    first_frame = cv2.imread(keyframe_files[0])
    height, width, _ = first_frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Write each keyframe to the video
    for frame_file in keyframe_files:
        frame = cv2.imread(frame_file)
        video_writer.write(frame)

    video_writer.release()
    print(f"Summarized video saved to {output_video}")


if __name__ == "__main__":
    SUMMARY_KEYFRAME_DIR = "data/summaries/"
    OUTPUT_VIDEO_PATH = "data/summaries/summarized_video.mp4"
    FPS = 1  # One frame per second

    reconstruct_video(SUMMARY_KEYFRAME_DIR, OUTPUT_VIDEO_PATH, FPS)
