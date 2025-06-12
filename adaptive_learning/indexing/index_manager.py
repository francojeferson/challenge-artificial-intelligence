"""
Index Manager Module

This module handles the indexing of ingested resources for the Adaptive Learning System.
It provides functionality to store and retrieve data efficiently for search operations.

Key Responsibilities:
- Aggregate data from ingestion modules (text, PDF, video, image).
- Index content and metadata for efficient keyword and semantic search.
- Ensure all processing is local and privacy-respecting.
- Support retrieval by type, topic, and relevance.

Dependencies:
- json: For storing index data in a simple JSON format (initial implementation).
- os: For file and directory operations.
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class IndexManager:
    """
    A class to manage the indexing and retrieval of ingested resources.
    """

    def __init__(self, index_file_path: str = "index_data/simple_index.json"):
        """
        Initialize the IndexManager with a path to store the index file.

        Args:
            index_file_path (str): Path to the JSON file where the index will be stored.
        """
        self.index_file_path = index_file_path
        self.index_data: List[Dict[str, Any]] = []
        self.embedder = None
        self.vector_index = None
        self.load_index()
        self.initialize_vector_index()

    def load_index(self) -> None:
        """
        Load the existing index from the file if it exists.
        """
        try:
            if os.path.exists(self.index_file_path):
                with open(self.index_file_path, "r", encoding="utf-8") as f:
                    self.index_data = json.load(f)
                print(f"Loaded index with {len(self.index_data)} entries.")
            else:
                print(
                    f"No existing index found at {self.index_file_path}. Starting fresh."
                )
                self.index_data = []
        except Exception as e:
            print(f"Error loading index from {self.index_file_path}: {e}")
            self.index_data = []

    def save_index(self) -> None:
        """
        Save the current index to the file.
        """
        try:
            os.makedirs(os.path.dirname(self.index_file_path), exist_ok=True)
            with open(self.index_file_path, "w", encoding="utf-8") as f:
                json.dump(self.index_data, f, ensure_ascii=False, indent=2)
            print(
                f"Saved index with {len(self.index_data)} entries to {self.index_file_path}."
            )
        except Exception as e:
            print(f"Error saving index to {self.index_file_path}: {e}")

    def add_resource(self, resource: Dict[str, Any]) -> None:
        """
        Add a new resource to the index.

        Args:
            resource (Dict[str, Any]): Dictionary containing metadata, content, and processed content of the resource.
        """
        # Add timestamp for indexing
        resource["metadata"]["indexed_at"] = datetime.now().isoformat()
        # Check for duplicates based on file_path
        file_path = resource["metadata"].get("file_path", "")
        if any(
            entry["metadata"].get("file_path", "") == file_path
            for entry in self.index_data
        ):
            print(f"Duplicate resource found for {file_path}. Updating existing entry.")
            self.update_resource(file_path, resource)
        else:
            self.index_data.append(resource)
            print(
                f"Added resource {resource['metadata'].get('file_name', 'unknown')} to index."
            )
            # Add to vector index if initialized
            if hasattr(self, "vector_index") and hasattr(self, "embedder"):
                self.add_to_vector_index(resource, len(self.index_data) - 1)

    def update_resource(self, file_path: str, updated_resource: Dict[str, Any]) -> None:
        """
        Update an existing resource in the index based on file_path.

        Args:
            file_path (str): Path to the file to identify the resource.
            updated_resource (Dict[str, Any]): Updated dictionary with resource data.
        """
        for i, entry in enumerate(self.index_data):
            if entry["metadata"].get("file_path", "") == file_path:
                updated_resource["metadata"]["updated_at"] = datetime.now().isoformat()
                self.index_data[i] = updated_resource
                print(
                    f"Updated resource {updated_resource['metadata'].get('file_name', 'unknown')} in index."
                )
                return
        # If not found, add as new
        self.add_resource(updated_resource)

    def search_by_keyword(
        self, keyword: str, resource_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search the index for resources containing the keyword in content or metadata.

        Args:
            keyword (str): Keyword to search for.
            resource_type (Optional[str]): Filter by resource type (e.g., '.txt', '.pdf').

        Returns:
            List[Dict[str, Any]]: List of matching resources.
        """
        keyword = keyword.lower()
        results = []
        for entry in self.index_data:
            if (
                resource_type
                and entry["metadata"].get("file_type", "").lower()
                != resource_type.lower()
            ):
                continue
            content = entry.get("content", "").lower()
            file_name = entry["metadata"].get("file_name", "").lower()
            if keyword in content or keyword in file_name:
                results.append(entry)
        return results

    def search_by_type(self, resource_type: str) -> List[Dict[str, Any]]:
        """
        Search the index for resources of a specific type.

        Args:
            resource_type (str): Resource type to filter by (e.g., '.txt', '.pdf').

        Returns:
            List[Dict[str, Any]]: List of matching resources.
        """
        resource_type = resource_type.lower()
        return [
            entry
            for entry in self.index_data
            if entry["metadata"].get("file_type", "").lower() == resource_type
        ]

    def get_all_resources(self) -> List[Dict[str, Any]]:
        """
        Retrieve all resources in the index.

        Returns:
            List[Dict[str, Any]]: List of all resources.
        """
        return self.index_data

    def initialize_vector_index(self) -> None:
        """
        Initialize the FAISS vector index and embedder for semantic search.
        """
        try:
            import faiss
            from sentence_transformers import SentenceTransformer

            # Initialize the embedder model
            self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
            # Initialize FAISS index (dimension based on the model's output)
            dimension = self.embedder.get_sentence_embedding_dimension()
            self.vector_index = faiss.IndexFlatL2(dimension)
            print("Initialized FAISS vector index for semantic search.")
            # Build vector index if data already exists
            if self.index_data:
                self.build_vector_index()
        except Exception as e:
            print(f"Error initializing vector index: {e}")
            self.embedder = None
            self.vector_index = None

    def build_vector_index(self) -> None:
        """
        Build the FAISS vector index from the current index data.
        """
        if not self.embedder or not self.vector_index:
            print("Vector index or embedder not initialized. Skipping build.")
            return

        try:
            import numpy as np

            # Reset the index
            self.vector_index.reset()
            # Generate embeddings for all resources
            embeddings = []
            for resource in self.index_data:
                content = resource.get("content", "")
                if content:
                    embedding = self.embedder.encode(
                        content[:1000]
                    )  # Limit content for performance
                    embeddings.append(embedding)
                else:
                    embeddings.append(
                        np.zeros(self.embedder.get_sentence_embedding_dimension())
                    )
            # Add embeddings to FAISS index
            if embeddings:
                embeddings_array = np.array(embeddings).astype("float32")
                self.vector_index.add(embeddings_array)
                print(f"Built vector index with {len(embeddings)} embeddings.")
        except Exception as e:
            print(f"Error building vector index: {e}")

    def add_to_vector_index(self, resource: Dict[str, Any], index: int) -> None:
        """
        Add a single resource's embedding to the FAISS vector index.

        Args:
            resource (Dict[str, Any]): The resource to add.
            index (int): The index of the resource in the index_data list.
        """
        if not self.embedder or not self.vector_index:
            return

        try:
            import numpy as np

            content = resource.get("content", "")
            if content:
                embedding = self.embedder.encode(
                    content[:1000]
                )  # Limit content for performance
            else:
                embedding = np.zeros(self.embedder.get_sentence_embedding_dimension())
            embedding_array = np.array([embedding]).astype("float32")
            if index < self.vector_index.ntotal:
                # Replace existing embedding
                self.vector_index.remove_ids(np.array([index]))
                self.vector_index.add_with_ids(embedding_array, np.array([index]))
            else:
                # Add new embedding
                self.vector_index.add_with_ids(embedding_array, np.array([index]))
        except Exception as e:
            print(f"Error adding resource to vector index: {e}")

    def search_by_similarity(
        self, query: str, k: int = 5, resource_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search the index for resources semantically similar to the query.

        Args:
            query (str): Query text to search for.
            k (int): Number of top similar results to return.
            resource_type (Optional[str]): Filter by resource type (e.g., '.txt', '.pdf').

        Returns:
            List[Dict[str, Any]]: List of matching resources ordered by similarity.
        """
        if not self.embedder or not self.vector_index:
            print("Semantic search not available. Initializing vector index now...")
            self.initialize_vector_index()
            if not self.embedder or not self.vector_index:
                print("Failed to initialize vector index for semantic search.")
                return []

        try:
            import numpy as np

            # Generate embedding for the query
            query_embedding = self.embedder.encode(query)
            query_array = np.array([query_embedding]).astype("float32")
            # Search for top k similar embeddings
            distances, indices = self.vector_index.search(query_array, k)
            results = []
            for i, idx in enumerate(indices[0]):
                if idx >= 0 and idx < len(self.index_data):
                    entry = self.index_data[idx]
                    if (
                        resource_type
                        and entry["metadata"].get("file_type", "").lower()
                        != resource_type.lower()
                    ):
                        continue
                    entry["similarity_score"] = float(distances[0][i])
                    results.append(entry)
            return results
        except Exception as e:
            print(f"Error performing similarity search: {e}")
            return []


def build_index_from_resources(
    resources: List[Dict[str, Any]],
    index_file_path: str = "index_data/simple_index.json",
) -> IndexManager:
    """
    Build an index from a list of ingested resources.

    Args:
        resources (List[Dict[str, Any]]): List of resources to index.
        index_file_path (str): Path to save the index file.

    Returns:
        IndexManager: Initialized IndexManager with the indexed resources.
    """
    indexer = IndexManager(index_file_path)
    for resource in resources:
        indexer.add_resource(resource)
    indexer.save_index()
    return indexer


if __name__ == "__main__":
    # Example usage for testing
    from ..ingestion.text_ingestor import ingest_text_directory
    from ..ingestion.pdf_ingestor import ingest_pdf_directory
    from ..ingestion.video_ingestor import ingest_video_directory
    from ..ingestion.image_ingestor import ingest_image_directory

    resources_dir = "../../resources"
    all_resources = []

    # Ingest all types of resources
    text_data = ingest_text_directory(os.path.join(resources_dir, "text"))
    all_resources.extend(text_data)
    print(f"Added {len(text_data)} text resources.")

    pdf_data = ingest_pdf_directory(os.path.join(resources_dir, "pdf"))
    all_resources.extend(pdf_data)
    print(f"Added {len(pdf_data)} PDF resources.")

    video_data = ingest_video_directory(os.path.join(resources_dir, "video"))
    all_resources.extend(video_data)
    print(f"Added {len(video_data)} video resources.")

    image_data = ingest_image_directory(os.path.join(resources_dir, "image"))
    all_resources.extend(image_data)
    print(f"Added {len(image_data)} image resources.")

    # Build and save index
    indexer = build_index_from_resources(all_resources)
    print(f"Total resources indexed: {len(indexer.get_all_resources())}")

    # Test search functionality
    test_keyword = "programming"
    search_results = indexer.search_by_keyword(test_keyword)
    print(f"Search results for '{test_keyword}': {len(search_results)} matches.")
    for result in search_results:
        print(f" - {result['metadata'].get('file_name', 'unknown')}")
