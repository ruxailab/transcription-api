from functools import lru_cache
import whisper
import requests
import tempfile

from fastapi import HTTPException

# Base Provider
from app.services.providers.base import BaseProvider


@lru_cache(maxsize=4)  # Cache up to 4 model sizes: "tiny", "base", "medium", "large"
def get_whisper_model(model_size: str):
    print(f"🔁 Loading Whisper model: {model_size}")
    return whisper.load_model(model_size)


class WhisperLocalProvider(BaseProvider):
    def __init__(self, model_size: str):
        """
        Initialize the WhisperLocalProvider with a specific model size.
        :param model_size: Size of the Whisper model to load (e.g., "tiny", "base", "medium", "large").
        """
        print(f"⚙️ Instantiating WhisperLocalProvider with: {model_size}")
        self.model = get_whisper_model(model_size)

    def transcribe(self, audio_url: str) -> dict:
        # Download audio file
        try:
            response = requests.get(audio_url)
            response.raise_for_status()
        except requests.exceptions.MissingSchema:
            raise ValueError("Invalid URL format.")
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=422, detail=f"Failed to fetch audio: {str(e)}"
            )

        # with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as tmp:
        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
            tmp.write(response.content)
            tmp.flush()

            # Transcribe with Whisper
            result = self.model.transcribe(tmp.name)

        return {
            "transcript": result["text"],
            "language": result.get("language"),
            "segments": result.get("segments"),
        }
