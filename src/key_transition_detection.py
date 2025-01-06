"""
Module for detecting key transitions and phrases from transcripts.
"""

import spacy
from transformers import pipeline
import re


def detect_transitions_and_phrases(transcript_path):
    """
    Detects key transitions and phrases in the transcript.

    Args:
        transcript_path (str): Path to the transcript file.

    Returns:
        dict: A dictionary with detected transitions and key phrases.
    """
    # Load transcript
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    # Load spaCy NLP model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(transcript)

    # Detect major transitions (e.g., topic changes)
    print("Detecting major transitions...")
    transitions = []
    for sent in doc.sents:
        if re.match(r"\b(chapter|section|topic|overview|summary|conclusion)\b", sent.text, re.IGNORECASE):
            transitions.append(sent.text.strip())

    # Detect key phrases
    print("Detecting key phrases...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    key_phrases = summarizer(transcript, max_length=100, min_length=25, do_sample=False)

    print(f"Detected {len(transitions)} transitions and key phrases.")
    return {"transitions": transitions, "key_phrases": key_phrases[0]["summary_text"]}


if __name__ == "__main__":
    TRANSCRIPT_PATH = "data/transcripts/transcript.txt"  # Replace with your transcript path
    output = detect_transitions_and_phrases(TRANSCRIPT_PATH)
    print("Transitions:")
    print("\n".join(output["transitions"]))
    print("\nKey Phrases:")
    print(output["key_phrases"])
