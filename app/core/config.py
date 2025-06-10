from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    device: str = "cpu"
    openai_api_key: str = "NAN"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
