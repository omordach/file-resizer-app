import time
from fastapi import Request, HTTPException

class RateLimiter:
    def __init__(self, limit: int = 20, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clients = {}  # { client_ip: [timestamps] }

    def check(self, client_ip: str):
        now = time.time()
        window_start = now - self.window_seconds

        # Initialize if client not tracked yet
        if client_ip not in self.clients:
            self.clients[client_ip] = []

        # Filter timestamps that are still in the current window
        request_times = [ts for ts in self.clients[client_ip] if ts > window_start]
        request_times.append(now)  # Add current request timestamp

        self.clients[client_ip] = request_times

        if len(request_times) > self.limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    try:
        rate_limiter.check(client_ip)
    except HTTPException as e:
        raise e
    response = await call_next(request)
    return response
