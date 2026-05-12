from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repository import BaseRepository
from app.models.enrollment import Enrollment

class EnrollmentRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Enrollment, session=session)

    async def check_existing(self, student_id: int, classroom_cod: str) -> bool:
        # To-Do
        pass
        