from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repository import BaseRepository
from app.models.feedback import Feedback

class FeedbackRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Feedback, session=session)