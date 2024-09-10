from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, url: str = "http://localhost:6333"):
        self.client = QdrantClient(url=url)

    def create_collection(self, collection_name: str, vector_size: int, distance: Distance = Distance.COSINE):
        """Create a new collection in Qdrant."""
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )

    def add_points(self, collection_name: str, points: List[PointStruct], wait: bool = True):
        """Add points to the collection."""
        return self.client.upsert(
            collection_name=collection_name,
            wait=wait,
            points=points
        )

    def search(self, collection_name: str, query_vector: List[float], limit: int = 5):
        """Search for similar vectors in the collection."""
        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )

    def delete_collection(self, collection_name: str):
        """Delete the collection."""
        self.client.delete_collection(collection_name=collection_name)

# Usage example
if __name__ == "__main__":
    vector_store = VectorStore(url="http://localhost:6333")
    
    # Create a collection
    vector_store.create_collection(
        collection_name="test_collection",
        vector_size=4,
        distance=Distance.DOT
    )
    
    # Add points
    points = [
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
        PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
    ]
    operation_info = vector_store.add_points("test_collection", points)
    print(operation_info)
    
    # Search
    results = vector_store.search("test_collection", query_vector=[0.2, 0.3, 0.4, 0.5], limit=3)
    for result in results:
        print(f"ID: {result.id}, Score: {result.score}, Payload: {result.payload}")