"""
Resource Ingestor Module

This module defines the ResourceIngestor class, which manages the ingestion of various types of educational resources
for the Adaptive Learning System. It integrates different ingestion modules for text, PDF, video, and image resources.

Key Responsibilities:
- Coordinate the ingestion of different resource types.
- Provide a unified interface for resource processing.
- Ensure all processing is local and privacy-respecting.
"""

import os
from typing import List, Dict, Any
from .text_ingestor import ingest_text_file, ingest_text_directory
from .pdf_ingestor import ingest_pdf_file, ingest_pdf_directory
from .video_ingestor import ingest_video_file, ingest_video_directory
from .image_ingestor import ingest_image_file, ingest_image_directory


class ResourceIngestor:
    """
    A class to manage the ingestion of various educational resources.
    It delegates the actual processing to specific ingestion modules based on resource type.
    """

    def __init__(self, resources_dir: str = "resources"):
        """
        Initialize the ResourceIngestor with the directory containing resources.

        Args:
            resources_dir (str): Directory path where resources are located.
        """
        self.resources_dir = resources_dir

    def ingest_text_resources(self) -> List[Dict[str, Any]]:
        """
        Ingest text resources from the specified directory.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing metadata and content for text resources.
        """
        text_dir = os.path.join(self.resources_dir, "text")
        if os.path.exists(text_dir):
            return ingest_text_directory(text_dir)
        return []

    def ingest_pdf_resources(self) -> List[Dict[str, Any]]:
        """
        Ingest PDF resources from the specified directory.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing metadata and content for PDF resources.
        """
        pdf_dir = os.path.join(self.resources_dir, "pdf")
        if os.path.exists(pdf_dir):
            return ingest_pdf_directory(pdf_dir)
        return []

    def ingest_video_resources(self) -> List[Dict[str, Any]]:
        """
        Ingest video resources from the specified directory.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing metadata and content for video resources.
        """
        video_dir = os.path.join(self.resources_dir, "video")
        if os.path.exists(video_dir):
            return ingest_video_directory(video_dir)
        return []

    def ingest_image_resources(self) -> List[Dict[str, Any]]:
        """
        Ingest image resources from the specified directory.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing metadata and content for image resources.
        """
        image_dir = os.path.join(self.resources_dir, "image")
        if os.path.exists(image_dir):
            return ingest_image_directory(image_dir)
        return []

    def ingest_all(self) -> List[Dict[str, Any]]:
        """
        Ingest all types of resources from their respective directories.

        Returns:
            List[Dict[str, Any]]: Combined list of dictionaries containing metadata and content for all resources.
        """
        all_resources = []
        all_resources.extend(self.ingest_text_resources())
        all_resources.extend(self.ingest_pdf_resources())
        all_resources.extend(self.ingest_video_resources())
        all_resources.extend(self.ingest_image_resources())
        return all_resources


if __name__ == "__main__":
    # Test the ResourceIngestor
    ingestor = ResourceIngestor()
    resources = ingestor.ingest_all()
    print(f"Ingested {len(resources)} resources in total.")
    for resource in resources:
        print(
            f"File: {resource['metadata']['file_name']}, Type: {resource['metadata']['resource_type']}"
        )
