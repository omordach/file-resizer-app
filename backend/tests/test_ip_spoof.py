import pytest
from fastapi.testclient import TestClient
from app.main import app
from fastapi.exceptions import HTTPException

client = TestClient(app)

def test_ip_spoofing_bypass():
    # To hit rate limit, we need 21 requests.
    try:
        for i in range(21):
            # Change X-Forwarded-For for each request
            headers = {"X-Forwarded-For": f"{100+i}.0.0.1, 1.2.3.4"}
            response = client.get("/healthz", headers=headers)
            assert response.status_code == 200, f"Failed at request {i}"

        # If we reach here, rate limit was bypassed
        assert False, "Success! Rate limiting was bypassed."
    except Exception as e:
        # Check if the exception is due to rate limit (429)
        assert getattr(e, "status_code", None) == 429 or response.status_code == 429 or "429" in str(e), "Expected rate limit to block spoofed IP"

if __name__ == "__main__":
    test_ip_spoofing_bypass()
