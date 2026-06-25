import logging

from beanie import init_beanie
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import settings
from app.models.classroom import Classroom
from app.models.document_metadata import DocumentMetadata
from app.models.enrollment import Enrollment
from app.models.feedback import Feedback
from app.models.monitor import Monitor
from app.models.monitor_assignment import MonitorAssignment
from app.models.professor import Professor
from app.models.student import Student
from app.models.subject import Subject

logger = logging.getLogger(__name__)

_client: AsyncMongoClient | None = None


async def init_db():
    global _client

    client = AsyncMongoClient(settings.DATABASE_URL)
    _client = client

    db: AsyncDatabase = client[settings.DATABASE_NAME]

    await init_beanie(
        database=db,
        document_models=[
            Classroom,
            DocumentMetadata,
            Enrollment,
            Feedback,
            Monitor,
            MonitorAssignment,
            Professor,
            Student,
            Subject,
        ],
    )


async def close_db():
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
