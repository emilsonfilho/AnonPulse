from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.session import get_session
from app.repositories.subject_repository import SubjectRepository

def get_subject_repository(
        session: AsyncSession = Depends(get_session)
):
    return SubjectRepository(session)