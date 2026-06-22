"""Configurações da aplicação."""

from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Configurações carregadas das variáveis de ambiente."""

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "mongodb://root:example@mongo:27017/anonpulse?authSource=admin"
    )
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "anonpulse")

    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "anonpulse")
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "anonpulse_admin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "AnonPulseKeySecure2026!")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
