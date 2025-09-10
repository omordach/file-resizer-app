# --- Stage 1: Build Frontend ---
FROM node:20 AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build


# --- Stage 2: Build Backend ---
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    imagemagick \
    ghostscript \
    wget \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN useradd -m appuser
COPY backend/app ./app
COPY backend/tests ./tests
#COPY backend/.env /app/.env
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built frontend from the previous stage
COPY --from=frontend-builder /app/frontend/dist ./static

# Ensure non-root can access working directory and static files
RUN chown -R appuser:appuser /app
USER appuser

ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
 CMD wget -qO- http://127.0.0.1:${PORT}/healthz || exit 1
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
