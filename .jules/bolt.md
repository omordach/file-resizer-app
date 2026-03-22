## 2024-03-22 - Prevented React memory leaks in FileResizerForm
**Learning:** Object URLs generated via `URL.createObjectURL(file)` were causing memory leaks and unneeded re-evaluations on every render.
**Action:** Always wrap Object URLs in `useEffect` hooks with cleanup functions (`URL.revokeObjectURL`) to maintain memory efficiency, particularly when components can frequently re-render or be unmounted.

## 2024-03-22 - FastAPI Blocking Synchronous Calls
**Learning:** Using `async def` for FastAPI endpoints that execute blocking synchronous code (like `subprocess.run()`) causes the entire asyncio event loop to block, halting concurrent request processing.
**Action:** Always define endpoints containing heavy synchronous I/O or processing as standard `def` instead of `async def` in FastAPI, which delegates the execution to an internal threadpool.
