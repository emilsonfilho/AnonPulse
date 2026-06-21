import logging
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from beanie import init_beanie

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: AsyncMongoClient | None = None

async def init_db(document_models: list | None = None):
    global _client

    client = AsyncMongoClient(settings.DATABASE_URL)
    _client = client

    db: AsyncDatabase = client[settings.DATABASE_NAME]

    await init_beanie(
        database=db,
        document_models=document_models or [],
    )

async def close_db():
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None