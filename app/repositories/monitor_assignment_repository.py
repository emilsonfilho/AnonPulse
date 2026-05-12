from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repository import BaseRepository
from app.models.monitor_assignment import MonitorAssignment

class MonitorAssignmentRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=MonitorAssignment, session=session)

    async def check_existing(self, monitor_registration: str, classroom_cod: str) -> bool:
        # To-Do
        pass
        