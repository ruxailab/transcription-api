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
