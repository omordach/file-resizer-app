## 2024-03-22 - [Missing File Extension Validation]
**Vulnerability:** The application accepts any file extension and passes it to ImageMagick/Ghostscript, allowing potential processing of malicious SVGs, HTMLs, or other dangerous file formats.
**Learning:** Even though `NamedTemporaryFile` randomizes the base name, it preserves the user-supplied extension. ImageMagick relies on extensions to determine delegates, which can trigger dangerous parsers.
**Prevention:** Always use an allowlist of strictly safe file extensions (e.g., .jpg, .png, .pdf) and validate the `content_type` before processing files.
