import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the devops-monitor folder to PYTHONPATH to import api modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from api.main import app, store

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_store():
    # Clear the servers store before each test
    store.clear()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_percent" in data

def test_create_server_unauthorized():
    payload = {
        "name": "Test Server",
        "host": "127.0.0.1",
        "port": 80
    }
    # No header X-API-Key
    response = client.post("/servers", json=payload)
    assert response.status_code == 403

    # Invalid header X-API-Key
    response = client.post("/servers", json=payload, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 403

def test_create_server_authorized_and_listed():
    payload = {
        "name": "Production Webserver",
        "host": "127.0.0.1",
        "port": 80
    }
    headers = {"X-API-Key": "dev-secret-key"}
    
    # Create server
    response = client.post("/servers", json=payload, headers=headers)
    assert response.status_code == 201
    server_data = response.json()
    assert "id" in server_data
    assert server_data["name"] == "Production Webserver"
    assert server_data["status"] == "unknown"
    
    # Get all servers
    get_response = client.get("/servers")
    assert get_response.status_code == 200
    servers_list = get_response.json()
    assert len(servers_list) == 1
    assert servers_list[0]["id"] == server_data["id"]

def test_get_nonexistent_server():
    response = client.get("/servers/nonexistent-id")
    assert response.status_code == 404
