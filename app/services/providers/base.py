from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_url: str) -> dict:
        """Transcribe an audio file from a given URL"""
        pass
