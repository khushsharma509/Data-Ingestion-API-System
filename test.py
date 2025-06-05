import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ingest_and_status():
    # Test ingestion
    response = client.post("/ingest", json={"ids": [1,2,3,4,5], "priority": "HIGH"})
    assert response.status_code == 200
    ingestion_id = response.json()["ingestion_id"]
    
    # Test status
    status_response = client.get(f"/status/{ingestion_id}")
    assert status_response.status_code == 200
    data = status_response.json()
    assert data["ingestion_id"] == ingestion_id
    assert len(data["batches"]) == 2


def test_ingest_and_status_different_batch_sizes():
    # Test ingestion with 4 IDs (should create 2 batches: [1,2,3], [4])
    response = client.post("/ingest", json={"ids": [1, 2, 3, 4], "priority": "MEDIUM"})
    assert response.status_code == 200
    ingestion_id = response.json()["ingestion_id"]

    # Test status
    status_response = client.get(f"/status/{ingestion_id}")
    assert status_response.status_code == 200
    data = status_response.json()
    assert data["ingestion_id"] == ingestion_id
    assert len(data["batches"]) == 2
    assert data["batches"][0]["ids"] == [1, 2, 3]
    assert data["batches"][1]["ids"] == [4]

def test_ingest_and_status_single_batch():
    # Test ingestion with 3 IDs (should create 1 batch)
    response = client.post("/ingest", json={"ids": [7, 8, 9], "priority": "LOW"})
    assert response.status_code == 200
    ingestion_id = response.json()["ingestion_id"]

    # Test status
    status_response = client.get(f"/status/{ingestion_id}")
    assert status_response.status_code == 200
    data = status_response.json()
    assert data["ingestion_id"] == ingestion_id
    assert len(data["batches"]) == 1
    assert data["batches"][0]["ids"] == [7, 8, 9]
