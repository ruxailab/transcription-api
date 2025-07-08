from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_transcribe_invalid_provider():
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


def test_transcribe_invalid_model_for_whisper():
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
    assert "Model 'any' is not valid for provider 'whisper'" in str(data)


def test_transcribe_invalid_url():
    response = client.post(
        "/api/v1/transcribe",
        json={"audio_url": "not-a-valid-url", "provider": "whisper", "model": "tiny"},
    )
    assert response.status_code == 422  # Pydantic will reject invalid HttpUrl
    data = response.json()
    assert data["status"] == "error"
    assert "audio_url" in data["details"]


def test_transcribe_whisper_tiny_success():
    response = client.post(
        "/api/v1/transcribe",
        json={
            "audio_url": "https://thevoiceovervoice.co.uk/wp-content/uploads/Posy_British-English_Trailer-Demo.mp3",
            "provider": "whisper",
            "model": "tiny",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["provider"] == "whisper"
    assert data["model"] == "tiny"
    assert (
        "transcript" in data
        and isinstance(data["transcript"], str)
        and len(data["transcript"]) > 0
    )

    # Validate language
    assert "language" in data and isinstance(data["language"], str)

    # Validate segments
    assert "segments" in data and isinstance(data["segments"], list)
    for segment in data["segments"]:
        assert "start" in segment and isinstance(segment["start"], (int, float))
        assert "end" in segment and isinstance(segment["end"], (int, float))
        assert "text" in segment and isinstance(segment["text"], str)


# # Uncomment this test if you have OpenAI API key configured (Takes Cost :D)
# def test_transcribe_openai_whisper_1_success():
#     response = client.post(
#         "/api/v1/transcribe",
#         json={
#             "audio_url": "https://thevoiceovervoice.co.uk/wp-content/uploads/Posy_British-English_Trailer-Demo.mp3",
#             "provider": "openai",
#             "model": "whisper-1",  # OpenAI's Whisper model
#         },
#     )

#     assert response.status_code == 200
#     data = response.json()

#     assert data["status"] == "success"
#     assert data["provider"] == "openai"
#     assert data["model"] == "whisper-1"
#     assert (
#         "transcript" in data
#         and isinstance(data["transcript"], str)
#         and len(data["transcript"]) > 0
#     )

#     # Validate language
#     assert "language" in data and isinstance(data["language"], str)

#     # Validate segments
#     assert "segments" in data and isinstance(data["segments"], list)
#     for segment in data["segments"]:
#         assert "start" in segment and isinstance(segment["start"], (int, float))
#         assert "end" in segment and isinstance(segment["end"], (int, float))
#         assert "text" in segment and isinstance(segment["text"], str)
