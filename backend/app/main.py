from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from .utils import process_file

app = FastAPI()

app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")

@app.post("/api/process")
async def process(
    file: UploadFile = File(...),
    file_type: str = Form(...),
    width: int = Form(None),
    height: int = Form(None),
    quality: str = Form(None)
):
    if file.size > 30 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 30MB limit.")

    output_path = process_file(file, file_type, width, height, quality)
    return FileResponse(output_path, filename=os.path.basename(output_path))