from unittest.mock import patch, MagicMock
import pytest
from fastapi import HTTPException

from app.schemas.transcribe import (
    TranscribeRequest,
    TranscriptionProvider,
    TranscriptionModel,
)

from app.services.transcriber import TranscriptionManager


#### Whisper Local Provider Tests ####
@patch("app.services.transcriber.WhisperLocalProvider")
def test_transcription_manager_whisper_tiny_success(mock_whisper):
    # Setup mock behavior
    mock_instance = MagicMock()
    mock_instance.transcribe.return_value = {
        "transcript": "hello world",
        "language": "en",
        "segments": [{"start": 0.0, "end": 1.0, "text": "hello world"}],
    }
    mock_whisper.return_value = mock_instance

    # Prepare request
    request = TranscribeRequest(
        audio_url="https://example.com/audio.mp3",
        provider=TranscriptionProvider.whisper,
        model=TranscriptionModel.tiny,
    )

    # Call the manager
    response = TranscriptionManager.transcribe(request)

    # Assertions
    assert response.status == "success"
    assert response.transcript == "hello world"
    assert response.language == "en"
    assert response.model == "tiny"
    assert response.audio_url == request.audio_url
    assert response.provider == TranscriptionProvider.whisper
    assert isinstance(response.segments, list)


#### OpenAI Provider Tests ####
@patch("app.services.transcriber.OpenAIProvider")
def test_transcription_manager_openai_transcribe_failure(mock_openai_provider):
    mock_instance = MagicMock()
    mock_instance.transcribe.side_effect = HTTPException(
        status_code=503, detail="OpenAI service down"
    )
    mock_openai_provider.return_value = mock_instance

    request = TranscribeRequest(
        audio_url="https://example.com/audio.mp3",
        provider="openai",  # Using string if Enums are bypassed
        model="whisper-1",
    )

    with pytest.raises(HTTPException) as exc_info:
        TranscriptionManager.transcribe(request)

    assert exc_info.value.status_code == 503
    assert "down" in str(exc_info.value.detail).lower()


@patch("app.services.transcriber.OpenAIProvider")
def test_transcription_manager_openai_whisper_1_success(mock_openai_whisper):
    # Setup mock behavior
    mock_instance = MagicMock()
    mock_instance.transcribe.return_value = {
        "transcript": "hello world",
        "language": "en",
        "segments": [{"start": 0.0, "end": 1.0, "text": "hello world"}],
    }
    mock_openai_whisper.return_value = mock_instance

    # Prepare request
    request = TranscribeRequest(
        audio_url="https://example.com/audio.mp3",
        provider=TranscriptionProvider.openai,
        model=TranscriptionModel.whisper_1,
    )

    # Call the manager
    response = TranscriptionManager.transcribe(request)

    # Assertions
    assert response.status == "success"
    assert response.transcript == "hello world"
    assert response.language == "en"
    assert response.model == "whisper-1"
    assert response.audio_url == request.audio_url
    assert response.provider == TranscriptionProvider.openai
    assert isinstance(response.segments, list)


# pytest ./tests/unit/service/test_transcribe.py
