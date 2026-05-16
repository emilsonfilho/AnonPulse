from app.core.exceptions.custom_exceptions import (
    MonitorAssignmentAlreadyExistsException,
    MonitorAssignmentHasFeedbackException,
    MonitorAssignmentNotFoundException,
)
from app.core.mapper import Mapper
from app.models.monitor_assignment import MonitorAssignment
from app.repositories.monitor_assignment_repository import MonitorAssignmentRepository
from app.schemas.monitor_assignment_schema import (
    CreateMonitorAssignmentRequest,
    MonitorAssignmentResponse,
    UpdateMonitorAssignmentRequest,
)
from app.services.base_service import BaseService


class MonitorAssignmentService(
    BaseService[
        MonitorAssignment,
        CreateMonitorAssignmentRequest,
        UpdateMonitorAssignmentRequest,
        MonitorAssignmentResponse,
    ]
):
    def __init__(self, repository: MonitorAssignmentRepository) -> None:
        super().__init__(
            repository=repository,
            response_schema=MonitorAssignmentResponse,
            not_found_exception=MonitorAssignmentNotFoundException,
        )

    async def create(
        self, request: CreateMonitorAssignmentRequest
    ) -> MonitorAssignmentResponse:
        already_assigned = await self.repository.check_existing(
            request.monitor_registration_number, request.classroom_cod
        )

        if already_assigned:
            raise MonitorAssignmentAlreadyExistsException(
                request.monitor_registration_number, request.classroom_cod
            )

        assignment = MonitorAssignment(**request.model_dump())
        new_assignment = await self.repository.create(assignment)

        return Mapper.to_response(new_assignment, self.response_schema)

    async def delete(self, id: int) -> None:
        assignment = await self.get_or_raise(id)

        if assignment.feedbacks:
            raise MonitorAssignmentHasFeedbackException(id)

        await self.repository.delete(id)
