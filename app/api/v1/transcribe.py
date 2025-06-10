from fastapi import APIRouter, status, HTTPException
from fastapi.exceptions import RequestValidationError

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
    try:
        return TranscriptionManager.transcribe(request)
    except RequestValidationError as ve:
        # raise RequestValidationError("Unsupported provider")
        # Thrown by Me
        raise HTTPException(status_code=400, detail=str(ve))
