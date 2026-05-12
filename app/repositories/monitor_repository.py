from sqlalchemy.ext.asyncio import AsyncSession

from app.models.monitor import Monitor
from app.repositories.base_repository import BaseRepository

class MonitorRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Monitor, session=session)