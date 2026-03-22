## 2024-03-22 - Prevented React memory leaks in FileResizerForm
**Learning:** Object URLs generated via `URL.createObjectURL(file)` were causing memory leaks and unneeded re-evaluations on every render.
**Action:** Always wrap Object URLs in `useEffect` hooks with cleanup functions (`URL.revokeObjectURL`) to maintain memory efficiency, particularly when components can frequently re-render or be unmounted.
