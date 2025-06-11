"""
__init__.py

Central module for indexing ingested resources in the Adaptive Learning System.
Provides functionality to store and index data for efficient search and retrieval.
"""

from typing import List, Dict, Any
import os
import json

try:
    from elasticsearch import Elasticsearch
    from elasticsearch.exceptions import RequestError
except ImportError:
    Elasticsearch = None
    RequestError = None

try:
    import pinecone
except ImportError:
    pinecone = None

try:
    import faiss
    import numpy as np
except ImportError:
    faiss = np = None


class ResourceIndexer:
    """
    Manages the indexing of ingested resources for search and retrieval.
    Supports multiple backend options for flexibility.
    """

    def __init__(
        self, index_backend: str = "elasticsearch", index_dir: str = "index_data"
    ):
        """
        Initialize the indexer with a specified backend.

        Args:
            index_backend (str): Backend to use for indexing ('elasticsearch', 'pinecone', 'faiss', 'simple').
            index_dir (str): Directory to store index data or configuration.
        """
        self.index_backend = index_backend.lower()
        self.index_dir = index_dir
        os.makedirs(self.index_dir, exist_ok=True)

        self.client = None
        self.index_name = "adaptive_learning_resources"

        if self.index_backend == "elasticsearch" and Elasticsearch is not None:
            self.client = Elasticsearch(["http://localhost:9200"])
            if not self.client.ping():
                raise ConnectionError(
                    "Failed to connect to Elasticsearch at localhost:9200"
                )
            self._initialize_elasticsearch_index()
        elif self.index_backend == "pinecone" and pinecone is not None:
            # Pinecone initialization would require API key setup
            raise NotImplementedError("Pinecone backend is not fully implemented yet.")
        elif self.index_backend == "faiss" and faiss is not None:
            # FAISS initialization for local vector search
            self.dimension = 128  # Example dimension for embeddings
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index_path = os.path.join(self.index_dir, "faiss_index")
            self.metadata_store = []
        else:
            # Fallback to a simple JSON-based storage if no backend is available
            self.index_backend = "simple"
            self.index_file = os.path.join(self.index_dir, "simple_index.json")
            self.simple_index = []
            if os.path.exists(self.index_file):
                with open(self.index_file, "r", encoding="utf-8") as f:
                    self.simple_index = json.load(f)

    def _initialize_elasticsearch_index(self):
        """
        Initialize Elasticsearch index with mappings for resource data.
        """
        if not self.client:
            return

        mapping = {
            "mappings": {
                "properties": {
                    "filepath": {"type": "keyword"},
                    "type": {"type": "keyword"},
                    "text": {"type": "text"},
                    "metadata": {"type": "object"},
                    "transcript": {"type": "text"},
                    "exif_data": {"type": "object"},
                    "tokens": {"type": "text"},
                    "entities": {"type": "object"},
                }
            }
        }

        try:
            if not self.client.indices.exists(index=self.index_name):
                self.client.indices.create(index=self.index_name, body=mapping)
        except RequestError as e:
            if e.error != "resource_already_exists_exception":
                raise

    def index_resource(self, resource_data: Dict[str, Any]):
        """
        Index a single resource based on its type and content.

        Args:
            resource_data (Dict[str, Any]): Data of the resource to index.
        """
        resource_type = self._determine_resource_type(resource_data)

        if self.index_backend == "elasticsearch" and self.client:
            self.client.index(
                index=self.index_name,
                body={
                    "filepath": resource_data.get("filepath"),
                    "type": resource_type,
                    "text": resource_data.get("text", ""),
                    "metadata": resource_data.get("metadata", {}),
                    "transcript": resource_data.get("transcript", ""),
                    "exif_data": resource_data.get("exif_data", {}),
                    "tokens": resource_data.get("tokens", []),
                    "entities": resource_data.get("entities", []),
                },
            )
        elif self.index_backend == "faiss" and faiss is not None:
            # Placeholder for vector embedding with FAISS
            # In a real implementation, convert text to vector using a model
            if "text" in resource_data or "transcript" in resource_data:
                text_content = resource_data.get(
                    "text", resource_data.get("transcript", "")
                )
                # Dummy vector for illustration
                vector = np.random.rand(self.dimension).astype("float32")
                self.index.add(np.array([vector]))
                self.metadata_store.append(
                    {
                        "filepath": resource_data.get("filepath"),
                        "type": resource_type,
                        "text": text_content,
                        "metadata": resource_data.get("metadata", {}),
                    }
                )
        else:
            # Simple JSON storage
            self.simple_index.append(
                {
                    "filepath": resource_data.get("filepath"),
                    "type": resource_type,
                    "text": resource_data.get("text", ""),
                    "metadata": resource_data.get("metadata", {}),
                    "transcript": resource_data.get("transcript", ""),
                    "exif_data": resource_data.get("exif_data", {}),
                    "tokens": resource_data.get("tokens", []),
                    "entities": resource_data.get("entities", []),
                }
            )
            with open(self.index_file, "w", encoding="utf-8") as f:
                json.dump(self.simple_index, f, indent=2)

    def batch_index(self, resources_data: List[Dict[str, Any]]):
        """
        Index multiple resources at once.

        Args:
            resources_data (List[Dict[str, Any]]): List of resource data to index.
        """
        for resource_data in resources_data:
            self.index_resource(resource_data)

        if self.index_backend == "faiss" and faiss is not None:
            faiss.write_index(self.index, self.index_path)

    def search(
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
        if self.index_backend == "elasticsearch" and self.client:
            body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["text^2", "transcript", "tokens"],
                    }
                },
                "size": max_results,
            }
            if resource_type:
                body["query"] = {
                    "bool": {
                        "must": body["query"],
                        "filter": {"term": {"type": resource_type}},
                    }
                }
            response = self.client.search(index=self.index_name, body=body)
            return [hit["_source"] for hit in response["hits"]["hits"]]
        elif self.index_backend == "faiss" and faiss is not None:
            # Placeholder for FAISS search
            # In a real implementation, convert query to vector and search
            results = []
            for i, meta in enumerate(self.metadata_store):
                if resource_type and meta["type"] != resource_type:
                    continue
                if query.lower() in meta.get("text", "").lower():
                    results.append(meta)
                if len(results) >= max_results:
                    break
            return results
        else:
            # Simple search in JSON index
            results = []
            for item in self.simple_index:
                if resource_type and item["type"] != resource_type:
                    continue
                text_content = item.get("text", "") + item.get("transcript", "")
                if query.lower() in text_content.lower():
                    results.append(item)
                if len(results) >= max_results:
                    break
            return results

    def _determine_resource_type(self, resource_data: Dict[str, Any]) -> str:
        """
        Determine the type of resource based on its data structure or filepath.

        Args:
            resource_data (Dict[str, Any]): Resource data.

        Returns:
            str: Type of resource ('text', 'pdf', 'video', 'image').
        """
        filepath = resource_data.get("filepath", "").lower()
        if "transcript" in resource_data:
            return "video"
        elif "exif_data" in resource_data:
            return "image"
        elif filepath.endswith(".pdf"):
            return "pdf"
        elif filepath.endswith((".txt", ".json")):
            return "text"
        elif filepath.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")):
            return "image"
        elif filepath.endswith((".mp4", ".avi", ".mov", ".mkv")):
            return "video"
        return "unknown"
