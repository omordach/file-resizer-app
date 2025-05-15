import time
from fastapi import Request, HTTPException

class RateLimiter:
    def __init__(self, limit: int = 10, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.store = {}

    def check(self, ip: str):
        current_time = time.time()
        requests = self.store.get(ip, [])
        # Keep only recent requests
        requests = [req_time for req_time in requests if current_time - req_time < self.window_seconds]

        if len(requests) >= self.limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        requests.append(current_time)
        self.store[ip] = requests

rate_limiter = RateLimiter(limit=10, window_seconds=60)

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    rate_limiter.check(client_ip)
    return await call_next(request)
