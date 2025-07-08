from openai import OpenAI
import requests
import tempfile
import os

from fastapi import HTTPException

from app.core.config import settings

# Base Provider
from app.services.providers.base import BaseProvider


class OpenAIProvider(BaseProvider):
    def __init__(self, model_name: str):
        """
        https://platform.openai.com/docs/api-reference/audio/createTranscription
        Initialize the OpenAIProvider with a specific model name.
        :param model_name: Name of the OpenAI model to use (e.g., "whisper-1").
        """
        print(f"⚙️ Instantiating OpenAIProvider with: {model_name}")
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=422, detail="OpenAI API key is not configured."
            )
        # Initialize the OpenAI client
        self.client = OpenAI()
        self.model_name = model_name

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
        

        # Write to temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(response.content)
            tmp.flush()  # Ensure all content is written
            tmp_path = tmp.name  # Save the path to open later

        try:
            with open(tmp_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model=self.model_name,
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"],
                ).model_dump()  # Convert to dict :D

        finally:
            os.remove(tmp_path)  # Clean up manually

        return {
            "transcript": transcription.get("text"),
            "language": transcription.get("language"),
            "segments": transcription.get("segments", []),
        }
