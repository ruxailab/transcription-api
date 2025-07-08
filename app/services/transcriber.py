from fastapi import HTTPException

# Schemas
from app.schemas.transcribe import TranscribeRequest, TranscribeResponse

# Providers
from app.services.providers.whisper_local import WhisperLocalProvider
from app.services.providers.open_ai import OpenAIProvider


class TranscriptionManager:
    @staticmethod
    def transcribe(request: TranscribeRequest):
        audio_url = request.audio_url
        provider_name = request.provider.value
        model_name = request.model.value if request.model else "base"

        if provider_name == "whisper":
            provider = WhisperLocalProvider(model_size=model_name)
        elif provider_name == "openai":
            provider = OpenAIProvider(model_name=model_name)
        else:
            # This Point will not be reached due to Schema validation by FastAPI :D
            raise HTTPException(
                status_code=422,
                detail=f"Provider '{provider_name}' is not supported.",
            )

        # Call the provider's transcribe method
        result = provider.transcribe(audio_url)

        return TranscribeResponse(
            status="success",
            provider=provider_name,
            model=model_name,
            audio_url=audio_url,
            transcript=result["transcript"],
            language=result.get("language"),
            segments=result.get("segments"),
        )
