import os
import sys
from fastapi.testclient import TestClient

# Ensure the backend app is importable regardless of where tests are run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app


client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200