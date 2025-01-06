"""
Module for summarizing transcripts into a concise structured summary.
"""

from transformers import pipeline
import os


def summarize_transcript(transcript_path, output_path, max_chunk_size=1000):
    """
    Summarizes a transcript into a concise structured summary.

    Args:
        transcript_path (str): Path to the transcript file.
        output_path (str): Path to save the summarized text.
        max_chunk_size (int): Maximum size of each transcript chunk for summarization.

    Returns:
        None
    """
    # Load transcript
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    # Split transcript into chunks
    chunks = split_into_chunks(transcript, max_chunk_size)

    # Load summarization model
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Summarize each chunk
    print("Summarizing transcript...")
    summary = ""
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i + 1}/{len(chunks)}...")
        summarized_chunk = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
        summary += f"{summarized_chunk}\n\n"

    # Save the summary
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"Summary saved to {output_path}")


def split_into_chunks(text, max_size):
    """
    Splits text into smaller chunks of a maximum size.

    Args:
        text (str): The input text to split.
        max_size (int): Maximum size of each chunk.

    Returns:
        list: List of text chunks.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk) + word) < max_size:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


if __name__ == "__main__":
    TRANSCRIPT_PATH = "data/transcripts/transcript.txt"  # Path to the transcript
    OUTPUT_PATH = "data/summaries/summary.txt"          # Path to save the summary
    summarize_transcript(TRANSCRIPT_PATH, OUTPUT_PATH)
