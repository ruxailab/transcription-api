from fastapi import APIRouter, status

# Schemas
from app.schemas.common import ErrorResponse
from app.schemas.transcribe import TranscribeRequest, TranscribeResponse

# Services
from app.services.transcriber import TranscriptionManager

router = APIRouter()


@router.post(
    "/transcribe",
    tags=["Transcription"],  # ✅ Shows "Transcribe" section in Swagger UI
    status_code=status.HTTP_200_OK,  # ✅ Explicit 200 code (optional, but clear)
    response_model=TranscribeResponse,  # ✅ Runtime validation + docs + schema
    responses={
        200: {
            "model": TranscribeRequest,
            "description": "Transcription successful",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "provider": "whisper",
                        "model": "tiny",
                        "audio_url": "https://example.com/audio.mp3",
                        "transcript": "Transcribed text goes here.",
                        "language": "en",
                        "segments": [
                            {
                                "start": 0.0,
                                "end": 5.0,
                                "text": "This is the first segment of the transcription.",
                            },
                            {
                                "start": 5.1,
                                "end": 10.0,
                                "text": "This is the second segment of the transcription.",
                            },
                        ],
                    }
                }
            },
        },
        422: {
            "model": ErrorResponse,
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Some required fields are missing or invalid.",
                        "details": "audio_url: Invalid URL format; provider: Value must be one of 'whisper', 'openai'.",
                    }
                }
            },
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Something went wrong on our side. Please try again later.",
                    }
                }
            },
        },
    },
)
def transcribe(request: TranscribeRequest):
    """
    Transcription endpoint to handle audio transcription requests.
    This is a placeholder for the actual transcription logic.
    """
    return TranscriptionManager.transcribe(request)
