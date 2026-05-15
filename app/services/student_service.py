from app.core.exceptions.custom_exceptions import StudentAlreadyExistsException, StudentNotFoundException
from app.services.base_service import BaseService
from app.repositories.student_repository import StudentRepository
from app.schemas.student_schema import StudentResponse, CreateStudentRequest, UpdateStudentRequest
from app.models.student import Student

class StudentService(BaseService[Student, CreateStudentRequest, UpdateStudentRequest, StudentResponse]):
    def __init__(self, repository: StudentRepository) -> None:
        super().__init__(
            repository=repository,
            response_schema=StudentResponse,
            not_found_exception=StudentNotFoundException,
            already_exists_exception=StudentAlreadyExistsException
        )

    async def create(self, request: CreateStudentRequest) -> StudentResponse:
        return await super().create(request, identifier_value=request.registration)