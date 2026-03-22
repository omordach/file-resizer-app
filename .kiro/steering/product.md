# Product Overview

File Resizer App is a web-based tool for resizing images (JPG, PNG) and PDF files. Users upload files through a drag-and-drop interface, specify dimensions and quality settings, and receive processed files.

## Key Features

- Image resizing with custom width/height/quality parameters
- PDF resizing using Ghostscript
- File size limit: 30MB per upload
- reCAPTCHA protection against abuse
- Rate limiting middleware for API protection
- Fully containerized deployment with Docker

## User Flow

1. Upload file via drag-and-drop or file picker
2. Select file type (Image or PDF)
3. Specify dimensions (width/height) and quality
4. Complete reCAPTCHA verification
5. Process and download resized file
