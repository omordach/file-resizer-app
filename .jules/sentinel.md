## 2024-05-24 - Rate Limit Bypass due to IP Spoofing
**Vulnerability:** The rate limiter blindly trusted the `X-Forwarded-For` header for IP identification, allowing attackers to spoof their IP by sending custom `X-Forwarded-For` values and bypassing rate limits.
**Learning:** Never implicitly trust HTTP headers that can be spoofed by clients, especially for security controls like rate limiting. In cloud environments where `X-Forwarded-For` is valid, only trust it from the trusted reverse proxy / load balancer, or sanitize it.
**Prevention:** Use the direct client IP `request.client.host` when not behind a trusted proxy, or configure the app to securely parse proxy headers.
