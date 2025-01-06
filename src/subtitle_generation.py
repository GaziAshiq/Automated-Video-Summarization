"""
Module for generating subtitles and transcripts using Whisper.
"""

import whisper
import os

def generate_subtitles(input_video, output_dir):
    """
    Generates subtitles and a transcript from the input video.

    Args:
        input_video (str): Path to the input video file.
        output_dir (str): Directory to save the subtitles and transcript.

    Returns:
        str: Path to the generated transcript.
    """
    os.makedirs(output_dir, exist_ok=True)
    model = whisper.load_model("base")  # You can switch to 'medium' or 'large' for better accuracy

    print(f"Transcribing video: {input_video}...")
    result = model.transcribe(input_video)

    # Save the transcript
    transcript_path = os.path.join(output_dir, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Save subtitles in SRT format
    subtitles_path = os.path.join(output_dir, "subtitles.srt")
    with open(subtitles_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"{segment['id']}\n")
            f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            f.write(f"{text}\n\n")

    print(f"Transcription complete. Transcript saved to {transcript_path}")
    print(f"Subtitles saved to {subtitles_path}")
    return transcript_path

def format_timestamp(seconds):
    """Formats a timestamp in seconds to SRT time format (hh:mm:ss,ms)."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

if __name__ == "__main__":
    INPUT_VIDEO = "data/input_videos/sample.mp4"  # Replace with your video file
    OUTPUT_DIR = "data/transcripts/"
    generate_subtitles(INPUT_VIDEO, OUTPUT_DIR)
