# Use Python slim image as base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install ImageMagick, Ghostscript, and other necessary dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    imagemagick \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files into the container
COPY ./backend/app ./app
COPY ./backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy frontend build files into the container (for static files)
COPY ./frontend/dist ./static

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Set the entrypoint for the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
