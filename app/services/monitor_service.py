from app.core.exceptions.custom_exceptions import MonitorAlreadyExistsExcepion, MonitorNotFoundException
from app.core.mapper import Mapper
from app.services.base_service import BaseService
from app.repositories.monitor_repository import MonitorRepository
from app.schemas.monitor_schema import MonitorResponse, CreateMonitorRequest
from app.models.monitor import Monitor

class MonitorService(BaseService):
    def __init__(self, repository: MonitorRepository) -> None:
        self.repository = repository

    async def _get_monitor_or_raise(self, registration: str):
        return self.get_or_raise(
            registration,
            MonitorNotFoundException
        )

    async def create_monitor(self, data: CreateMonitorRequest) -> MonitorResponse:
        monitor = await self.repository.get_by_registration(data.registration)  
        
        if monitor:
            raise MonitorAlreadyExistsExcepion()
        
        monitor = Monitor(**data.model_dump())
        new_monitor = self.repository.create(monitor)

        return Mapper.to_response(new_monitor, MonitorResponse) 