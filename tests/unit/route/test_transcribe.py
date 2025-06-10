from fastapi.testclient import TestClient
from app.main import app

from unittest.mock import patch

client = TestClient(app)


def test_transcribe_route_invalid_provider():
    response = client.post(
        "/api/v1/transcribe",
        json={
            "audio_url": "https://example.com/audio.mp3",
            "provider": "invalid",  # Not yet supported
        },
    )
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert "provider" in data["details"]


def test_transcribe_route_invalid_model():
    response = client.post(
        "/api/v1/transcribe",
        json={
            "audio_url": "https://example.com/audio.mp3",
            "provider": "whisper",
            "model": "any",  # Not valid for whisper
        },
    )
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert "Model 'any' is not valid for provider 'whisper'" in str(data)


def test_transcribe_route_invalid_url():
    response = client.post(
        "/api/v1/transcribe",
        json={
            "audio_url": "not-a-valid-url",
            "provider": "whisper",
            "model": "tiny",
        },
    )
    assert response.status_code == 422  # Pydantic will reject invalid HttpUrl
    data = response.json()
    assert data["status"] == "error"
    assert "audio_url" in data["details"]


def test_transcribe_route_missing_audio_url():
    response = client.post(
        "/api/v1/transcribe",
        json={"provider": "whisper", "model": "tiny"},  # Missing audio_url
    )
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert "audio_url" in data["details"]


@patch("app.api.v1.transcribe.TranscriptionManager.transcribe")
def test_transcribe_route_success(mock_transcribe):
    mock_transcribe.return_value = {
        "status": "success",
        "provider": "whisper",
        "model": "tiny",
        "audio_url": "https://example.com/audio.mp3",
        "transcript": "Hello world",
        "language": "en",
        "segments": [
            {
                "start": 0.0,
                "end": 1.0,
                "text": "Hello",
                "confidence": 0.95,
            },
            {
                "start": 1.0,
                "end": 2.0,
                "text": "world",
                "confidence": 0.95,
            },
        ],
    }

    payload = {
        "provider": "whisper",
        "model": "tiny",
        "audio_url": "https://example.com/audio.mp3",
    }

    response = client.post("/api/v1/transcribe", json=payload)
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "status": "success",
        "provider": "whisper",
        "model": "tiny",
        "audio_url": "https://example.com/audio.mp3",
        "transcript": "Hello world",
        "language": "en",
        "segments": [
            {
                "start": 0.0,
                "end": 1.0,
                "text": "Hello",
                "confidence": 0.95,
            },
            {
                "start": 1.0,
                "end": 2.0,
                "text": "world",
                "confidence": 0.95,
            },
        ],
    }
