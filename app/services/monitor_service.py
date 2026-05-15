from app.core.exceptions.custom_exceptions import MonitorAlreadyExistsException, MonitorNotFoundException
from app.services.base_service import BaseService
from app.repositories.monitor_repository import MonitorRepository
from app.schemas.monitor_schema import MonitorResponse, CreateMonitorRequest, UpdateMonitorRequest
from app.models.monitor import Monitor

class MonitorService(BaseService[Monitor, CreateMonitorRequest, UpdateMonitorRequest, MonitorResponse]):
    def __init__(self, repository: MonitorRepository) -> None:
        super().__init__(
            repository=MonitorRepository,
            response_schema=MonitorResponse,
            not_found_exception=MonitorNotFoundException,
            already_exists_exception=MonitorAlreadyExistsException
        )
    async def create(self, request: CreateMonitorRequest) -> MonitorResponse:
        return await super().create(request, identifier_value=request.registration)