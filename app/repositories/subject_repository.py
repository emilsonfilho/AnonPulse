from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Params, Page
from app.models.subject import Subject
from sqlalchemy import select
from typing import Any
from app.schemas.subject_schema import SubjectResponse

class SubjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, subject: Subject) -> Subject:
        self.session.add(subject)

        await self.session.commit()
        await self.session.refresh(subject)

        return subject

    async def list_all(self, params: Params) -> Page[SubjectResponse]:
        # To-Do
        pass

    async def get_by_code(self, code: str) -> Subject | None:
        query = select(Subject).where(
            Subject.cod == code
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def update(self, code: str, data: dict[str, Any]) -> Subject:
        # To-Do
        pass

    async def delete(self, code: str) -> None:
        # To-Do
        pass