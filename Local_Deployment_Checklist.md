# File Resizer App

A lightweight web tool to resize images or PDFs directly in your browser.

---

## ✅ Deployment Checklist

### 🛠️ Local Development Checklist

1. **Clone Repository**

   ```bash
   git clone <your-repo-url>
   cd file-resizer-app
   ```

2. **Install Frontend Dependencies & Build**

   ```bash
   cd frontend
   npm install
   npm run build
   ```

3. **Run Backend Locally**

   ```bash
   cd ../backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

4. **Access the Application**

   * Open: [http://localhost:8000](http://localhost:8000)

---

### 🐳 Docker Deployment Checklist

1. **Build Frontend**

   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Build Docker Image**

   ```bash
   cd ../backend
   docker build -t file-resizer-app .
   ```

3. **Run Docker Container Locally**

   ```bash
   docker run -p 8000:8000 file-resizer-app
   ```

4. **Tag Docker Image (Optional)**

   ```bash
   docker tag file-resizer-app your-dockerhub-username/file-resizer-app:latest
   ```

5. **Push Docker Image to Docker Hub (Optional)**

   ```bash
   docker push your-dockerhub-username/file-resizer-app:latest
   ```

6. **Access the Application**

   * Open: [http://localhost:8000](http://localhost:8000)

---

## ✅ Health Check

* **Endpoint**: `GET /health`
* **Example**:

  ```bash
  curl http://localhost:8000/health
  ```
* **Expected Response**:

  ```json
  {"status": "ok"}
  ```

---

## ✅ Operational Notes

* **Max upload file size**: 30 MB
* **Logs**: Console or Docker logs
* **Data Handling**: No data retention (stateless)
