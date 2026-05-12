from datetime import date

from app.core.exceptions.custom_exceptions import EnrollmentNotFoundException, EnrollmentAlreadyExistsExcepion
from app.core.mapper import Mapper
from app.services.base_service import BaseService
from app.repositories.enrollment_repository import EnrollmentRepository
from app.schemas.enrollment_schema import EnrollmentResponse, CreateEnrollmentRequest, UpdateEnrollmentRequest
from app.models.enrollment import Enrollment

class EnrollmentService(BaseService[Enrollment, CreateEnrollmentRequest, UpdateEnrollmentRequest, EnrollmentResponse]):
    def __init__(self, repository: EnrollmentRepository) -> None:
        super().__init__(
            repository=repository,
            response_schema=EnrollmentResponse,
            not_found_exception=EnrollmentNotFoundException,
        )

    async def create(self, request: CreateEnrollmentRequest) -> EnrollmentResponse:
        already_enrolled = await self.repository.check_existing(request.student_id, request.classroom_cod)

        if already_enrolled:
            raise EnrollmentAlreadyExistsExcepion(request.student_id, request.classroom_cod)
        
        enrollment = Enrollment(
            **request.model_dump(),
            is_active=True,
            enrolled_at=date.today()
        )
        new_enrollment = await self.repository.create(enrollment)

        return Mapper.to_response(new_enrollment, EnrollmentResponse)
    
    async def delete(self, id: int) -> None:
        await self.get_or_raise(id)

        await self.repository.update(id, {"isActive": False})