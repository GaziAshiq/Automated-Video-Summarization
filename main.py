"""
Main script to automate the entire video summarization pipeline.
"""

"""
Main script to automate the entire video summarization pipeline.
"""

import argparse
import os
import numpy as np  # Import NumPy for saving features
from src.preprocessing import extract_frames
from src.keyframe_detection import detect_keyframes
from src.feature_extraction import extract_features
from src.summarization import summarize_keyframes
from src.reconstruction import reconstruct_video



def main(input_video, output_dir, frame_rate=1, n_clusters=5, fps=1):
    """
    Automates the video summarization pipeline.

    Args:
        input_video (str): Path to the input video file.
        output_dir (str): Directory to save intermediate and final results.
        frame_rate (int): Frame extraction rate in seconds.
        n_clusters (int): Number of clusters for keyframe summarization.
        fps (int): Frames per second for the output summarized video.
    """
    # Ensure output directories exist
    frames_dir = os.path.join(output_dir, "frames")
    summaries_dir = os.path.join(output_dir, "summaries")
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(summaries_dir, exist_ok=True)

    # Step 1: Extract frames from the input video
    print("\nStep 1: Extracting frames...")
    extract_frames(input_video, frames_dir, frame_rate)

    # Step 2: Detect keyframes
    print("\nStep 2: Detecting keyframes...")
    keyframe_files = detect_keyframes(frames_dir, threshold=0.5)

    # Step 3: Extract features from keyframes
    print("\nStep 3: Extracting features...")
    features_file = os.path.join(output_dir, "features.npy")
    features = extract_features(keyframe_files)
    np.save(features_file, features)

    # Step 4: Summarize keyframes using clustering
    print("\nStep 4: Summarizing keyframes...")
    summary_keyframes = summarize_keyframes(features_file, summaries_dir, n_clusters)

    # Step 5: Reconstruct the summarized video
    print("\nStep 5: Reconstructing summarized video...")
    output_video = os.path.join(output_dir, "summarized_video.mp4")
    reconstruct_video(summaries_dir, output_video, fps)

    print("\nPipeline completed successfully!")
    print(f"Summarized video saved to: {output_video}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Video Summarization")
    parser.add_argument("--input_video", type=str, required=True, help="Path to the input video file")
    parser.add_argument("--output_dir", type=str, default="data", help="Directory to save results")
    parser.add_argument("--frame_rate", type=int, default=1, help="Frame extraction rate in seconds")
    parser.add_argument("--n_clusters", type=int, default=5, help="Number of clusters for summarization")
    parser.add_argument("--fps", type=int, default=1, help="Frames per second for the output summarized video")

    args = parser.parse_args()
    main(
        input_video=args.input_video,
        output_dir=args.output_dir,
        frame_rate=args.frame_rate,
        n_clusters=args.n_clusters,
        fps=args.fps,
    )
