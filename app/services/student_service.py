from app.core.exceptions.custom_exceptions import StudentAlreadyExistsExcepion, StudentNotFoundException
from app.services.base_service import BaseService
from app.repositories.student_repository import StudentRepository
from app.schemas.student_schema import StudentResponse, StudentRequest

class StudentService(BaseService):
    def __init__(self, repository: StudentRepository) -> None:
        super().__init__(
            repository=repository,
            response_schema=StudentResponse,
            not_found_exception=StudentNotFoundException,
            already_exists_exception=StudentAlreadyExistsExcepion
        )

    async def create(self, request: StudentRequest) -> StudentResponse:
        return await super().create(request, identifier_value=request.student)