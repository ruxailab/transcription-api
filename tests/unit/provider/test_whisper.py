import pytest
from unittest.mock import patch, MagicMock
from app.services.providers.whisper_local import WhisperLocalProvider


def test_whisper_provider_invalid_url():
    provider = WhisperLocalProvider(model_size="tiny")

    with pytest.raises(
        RuntimeError,
        match=r"Failed to load audio:.*",
    ):
        provider.transcribe("https://invalid-url.com/audio.mp3")


@patch("app.services.providers.whisper_local.get_whisper_model")
@patch("app.services.providers.whisper_local.requests.get")
def test_whisper_provider_success(mock_get, mock_load_model):
    # Fake audio content
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"fake-audio-bytes"

    # Mock the whisper model's transcribe function
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {
        "text": "Hello world",
        "language": "en",
        "segments": [{"start": 0.0, "end": 1.0, "text": "Hello world"}],
        "duration": 1.0,
    }
    mock_load_model.return_value = mock_model

    provider = WhisperLocalProvider(model_size="tiny")
    result = provider.transcribe("https://example.com/audio.mp3")

    assert result["transcript"] == "Hello world"
    assert result["language"] == "en"
    assert "segments" in result
