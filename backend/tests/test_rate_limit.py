import pytest
from fastapi import HTTPException
from app.rate_limit import RateLimiter

def test_allows_requests_within_limit():
    limiter = RateLimiter(limit=3, window_seconds=60)
    client_ip = "127.0.0.1"
    
    # Should allow up to 3 requests
    for _ in range(3):
        limiter.check(client_ip)  # Should not raise

def test_blocks_requests_above_limit():
    limiter = RateLimiter(limit=2, window_seconds=60)
    client_ip = "127.0.0.1"

    # First two should pass
    limiter.check(client_ip)
    limiter.check(client_ip)

    # Third should fail
    with pytest.raises(HTTPException) as exc_info:
        limiter.check(client_ip)
    
    assert exc_info.value.status_code == 429
    assert "Rate limit exceeded" in str(exc_info.value.detail)

def test_cleanup_removes_old_entries():
    limiter = RateLimiter(limit=2, window_seconds=1)  # 1 second window for testing
    client_ip = "127.0.0.1"

    # Fill the limit
    limiter.check(client_ip)
    limiter.check(client_ip)

    # Should now block
    with pytest.raises(HTTPException):
        limiter.check(client_ip)

    # Wait for window to expire
    import time
    time.sleep(1.1)

    # Cleanup and try again
    limiter.cleanup()
    limiter.check(client_ip)  # Should pass again after cleanup
