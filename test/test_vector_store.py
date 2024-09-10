import sys
import os
# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from qdrant_client.models import Distance, PointStruct
from src.vector_store.vector_store import VectorStore

@pytest.fixture
def vector_store():
    return VectorStore(url="http://localhost:6333")

@pytest.fixture
def collection_name():
    return "test_healthcare_collection"

def test_create_collection(vector_store, collection_name):
    vector_store.create_collection(collection_name, vector_size=4, distance=Distance.COSINE)
    # If no exception is raised, we assume the collection was created successfully
    assert True

def test_add_points(vector_store, collection_name):
    points = [
        PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"symptom": "fever"}),
        PointStruct(id=2, vector=[0.2, 0.3, 0.4, 0.5], payload={"symptom": "cough"}),
    ]
    operation_info = vector_store.add_points(collection_name, points)
    assert operation_info.status == "completed"

def test_search(vector_store, collection_name):
    query_vector = [0.1, 0.2, 0.3, 0.4]
    results = vector_store.search(collection_name, query_vector, limit=1)
    assert len(results) == 1
    assert results[0].payload["symptom"] == "fever"

def test_delete_collection(vector_store, collection_name):
    vector_store.delete_collection(collection_name)
    # If no exception is raised, we assume the collection was deleted successfully
    assert True

if __name__ == "__main__":
    pytest.main()