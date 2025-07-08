import os
import pytest
from unittest.mock import patch, MagicMock
from app.services.providers.open_ai import OpenAIProvider
from fastapi import HTTPException


def test_openai_provider_invalid_url_format():
    provider = OpenAIProvider(model_name="whisper-1")

    with pytest.raises(
        ValueError,
        match=r"Invalid URL format.",
    ):
        provider.transcribe("invalid")


def test_openai_provider_invalid_url():
    provider = OpenAIProvider(model_name="whisper-1")

    with pytest.raises(
        HTTPException,
        match=r"Failed to fetch audio:.*",
    ):
        provider.transcribe("http://nonexistent.local/audio.mp3")


from openai import APIConnectionError


@patch.dict(os.environ, {"OPENAI_API_KEY": "fake-key"})
@patch("app.services.providers.open_ai.OpenAI")
@patch("app.services.providers.open_ai.requests.get")
def test_openai_provider_server_unavailable(mock_requests_get, mock_openai_class):
    # Fake audio content download
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.content = b"fake-mp3-audio-bytes"

    # Setup mock OpenAI client that raises APIConnectionError
    mock_transcriptions = MagicMock()
    mock_transcriptions.create.side_effect = APIConnectionError(
        message="Server down", request=None
    )

    mock_audio = MagicMock()
    mock_audio.transcriptions = mock_transcriptions

    mock_client = MagicMock()
    mock_client.audio = mock_audio

    mock_openai_class.return_value = mock_client

    provider = OpenAIProvider(model_name="whisper-1")

    with pytest.raises(HTTPException) as exc_info:
        provider.transcribe("https://example.com/audio.mp3")

    assert exc_info.value.status_code == 503
    assert "unavailable" in str(exc_info.value.detail).lower()


@patch.dict(os.environ, {"OPENAI_API_KEY": "fake-key"})
@patch("app.services.providers.open_ai.requests.get")
@patch("app.services.providers.open_ai.OpenAI")
def test_openai_provider_success(mock_openai_class, mock_get):
    # Fake audio content
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"fake-mp3-audio-bytes"

    # 2. Mock OpenAI client + response
    mock_audio_file = MagicMock()
    mock_audio_file.model_dump.return_value = {
        "text": "Test transcription",
        "language": "english",
        "segments": [{"start": 0.0, "end": 2.0, "text": "Test transcription"}],
    }

    # Setup nested attributes: client.audio.transcriptions.create(...)
    mock_transcriptions = MagicMock()
    mock_transcriptions.create.return_value = mock_audio_file

    mock_audio = MagicMock()
    mock_audio.transcriptions = mock_transcriptions

    mock_client = MagicMock()
    mock_client.audio = mock_audio

    # Ensure OpenAI() returns this mock client
    mock_openai_class.return_value = mock_client

    provider = OpenAIProvider(model_name="whisper-1")
    result = provider.transcribe("https://example.com/audio.mp3")

    assert result["transcript"] == "Test transcription"
    assert result["language"] == "english"
    assert isinstance(result["segments"], list)
