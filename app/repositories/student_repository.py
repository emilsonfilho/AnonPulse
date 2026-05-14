from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repository import BaseRepository
from app.models.student import Student

class StudentRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Student, session=session)