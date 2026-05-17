from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select
from sqlalchemy.orm import selectinload, joinedload
from typing import Any

from app.repositories.base_repository import BaseRepository
from app.models.classroom import Classroom

class ClassroomRepository(BaseRepository[Classroom]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Classroom, session=session)
    
    async def list_by_professor(self, professor_id: int, params: Params, options: list[Any] | None = None) -> Page[Classroom]:
        query = select(self.model).where(self.model.professor_id == professor_id)

        if options:
            query = query.options(*options)

        return await paginate(self.session, query, params)
    
    async def list_by_subject(self, subject_cod: str, params: Params, options: list[Any] | None = None) -> Page[Classroom]:
        query = select(self.model).where(self.model.subject_cod == subject_cod)
        
        if options:
            query = query.options(*options)

        return await paginate(self.session, query, params)