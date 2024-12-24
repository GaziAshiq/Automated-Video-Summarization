# Automated Video Summarization

This project aims to create a system for summarizing videos automatically using AI. It extracts keyframes, processes features, and reconstructs a summarized video for applications like surveillance, entertainment, and more.

## Features
- Extracts keyframes based on visual differences.
- Summarizes videos by clustering similar scenes.
- Reconstructs videos from selected keyframes.

## Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.

## Usage
Run the main pipeline:
```bash
python main.py --input data/input_videos/sample.mp4 --output data/summaries/
