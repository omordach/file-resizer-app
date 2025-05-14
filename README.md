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


### 🐳 Docker Deployment (All-in-One)

#### 1. Build the Frontend

```bash
cd frontend
npm install
npm run build
```

#### 2. Build Docker Image

From the root directory of the project, run:
```bash
docker build -t file-resizer-app -f backend/Dockerfile .
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
