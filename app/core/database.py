import logging
from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.core.config import settings

logger = logging.getLogger(__name__)

_client = None


async def init_db(document_models: list | None = None):
    global _client

    _client = AsyncMongoClient(settings.DATABASE_URL)
    db_name = getattr(settings, "DATABASE_NAME", "anonpulse_db")
    db = _client[db_name]

    if document_models is None:
        document_models = []

    await init_beanie(
        database=db,
        document_models=document_models,
    )


async def close_db():
    global _client
    if _client is not None:
        _client.close()
        _client = None