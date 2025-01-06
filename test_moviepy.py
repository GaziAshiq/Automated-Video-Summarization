from moviepy.video.io.VideoFileClip import VideoFileClip

video_path = "data/input_videos/sample.mp4"

try:
    video = VideoFileClip(video_path)
    print(dir(video))  # Print available attributes/methods
except Exception as e:
    print(f"Error: {e}")
