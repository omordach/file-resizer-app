# Technology Stack

## Backend

- **Framework**: FastAPI (Python 3.11)
- **Server**: Uvicorn ASGI server
- **Image Processing**: Pillow (PIL), ImageMagick
- **PDF Processing**: Ghostscript
- **Testing**: pytest, httpx
- **Environment**: python-dotenv for configuration

## Frontend

- **Framework**: React 18.x
- **Build Tool**: Vite 6.x
- **Styling**: TailwindCSS 3.4.x with PostCSS 8.x and Autoprefixer 10.x
- **UI Components**: Radix UI primitives (label, select, slot)
- **Utilities**: clsx 2.x, tailwind-merge 3.x, class-variance-authority 0.7.x
- **Icons**: lucide-react 0.556.x
- **File Upload**: react-dropzone 14.x
- **Security**: react-google-recaptcha 3.x
- **Testing**: Playwright 1.57.x for E2E tests

## Infrastructure

- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose
- **Base Images**: node:20 (frontend build), python:3.11-slim (backend)

## Common Commands

### Development

```bash
# Backend (local)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Frontend (local)
cd frontend
npm install
npm run dev

# Backend tests
cd backend
pytest

# Frontend E2E tests
cd frontend
npx playwright test
```

### Docker

```bash
# Build and run with Docker
docker build -t file-resizer-app -f backend/Dockerfile .
docker run -p 8080:8080 file-resizer-app

# Build and run with Docker Compose
docker-compose up --build
docker-compose down
```

### Environment Variables

- `RECAPTCHA_SECRET_KEY`: Google reCAPTCHA secret key
- `DISABLE_CAPTCHA`: Set to "true" to bypass reCAPTCHA (testing only)
- `PORT`: Server port (default: 8080)
- `PYTHONPATH`: Set to /app in Docker environment
