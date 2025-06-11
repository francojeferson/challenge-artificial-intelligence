"""
Image Ingestion Module

This module handles the ingestion of image resources for the Adaptive Learning System.
It extracts metadata and tags from image files for indexing.

Key Responsibilities:
- Extract metadata (EXIF data) from image files.
- Generate basic tags or descriptions if possible.
- Ensure all processing is local and privacy-respecting.

Dependencies:
- PIL (Pillow): For reading image files and extracting metadata.
- exifread: For detailed EXIF data extraction.
"""

import os
from typing import Dict, List, Any
from PIL import Image
import exifread


def ingest_image_file(file_path: str) -> Dict[str, Any]:
    """
    Ingest a single image file and extract its metadata.

    Args:
        file_path (str): Path to the image file.

    Returns:
        Dict[str, Any]: Dictionary containing metadata and inferred content description.
    """
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_path)[1].lower()
    metadata = {
        "file_name": file_name,
        "file_path": file_path,
        "file_type": file_extension,
        "size_bytes": os.path.getsize(file_path),
        "last_modified": os.path.getmtime(file_path),
        "width": 0,
        "height": 0,
        "resource_type": "image",
    }

    # Extract basic image metadata using PIL
    try:
        with Image.open(file_path) as img:
            metadata["width"], metadata["height"] = img.size
            metadata["format"] = img.format
            if hasattr(img, "info") and img.info:
                for key, value in img.info.items():
                    if isinstance(value, (str, int, float)):
                        metadata[f"info_{key}"] = value
    except Exception as e:
        print(f"Error reading image metadata with PIL for {file_path}: {e}")

    # Extract detailed EXIF data using exifread
    try:
        with open(file_path, "rb") as f:
            tags = exifread.process_file(f, details=False)
            for tag, value in tags.items():
                if isinstance(value, (str, int, float)):
                    metadata[f"exif_{tag}"] = str(value)
    except Exception as e:
        print(f"Error reading EXIF data for {file_path}: {e}")

    # Infer content description and tags from file name and directory structure
    content = f"Image file: {file_name}"
    inferred_tags = []
    try:
        # Extract potential tags from file name (split by non-alphanumeric characters)
        name_parts = "".join(c if c.isalnum() else " " for c in file_name).split()
        inferred_tags.extend([part.lower() for part in name_parts if len(part) > 2])

        # Extract potential tags from directory name
        dir_name = os.path.basename(os.path.dirname(file_path))
        dir_parts = "".join(c if c.isalnum() else " " for c in dir_name).split()
        inferred_tags.extend([part.lower() for part in dir_parts if len(part) > 2])

        # Remove duplicates and limit to top 10 tags
        inferred_tags = list(set(inferred_tags))[:10]
        metadata["inferred_tags"] = inferred_tags
        content = f"Image file: {file_name} (Tags: {', '.join(inferred_tags)})"
    except Exception as e:
        print(f"Error inferring tags for {file_path}: {e}")
        metadata["inferred_tags"] = []

    return {"metadata": metadata, "content": content, "processed_content": content}


def ingest_image_directory(directory_path: str) -> List[Dict[str, Any]]:
    """
    Ingest all image files in a directory and its subdirectories.

    Args:
        directory_path (str): Path to the directory containing image files.

    Returns:
        List[Dict[str, Any]]: List of dictionaries with metadata for each file.
    """
    image_data = []
    supported_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(supported_extensions):
                file_path = os.path.join(root, file)
                data = ingest_image_file(file_path)
                if data:
                    image_data.append(data)

    return image_data


if __name__ == "__main__":
    # Example usage for testing
    sample_dir = "../../resources/image"
    if os.path.exists(sample_dir):
        image_resources = ingest_image_directory(sample_dir)
        print(f"Ingested {len(image_resources)} image resources.")
        for resource in image_resources:
            print(
                f"File: {resource['metadata']['file_name']}, Dimensions: {resource['metadata'].get('width', 0)}x{resource['metadata'].get('height', 0)}"
            )
    else:
        print(f"Sample directory {sample_dir} not found.")
