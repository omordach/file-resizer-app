import asyncio
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

for _ in range(21):
    response = client.get("/healthz")

print(response.status_code)
print(response.text)
