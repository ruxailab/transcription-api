# Transcription API

## Project Setup

### 1. Activate Virtual Environment

```bash
$ source venv/bin/activate
```

### 2. Install Dependencies (if needed)

```bash
$ pip install -r requirements.txt
```

### 3. Run the API

```bash
$ uvicorn app.main:app --reload
```

## Run Tests

All commands below should be run from the project root.

### All Tests

```bash
$ pytest
```

### Unit Tests Only

```bash
$ pytest ./tests/unit
```

### Integration Tests Only

```bash
$ pytest ./tests/integration
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc UI: http://localhost:8000/redoc
