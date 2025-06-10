from enum import Enum
from pydantic import BaseModel, HttpUrl, Field


class TranscriptionProvider(str, Enum):
    whisper = "whisper"
    openai = "openai"


class TranscribeRequest(BaseModel):
    audio_url: HttpUrl
    provider: TranscriptionProvider


class TranscribeResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "success"})
    # status: str = Field(..., json_schema_extra={"example": "success"})
    # transcript: str = Field(
    #     ..., json_schema_extra={"example": "Transcribed text goes here."}
    # )
    # provider: TranscriptionProvider = Field(
    #     ..., json_schema_extra={"example": "whisper"}
    # )
    # audio_url: HttpUrl = Field(
    #     ..., json_schema_extra={"example": "https://example.com/audio.mp3"}
    # )
