# File Resizer App

A web-based tool to resize Images and PDFs using FastAPI, ImageMagick, and Ghostscript. Fully containerized with Docker.

## ✅ Build and Run


### **Docker Build & Run**

#### Build Docker Image

```bash
docker build -t file-resizer-app -f backend/Dockerfile .
```

#### Run Docker Container

```bash
docker run -p 8080:8080 file-resizer-app
```

Access the app at [http://localhost:8080](http://localhost:8080).

---

### 4. **Docker Compose Alternative**

If you prefer **docker-compose**, use:

```bash
docker-compose up --build
```

And stop with:

```bash
docker-compose down
```
