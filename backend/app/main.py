import os
import requests
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from .utils import process_file
from .rate_limit import rate_limit_middleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()
app.middleware("http")(rate_limit_middleware)

# Global exception handler for unhandled server errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong. Please try again later."}
    )

def verify_recaptcha(token: str):
    if os.getenv("DISABLE_CAPTCHA") == "true":
        print("⚠️ CAPTCHA verification is disabled for testing")
        return

    secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
    if not secret_key:
        raise HTTPException(status_code=500, detail="reCAPTCHA secret key not configured")
    
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": secret_key, "response": token}
    )
    result = response.json()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail="Invalid reCAPTCHA verification")

@app.post("/api/process")
async def process(
    file: UploadFile = File(...),
    file_type: str = Form(...),
    width: str = Form(None),
    height: str = Form(None),
    quality: str = Form(None),
    captcha_token: str = Form(...)
):
    # Validate reCAPTCHA token first
    verify_recaptcha(captcha_token)

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
