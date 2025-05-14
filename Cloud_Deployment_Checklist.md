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

## ✅ Cloud Deployment Checklist (When Ready)

1. **Push Docker Image to Container Registry**
   Example for Docker Hub:

   ```bash
   docker tag file-resizer-app your-dockerhub-username/file-resizer-app:latest
   docker push your-dockerhub-username/file-resizer-app:latest
   ```

2. **Deploy to Cloud Provider**

   * **AWS ECS / Fargate**

     * Create Task Definition
     * Use Docker Hub or ECR image
     * Expose port 8000

   * **Google Cloud Run**

     ```bash
     gcloud run deploy file-resizer-app \
       --image=gcr.io/YOUR_PROJECT_ID/file-resizer-app \
       --platform=managed \
       --region=YOUR_REGION \
       --allow-unauthenticated \
       --port=8000
     ```

   * **Azure Container Apps**

     * Create App with Docker Hub or Azure Container Registry image
     * Expose port 8000

3. **Configure Networking & SSL**

   * Ensure port 8000 is accessible
   * Set up HTTPS via cloud provider’s load balancer if needed

4. **Access Your Deployed Application**

   * Use the generated public URL from your cloud provider

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


