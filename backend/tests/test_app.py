from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_serves_frontend():
    response = client.get("/")
    assert response.status_code == 200

def test_health_endpoints():
    r1 = client.get("/healthz")
    r2 = client.get("/readyz")
    assert r1.status_code == 200 and r1.json()["status"] == "ok"
    assert r2.status_code == 200 and r2.json()["status"] == "ready"
