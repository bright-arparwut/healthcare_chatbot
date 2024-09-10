from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, url: str = "http://localhost:6333", collection_name: str = "healthcare_collection"):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name

    def create_collection(self, vector_size: int = 1536, distance: Distance = Distance.COSINE):
        """Create a new collection in Qdrant."""
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )

    def add_points(self, vectors: List[List[float]], payloads: List[Dict[str, Any]], ids: List[str] = None):
        """Add points (vectors and payloads) to the collection."""
        points = [
            PointStruct(id=id, vector=vector, payload=payload)
            for id, vector, payload in zip(ids or range(len(vectors)), vectors, payloads)
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_vector: List[float], limit: int = 5):
        """Search for similar vectors in the collection."""
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )

    def delete_collection(self):
        """Delete the collection."""
        self.client.delete_collection(collection_name=self.collection_name)