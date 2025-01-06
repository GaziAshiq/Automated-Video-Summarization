"""
Module for generating short video clips based on key points or transitions.
"""

import os
import re
from moviepy.video.io.VideoFileClip import VideoFileClip  # pylint: disable=import-error


def parse_srt(srt_path):
    """Parses an SRT file and extracts timestamps and subtitles."""
    with open(srt_path, "r", encoding="utf-8") as f:
        srt_content = f.read()

    subtitles = []
    srt_blocks = srt_content.strip().split("\n\n")

    for block in srt_blocks:
        lines = block.split("\n")
        if len(lines) >= 3:
            times = lines[1]
            text = " ".join(lines[2:])
            start, end = parse_srt_timestamp(times)
            subtitles.append({"start": start, "end": end, "text": text})

    return subtitles


def parse_srt_timestamp(timestamp):
    """Parses an SRT timestamp in the format `hh:mm:ss,ms --> hh:mm:ss,ms`."""
    start, end = timestamp.split(" --> ")
    return convert_to_seconds(start), convert_to_seconds(end)


def convert_to_seconds(srt_time):
    """Converts an SRT time format (hh:mm:ss,ms) to seconds."""
    time_parts = re.split("[:,]", srt_time)
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])
    milliseconds = int(time_parts[3])
    return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0


def generate_clips(video_path, srt_path, output_dir, key_phrases):
    """
    Generates short video clips based on key phrases matched to subtitles.

    Args:
        video_path (str): Path to the input video file.
        srt_path (str): Path to the SRT file.
        output_dir (str): Directory to save the generated clips.
        key_phrases (list): List of key phrases to extract clips for.

    Returns:
        list: List of paths to the generated clips.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not os.path.exists(srt_path):
        raise FileNotFoundError(f"SRT file not found: {srt_path}")

    os.makedirs(output_dir, exist_ok=True)

    # Parse subtitles
    subtitles = parse_srt(srt_path)

    # Load the video
    video = VideoFileClip(video_path)

    # Match key phrases to subtitles and generate clips
    clips = []
    for phrase in key_phrases:
        print(f"Checking for phrase: '{phrase}'")
        for subtitle in subtitles:
            print(f"Subtitle: '{subtitle['text']}'")
            if phrase.lower() in subtitle["text"].lower():
                print(f"Match found: '{subtitle['text']}' for phrase: '{phrase}'")
                start, end = subtitle["start"], subtitle["end"]
                clip_path = os.path.join(output_dir, f"clip_{start:.0f}_{end:.0f}.mp4")
                try:
                    # Use `subclipped` instead of `subclip`
                    video.subclipped(start, end).write_videofile(
                        clip_path, codec="libx264"
                    )  # pylint: disable=no-member
                    clips.append(clip_path)
                except Exception as e:
                    print(f"Error generating clip for phrase '{phrase}': {e}")
                break  # Avoid duplicate matches for the same phrase

    print(f"Generated {len(clips)} clips.")
    return clips


if __name__ == "__main__":
    # Input paths
    VIDEO_PATH = "data/input_videos/sample.mp4"
    SRT_PATH = "data/transcripts/subtitles.srt"
    OUTPUT_DIR = "data/clips/"

    # Key phrases to match
    KEY_PHRASES = [
        "Node.js",
        "programming",
        "Node APIs",
        "frustrating",
        "security",
        "Reverse it",
        "Dino",
        "TypeScript",
        "secured by default",
    ]

    # Generate video clips
    generate_clips(VIDEO_PATH, SRT_PATH, OUTPUT_DIR, KEY_PHRASES)
