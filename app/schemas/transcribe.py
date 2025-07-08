from pydantic import BaseModel, HttpUrl, model_validator, Field
from enum import Enum
from typing import Optional


class TranscriptionModel(str, Enum):
    # Local Whisper models
    tiny = "tiny"
    base = "base"
    medium = "medium"
    large = "large"
    # OpenAI models for transcription
    whisper_1 = "whisper-1"


class TranscriptionProvider(str, Enum):
    whisper = "whisper"
    openai = "openai"


class TranscribeRequest(BaseModel):
    audio_url: HttpUrl
    provider: TranscriptionProvider
    model: Optional[TranscriptionModel] = Field(
        default=None,
        description=(
            "Name of the transcription model to use.\n\n"
            "🧠 **Available models by provider:**\n"
            "- `whisper`: `tiny`, `base`, `medium`, `large`\n"
            "- `openai`: `whisper-1`"
        ),
        json_schema_extra={"example": "tiny"},
    )

    @model_validator(mode="before")
    def check_model_provider_compatibility(cls, values):
        provider = values.get("provider")
        model = values.get("model")

        if model is None:
            return values  # No model specified, skip validation

        # Define model compatibility per provider
        whisper_models = {"tiny", "base", "medium", "large"}
        openai_models = {"whisper-1", "gpt_4o_transcribe", "gpt_4o_mini_transcribe"}

        if provider == TranscriptionProvider.whisper and model not in whisper_models:
            raise ValueError(f"Model '{model}' is not valid for provider 'whisper'")

        if provider == TranscriptionProvider.openai and model not in openai_models:
            raise ValueError(f"Model '{model}' is not valid for provider 'openai'")

        return values


class TranscribeResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "success"})

    provider: TranscriptionProvider = Field(
        ..., json_schema_extra={"example": "whisper"}
    )
    model: Optional[TranscriptionModel] = Field(
        None,
        description=(
            "Name of the transcription model used.\n\n"
            "🧠 **Available models by provider:**\n"
            "- `whisper`: `tiny`, `base`, `medium`, `large`\n"
            "- `openai`: `whisper-1`"
        ),
        json_schema_extra={"example": "tiny"},
    )
    audio_url: HttpUrl = Field(
        ..., json_schema_extra={"example": "https://example.com/audio.mp3"}
    )
    transcript: str = Field(
        ..., json_schema_extra={"example": "Transcribed text goes here."}
    )
    language: Optional[str] = Field(default=None, json_schema_extra={"example": "en"})
    segments: Optional[list] = Field(
        default=None,
        json_schema_extra={
            "example": [
                {
                    "start": 0.0,
                    "end": 3.5,
                    "text": "Hello, and welcome to the recording.",
                },
                {
                    "start": 3.5,
                    "end": 7.2,
                    "text": "This is a test of Whisper transcription.",
                },
            ]
        },
    )
