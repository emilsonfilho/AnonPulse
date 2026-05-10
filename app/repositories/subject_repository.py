from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subject import Subject
from sqlalchemy import select

class SubjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, subject: Subject):
        self.session.add(subject)

        await self.session.commit()
        await self.session.refresh(subject)

        return subject
    
    async def get_by_code(self, code: str):
        query = select(Subject).where(
            Subject.cod == code
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()