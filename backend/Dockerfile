FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ghostscript imagemagick && \
    pip install fastapi uvicorn python-multipart

WORKDIR /app
COPY ./app ./app
COPY ../frontend/dist ./static

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]