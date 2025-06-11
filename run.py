"""
run.py

Entry point script for the Adaptive Learning System.
This script integrates ingestion modules to process resources and builds an index for search functionality.
"""

import os
import sys
from adaptive_learning.ingestion.text_ingestor import ingest_text_directory
from adaptive_learning.ingestion.pdf_ingestor import ingest_pdf_directory
from adaptive_learning.ingestion.video_ingestor import ingest_video_directory
from adaptive_learning.ingestion.image_ingestor import ingest_image_directory
from adaptive_learning.indexing.index_manager import (
    build_index_from_resources,
    IndexManager,
)


def main():
    """
    Main function to ingest resources and build an index for the Adaptive Learning System.
    """
    resources_dir = "resources"
    all_resources = []

    print("Starting resource ingestion process...")

    # Ingest all types of resources from their respective directories
    text_data = ingest_text_directory(os.path.join(resources_dir, "text"))
    all_resources.extend(text_data)
    print(f"Ingested {len(text_data)} text resources.")

    pdf_data = ingest_pdf_directory(os.path.join(resources_dir, "pdf"))
    all_resources.extend(pdf_data)
    print(f"Ingested {len(pdf_data)} PDF resources.")

    video_data = ingest_video_directory(os.path.join(resources_dir, "video"))
    all_resources.extend(video_data)
    print(f"Ingested {len(video_data)} video resources.")

    image_data = ingest_image_directory(os.path.join(resources_dir, "image"))
    all_resources.extend(image_data)
    print(f"Ingested {len(image_data)} image resources.")

    # Build and save the index
    indexer = build_index_from_resources(all_resources, "index_data/simple_index.json")
    print(f"Total resources indexed: {len(indexer.get_all_resources())}")

    # Test search functionality
    test_keyword = "programming"
    search_results = indexer.search_by_keyword(test_keyword)
    print(f"\nSearch results for '{test_keyword}': {len(search_results)} matches.")
    for i, result in enumerate(search_results, 1):
        print(f"Result {i}:")
        print(f"  File: {result['metadata'].get('file_name', 'unknown')}")
        print(f"  Type: {result['metadata'].get('file_type', 'unknown')}")
        content_snippet = result.get("content", "")[:200]
        if content_snippet:
            print(f"  Content Snippet: {content_snippet}...")

    print("\nResource ingestion and indexing completed successfully.")


if __name__ == "__main__":
    main()
