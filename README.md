# File Resizer App

A lightweight web tool to resize images or PDFs directly in your browser.

---

## ✅ Project Structure

```
file-resizer-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── utils.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── FileUploadForm.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

---

## ✅ Deployment & Usage Instructions (Local & Docker)

### 🛠️ Local Development & Testing

#### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd file-resizer-app
```

#### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
npm run build
```

> This will build the frontend and place it in `backend/static`.

#### 3. Run Backend Locally (Python Environment Required)

```bash
cd ../backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> Access the app at [http://localhost:8000](http://localhost:8000).

---

### 🐳 Docker Deployment (All-in-One)

#### 1. Build the Frontend

```bash
cd frontend
npm install
npm run build
```

#### 2. Build Docker Image

```bash
cd ../backend
docker build -t file-resizer-app .
```

#### 3. Run Docker Container Locally

```bash
docker run -p 8000:8000 file-resizer-app
```

> Access the app at [http://localhost:8000](http://localhost:8000).

#### 4. Tag Docker Image (Optional, for Pushing)

```bash
docker tag file-resizer-app your-dockerhub-username/file-resizer-app:latest
```

#### 5. Push Docker Image to Docker Hub (Optional)

```bash
docker push your-dockerhub-username/file-resizer-app:latest
```

---

## ✅ Health Check

The application exposes a simple health check endpoint:

* **GET /health**

Example usage:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok"}
```

---

## ✅ Notes

* **Max upload file size**: 30 MB
* **Logs**: Available in Docker or Python console output
* **Data Handling**: Stateless, no user data retention

---

## ✅ .gitignore Example

```
# Node dependencies
frontend/node_modules

# Build outputs
frontend/dist

# Python
__pycache__/
*.pyc

# Docker
**/static/

# OS
.DS_Store

# Environment files
.env
```

---

## ✅ Contributing

1. Fork this repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

We welcome contributions that improve functionality, UX, or documentation.

---

## ✅ License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## ✅ Changelog

### v1.0.0

* Initial release with:

  * PDF resizing
  * Image resizing
  * Dockerized deployment
  * React + FastAPI integration
