"""Configurações da aplicação."""

from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Configurações carregadas das variáveis de ambiente."""

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite+aiosqlite:///database/anonpulse.db"
    )

    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "anonpulse")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
