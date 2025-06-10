from fastapi.exceptions import RequestValidationError

# Schemas
from app.schemas.transcribe import TranscribeRequest, TranscribeResponse


class TranscriptionManager:
    _providers = {
        # "openai": OpenAIProvider(),
        # "whisper": WhisperLocalProvider(),
    }

    @staticmethod
    def transcribe(request: TranscribeRequest):
        provider_name = (
            request.provider.value
        )  # If enum, .value; otherwise just request.provider
        provider = TranscriptionManager._providers.get(provider_name)
        print(f"TranscriptionManager: Using provider '{provider_name}'")

        if not provider:
            raise RequestValidationError(f"Unsupported provider: {provider_name}")

        result = provider.transcribe(request.audio_url, request.model)

        return TranscribeResponse(
            status="success",
            # provider=provider_name,
            # transcript=result["transcript"],
            # metadata=result.get("meta"),
        )
