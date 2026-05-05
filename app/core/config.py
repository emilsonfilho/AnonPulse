from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import create_engine

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database/anonpulse.db")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

engine = create_engine(settings.DATABASE_URL)
