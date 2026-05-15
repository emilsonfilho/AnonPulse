from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.repositories.base_repository import BaseRepository
from app.models.classroom import Classroom

class ClassroomRepository(BaseRepository[Classroom]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Classroom, session=session)
    
    async def get_with_details(self, classroom_cod: str) -> Classroom | None:
        query =(
            select(self.model)
            .where(self.model.cod == classroom_cod)
            .options(
                selectinload(self.model.professor),
                selectinload(self.model.subject),
            )
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def list_by_professor(self, professor_id: int, params: Params) -> Page[Classroom]:
        query = select(self.model).where(self.model.professor_id == professor_id)
        return await paginate(self.session, query, params)
    
    async def list_by_subject(self, subject_cod: str, params: Params) -> Page[Classroom]:
        query = select(self.model).where(self.model.subject_cod == subject_cod)
        return await paginate(self.session, query, params)