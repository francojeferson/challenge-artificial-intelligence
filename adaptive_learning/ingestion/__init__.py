"""
Ingestion Module for Adaptive Learning System

This package contains modules for ingesting various types of educational resources.
Each module is responsible for processing a specific type of resource (text, PDF, video, image)
and extracting content and metadata for indexing.

Modules:
- text_ingestor: Handles ingestion of text files (.txt, .json) using NLP tools.
- pdf_ingestor: Handles ingestion of PDF files using text extraction libraries.
- video_ingestor: Handles ingestion of video files by extracting and transcribing audio.
- image_ingestor: Handles ingestion of image files by extracting metadata.

Key Responsibilities:
- Ingest diverse educational resources for the Adaptive Learning System.
- Extract content and metadata for indexing and search.
- Ensure all processing is local and privacy-respecting.
- Maintain modularity and extensibility for future resource types.
"""

from .text_ingestor import ingest_text_file, ingest_text_directory
from .pdf_ingestor import ingest_pdf_file, ingest_pdf_directory
from .video_ingestor import ingest_video_file, ingest_video_directory
from .image_ingestor import ingest_image_file, ingest_image_directory
from .resource_ingestor import ResourceIngestor

__all__ = [
    "ingest_text_file",
    "ingest_text_directory",
    "ingest_pdf_file",
    "ingest_pdf_directory",
    "ingest_video_file",
    "ingest_video_directory",
    "ingest_image_file",
    "ingest_image_directory",
    "ResourceIngestor",
]
