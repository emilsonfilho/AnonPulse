from fastapi_pagination import Params, Page
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.models.professor import Professor

class ProfessorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self, params: Params) -> Page[Professor]:
        # To-Do
        pass

    async def get_by_id(self, id: int) -> Professor | None:
        # To-Do 
        pass

    async def create(self, professor: Professor) -> Professor:
        # To-Do
        pass

    async def update(self, id: int, data: dict[str, Any]) -> Professor:
        # To-Do
        pass

    async def delete(self, id: int) -> None:
        # To-Do
        pass