import pytest
from app.rate_limit import rate_limiter

@pytest.fixture(autouse=True)
def reset_rate_limiter():
    rate_limiter.clients = {}
