from sqlalchemy.ext.asyncio import AsyncSession

from app.models.professor import Professor
from app.repositories.base_repository import BaseRepository

class ProfessorRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Professor, session=session)
