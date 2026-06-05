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

def test_get_server():
    payload = {"name": "Test", "host": "127.0.0.1", "port": 80}
    headers = {"X-API-Key": "dev-secret-key"}
    create_resp = client.post("/servers", json=payload, headers=headers)
    server_id = create_resp.json()["id"]

    get_resp = client.get(f"/servers/{server_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == server_id

def test_get_nonexistent_server():
    response = client.get("/servers/nonexistent-id")
    assert response.status_code == 404

def test_delete_server():
    payload = {"name": "Test", "host": "127.0.0.1", "port": 80}
    headers = {"X-API-Key": "dev-secret-key"}
    create_resp = client.post("/servers", json=payload, headers=headers)
    server_id = create_resp.json()["id"]

    # Delete unauthorized
    del_resp_unauth = client.delete(f"/servers/{server_id}")
    assert del_resp_unauth.status_code == 403

    # Delete success
    del_resp = client.delete(f"/servers/{server_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["id"] == server_id

    # Delete nonexistent
    del_resp_non = client.delete(f"/servers/nonexistent-id", headers=headers)
    assert del_resp_non.status_code == 404

def test_check_server():
    payload = {"name": "Test", "host": "127.0.0.1", "port": 80}
    headers = {"X-API-Key": "dev-secret-key"}
    create_resp = client.post("/servers", json=payload, headers=headers)
    server_id = create_resp.json()["id"]

    # Check success
    check_resp = client.post(f"/servers/{server_id}/check")
    assert check_resp.status_code == 200
    assert check_resp.json()["status"] == "check initiated"

    # Check nonexistent
    check_resp_non = client.post(f"/servers/nonexistent-id/check")
    assert check_resp_non.status_code == 404

def test_get_servers_filtered():
    payload = {"name": "Test", "host": "127.0.0.1", "port": 80}
    headers = {"X-API-Key": "dev-secret-key"}
    client.post("/servers", json=payload, headers=headers)
    
    # Filter by unknown status
    get_resp = client.get("/servers?status=unknown")
    assert get_resp.status_code == 200
    assert len(get_resp.json()) == 1

    # Filter by UP status
    get_resp_up = client.get("/servers?status=UP")
    assert get_resp_up.status_code == 200
    assert len(get_resp_up.json()) == 0
