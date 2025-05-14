# File Resizer App

A web-based tool to resize Images and PDFs using FastAPI, ImageMagick, and Ghostscript. Fully containerized with Docker.

## ✅ Build and Run

### 1. **Frontend Setup with Shadcn UI**

#### Initialize Shadcn UI

```bash
cd frontend
npx shadcn@latest init
```

> **Note:**  
> If prompted, add a `jsconfig.json` with the following content to support `@/` alias:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

#### Add UI Components

```bash
npx shadcn@latest add button input select label card
```

#### Install Dependencies and Build Frontend

```bash
npm install
npm run build
```

---

### 2. **Backend Setup**

#### Install Python Dependencies

```bash
cd ../backend
pip install -r requirements.txt
```

#### (Optional) Run Locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

### 3. **Docker Build & Run**

#### Build Docker Image

```bash
docker build -t file-resizer-app -f backend/Dockerfile .
```

#### Run Docker Container

```bash
docker run -p 8000:8000 file-resizer-app
```

Access the app at [http://localhost:8000](http://localhost:8000).

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