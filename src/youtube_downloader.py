"""
Module for downloading YouTube videos using yt-dlp with cookies support.
"""

import os
import yt_dlp


def download_youtube_video(youtube_url, output_dir, cookies_file=None):
    """
    Downloads a YouTube video using yt-dlp with optional cookies.

    Args:
        youtube_url (str): The URL of the YouTube video.
        output_dir (str): Directory to save the downloaded video.
        cookies_file (str): Path to the cookies file for authentication.

    Returns:
        str: Path to the downloaded video file.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "best",
        "outtmpl": output_template,
        "quiet": True,  # Minimize output for cleaner logs
    }

    if cookies_file:
        ydl_opts["cookies"] = cookies_file

    print(f"Downloading YouTube video from {youtube_url}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            video_path = ydl.prepare_filename(info_dict)
        print(f"Downloaded video saved to: {video_path}")
        return video_path
    except yt_dlp.utils.DownloadError as error:
        print(f"Error downloading video: {error}")
        return None


if __name__ == "__main__":
    TEST_URL = "https://youtu.be/swXWUfufu2w"  # Replace with your test URL
    OUTPUT_DIR = "data/input_videos/"
    COOKIES_FILE = "cookies.txt"  # Path to cookies file
    download_youtube_video(TEST_URL, OUTPUT_DIR, COOKIES_FILE)
