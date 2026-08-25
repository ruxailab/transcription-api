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
python3.12 -m venv env
source env/bin/activate
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

---
## 🛠️ Deployment Guide

The API is deployed as a **CPU-only** Dockerized FastAPI service on **Google Cloud Run**. Shared deploy logic lives in [`.github/workflows/deploy-reusable.yml`](.github/workflows/deploy-reusable.yml); callers trigger it per branch:

| Branch | Workflow | Cloud Run service |
|---|---|---|
| `main` | [`deploy-prod.yml`](.github/workflows/deploy-prod.yml) | `transcription-api` |
| `develop` | [`deploy-dev.yml`](.github/workflows/deploy-dev.yml) | `transcription-api-dev` |

| Setting | Value |
|---|---|
| Project | `ruxailab-develop` |
| Region | `us-central1` |
| Artifact Registry repo | `containers` |
| Image | `transcription-api` |
| Resources | 2 CPU · 8 Gi memory · port 8000 |
| Runtime device | `DEVICE=cpu` |

### Prerequisites

- Google Cloud project with billing enabled
- Artifact Registry repository `containers` in `us-central1`
- APIs enabled: Artifact Registry, Cloud Run
- GitHub repository secrets:
  - **`GCP_SA_KEY_PROD`** — JSON key for the production GCP service account (used by `deploy-prod.yml`)
  - **`GCP_SA_KEY_DEV`** — JSON key for the development GCP service account (used by `deploy-dev.yml`)
  - **`OPENAI_API_KEY_PROD`** / **`OPENAI_API_KEY_DEV`** — injected into the matching Cloud Run service as an env var

### Automatic deploy (recommended)

1. Configure the secrets above in the GitHub repository settings.
2. Push (or merge) to `main` (prod) or `develop` (dev).
3. The workflow will:
   - Authenticate to GCP with `GCP_SA_KEY_PROD` or `GCP_SA_KEY_DEV` (mapped to `GCP_SA_KEY` in the reusable workflow)
   - Build and push `us-central1-docker.pkg.dev/ruxailab-develop/containers/transcription-api:sha-<short-sha>`
   - Deploy the image to the matching Cloud Run service with `DEVICE=cpu` and `OPENAI_API_KEY`

### Manual deploy (optional)

Use this only when you need to deploy outside CI (e.g. a hotfix from a local machine).

```bash
PROJECT_ID="ruxailab-develop"
REGION="us-central1"
REPO="containers"
IMAGE="transcription-api"
SERVICE="transcription-api"
TAG="sha-$(git rev-parse --short HEAD)"
IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE}:${TAG}"

gcloud auth login
gcloud config set project "$PROJECT_ID"
gcloud auth configure-docker "${REGION}-docker.pkg.dev"

docker build -t "${IMAGE_URI}" .
docker push "${IMAGE_URI}"

gcloud run deploy "${SERVICE}" \
  --image "${IMAGE_URI}" \
  --region "${REGION}" \
  --allow-unauthenticated \
  --cpu 2 \
  --memory 2Gi \
  --port 8000 \
  --set-env-vars "DEVICE=cpu,OPENAI_API_KEY=${OPENAI_API_KEY}"
```

<!-- GSoC Docs -->
## GSoC Docs <a id="gsoc"></a>
This repository is part of the [Google Summer of Code (GSoC) 2025](https://summerofcode.withgoogle.com/) program.

- **Contributor:** [Basma Elhoseny](https://github.com/basmaelhoseny01)
- **Mentors:** [Karine](https://github.com/KarinePistili) - [Marc](https://github.com/marcgc21)

> ### 🔗 Useful Links
> - 🧠 **GSoC'25 Project Page:** [Transcription Tool for Usability Testing GSoC 25 Program](https://summerofcode.withgoogle.com/programs/2025/projects/aOHlFhUA)  
> - 🧾 **Proof of Work:** [gsoc_2025_summary.md](https://github.com/ruxailab/transcription-api/blob/main/gsoc_2025_summary.md)

<!-- License -->
## <img align="center" height="60px" src="https://cdn-icons-png.freepik.com/512/1046/1046441.png"> License <a id="license"></a>
This software is licensed under the MIT License. See the [LICENSE](https://github.com/ruxailab/transcription-api/blob/main/LICENSE) file for more information.
<div align="center">
    © 2025 RUXAILAB.
</div>

