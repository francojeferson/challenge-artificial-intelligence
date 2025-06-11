"""
__init__.py

Main module for the Adaptive Learning System.
Integrates various components for resource processing, indexing, and adaptive learning.
"""

import os
from typing import List, Dict

from .ingestion import ResourceIngestor
from .indexing import ResourceIndexer


class AdaptiveLearningSystem:
    """
    Central class for the Adaptive Learning System.
    Manages resource ingestion, indexing, and future adaptive learning components.
    """

    def __init__(
        self,
        resources_dir: str = "resources",
        index_dir: str = "index_data",
        index_backend: str = "simple",
    ):
        """
        Initialize the adaptive learning system with ingestion and indexing components.

        Args:
            resources_dir (str): Directory containing resource files.
            index_dir (str): Directory to store index data.
            index_backend (str): Backend to use for indexing ('elasticsearch', 'pinecone', 'faiss', 'simple').
        """
        self.resources_dir = resources_dir
        self.index_dir = index_dir
        self.ingestor = ResourceIngestor(resources_dir=resources_dir)
        self.indexer = ResourceIndexer(index_backend=index_backend, index_dir=index_dir)

    def process_resources(self) -> List[Dict]:
        """
        Process all resources by ingesting and indexing them.

        Returns:
            List[Dict]: List of ingested and indexed resource data.
        """
        # Ingest all resources
        ingested_data = self.ingestor.ingest_all()
        print(f"Ingested {len(ingested_data)} resources.")

        # Index the ingested data
        self.indexer.batch_index(ingested_data)
        print(
            f"Indexed {len(ingested_data)} resources using {self.indexer.index_backend} backend."
        )

        return ingested_data

    def search_resources(
        self, query: str, resource_type: str = None, max_results: int = 10
    ) -> List[Dict]:
        """
        Search for resources based on a query.

        Args:
            query (str): Search query.
            resource_type (str, optional): Type of resource to filter by.
            max_results (int): Maximum number of results to return.

        Returns:
            List[Dict]: List of matching resource data.
        """
        results = self.indexer.search(query, resource_type, max_results)
        print(f"Found {len(results)} results for query: '{query}'")
        return results


def main():
    """
    Main function to test the Adaptive Learning System components.
    """
    system = AdaptiveLearningSystem()
    system.process_resources()

    # Test search functionality
    test_query = "learning"
    search_results = system.search_resources(test_query)
    for i, result in enumerate(search_results, 1):
        print(f"\nResult {i}:")
        print(f"  Filepath: {result.get('filepath')}")
        print(f"  Type: {result.get('type')}")
        text_snippet = result.get("text", result.get("transcript", ""))[:200]
        if text_snippet:
            print(f"  Text Snippet: {text_snippet}...")


if __name__ == "__main__":
    main()
