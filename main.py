"""
Main script for the Automated Video Summarization pipeline.
"""

import argparse
import os
from src.youtube_downloader import download_youtube_video
from src.preprocessing import extract_frames


def main(youtube_url=None, input_video=None, output_dir="data/frames/", frame_rate=1, cookies_file=None):
    """
    Main pipeline for processing YouTube or local videos.

    Args:
        youtube_url (str): URL of the YouTube video to process.
        input_video (str): Path to a local video file.
        output_dir (str): Directory to save the extracted frames.
        frame_rate (int): Frame extraction rate in seconds.
        cookies_file (str): Path to cookies file for YouTube authentication.
    """
    os.makedirs(output_dir, exist_ok=True)

    if youtube_url:
        # Download YouTube video
        print("Processing YouTube video...")
        input_video = download_youtube_video(
            youtube_url, "data/input_videos/", cookies_file)
        if input_video is None:
            print("Failed to download YouTube video. Exiting.")
            return

    if not input_video:
        print("Error: No input video provided.")
        return

    # Extract frames
    print("Extracting frames from video...")
    extract_frames(input_video, output_dir, frame_rate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automated Video Summarization")
    parser.add_argument("--youtube_url", type=str,
                        help="URL of the YouTube video to process")
    parser.add_argument("--input_video", type=str,
                        help="Path to a local video file")
    parser.add_argument("--output_dir", type=str, default="data/frames/",
                        help="Directory to save extracted frames")
    parser.add_argument("--frame_rate", type=int, default=1,
                        help="Frame extraction rate in seconds")
    parser.add_argument("--cookies_file", type=str,
                        default="data/cookies/cookies.txt", help="Path to YouTube cookies file")

    args = parser.parse_args()
    main(
        youtube_url=args.youtube_url,
        input_video=args.input_video,
        output_dir=args.output_dir,
        frame_rate=args.frame_rate,
        cookies_file=args.cookies_file,
    )
