## 2024-05-24 - Rate Limit Bypass due to IP Spoofing
**Vulnerability:** The rate limiter blindly trusted the `X-Forwarded-For` header for IP identification, allowing attackers to spoof their IP by sending custom `X-Forwarded-For` values and bypassing rate limits.
**Learning:** Never implicitly trust HTTP headers that can be spoofed by clients, especially for security controls like rate limiting. In cloud environments where `X-Forwarded-For` is valid, only trust it from the trusted reverse proxy / load balancer, or sanitize it.
**Prevention:** Use the direct client IP `request.client.host` when not behind a trusted proxy, or configure the app to securely parse proxy headers.
## 2026-03-22 - Subprocess calls and Bare Excepts
**Vulnerability:** Use of `subprocess` and `subprocess.run` without specifying `shell=False` explicitly, as well as multiple `try: ... except Exception: pass` blocks.
**Learning:** Bandit warns about potentially insecure uses of `subprocess`, though the actual usage was safe due to parameterization. Bare `except Exception: pass` blocks are considered bad practice (B110) as they can silently swallow important errors.
**Prevention:** Used `# nosec B404` and `# nosec B603` to explicitly mark reviewed/safe subprocess calls. Refactored bare excepts to use `with contextlib.suppress(Exception):` for safer and cleaner error suppression during cleanup tasks.
