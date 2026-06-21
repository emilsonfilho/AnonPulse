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

    MINIO_ROOT_USER: str = os.getenv("MINIO_ROOT_USER", "minioadmin")
    MINIO_ROOT_PASSWORD: str = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "anonpulse-documents")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
