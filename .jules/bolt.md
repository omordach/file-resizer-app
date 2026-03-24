## 2024-03-22 - Prevented React memory leaks in FileResizerForm
**Learning:** Object URLs generated via `URL.createObjectURL(file)` were causing memory leaks and unneeded re-evaluations on every render.
**Action:** Always wrap Object URLs in `useEffect` hooks with cleanup functions (`URL.revokeObjectURL`) to maintain memory efficiency, particularly when components can frequently re-render or be unmounted.

## 2024-03-22 - FastAPI Blocking Synchronous Calls
**Learning:** Using `async def` for FastAPI endpoints that execute blocking synchronous code (like `subprocess.run()`) causes the entire asyncio event loop to block, halting concurrent request processing.
**Action:** Always define endpoints containing heavy synchronous I/O or processing as standard `def` instead of `async def` in FastAPI, which delegates the execution to an internal threadpool.

## 2024-03-24 - O(N) Overhead in Middleware Global State Cleanup
**Learning:** Performing a global state cleanup (like pruning expired items from a dictionary of thousands of connected clients) on every single request in a middleware converts what should be an O(1) request check into an O(N) operation per request, killing server throughput.
**Action:** Always decouple periodic maintenance tasks from the hot path. If they must run synchronously, amortize the cost by restricting execution frequency to at most once per time window (e.g. check if `now - last_cleanup > window_seconds`). When scanning list timestamps, check the last element `timestamp[-1]` instead of `any()` scanning the full list, as timestamps are chronological.
