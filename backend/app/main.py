import os
import logging
import requests
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask
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

logger = logging.getLogger("file-resizer-app")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

# Global exception handler for unhandled server errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong. Please try again later."}
    )

def verify_recaptcha(token: str):
    if os.getenv("DISABLE_CAPTCHA") == "true":
        logger.warning("CAPTCHA verification is disabled for testing")
        return

    secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
    if not secret_key:
        raise HTTPException(status_code=500, detail="reCAPTCHA secret key not configured")
    
    try:
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret_key, "response": token},
            timeout=5,
        )
        result = response.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to verify captcha")
    if not result.get("success"):
        raise HTTPException(status_code=400, detail="Invalid reCAPTCHA verification")


def get_client_ip(request: Request) -> str:
    # Prefer X-Forwarded-For (Cloud Run) then fall back
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/readyz")
async def readyz():
    # place lightweight checks here if needed
    return {"status": "ready"}

@app.post("/api/process")
async def process(
    request: Request,
    file: UploadFile = File(...),
    file_type: str = Form(...),
    width: str = Form(None),
    height: str = Form(None),
    quality: str = Form(None),
    captcha_token: str = Form(...),
):
    # Validate reCAPTCHA token first
    verify_recaptcha(captcha_token)

    # Safely convert width and height to integers if valid
    width = int(width) if width and width.isdigit() else None
    height = int(height) if height and height.isdigit() else None

    # Enforce size limit
    max_mb = int(os.getenv("MAX_UPLOAD_MB", "30"))
    max_bytes = max_mb * 1024 * 1024
    cl = request.headers.get("content-length")
    try:
        if cl and int(cl) > max_bytes:
            raise HTTPException(status_code=400, detail=f"File exceeds {max_mb}MB limit.")
    except ValueError:
        pass

    # Validate content type
    allowed_types = {
        "Image": {"image/jpeg", "image/png", "image/webp"},
        "PDF": {"application/pdf"},
    }
    ctype = getattr(file, "content_type", None)
    if file_type not in allowed_types or (ctype and ctype not in allowed_types[file_type]):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    output_path = process_file(file, file_type, width, height, quality, max_bytes=max_bytes)
    if not output_path:
        raise HTTPException(status_code=500, detail="Failed to process file. Check server logs.")

    return FileResponse(
        output_path,
        filename=os.path.basename(output_path),
        background=BackgroundTask(lambda p=output_path: os.remove(p) if os.path.exists(p) else None),
    )

# Mount static files after API routes
# Locally
# app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")
# Docker
app.mount("/", StaticFiles(directory="./static", html=True), name="frontend")
