from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subject import Subject
from app.repositories.base_repository import BaseRepository
class SubjectRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Subject, session=session)