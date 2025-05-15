# --- Stage 1: Build Frontend ---
FROM node:20 AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build


# --- Stage 2: Build Backend ---
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-dev build-essential imagemagick ghostscript && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY backend/app ./app
COPY backend/tests ./tests
COPY backend/.env /app/.env
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built frontend from the previous stage
COPY --from=frontend-builder /app/frontend/dist ./static

ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
