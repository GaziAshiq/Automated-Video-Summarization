"""
Module for extracting features from keyframes using a pretrained ResNet model.
"""

import os
import sys
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def extract_features(keyframe_files, model=None, device=None):
    """
    Extracts features from a list of keyframes using a pretrained model.

    Args:
        keyframe_files (list): List of keyframe file paths.
        model (torch.nn.Module): Pretrained model for feature extraction.
        device (torch.device): Device to run the model on (CPU or GPU).

    Returns:
        dict: A dictionary mapping keyframe filenames to feature vectors.
    """
    if model is None:
        # Load pretrained ResNet model
        model = models.resnet50(pretrained=True)
        # Remove the classification layer
        model = torch.nn.Sequential(*list(model.children())[:-1])
        model.eval()

    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # Image preprocessing pipeline
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                             0.229, 0.224, 0.225]),
    ])

    features = {}

    for keyframe_file in keyframe_files:
        image = Image.open(keyframe_file).convert("RGB")
        input_tensor = preprocess(image).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(input_tensor).squeeze().cpu().numpy()
            features[keyframe_file] = output

    print(f"Extracted features for {len(features)} keyframes.")
    return features


if __name__ == "__main__":
    FRAME_DIR = "data/frames/"  # Directory where frames are stored
    OUTPUT_FILE = "data/features.npy"  # File to save extracted features

    # Detect keyframes
    from src.keyframe_detection import detect_keyframes
    keyframe_files = detect_keyframes(FRAME_DIR, threshold=0.5)

    # Extract features
    features = extract_features(keyframe_files)

    # Save features
    np.save(OUTPUT_FILE, features)
    print(f"Features saved to {OUTPUT_FILE}")
