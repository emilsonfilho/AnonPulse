from datetime import datetime, timezone

from app.core.exceptions.custom_exceptions import (
    EnrollmentAlreadyExistsException,
    EnrollmentNotFoundException,
)
from app.core.mapper import Mapper
from app.models.enrollment import Enrollment
from app.repositories.enrollment_repository import EnrollmentRepository
from app.schemas.enrollment_schema import (
    CreateEnrollmentRequest,
    EnrollmentResponse,
    UpdateEnrollmentRequest,
)
from app.services.base_service import BaseService


class EnrollmentService(
    BaseService[
        Enrollment, CreateEnrollmentRequest, UpdateEnrollmentRequest, EnrollmentResponse
    ]
):
    def __init__(self, repository: EnrollmentRepository) -> None:
        super().__init__(
            repository=repository,
            response_schema=EnrollmentResponse,
            not_found_exception=EnrollmentNotFoundException,
            already_exists_exception=EnrollmentAlreadyExistsException,
        )

    async def create(self, request: CreateEnrollmentRequest) -> EnrollmentResponse:
        already_enrolled = await self.repository.check_existing(
            request.student_id, request.classroom_cod
        )

        if already_enrolled:
            raise EnrollmentAlreadyExistsException(
                request.student_id,
            )

        enrollment = Enrollment(
            **request.model_dump(),
            is_active=True,
            enrolled_at=datetime.now(timezone.utc),
        )
        new_enrollment = await self.repository.create(enrollment)

        return Mapper.to_response(new_enrollment, EnrollmentResponse)

    async def delete(self, id: int) -> None:
        await self.get_or_raise(id)

        await self.repository.update(id, {"isActive": False})
