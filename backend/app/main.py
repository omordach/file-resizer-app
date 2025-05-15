from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from .utils import process_file
from .rate_limit import rate_limit_middleware

app = FastAPI()
app.middleware("http")(rate_limit_middleware)

@app.post("/api/process")
async def process(
    file: UploadFile = File(...),
    file_type: str = Form(...),
    width: str = Form(None),
    height: str = Form(None),
    quality: str = Form(None)
):
    # Safely convert width and height to integers if valid
    width = int(width) if width and width.isdigit() else None
    height = int(height) if height and height.isdigit() else None

    if file.size > 30 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 30MB limit.")

    output_path = process_file(file, file_type, width, height, quality)
    if not output_path:
        raise HTTPException(status_code=500, detail="Failed to process file. Check server logs.")

    return FileResponse(output_path, filename=os.path.basename(output_path))

# Mount static files after API routes
# Locally
# app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")
# Docker
app.mount("/", StaticFiles(directory="./static", html=True), name="frontend")
