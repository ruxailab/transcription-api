# 📝 Transcription API – Setup & Usage Guide

## ✅ Requirements

- Python **3.12** (⚠️ Do **not** use 3.13 – compatibility issues)
- FFmpeg (required for Whisper to process audio)

---

## ⚙️ Setup Instructions

### 1. Set Python Version (Optional if using `pyenv`)

```bash
pyenv local 3.12.3  # ensures 3.12.x is used in this directory
```

### 2. Create & Activate Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Install FFmpeg

```bash
brew install ffmpeg  # For macOS
# OR
sudo apt install ffmpeg  # For Ubuntu/Debian
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 🌐 Postman Collection

For testing the API endpoints, you can use the following Postman collection:

- [RuxAiLab Transcription Tool APIs Postman Collection](https://www.postman.com/ruxailab/ruxailab-workspace/collection/slzg8if/transcription-api)

---

## 🚀 Run the API Server

```bash
uvicorn app.main:app --reload
```

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc UI: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧺 Running Tests

> Make sure your virtual environment is activated before running tests.

### Run All Tests

```bash
pytest
```

### Unit Tests Only

```bash
pytest ./tests/unit
```

### Integration Tests Only

```bash
pytest ./tests/integration
```

---

## 🔊 Audio Sample Links (For Testing)

You can use sample audio files from:

**🔗** [https://thevoiceovervoice.co.uk/female-voice-over-samples/](https://thevoiceovervoice.co.uk/female-voice-over-samples/)


## Deployment Guide
Deploy a Dockerized FastAPI service to Google Cloud Run with NVIDIA L4 GPUs. Images are stored in Artifact Registry and built with Cloud Build.

### Prerequisites

- A Google Cloud project (e.g. `ruxailab-develop`)
- **gcloud CLI** installed: [Install guide](https://cloud.google.com/sdk/docs/install)
- Billing enabled on the GCP project

### Set your active project & region
```bash
# Project / region / registry
PROJECT_ID="ruxailab-develop"     # your-gcp-project
REGION="europe-west4"             # choose a region near you / with GPU
REPO="containers"                 # Artifact Registry repo name

# Image naming
IMAGE="transcription-api"
TAG="gpu-v1"                      # Change per New Releases :D

# Cloud Run service name
export SERVICE="transcription-api-gpu"
```

### Authenticate & set project/region
```bash
gcloud auth login

# Set your active project & region
gcloud config set project "$PROJECT_ID"
gcloud config set run/region "$REGION"
```

### Enable required APIs
```bash
gcloud services enable   artifactregistry.googleapis.com   run.googleapis.com   cloudbuild.googleapis.com
```

### Create Artifact Registry (Docker)
```bash
gcloud artifacts repositories create "$REPO"   --repository-format=docker   --location="$REGION"
```

### Build & Push the Image (Cloud Build)
```bash
gcloud builds submit   --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$TAG" .
```

### Deploy to Cloud Run with GPU (L4)
```bash
gcloud beta run deploy "$SERVICE"   --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$TAG"   --region "$REGION"   --allow-unauthenticated   --gpu 1   --gpu-type nvidia-l4   --cpu 4   --memory 16Gi   --concurrency 1   --no-cpu-throttling   --port 8000   --set-env-vars "DEVICE=cuda,OPENAI_API_KEY=YOUR_API_KEY_HERE"
```

### Updating to a New Version
```bash
export TAG="gpu-v2"
gcloud builds submit   --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$TAG" .

gcloud beta run deploy "$SERVICE"   --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$TAG"   --region "$REGION"   --allow-unauthenticated   --gpu 1   --gpu-type nvidia-l4   --cpu 4   --memory 16Gi   --concurrency 1   --no-cpu-throttling   --port 8000
```

### Optional: CPU-only Deployment
```bash
export TAG="v1"
gcloud builds submit   --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$TAG" .

gcloud run deploy "transcription-api"   --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$TAG"   --region "$REGION"   --allow-unauthenticated   --cpu 2   --memory 2Gi   --port 8000  --set-env-vars "DEVICE=cuda,OPENAI_API_KEY=YOUR_API_KEY_HERE"
```

