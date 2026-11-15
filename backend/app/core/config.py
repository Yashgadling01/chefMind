
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    MONGODB_URL: str
    DATABASE_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
