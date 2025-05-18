import time
from fastapi import Request, HTTPException

class RateLimiter:
    def __init__(self, limit: int = 20, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clients = {}  # { client_ip: [timestamps] }

    def cleanup(self):
        now = time.time()
        window_start = now - self.window_seconds
        # Keep only active IPs with recent requests
        self.clients = {
            ip: [ts for ts in timestamps if ts > window_start]
            for ip, timestamps in self.clients.items()
            if any(ts > window_start for ts in timestamps)
        }

    def check(self, client_ip: str):
        now = time.time()
        window_start = now - self.window_seconds

        # Cleanup old records before checking
        self.cleanup()

        if client_ip not in self.clients:
            self.clients[client_ip] = []

        # Filter timestamps that are still in the window
        request_times = [ts for ts in self.clients[client_ip] if ts > window_start]
        request_times.append(now)

        self.clients[client_ip] = request_times

        if len(request_times) > self.limit:
            print(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    # Skip static assets from rate limiting
    if request.url.path.startswith("/assets") or request.url.path in ["/favicon.ico", "/manifest.json", "/robots.txt"]:
        return await call_next(request)

    client_ip = request.client.host
    try:
        rate_limiter.check(client_ip)
    except HTTPException as e:
        raise e

    response = await call_next(request)
    return response
