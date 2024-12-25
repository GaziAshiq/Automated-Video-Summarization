"""
Module for summarizing videos by clustering keyframes using K-Means.
"""

import numpy as np
from sklearn.cluster import KMeans
import os
import shutil


def summarize_keyframes(features_file, output_dir, n_clusters=5):
    """
    Summarizes keyframes by clustering their features.

    Args:
        features_file (str): Path to the file containing keyframe features.
        output_dir (str): Directory to save the selected summary keyframes.
        n_clusters (int): Number of clusters for K-Means.

    Returns:
        list: List of selected keyframe filenames.
    """
    # Load features
    features = np.load(features_file, allow_pickle=True).item()
    filenames = list(features.keys())
    feature_vectors = np.array(list(features.values()))

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(feature_vectors)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Select one representative frame per cluster
    summary_keyframes = []
    for cluster_id in range(n_clusters):
        cluster_indices = np.where(kmeans.labels_ == cluster_id)[0]
        # Choose the first frame in the cluster
        representative_index = cluster_indices[0]
        representative_frame = filenames[representative_index]
        summary_keyframes.append(representative_frame)

        # Copy the selected frame to the output directory
        shutil.copy(representative_frame, os.path.join(
            output_dir, os.path.basename(representative_frame)))

    print(f"Selected {len(summary_keyframes)} keyframes for the summary.")
    return summary_keyframes


if __name__ == "__main__":
    FEATURES_FILE = "data/features.npy"
    SUMMARY_DIR = "data/summaries/"
    NUM_CLUSTERS = 5  # Number of summary frames

    summarize_keyframes(FEATURES_FILE, SUMMARY_DIR, NUM_CLUSTERS)
