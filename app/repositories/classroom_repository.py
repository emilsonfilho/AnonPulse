from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repository import BaseRepository
from app.models.classroom import Classroom

class ClassroomRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Classroom, session=session)