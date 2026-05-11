from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Params, Page

from app.models.monitor import Monitor

class MonitorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_registration(registration: str) -> Monitor:
        # To-Do
        pass
        
    async def create(self, monitor: Monitor) -> Monitor:
        # To-Do
        pass
        